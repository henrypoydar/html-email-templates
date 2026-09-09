"""Send an HTML + plain-text sample through Gmail SMTP using an app password."""

import argparse
import os
import smtplib
import ssl
from email import policy
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample", choices=[p.name for p in sorted((ROOT / "samples").iterdir()) if p.is_dir()])
    parser.add_argument("--to", help="Recipient address; defaults to GMAIL_EMAIL")
    args = parser.parse_args()
    sender = os.environ.get("GMAIL_EMAIL", "").strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    if not sender or not password:
        parser.error("Set GMAIL_EMAIL and GMAIL_APP_PASSWORD in your environment. See README.md.")
    recipient = args.to or sender
    for address in (sender, recipient):
        if any(char.isspace() for char in address) or address.count("@") != 1 or any(char in address for char in ",;<>"):
            parser.error("Use a single email address without a display name for GMAIL_EMAIL and --to.")

    sample = ROOT / "samples" / args.sample
    message = EmailMessage(policy=policy.SMTP)
    message["Subject"] = "[Template test] " + sample.joinpath("subject.txt").read_text(encoding="utf-8").strip()
    message["From"] = sender
    message["To"] = recipient
    message["Date"] = formatdate(localtime=True)
    message["Message-ID"] = make_msgid()
    message.set_content(sample.joinpath("email.txt").read_text(encoding="utf-8"))
    message.add_alternative(sample.joinpath("email.html").read_text(encoding="utf-8"), subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=30) as smtp:
            smtp.login(sender, password)
            smtp.send_message(message, from_addr=sender, to_addrs=[recipient])
    except smtplib.SMTPAuthenticationError:
        parser.exit(1, "Gmail authentication failed. Check GMAIL_EMAIL and your Google app password.\n")
    except ssl.SSLCertVerificationError:
        parser.exit(1, "TLS certificate verification failed before sending. Configure Python's CA certificates; on macOS try SSL_CERT_FILE=/etc/ssl/cert.pem.\n")
    except (smtplib.SMTPException, OSError) as error:
        detail = str(error).replace(password, "[redacted]")
        raw_password = os.environ.get("GMAIL_APP_PASSWORD", "")
        if raw_password:
            detail = detail.replace(raw_password, "[redacted]")
        parser.exit(1, f"{type(error).__name__}: {detail}\nSMTP delivery could not be confirmed; check Sent before retrying.\n")
    print(f"Gmail accepted the {args.sample} sample for delivery to {recipient}.")


if __name__ == "__main__":
    main()
