import typing

import django.core.checks
from django import forms
from django.db.models.options import DEFAULT_NAMES as META_ATTRS
from django.utils.translation import gettext_lazy as _

from . import CheckID


class ListField(forms.Field):
    default_error_messages = {
        "invalid_list": _("Enter a list of values."),
    }

    def __init__(self, base_field, **kwargs):
        self.base_field = base_field
        super().__init__(**kwargs)

    def to_python(self, value: typing.Any) -> list:
        if not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise forms.ValidationError(
                self.error_messages["invalid_list"], code="invalid_list"
            )
        return [self.base_field.to_python(val) for val in value]

    def validate(self, value: list) -> None:
        if self.required and not value:
            raise forms.ValidationError(
                self.error_messages["required"], code="required"
            )
        for val in value:
            self.base_field.validate(val)


class UnionField(forms.Field):
    default_error_messages = {
        "type_invalid": _("%(value)s is not one of the available types."),
    }

    def __init__(self, base_fields, **kwargs):
        assert isinstance(base_fields, dict)
        self.base_fields = base_fields
        super().__init__(**kwargs)

    def to_python(self, value: typing.Any) -> list:
        for type_, field in self.base_fields.items():
            if isinstance(value, type_):
                return field.to_python(value)
        raise forms.ValidationError(
            self.error_messages["type_invalid"],
            code="type_invalid",
            params={"value": value},
        )

    def validate(self, value: typing.Any) -> None:
        for type_, field in self.base_fields.items():
            if isinstance(value, type_):
                field.validate(value)
                return


class DictField(forms.ChoiceField):
    default_error_messages = {
        "invalid_choice": _("ID %(value)s is not one of the available checks."),
        "invalid_dict": _("Must be a dict."),
        "id_required": _("`id` field is required."),
    }

    def __init__(self, id_choices, **kwargs):
        super().__init__(choices=id_choices, **kwargs)

    def to_python(self, value: typing.Any) -> dict:
        if not value:
            return {}
        if not isinstance(value, dict):
            raise forms.ValidationError(
                self.error_messages["invalid_dict"], code="invalid_dict",
            )
        return {str(k): v for k, v in value.items()}

    def validate(self, value: dict) -> None:
        if self.required and not value:
            raise forms.ValidationError(
                self.error_messages["required"], code="required"
            )
        if "id" not in value:
            raise forms.ValidationError(
                self.error_messages["id_required"], code="id_required"
            )
        if not self.valid_value(value["id"]):
            raise forms.ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value["id"]},
            )


class ConfigForm(forms.Form):
    checks = ListField(
        UnionField(
            {
                str: forms.ChoiceField(
                    choices=CheckID.__members__.items(),
                    error_messages={
                        "invalid_choice": _(
                            "%(value)s is not one of the available checks."
                        ),
                    },
                ),
                dict: DictField(id_choices=CheckID.__members__.items()),
            }
        ),
        required=False,
    )

    def clean_checks(self) -> typing.List[dict]:
        result = {}
        for check in self.cleaned_data["checks"]:
            if isinstance(check, str):
                result[check] = {}
            else:
                result[check["id"]] = check
        return result

    def is_valid(self, check_forms: typing.Dict[CheckID, "typing.Type[CheckForm]"]) -> bool:  # type: ignore
        if not super().is_valid():
            return False
        checks = self.cleaned_data.get("checks", {})
        rforms = {
            name: check_forms[name](data=value)
            for name, value in checks.items()
            if name in check_forms
        }
        if forms.all_valid(rforms.values()):  # type: ignore
            self.cleaned_data["checks"] = {
                name: f.cleaned_data for name, f in rforms.items()
            }
            return True
        self.errors["checks"] = {name: form.errors for name, form in rforms.items()}
        return False


class CheckForm(forms.Form):
    level = forms.ChoiceField(
        choices=[(c, c) for c in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]],
        required=False,
    )

    def clean_level(self) -> typing.Optional[int]:
        if self.cleaned_data["level"]:
            return getattr(django.core.checks, self.cleaned_data["level"])
        return None


class CheckAttrsForm(CheckForm):
    attrs = ListField(forms.CharField())


class CheckMetaAttrsForm(CheckForm):
    attrs = forms.MultipleChoiceField(choices=[(o, o) for o in META_ATTRS])


class CheckGettTextFuncForm(CheckForm):
    gettext_func = forms.CharField(required=False)
