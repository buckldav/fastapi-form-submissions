from traceback import print_exc
import pytest
from project.main import app
from project.forms import (
    Form,
    FormAlert,
    FormNotify,
    contact_form,
    get_form_submission_message,
    validate_submission,
    get_form_submission_success_alert,
    get_email_recipients,
)
from project.config import CONFIG
import json
import jsonschema
import datetime


@pytest.mark.asyncio
async def test_make_forms():
    with open("./project/json/no_id.json", "r") as f:
        try:
            Form(**dict(json.load(f)))
            assert False
        except jsonschema.SchemaError:
            assert True

    with open("./project/json/no_title.json", "r") as f:
        try:
            Form(**dict(json.load(f)))
            assert False
        except jsonschema.SchemaError:
            assert True

    with open("./project/json/minimum_invalid.json", "r") as f:
        try:
            Form(**dict(json.load(f)))
            assert False
        except jsonschema.SchemaError:
            assert True

    with open("./project/json/minimum_valid.json", "r") as f:
        try:
            minimum_valid = Form(**dict(json.load(f)))
            assert True
        except jsonschema.SchemaError:
            assert False


@pytest.mark.asyncio
async def test_validate_submission():
    def _validate_valid(submission):
        try:
            validate_submission(submission, contact_form)
            assert True
        except:
            assert False

    def _validate_invalid(submission, log=False):
        try:
            validate_submission(submission, contact_form)
            assert False
        except jsonschema.ValidationError:
            if log:
                print_exc()
            assert True

    valid_submission = {"name": "Fred", "email": "me@example.com", "message": "Hi"}
    _validate_valid(valid_submission)
    valid_submission_honeypot = {
        "name": "Fred",
        "email": "me@example.com",
        "message": "Hi",
        "smforms-bot-field": None,
    }
    _validate_valid(valid_submission_honeypot)

    invalid_submission_missing_field = {
        "name": "Fred",
        "email": "me@example.com",
    }
    _validate_invalid(invalid_submission_missing_field)
    invalid_submission_name_too_long = {
        "name": "F" * 1000,
        "email": "me@example.com",
        "message": "Hi",
    }
    _validate_invalid(invalid_submission_name_too_long)
    invalid_submission_name_wrong_type = {
        "name": 1000,
        "email": "me@example.com",
        "message": "Hi",
    }
    _validate_invalid(invalid_submission_name_wrong_type)
    invalid_submission_email_not_email = {
        "name": "Fred",
        "email": "aaaaaah",
        "message": "Hi",
    }
    _validate_invalid(invalid_submission_email_not_email)
    invalid_submission_email_wrong_type = {
        "name": "Fred",
        "email": False,
        "message": "Hi",
    }
    _validate_invalid(invalid_submission_email_wrong_type)
    invalid_submission_honeypot = {
        "name": "Fred",
        "email": "me@example.com",
        "message": "Hi",
        "smforms-bot-field": "Hi",
    }
    _validate_invalid(invalid_submission_honeypot)


@pytest.mark.asyncio
async def test_contact_form_submission_message():
    valid_submission = {"name": "Fred", "email": "me@example.com", "message": "Hi"}
    date = datetime.datetime.now()
    message = get_form_submission_message(valid_submission, contact_form, date)
    assert (
        message
        == f"""Form submission received for {contact_form.jsonSchema["title"]} on {date.strftime("%Y-%m-%d, %H:%M:%S")}.

{{
  "name": "Fred",
  "email": "me@example.com",
  "message": "Hi"
}}"""
    )


@pytest.mark.asyncio
async def test_get_form_submission_success_alert():
    assert (
        get_form_submission_success_alert(contact_form)
        == contact_form.alerts[FormAlert.SUCCESS]
    )
    with open("./project/json/minimum_valid.json", "r") as f:
        minimum_valid = Form(**dict(json.load(f)))
    assert (
        get_form_submission_success_alert(minimum_valid) == CONFIG.default_success_alert
    )


@pytest.mark.asyncio
async def test_get_email_recipients():
    emails = ["me1@example.com", "me2@example.com"]
    recipients = get_email_recipients(
        [FormNotify(recipient=emails[0]), FormNotify(recipient=emails[1])]
    )
    assert recipients[0] == emails[0]
    assert recipients[1] == emails[1]
    assert len(recipients) == len(emails)
