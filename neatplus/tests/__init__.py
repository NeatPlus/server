from django.test import RequestFactory
from django.urls import reverse as django_reverse
from model_bakery import baker, random_gen
from rest_flex_fields import EXPAND_PARAM, WILDCARD_VALUES
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APITestCase


class FullTestCase(APITestCase, APILiveServerTestCase):

    fixtures = ["support/content/email.yaml"]

    baker = baker
    baker.generators.add("neatplus.fields.LowerCharField", random_gen.gen_string)
    baker.generators.add("neatplus.fields.LowerEmailField", random_gen.gen_email)
    baker.generators.add("neatplus.fields.LowerTextField", random_gen.gen_text)
    baker.generators.add("ckeditor.fields.RichTextField", random_gen.gen_text)
    baker.generators.add(
        "ckeditor_uploader.fields.RichTextUploadingField", random_gen.gen_text
    )
    baker.generators.add(
        "django.contrib.gis.db.models.fields.PointField", random_gen.gen_point
    )

    status_code = status
    factory = RequestFactory()

    @classmethod
    def reverse(
        cls,
        viewname,
        urlconf=None,
        args=None,
        kwargs=None,
        current_app=None,
        params=None,
    ):
        url = django_reverse(viewname, urlconf, args, kwargs, current_app)
        if params is None:
            params = {}
        if EXPAND_PARAM not in params and not url.startswith("/admin"):
            if WILDCARD_VALUES:
                params[EXPAND_PARAM] = WILDCARD_VALUES[0]
        extra_paths = []
        for key, value in params.items():
            extra_paths.append(f"{key}={value}")
        query_string = "&".join(extra_paths)
        url = f"{url}?{query_string}"
        return url
