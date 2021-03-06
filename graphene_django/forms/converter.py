from django import forms
from django.core.exceptions import ImproperlyConfigured

from graphene import ID, Boolean, Float, Int, List, String, UUID, Date, DateTime, Time

from .forms import GlobalIDFormField, GlobalIDMultipleChoiceField
from ..utils import import_single_dispatch


singledispatch = import_single_dispatch()


@singledispatch
def convert_form_field(field):
    raise ImproperlyConfigured(
        "Don't know how to convert the Django form field %s (%s) "
        "to Graphene type" % (field, field.__class__)
    )

from neomodel import (
    AliasProperty,
    ArrayProperty,
    BooleanProperty,
    DateProperty,
    DateTimeProperty,
    EmailProperty,
    FloatProperty,
    IntegerProperty,
    JSONProperty,
    RegexProperty,
    StringProperty,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
    One,
    OneOrMore,
)
from neomodel.relationship_manager import RelationshipDefinition


@convert_form_field.register(StringProperty)
@convert_form_field.register(RegexProperty)
def convert_form_field_to_string(field):
    return String(description=field.help_text)


@convert_form_field.register(forms.UUIDField)
@convert_form_field.register(RelationshipDefinition)
def convert_form_field_to_uuid(field):
    return UUID()


@convert_form_field.register(IntegerProperty)
@convert_form_field.register(forms.IntegerField)
@convert_form_field.register(forms.NumberInput)
def convert_form_field_to_int(field):
    return Int(description=field.help_text)


@convert_form_field.register(BooleanProperty)
def convert_form_field_to_boolean(field):
    return Boolean(description=field.help_text)


@convert_form_field.register(forms.NullBooleanField)
def convert_form_field_to_nullboolean(field):
    return Boolean(description=field.help_text)


@convert_form_field.register(forms.DecimalField)
@convert_form_field.register(forms.FloatField)
def convert_form_field_to_float(field):
    return Float(description=field.help_text)


@convert_form_field.register(forms.ModelMultipleChoiceField)
@convert_form_field.register(GlobalIDMultipleChoiceField)
def convert_form_field_to_list(field):
    return List(ID)


@convert_form_field.register(forms.DateField)
def convert_form_field_to_date(field):
    return Date(description=field.help_text)


@convert_form_field.register(forms.DateTimeField)
def convert_form_field_to_datetime(field):
    return DateTime(description=field.help_text, required=field.required)


@convert_form_field.register(forms.TimeField)
def convert_form_field_to_time(field):
    return Time(description=field.help_text, required=field.required)


@convert_form_field.register(forms.ModelChoiceField)
@convert_form_field.register(GlobalIDFormField)
def convert_form_field_to_id(field):
    return ID(required=field.required)
