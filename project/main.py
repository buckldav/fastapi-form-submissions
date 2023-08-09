import jsonschema
import datetime
from fastapi import FastAPI, BackgroundTasks, Body, HTTPException
from starlette.responses import JSONResponse
from fastapi_mail import MessageSchema, MessageType
from project.mail import fm
from project.forms import (
    contact_form,
    get_email_recipients,
    get_form_submission_message,
    validate_submission,
    get_form_submission_success_alert,
)

app = FastAPI()


@app.post("/forms/{id}/submit")
async def submit_form(
    background_tasks: BackgroundTasks, id: str, submission: dict = Body(...)
) -> JSONResponse:
    """
    Doesn't actually get a form by id, it just uses the contact_form.
    Validates submission. If invalid, 400.
    If valid, sends an email to those listed in contact_form.notify.
    """
    try:
        validate_submission(submission, contact_form)
    except jsonschema.ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    message = MessageSchema(
        subject=f'Form submission received for {contact_form.jsonSchema["title"]}',
        recipients=get_email_recipients(contact_form.notify),
        body=get_form_submission_message(
            submission, contact_form, datetime.datetime.now()
        ),
        subtype=MessageType.plain,
    )

    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(
        status_code=200,
        content={"message": get_form_submission_success_alert(contact_form)},
    )
