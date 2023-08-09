# FastAPI Form Submissions

> WARNING: This code was written as a proof of concept. It does not have any practical use on its own.

## Motivation

- Handle form submissions for forms defined with jsonschema (like [react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/docs/)).
- Validate form submissions against their jsonschemas.
- Sends notifications (emails) on form submit.

No database on purpose as this project was created to test submission, validation, and messaging and that's it.

## Usage

### Environment

The environment mail settings use SendGrid as an example, but you may use any SMTP service. In SendGrid's case, the `MAIL_PASSWORD` is your API Key.

```bash
cp .env.example .env
```

The `MAIL_RECIPIENT` will receive an email when you submit a form.

### Run App

```bash
pip install -r requirements.txt
sh run.sh
```

> The `/forms/{id}/submit` endpoint currently does not get a form by id, it just uses `project/json/contact.json` as the form that it's submitting to.

### Tests

Tests are in `project/test_main.py`.

```bash
# run all test with output (-s)
pytest -s
# run a single test (-k)
pytest -k test_get_form_submission_success_alert
```
