# HTML email templates

A shared home for polished, consistent HTML emails across my projects. This repository is the reference whenever a person or coding agent creates an email: start from an existing sample, keep the design conventions, and adapt the content and branding to the project.

## Samples

- **Welcome** — a welcome message with a primary action.
- **Notification** — a short update with a primary action.
- **Brief** — an optional announcement, a highlighted TL;DR, and sections with paragraphs, lists, emphasis, and links.

Each directory in `samples/` includes `email.html`, `email.txt`, and `subject.txt`. Content and links are placeholders.

## Preview

With Python 3, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://localhost:8000/preview/> for desktop and mobile previews in System, Light, or Dark mode. You can also open `preview/index.html` directly.

To export a sample for a client that opens `.eml` files:

```sh
python3 scripts/export_eml.py brief
```

The file is saved to `output/brief.eml`.

## Send a Gmail test

Create a [Google app password](https://myaccount.google.com/apppasswords) with 2-Step Verification enabled. From the repo, run these commands in **zsh**, replacing the addresses:

```zsh
export GMAIL_EMAIL='you@gmail.com'
read -rs 'GMAIL_APP_PASSWORD?Gmail app password: '; echo
export GMAIL_APP_PASSWORD
# macOS: use the system CA bundle if Python lacks default certificates.
export SSL_CERT_FILE=/etc/ssl/cert.pem
python3 scripts/send_gmail.py brief --to your-test-inbox@example.com
```

Use `welcome`, `notification`, or `brief`. Omitting `--to` sends to `GMAIL_EMAIL`. Each run sends HTML and plain text through Gmail SMTP with a `[Template test]` subject prefix.

Run in the same terminal where you exported the password; `.env` files are not loaded automatically. On other systems, omit the macOS certificate setting. Clear the password afterward with `unset GMAIL_APP_PASSWORD`.

SMTP submission has been verified. Check received emails in Gmail desktop and mobile, in both light and dark mode. Browser previews don't reproduce Gmail's color transformations; visual client testing is still pending.

## Reuse

Copy the closest sample into your project's mailer and record its source commit. Replace the branding, content, links, and footer. Preserve inline styles, `email-*` classes, and head styles; escape dynamic content through your template engine.

Keep the plain-text body in sync. With [AgentMail](https://www.agentmail.to/docs/messages#why-both-text-and-html), pass `subject.txt`, `email.txt`, and `email.html` as `subject`, `text`, and `html` in the same send call.

For briefs, remove the marked announcement table when unused and its matching plain text. The TL;DR panel supports prose or lists.

## Design

Based on [GitHub Primer Product UI](https://primer.style/product/), adapted for email using `@primer/primitives` 11.10.0 colors and [Primer typography](https://primer.style/product/primitives/typography/). This is an independent project.

Templates use a transparent 600px layout, blue links, neutral text, green action buttons, and light/dark styles. Titles are 32px; section headings 20px; body text 16px. Headings and emphasis are semibold. Line height is `1.5`, or `1.625` for section headings and 12px footer text.

## License

[MIT](LICENSE) — Copyright (c) 2026 Henry Poydar.
