# HTML email templates

A shared home for polished, consistent HTML emails across my projects. This repository is the reference whenever a person or coding agent creates an email: start from an existing sample, keep the design conventions, and adapt the content and branding to the project.

The goal is to replace ad hoc email formatting with a small, reusable design language. Gmail is the primary target, both in a desktop browser and in the mobile app. Native desktop email clients matter too, starting with Apple Mail; check Outlook when a project's audience needs it.

## What's here

- `samples/welcome/`: a welcome message with a primary action.
- `samples/notification/`: a summary notification with a primary action.
- Each sample includes `email.html`, a matching `email.txt` fallback, and `subject.txt`.
- `preview/index.html`: side-by-side desktop (800px) and mobile (375px) browser previews with a sample selector.
- `scripts/export_eml.py`: packages a sample as a multipart `.eml` file for local inspection. It does not send email.

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

The `open` command is for macOS; on other systems open the resulting file manually. Repeat with `notification`. Generated files stay in the ignored `output/` directory. Opening an `.eml` is a local rendering check; delivery through the actual sending provider still needs testing.

## Design conventions

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

1. Review both samples in the preview page, including narrow widths around 320px and 375px using browser responsive mode on the individual HTML file.
2. Use a consuming project's email sender to send the sample HTML, plain text, and subject to your own test inbox. Use the actual HTML body field/API; pasting rendered content into Gmail's composer can alter the markup.
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

Clone the private repository with an authenticated GitHub account:

```sh
git clone git@github.com:henrypoydar/html-email-templates.git
git -C html-email-templates rev-parse HEAD
```

For coding agents, include this instruction in the consuming project's instructions or email task:

> Use henrypoydar/html-email-templates as the design reference for HTML emails. Read its README and start with the closest sample. Preserve the layout, inline styling, mobile behavior, and matching plain-text alternative. Adapt branding and content to this project, record the source commit, and test the delivered result in Gmail desktop and mobile.

Pin integrations to a reviewed commit or, once available, a release tag. Avoid fetching templates from the moving `main` branch at send time. Bring reusable improvements back here so projects can adopt them deliberately.

## Next steps

1. **Approve the visual direction.** Preview the two samples and settle on shared colors, typography, spacing, button style, and which branding stays project-specific.
2. **Test one real integration.** Pick a project and its existing email provider, adapt the welcome sample, and send it to a test Gmail inbox. This repo currently has no delivery integration.
3. **Verify the client matrix.** Test both samples in Gmail desktop/mobile and Apple Mail, fix issues, and record results and screenshots.
4. **Add the common email types.** Prioritize password resets, invitations, receipts, and richer digests based on actual project needs.
5. **Version the reference.** Once the first templates pass client checks, tag `v0.1.0` and pin consuming projects to it. Extract shared components or add a package/build pipeline when repeated integration work justifies it.
