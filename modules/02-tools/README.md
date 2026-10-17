# Module 2 — Tool design and guardrails

## Goal

Decide whether one tool call may run. The decision is a `Decision` with `allowed` and `reason`.

## Concepts

A tool spec has a name, an effect (`read` or `write`), and typed fields. You check, in order:

1. Unknown argument names → `unknown_argument`
2. Missing required field → `missing_argument`
3. Wrong JSON-ish type → `bad_type`. A bool is not an integer.
4. Write whose name is not in `approval.granted` → `needs_human_approval`
5. Otherwise → `ok`

Least privilege in this repo also means the MCP server does not export the write tool. That is module 3. Here the write exists so you can see the grant.

The handler must not run when you return `allowed=False`. The library's `execute` follows that rule. Your function returns the decision; the grader does not need you to call the handler.

## Files

- Edit `exercises/module_02/exercise.py`
- Library `src/workshop/tools/auth.py`

## Run

```bash
PYTHONPATH=src python -m workshop check module-2
```

## Reason codes the grader expects

`ok`, `missing_argument`, `unknown_argument`, `bad_type`, `needs_human_approval`.

## Common mistake

Reading an `approved: true` field out of the model arguments. Those arguments are untrusted. The grant is the `Approval` object.

## What this module does not do

It does not check a password or a directory. The approver string is a label.
