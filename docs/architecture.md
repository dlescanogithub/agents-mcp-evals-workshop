# Architecture

## Pieces

| Piece | Path | Job |
| --- | --- | --- |
| Settings | `src/workshop/config.py` | Read the environment only |
| Logs | `src/workshop/logging_setup.py` | One JSON object per line, stderr |
| Retries | `src/workshop/retries.py` | Max attempts, delay capped |
| Trace | `src/workshop/tracing.py` | JSONL file or an in-memory list |
| Budget | `src/workshop/budget.py` | Simulated price and the admission check |
| Depot | `src/workshop/domain.py` | Three SKUs, three notes, all synthetic |
| Tools | `src/workshop/tools/` | Typed args, grant check, handlers |
| Loop | `src/workshop/agent/loop.py` | Steps, budget, retries, effects |
| Fake provider | `src/workshop/providers/fake.py` | Replay a script, ignore the prompt |
| Cassette | `src/workshop/providers/cassette.py` | JSON form of a script |
| Live adapter | `src/workshop/providers/live.py` | Off unless explicitly enabled |
| MCP subset | `src/workshop/mcpmini/` | Stdio JSON-RPC, two read tools |
| Gate | `src/workshop/evalkit/` | Golden cases and invariant ids |
| Deterministic checker | `src/workshop/evalkit/checker.py` | Phrase check vs author reference labels |
| Optional LLM judge | `src/workshop/evalkit/llm_judge.py` | Off unless configured. Not used by the gate |
| Lab follower | `src/workshop/labs/injection.py` | One scripted obedience to a note |
| Grader | `src/workshop/grading.py` | Loads `exercises/` or `solutions/` |
| CLI | `src/workshop/cli.py` | demo, eval, check, secretscan, llm-judge |

## Request path for the demo

1. `demo` loads the cassette turns.
2. `run_agent` copies the seed depot.
3. Each step asks `allow_model_call` with a reserve of 0.0001 simulated USD.
4. `FakeProvider.complete` returns the next `ModelTurn` and does not read messages.
5. A tool turn goes through `authorize_tool` and `execute`.
6. The final turn stops the loop.
7. The process prints the answer and the effect list.

No step opens a socket.

## MCP path

`python -m workshop.mcpmini` reads one JSON object per line on stdin and writes one JSON object per line on stdout. The client in `mcpmini/client.py` starts that process with pipes. The server implements:

- `server/discover`
- `tools/list`
- `tools/call` for `inventory.lookup` and `notes.search`
- an error for legacy `initialize`, naming revision `2026-07-28`
- an `Unsupported protocol version` error (`-32022`) when `_meta` does not carry that revision

It does not implement resources, prompts, tasks, pagination cursors, cancellation, streamable HTTP, icons, or full JSON Schema validation. Argument checks are the same small type check as the in-process tools.

The capstone does not spawn this process. It calls `execute` so a stuck subprocess cannot stall the gate. Module 3 is the stdio exercise, and `lookup_sku` is the subprocess test.

## Why two tool orders both pass

`shift_lookup` looks up stock and then notes. `shift_lookup_swapped` does the opposite. Both finals contain `bin B-1` and `recount matches the card`, and neither writes. The invariant list does not contain "tool order".

## Trust boundary

| Data | Trusted? |
| --- | --- |
| Tool catalog in code | Yes, it is the allowlist |
| `Approval.granted` | Yes, as far as this class goes. It is not a signed identity |
| Model turn from the fake provider | It may request a tool. The loop may refuse |
| Note text | No. Stored as data and prefixed `untrusted tool data` when it returns to the loop |
| Learner exercise | Graded. It is not on the CI gate's agent |

The vulnerable path sets `trust_writes=True` only inside `run_regression`. The golden injection case uses the same follower with `trust_writes` left false, and the write is blocked.
