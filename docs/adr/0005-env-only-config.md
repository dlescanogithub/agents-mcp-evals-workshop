# 0005 Environment-only configuration

## Status

Accepted. 2026-10-17.

## Context

A committed `.env` is a common way to leak a key. A library that auto-loads `.env` hides that the process is configured from the outside.

## Decision

`load_settings` reads a mapping, defaulting to `os.environ`. It does not open a file. `.env.example` documents the variables. `.gitignore` ignores `.env`. The live API key is omitted from `public_dict`.

## Consequences

A local shell can `set -a && source .env && set +a` if someone wants a file. CI sets nothing and gets the fake provider. Tests pass a dict and never touch the developer environment.
