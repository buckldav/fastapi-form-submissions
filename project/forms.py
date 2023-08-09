import datetime
import logging
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
from enum import Enum
import jsonschema
import json
from .mail import fm
from .config import CONFIG


class FormAlert(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    ERROR = "error"


class FormNotifyMethod(Enum):
    """Other methods besides email will be implemented in the future."""

    EMAIL = "email"
    # SMS = "sms"
    # ZULIP = "zulip"


class FormNotify(BaseModel):
    method: FormNotifyMethod = Field(default=FormNotifyMethod.EMAIL)
    recipient: str
    details: Optional[Dict[str, Any]] = Field(default={})

    def is_method_email(self):
        return self.method == FormNotifyMethod.EMAIL


class Form(BaseModel):
    jsonSchema: dict
    uiSchema: Dict[str, Any]
    formData: Dict[str, Any]
    alerts: Dict[FormAlert, str]
    notify: List[FormNotify]

    @field_validator("jsonSchema")
    def must_be_valid_json_schema_with_id(cls, jsonSchema: dict, values):
        """Ensure the json schema is valid. Raises jsonschema.SchemaError if invalid."""
        # raises exception if invalid https://python-jsonschema.readthedocs.io/en/latest/api/jsonschema/protocols/#jsonschema.protocols.Validator.check_schema
        jsonschema.Draft7Validator.check_schema(jsonSchema)
        if not "$id" in jsonSchema:
            raise jsonschema.SchemaError(
                "Schema required to have an $id that is a UUID."
            )
        if not "title" in jsonSchema:
            raise jsonschema.SchemaError("Schema required to have an title.")
        return jsonSchema


with open("./project/json/contact.json", "r") as f:
    contact_form = Form(**dict(json.load(f)))
    contact_form.notify = [
        FormNotify(
            method=FormNotifyMethod.EMAIL,
            recipient=CONFIG.mail_recipient,
            details={},
        )
    ]


def get_email_recipients(form_notify_list: List[FormNotify]) -> list[str]:
    return [
        nt.recipient for nt in filter(lambda nt: nt.is_method_email(), form_notify_list)
    ]


def get_form_submission_message(submission: dict, form: Form, date: datetime.datetime):
    return f"""Form submission received for {form.jsonSchema["title"]} on {date.strftime("%Y-%m-%d, %H:%M:%S")}.

{json.dumps(submission, indent=2)}"""


def validate_submission(submission: dict, form: Form) -> None:
    """Raises jsonschema.ValidationError if invalid."""
    jsonschema.validate(
        submission,
        form.jsonSchema,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


def get_form_submission_success_alert(form: Form) -> str:
    alert = form.alerts.get(FormAlert.SUCCESS)
    if alert is not None:
        return alert
    else:
        return CONFIG.default_success_alert
