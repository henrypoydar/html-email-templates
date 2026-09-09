# HTML email templates

Based on [GitHub Primer](https://primer.style/) and its [Product UI design guidelines](https://primer.style/product/), adapted for HTML email. The templates use Primer's colors, typography, spacing, and component styling, with email-compatible markup and light/dark appearance support. This is an independent project, not an official GitHub template library.

A shared home for polished, consistent HTML emails across my projects. This repository is the reference whenever a person or coding agent creates an email: start from an existing sample, keep the design conventions, and adapt the content and branding to the project.

The goal is to replace ad hoc email formatting with a small, reusable design language. Gmail is the primary target, both in a desktop browser and in the mobile app. Native desktop email clients matter too, starting with Apple Mail; check Outlook when a project's audience needs it.

## What's here

- `samples/welcome/`: a welcome message with a primary action.
- `samples/notification/`: a summary notification with a primary action.
- `samples/brief/`: a longer brief with an optional announcement above the TL;DR, followed by sections with paragraphs, bulleted and numbered lists, bold, italics, and links.
- Each sample includes `email.html`, a matching `email.txt` fallback, and `subject.txt`.
- `preview/index.html`: side-by-side desktop (800px) and mobile (375px) browser previews with a sample selector.
- `scripts/export_eml.py`: packages a sample as a multipart `.eml` file for local inspection. It does not send email.
- `scripts/send_gmail.py`: sends a sample through Gmail SMTP to inspect in a real inbox.

These are starter reference designs with fictional content and `example.com` links. They are not yet verified in real email clients. No sending provider or framework is required to view them.

## Preview locally

From this directory, with Python 3 installed:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://localhost:8000/preview/> and select a sample. Stop the server with Ctrl+C. You can also open `preview/index.html` directly in a browser.

To inspect an email file in a desktop client that supports opening `.eml` files:

```sh
python3 scripts/export_eml.py welcome
open output/welcome.eml
```

The `open` command is for macOS; on other systems open the resulting file manually. Repeat with `notification` or `brief`. Generated files stay in the ignored `output/` directory. Opening an `.eml` is a local rendering check; delivery through the actual sending provider still needs testing.

## Send a test through Gmail

Use Python 3 and a Gmail app password with the [Gmail SMTP service](https://support.google.com/a/answer/176600?hl=en). The sender uses TLS on `smtp.gmail.com:465`, sends both HTML and plain text, and defaults to your own inbox.

Create an app password at [Google App Passwords](https://myaccount.google.com/apppasswords) for the sending account, with a name such as `HTML email templates`. This requires 2-Step Verification. Use the generated password in the hidden prompt below.

From the repository directory, run this in zsh (the default macOS shell). Replace the example sender and recipient with your own addresses. These macOS certificate settings were verified in the brief test:

```zsh
export GMAIL_EMAIL='you@gmail.com'
export SSL_CERT_FILE=/etc/ssl/cert.pem
read -rs 'GMAIL_APP_PASSWORD?Gmail app password: '; echo
export GMAIL_APP_PASSWORD
python3 scripts/send_gmail.py brief --to your-test-inbox@example.com
```

The password lives in the environment of this terminal session and its child processes. Run the sender in that same terminal; exporting a variable there does not make it available to an already-running agent or another terminal. The hidden prompt keeps the actual password out of shell history. Use a Google app password, not your normal account password. The script accepts Google's spaced app-password format. It does not load `.env` files automatically.

If `GMAIL_APP_PASSWORD` is already exported in your terminal, you can skip the password prompt and run:

```sh
export SSL_CERT_FILE=/etc/ssl/cert.pem
GMAIL_EMAIL=you@gmail.com python3 scripts/send_gmail.py brief --to your-test-inbox@example.com
```

Expected output:

```text
Gmail accepted the brief sample for delivery to your-test-inbox@example.com.
```

On September 9, 2026, this command successfully submitted the brief to Gmail SMTP. Inbox receipt and visual rendering still need review. Look for **[Template test] Weekly brief: a simpler first week** in the recipient inbox, including Spam if necessary. Check the announcement, TL;DR, section spacing, lists, emphasis, and links on desktop and mobile.

To send a different sample or choose another test inbox:

```sh
python3 scripts/send_gmail.py welcome
python3 scripts/send_gmail.py brief --to another-inbox@example.com
```

Each invocation sends one real email with a `[Template test]` subject prefix. Open the received message in Gmail desktop and mobile. Sample links still point to `example.com`.

The `SSL_CERT_FILE` setting above fixes the missing default CA certificate file encountered with this Mac's Python installation, while keeping TLS certificate verification enabled. On other systems, use their configured CA certificates instead of the macOS path. For a Python.org installation, its `Install Certificates.command` in the corresponding `/Applications/Python .../` folder can also configure Python's default certificates.

When finished, remove the password from the current shell:

```sh
unset GMAIL_APP_PASSWORD
```

## Writing a brief

### Structure and content

Start with `samples/brief/`. Keep the TL;DR near the top: state the main takeaway and any decision or action the reader needs to take. The optional announcement sits immediately above it, after the brief title. To omit the announcement, remove the entire table between the `OPTIONAL ANNOUNCEMENT START` and `OPTIONAL ANNOUNCEMENT END` comments, and remove the corresponding announcement from `email.txt`. Its spacing is contained within that table.

Follow the summary with as many sections as needed. Use an `h2` for each section heading, `p` for paragraphs, `ul` or `ol` for lists, `strong` for bold emphasis, `em` for italics, and descriptive `a` links. Copy the sample's inline styles when adding blocks. Keep the plain-text version in sync, including every destination URL. Briefs can have several contextual links without a large primary-action button.

Preview the brief with and without its announcement, and scroll through the full desktop and mobile frames to inspect the longer content.

### Announcement and summary

The optional announcement adapts Primer's [informational Banner](https://primer.style/product/components/banner/) for email: a transparent background, 1px blue outline, 6px corners, and 16px padding. Its label is 14px semibold with a `1.5` line height; the message is 14px regular with the same line height. Keep it brief and use a descriptive link for more detail. The visible label identifies its purpose without relying on color. This static email adaptation has no dismiss control or live-alert behavior.

The TL;DR uses a neutral inset panel: Primer's `bgColor-muted`, a 1px `borderColor-default` outline, 6px corners, and 20px padding. This visual grouping works with a sentence, several paragraphs, or a list; bullets are optional. It uses the same 20px semibold / `1.625` heading as the later sections, followed by 16px / `1.5` body text. Keep the main takeaway and any requested decision here. The summary panel has its own light/dark colors; the announcement and outer email canvas stay transparent.

Keep the `email-summary` class and its inline background, border, and text colors together when reusing the panel. For multiple paragraphs, use 12px between them and no bottom margin on the last one. Lists use the same 16px body typography and 24px left padding as the main sections.

## Design conventions

### GitHub Primer

The samples follow [Primer Product UI](https://primer.style/product/), GitHub's design system: neutral text, blue links, subtle separators, system typography, and green primary actions. The experimental palettes have been replaced by this shared design.

Color values are taken from `@primer/primitives` **11.10.0** ([light tokens](https://unpkg.com/@primer/primitives@11.10.0/dist/css/functional/themes/light.css), [dark tokens](https://unpkg.com/@primer/primitives@11.10.0/dist/css/functional/themes/dark.css)).

| Role | Primer token | Light | Dark |
| --- | --- | --- | --- |
| Body and headings | `fgColor-default` | `#1f2328` | `#f0f6fc` |
| Secondary text | `fgColor-muted` | `#59636e` | `#9198a1` |
| Links | `fgColor-accent` | `#0969da` | `#4493f8` |
| Separators | `borderColor-default` | `#d1d9e0` | `#3d444d` |
| Summary panel fill | `bgColor-muted` | `#f6f8fa` | `#151b23` |
| Announcement outline | `borderColor-accent-emphasis` | `#0969da` | `#1f6feb` |
| Primary button background | `button-primary-bgColor-rest` | `#1f883d` | `#238636` |
| Primary button text | `button-primary-fgColor-rest` | `#ffffff` | `#ffffff` |

The font stack uses native system fonts with Helvetica/Arial fallbacks; no font downloads are required. Spacing uses 4px increments and buttons have 6px corners.

This is an email adaptation: resolved token values are inline, with dark-mode overrides in the head, rather than loading Primer's web components or CSS variables. The email canvas stays transparent. The browser preview uses Primer's white and `#0d1117` reading surfaces to compare contrast; the actual email client controls its own surface. The announcement is outlined and the summary has a subtle neutral fill. The project keeps its own name and content.

### Typography rules

Use complete [Primer typography styles](https://primer.style/product/primitives/typography/#line-height), pairing size, weight, and line height rather than applying one line height everywhere.

| Email role | Primer style | Size | Weight | Unitless line height |
| --- | --- | --- | --- | --- |
| Main title | Title large | 32px | 600 | 1.5 |
| Section headings, TL;DR | Title medium | 20px | 600 | 1.625 |
| Wordmark | Title small | 16px | 600 | 1.5 |
| Paragraphs and lists | Body large | 16px | 400 | 1.5 |
| Metadata, announcement, sign-off | Body medium | 14px | 400 | 1.5 |
| Footer | Body small | 12px | 400 | 1.625 |

The announcement heading uses 14px semibold / `1.5` to fit its compact banner treatment.

Line height is a multiplier of font size: 16px body text at `1.5` produces a 24px line box. Keep paragraph margins separate from line height. Titles retain the same size on mobile; only outer spacing changes.

Use inline `font-weight:600` on `strong` for semibold emphasis, and `em` for italics. Links inherit the surrounding text size. Action buttons use 16px semibold text at `1.5` as an email-specific adaptation. Keep semantic headings, left alignment, and the 600px content limit.

Primer publishes sizes in `rem`; these standalone emails use their pixel equivalents at a 16px root with unitless line heights and literal inline values.

### Light and dark appearance

All samples declare support for light and dark color schemes and include `prefers-color-scheme: dark` styles for text, links, rules, and buttons. Their outer canvas and content backgrounds stay transparent so the email client's reading surface shows through. Keep the `email-*` classes as well as inline styles when copying or adding styled elements.

The preview's **Appearance** selector offers System (automatic), Light, and Dark. This checks browser rendering of the authored styles. Gmail support differs by client: its apps can transform colors themselves instead of applying these media queries. See [Litmus's client testing guide](https://www.litmus.com/blog/the-ultimate-guide-to-dark-mode-for-email-marketers). Automatic appearance is implemented for clients that honor the styles; exact Gmail colors and readability still require a received-message check in both modes. A dark Gmail interface does not necessarily imply a dark message surface.

### Layout and content

- Use a restrained palette, generous spacing, a clear heading, readable system fonts, and one primary action.
- Keep the main content within 600px, with a fluid width and a small-screen spacing adjustment.
- Use presentation tables for email layout and inline essential styles. Keep media queries as enhancements. Gmail supports a subset of CSS, including media queries; see [Google's CSS support reference](https://developers.google.com/workspace/gmail/design/css).
- Include a subject, hidden preview text, meaningful link labels, and a matching plain-text body. Send both bodies as `multipart/alternative`.
- Keep important information as live text. Add useful alt text and explicit dimensions when introducing images.
- Replace all sample names, branding, destinations, and footer wording before use. Include preference or unsubscribe links appropriate to the message type.
- Escape dynamic text and attribute values with the consuming framework's escaping helpers. Validate dynamic link destinations. Do not insert arbitrary HTML from users.

## AgentMail: send both bodies

[AgentMail recommends providing both `text` and `html`](https://www.agentmail.to/docs/messages#why-both-text-and-html). HTML provides the styled experience, while plain text gives clients an alternative when HTML is unavailable. This repository treats both as required outputs, with equivalent content and destinations.

When using AgentMail, map the sample files to these send fields:

| AgentMail field | Sample file |
| --- | --- |
| `subject` | `subject.txt` (trim the trailing newline) |
| `text` | `email.txt` |
| `html` | Full contents of `email.html` |

Pass both bodies in the same `client.inboxes.messages.send(...)` call along with your sending `inbox_id` and test recipient `to`. Keep the full HTML document, including its head styles. The samples use inline essential styles plus a head style block for mobile spacing. Test the delivered result before adopting it in a project.

## Test in real email clients

Browser previews help with layout, but they do not emulate Gmail's processing, dark mode, or a desktop email client's rendering engine.

1. Review each sample in the preview page, including narrow widths around 320px and 375px using browser responsive mode on the individual HTML file.
2. Start with the Gmail SMTP test path above to inspect a delivered sample. Also test through a consuming project's email sender before adopting it there. Use the actual HTML body field/API; pasting rendered content into Gmail's composer can alter the markup.
3. Inspect the received message in Gmail desktop web, Gmail on your phone, and Apple Mail. Add Outlook if required by the consuming project.
4. Check light and dark mode, images disabled (when applicable), long names and headings, long links, and larger text. Confirm there is no horizontal overflow or clipped content and that the primary action remains readable and tappable.
5. Check the inbox subject and preview text, every link, footer content, and the plain-text part.
6. Record the tested commit, date, client/app version, device, appearance mode, and outcome in `docs/testing.md`. Keep screenshots with the review or in `docs/screenshots/`, using fictional data.

Initial verification status:

| Client | Status |
| --- | --- |
| Gmail desktop web | Not tested |
| Gmail mobile app | Not tested |
| Apple Mail | Not tested |
| Outlook | Not tested; project-dependent |

## Reuse from another project

For now, copy the nearest sample into the consuming project's mailer, adapt its content through that project's template engine, and record the source commit SHA. This keeps the library independent of any framework or sending provider. There is no shared rendering package yet.

Clone the public repository:

```sh
git clone https://github.com/henrypoydar/html-email-templates.git
git -C html-email-templates rev-parse HEAD
```

For coding agents, include this instruction in the consuming project's instructions or email task:

> Use henrypoydar/html-email-templates as the design reference for HTML emails. Read its README and start with the closest sample. Preserve the layout, inline styling, mobile behavior, and matching plain-text alternative. Adapt branding and content to this project, record the source commit, and test the delivered result in Gmail desktop and mobile.

Pin integrations to a reviewed commit or, once available, a release tag. Avoid fetching templates from the moving `main` branch at send time. Bring reusable improvements back here so projects can adopt them deliberately.

## Next steps

1. **Approve the visual direction.** Preview the samples and settle on shared colors, typography, spacing, button style, and which branding stays project-specific.
2. **Test one real integration.** Use the Gmail sender above for an initial rendering check, then pick a project and its existing email provider, adapt a sample, and test delivery through that provider too.
3. **Verify the client matrix.** Test each sample in Gmail desktop/mobile and Apple Mail, fix issues, and record results and screenshots.
4. **Add the common email types.** Prioritize password resets, invitations, receipts, and richer digests based on actual project needs.
5. **Version the reference.** Once the first templates pass client checks, tag `v0.1.0` and pin consuming projects to it. Extract shared components or add a package/build pipeline when repeated integration work justifies it.

## License

[MIT](LICENSE) — Copyright (c) 2026 Henry Poydar.
