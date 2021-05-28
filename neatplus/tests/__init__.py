from django.test import RequestFactory
from django.urls import reverse as django_reverse
from model_bakery import baker, random_gen
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APITestCase


class FullTestCase(APITestCase, APILiveServerTestCase):
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
        if params:
            extra_params = []
            for key, value in params.items():
                extra_params.append(f"{key}={value}")
            param = "&".join(extra_params)
            url = f"{url}?{param}"
        return url
