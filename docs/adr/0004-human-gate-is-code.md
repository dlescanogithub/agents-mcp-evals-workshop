# 0004 The human gate is code

## Status

Accepted. 2026-10-17.

## Context

A system prompt that says "do not change stock" is not a control. The lab note tells the model to change stock. The fake provider will request whatever the script says, including that write.

## Decision

`authorize_tool` allows a write only when the tool name is in `Approval.granted`. The model cannot add itself to that set by an argument. The MCP server does not export `inventory.adjust`. The regression path is the only caller that sets `trust_writes=True`, and the gate is expected to fail it.

The approver field is a label for the class. It is not authentication.

## Consequences

Module 2 can show a blocked write with an empty grant and a successful write with a grant. The injection lab can show the same request blocked or applied. A real deployment still needs an identity system in front of the grant.
