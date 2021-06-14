from django import template

register = template.Library()


@register.simple_tag
def create_list(*args):
    return args


@register.simple_tag
def val_not_in_list(val, list):
    return val not in list


@register.simple_tag
def bool_to_string(bool_val, true_val, false_val=None):
    return true_val if bool_val else false_val
