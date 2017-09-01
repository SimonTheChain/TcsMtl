import warnings

import lxml.etree as etree
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from openpyxl import load_workbook

from .forms import SeriesForm
from .models import Provider, Series, SeriesRating, SeriesInfo


def ingest(request):
    series_form = SeriesForm()

    if request.method == "POST":
        form = SeriesForm(request.POST)
        files = request.FILES.getlist("xlsx_files")

        if form.is_valid():

            for f in files:
                # Series
                series_object = Series()

                series_object.name = form.cleaned_data["name"]
                series_object.original_language_locale = form.cleaned_data["original_language_locale"]
                series_object.original_language_region = form.cleaned_data["original_language_region"]
                series_object.genre1 = form.cleaned_data["genre1"]
                series_object.genre2 = form.cleaned_data["genre2"]
                series_object.genre3 = form.cleaned_data["genre3"]
                series_object.provider = form.cleaned_data["provider"]

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    wb = load_workbook(f)

                for sheet in wb:

                    if sheet.title == "Serie":
                        rows = sheet.rows
                        next(rows)
                        next(rows)

                        for row in rows:

                            # Series ID
                            if series_object.amazon_id == row[3].value:
                                pass

                            else:
                                series_object.amazon_id = row[3].value

                            # Series start date
                            if series_object.date == str(row[16].value):
                                pass

                            else:
                                series_object.date = str(row[16].value)

                series_object.save()

                # Series Ratings
                all_ratings = SeriesRating.objects.filter(series=series_object)

                for sheet in wb:

                    if sheet.title == "Season":
                        rows = sheet.rows
                        next(rows)
                        next(rows)

                        for row in rows:

                            # Rating
                            try:
                                all_ratings.get(system=row[19].value)

                            except SeriesRating.DoesNotExist:
                                series_rating_object = SeriesRating()
                                series_rating_object.system = row[19].value
                                series_rating_object.value = row[20].value
                                series_rating_object.series = series_object
                                series_rating_object.save()

                            else:
                                pass

                # Series Info
                for sheet in wb:

                    if sheet.title == "Serie":
                        rows = sheet.rows
                        next(rows)
                        next(rows)

                        for row in rows:
                            info_object = SeriesInfo()

                            if str(row[0].value).replace(" ", "") == "None":
                                info_object.language_locale = None

                            else:
                                info_object.language_locale = str(row[0].value).replace(" ", "")

                            if str(row[1].value).replace(" ", "") == "None":
                                info_object.language_region = None

                            else:
                                info_object.language_region = str(row[1].value).replace(" ", "")

                            info_object.title = row[7].value
                            info_object.summary_short = row[9].value
                            info_object.summary_long = row[10].value
                            info_object.series = series_object

                            info_object.save()

        return render(
            request,
            "amazon_mec_ep/ingest_form.html",
            context={"SeriesForm": series_form, "files_ingest": files})

    else:
        return render(request, "amazon_mec_ep/ingest_form.html", context={"SeriesForm": series_form})


def mec_missing(request, pk):
    series = Series.objects.get(pk=pk)
    seriesinfo = SeriesInfo.objects.filter(series=series.id)

    default_selected = 0
    for si in seriesinfo:
        if si.default:
            default_selected += 1

    return render(
        request,
        "amazon_mec_ep/series_missing.html",
        context={"series": series, "default_selected": default_selected})


