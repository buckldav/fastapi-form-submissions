from fastapi_mail import FastMail, ConnectionConfig
from .config import CONFIG

conf = ConnectionConfig(
    MAIL_USERNAME=CONFIG.mail_username,
    MAIL_PASSWORD=CONFIG.mail_password,
    MAIL_FROM=CONFIG.mail_sender,
    MAIL_PORT=CONFIG.mail_port,
    MAIL_SERVER=CONFIG.mail_server,
    MAIL_FROM_NAME=CONFIG.mail_sender_name,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    # VALIDATE_CERTS=True,
)

fm = FastMail(conf)
