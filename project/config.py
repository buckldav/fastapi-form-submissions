from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    # FastMail SMTP server settings
    mail_console: bool = config("MAIL_CONSOLE", default=False, cast=bool)
    mail_server: str = config(
        "MAIL_SERVER", default="smtp.sendgrid.net"
    )  # smtp.sendgrid.net <- SendGrid SMTP server used for developement
    mail_port: int = config("MAIL_PORT", default=587, cast=int)
    mail_username: str = config("MAIL_USERNAME", default="")
    mail_password: str = config("MAIL_PASSWORD", default="")
    mail_sender: str = config(
        "MAIL_SENDER",
        default="noreply@example.com",  # Replace with desired email
    )
    mail_sender_name: str = config("MAIL_SENDER_NAME", default="Forms")
    mail_recipient: str = config("MAIL_RECIPIENT", default="me@example.com")

    # replies
    default_success_alert: str = config(
        "DEFAULT_SUCCESS_ALERT", default="Submission Received."
    )


CONFIG = Settings()
