# Security

This is a private teaching repo. It is not a service. Please do not open it to the public as part of a class unless the owner decides that.

## Reporting

Open a private security advisory on this repository, or contact the maintainer out of band. Do not put keys, tokens, or customer data in the report.

## What we expect contributors to do

- Do not commit `.env`, API keys, or real connection strings. `.env.example` has empty placeholders.
- Do not point CI at a live model. `WORKSHOP_ENABLE_LIVE_PROVIDER` stays unset in `.github/workflows/ci.yml`.
- Do not add real personal data or real company names to fixtures. The depot is synthetic.
- Run `python -m workshop secretscan .` before you push. CI runs it too.

## What the code enforces

- The default provider is fake. The live adapter raises `LiveProviderDisabled` unless two environment flags are set and a URL and key are present.
- Logs use `Settings.public_dict`, which records whether a key is set and does not record the key.
- The teaching server writes protocol frames to stdout and logs to stderr.
- Tests monkeypatch socket connect so a test that tries to open a network connection fails.

## Known limits

The secret scan looks for a few token shapes. It will miss a secret that does not match them. The human "approver" string is not an identity check. Keyword detection in module 6 is not a security control.