def mec_series(request, pk):
    series = Series.objects.get(pk=pk)
    nsmap = {
        "mdmec": "http://www.movielabs.com/schema/mdmec/v2.5",
        "md": "http://www.movielabs.com/schema/md/v2.5/md",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }
    schemalocation = "http://www.movielabs.com/schema/mdmec/v2.5 ../mdmec-v2.5.xsd"

    xml_root = etree.Element(
        "{%s}CoreMetadata" % nsmap["mdmec"],
        attrib={"{" + nsmap["xsi"] + "}schemaLocation": schemalocation},
        nsmap=nsmap)

    basic = etree.SubElement(
        xml_root,
        "{%s}Basic" % nsmap["mdmec"],
        attrib={"ContentID": "md:cid:org:{}:{}".format(
            series.provider.amazon_code,
            series.amazon_id)})

    for i in series.seriesinfo_set.all():
        locale_region = "{}-{}".format(i.language_locale, i.language_region)
        if i.default:
            info = etree.SubElement(
                basic,
                "{%s}LocalizedInfo" % nsmap["md"],
                attrib={
                    "language": locale_region,
                    "default": "true"})

        else:
            info = etree.SubElement(
                basic,
                "{%s}LocalizedInfo" % nsmap["md"],
                attrib={
                    "language": locale_region})

        title_display = etree.SubElement(info, "{%s}TitleDisplayUnlimited" % nsmap["md"])
        title_display.text = i.title
        title_sort = etree.SubElement(info, "{%s}TitleSort" % nsmap["md"])
        art = etree.SubElement(info, "{%s}ArtReference" % nsmap["md"])
        sum190 = etree.SubElement(info, "{%s}Summary190" % nsmap["md"])
        sum400 = etree.SubElement(info, "{%s}Summary400" % nsmap["md"])
        sum400.text = i.summary_short
        sum4000 = etree.SubElement(info, "{%s}Summary4000" % nsmap["md"])
        sum4000.text = i.summary_long

        genres = [series.genre1, series.genre2, series.genre3]
        print(genres)

        for g in genres:
            if g != "" and g is not None:
                genre = etree.SubElement(info, "{%s}Genre" % nsmap["md"], attrib={"id": g})

    year = etree.SubElement(basic, "{%s}ReleaseYear" % nsmap["md"])
    year.text = series.date[:4]
    date = etree.SubElement(basic, "{%s}ReleaseDate" % nsmap["md"])
    date.text = series.date
    work = etree.SubElement(basic, "{%s}WorkType" % nsmap["md"])
    work.text = "series"
    alt = etree.SubElement(basic, "{%s}AltIdentifier" % nsmap["md"])
    namespace = etree.SubElement(alt, "{%s}Namespace" % nsmap["md"])
    namespace.text = "ORG"
    identifier = etree.SubElement(alt, "{%s}Identifier" % nsmap["md"])
    identifier.text = series.amazon_id
    ratingset = etree.SubElement(basic, "{%s}RatingSet" % nsmap["md"])

    if not series.seriesrating_set:
        not_rated = etree.SubElement(ratingset, "{%s}NotRated" % nsmap["md"])
        not_rated.text = "true"

    else:
        for r in series.seriesrating_set.all():
            rating = etree.SubElement(ratingset, "{%s}Rating" % nsmap["md"])
            region = etree.SubElement(rating, "{%s}Region" % nsmap["md"])
            rating_country = etree.SubElement(region, "{%s}country" % nsmap["md"])
            rating_country.text = r.country
            rating_system = etree.SubElement(rating, "{%s}System" % nsmap["md"])
            rating_system.text = r.system
            rating_value = etree.SubElement(rating, "{%s}Value" % nsmap["md"])
            rating_value.text = r.value

    original_language = etree.SubElement(basic, "{%s}OriginalLanguage" % nsmap["md"])

    if series.original_language_region == "MX":
        original_locale_region = "{}-{}".format(
            series.original_language_locale,
            "419")

    else:
        original_locale_region = "{}-{}".format(
            series.original_language_locale,
            series.original_language_region)

    original_language.text = original_locale_region
    associate_org = etree.SubElement(basic, "{%s}AssociatedOrg" % nsmap["md"],
                                     attrib={"organizationID": series.provider.amazon_code, "role": "licensor"})

    company_display = etree.SubElement(xml_root, "{%s}CompanyDisplayCredit" % nsmap["mdmec"])
    display_string = etree.SubElement(company_display, "{%s}DisplayString" % nsmap["md"],
                                      attrib={"language": "en-US"})
    display_string.text = series.provider.name

    tree = etree.ElementTree(xml_root)
    xml_file = etree.tostring(
        tree,
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True)

    filename = "{}-{}-MEC-Series.xml".format(series.provider.amazon_code, series.amazon_id)

    response = HttpResponse(xml_file, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    return response


class ProviderListView(ListView):
    model = Provider
    ordering = ["name"]


class ProviderDetailView(DetailView):
    model = Provider


class ProviderCreate(CreateView):
    model = Provider
    fields = "__all__"


class ProviderUpdate(UpdateView):
    model = Provider
    fields = "__all__"


class ProviderDelete(DeleteView):
    model = Provider
    success_url = reverse_lazy("amazon_mec_ep:provider-list")


class SeriesList(ListView):
    model = Series
    ordering = ["name"]


class SeriesDetail(DetailView):
    model = Series

    def get_context_data(self, **kwargs):
        context = super(SeriesDetail, self).get_context_data(**kwargs)
        context["mec_ready"] = True

        try:
            info = SeriesInfo.objects.filter(series=context["object"].id)

        except SeriesInfo.DoesNotExist:
            context["mec_ready"] = False

        else:
            default = 0

            for i in info:

                if not i.language_region\
                        or not i.series.date \
                        or not i.title \
                        or not i.summary_short:
                    context["mec_ready"] = False

                if i.default:
                    default += 1

            if default != 1:
                context["mec_ready"] = False

        return context


class SeriesCreate(CreateView):
    model = Series
    fields = "__all__"


class SeriesUpdate(UpdateView):
    model = Series
    fields = "__all__"


class SeriesDelete(DeleteView):
    model = Series
    success_url = reverse_lazy("amazon_mec_ep:series-list")


class SeriesInfoCreate(CreateView):
    model = SeriesInfo
    fields = "__all__"


class SeriesInfoDetail(DetailView):
    model = SeriesInfo


class SeriesInfoUpdate(UpdateView):
    model = SeriesInfo
    fields = "__all__"


class SeriesInfoDelete(DeleteView):
    model = SeriesInfo
    success_url = reverse_lazy("amazon_mec_ep:series-list")


class SeriesRatingCreate(CreateView):
    model = SeriesRating
    fields = "__all__"


class SeriesRatingDetail(DetailView):
    model = SeriesRating


class SeriesRatingUpdate(UpdateView):
    model = SeriesRating
    fields = "__all__"


class SeriesRatingDelete(DeleteView):
    model = SeriesRating
    success_url = reverse_lazy("amazon_mec_ep:series-list")
