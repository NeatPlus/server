from django.urls import reverse as django_reverse
from model_bakery import baker, random_gen
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APITestCase


class APIFullTestCase(APITestCase, APILiveServerTestCase):
    baker = baker
    baker.generators.add("neatplus.fields.LowerCharField", random_gen.gen_string)
    baker.generators.add("neatplus.fields.LowerEmailField", random_gen.gen_email)
    baker.generators.add("neatplus.fields.LowerTextField", random_gen.gen_text)

    status_code = status

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
        extra_params = []
        if params:
            for key, value in params.items():
                extra_params.append(f"{key}={value}")
        param = "&".join(extra_params)
        final_url = f"{url}?{param}"
        return final_url
