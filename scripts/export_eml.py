"""Export a sample as multipart email for local inspection; never sends mail."""

import argparse
from email import policy
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample", choices=[p.name for p in sorted((ROOT / "samples").iterdir()) if p.is_dir()])
    args = parser.parse_args()
    sample = ROOT / "samples" / args.sample
    message = EmailMessage(policy=policy.SMTP)
    message["Subject"] = sample.joinpath("subject.txt").read_text().strip()
    message["From"] = "Example <preview@example.com>"
    message["To"] = "Preview <recipient@example.com>"
    message.set_content(sample.joinpath("email.txt").read_text())
    message.add_alternative(sample.joinpath("email.html").read_text(), subtype="html")
    output = ROOT / "output" / f"{args.sample}.eml"
    output.parent.mkdir(exist_ok=True)
    output.write_bytes(message.as_bytes())
    print(output)


if __name__ == "__main__":
    main()
