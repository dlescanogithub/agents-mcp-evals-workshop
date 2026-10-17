# Pre-reading

One sitting before session 1. No account, no install required to read this. Installing is in the README if you want to run the demo the night before.

## The loop

An agent in this class is a loop:

1. Ask a provider for a turn.
2. If the turn is a final answer, stop.
3. If the turn names a tool, run that tool only when the code allows it.
4. Append the tool result and go back to 1.
5. Stop anyway at a step cap or a budget cap.

The provider in the exercises is a script. It will not change its mind if you rephrase the question. That is a feature. You are testing the loop.

## A tool is a typed effect

`inventory.lookup` reads. `inventory.adjust` writes. A write needs a human grant: the tool's name sits in a set the program was given. A sentence in the user message is not a grant. A boolean is not an integer.

## An eval here is not a transcript

You will not be asked to match a list of tool calls in order. You will be asked questions like:

- Did the stock change?
- Does the answer mention the bin?
- Did the simulated cost stay under the cap?

Two different orders can both be right.

## What to ignore for now

MCP as a product surface, vendor model names, and prompt-injection filters. Session 1 module 3 shows a few JSON-RPC frames. Session 2 shows why a filter is not the control.

## Optional command

```bash
PYTHONPATH=src python -m workshop demo
```

You should see a bin id of `B-1`, `provider: fake`, and `network: none`.
