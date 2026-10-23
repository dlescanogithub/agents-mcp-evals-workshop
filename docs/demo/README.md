# Demo recording

Narrated recording of a real offline run, with a number trace.

[agents_mcp_evals_workshop_demo_en.mp4](agents_mcp_evals_workshop_demo_en.mp4) is about 106 seconds. The narration is English. The voice is text-to-speech generated with xAI. The video binary was not edited. Subtitle cue files are English. The `.es.srt` name is the original track filename; its cues are the same English lines as the `.en.srt` file.

- [English subtitles](agents_mcp_evals_workshop_demo_en.en.srt)
- [English subtitles (original `.es.srt` filename)](agents_mcp_evals_workshop_demo_en.es.srt)
- [Script that was used](script_used_agents_mcp_evals_workshop_demo_en.md)

The take was recorded on a fresh clone of this repo's main (`2b1209375b8f`, package 0.1.1, Python 3.12.15). It is fully offline: a fake provider, no API key, and no network call. The badge on screen says OFFLINE. Every number on screen or in the narration comes from that run. The map is [evidence_agents_mcp_evals_workshop_demo/number_trace.md](evidence_agents_mcp_evals_workshop_demo/number_trace.md).

## Commands

The terminal in the video uses a `lab $` prompt. The commands, as recorded in [terminal_take/terminal_dump.txt](evidence_agents_mcp_evals_workshop_demo/terminal_take/terminal_dump.txt) and mapped by scene in the number trace:

```bash
python -m workshop demo 2>/dev/null
jq -c '{method,tool:.params.name}' rq/list.json rq/adjust.json
python -m workshop.mcpmini < rq/list.json 2>/dev/null | jq -c '.result.tools|map(.name)'
python -m workshop.mcpmini < rq/adjust.json 2>/dev/null | jq -c .error
python -m workshop eval 2>/dev/null
python -m workshop eval-regression 2>/dev/null; echo exit=$?
python -m workshop check module-1 2>&- | head -1 | cut -d' ' -f1-4; python -m workshop check all --impl solution 2>&-
sed -n '9p' README.md | fold -s -w 126
sed -n '135p;137p;139p' README.md | fold -s -w 126
```

The `sed` lines print README text. They are not a run. The JSON-RPC requests fed to `workshop.mcpmini` are in [sources/rq/](evidence_agents_mcp_evals_workshop_demo/sources/rq/).

## Limits

These are the limits stated in the number trace and on the README lines the recording shows:

- The workshop has not been delivered.
- Two sessions of three hours (2×3 h) is [EST].
- `Approval.approver` is a label. The recording does not authenticate a person.
- MCP here is a small teaching subset, not the official SDK.
- Passing the gate means the synthetic cases passed. It does not show production readiness. The model is a script (fake provider).

The README numbers this take matches were measured on main commit `496a705` and Python 3.12.3. This take ran on main `2b12093` (docs-only commits since) and Python 3.12.15. Pytest, ruff, mypy, and secretscan results quoted in the README are not shown in the video.

## Spend

[spend.md](evidence_agents_mcp_evals_workshop_demo/spend.md) covers text-to-speech only. The figure is estimated. The take made no live model calls.

## Evidence

- [number_trace.md](evidence_agents_mcp_evals_workshop_demo/number_trace.md)
- [spend.md](evidence_agents_mcp_evals_workshop_demo/spend.md)
- [stt_transcript.txt](evidence_agents_mcp_evals_workshop_demo/stt_transcript.txt)
- [terminal_take/](evidence_agents_mcp_evals_workshop_demo/terminal_take/)
- [code/](evidence_agents_mcp_evals_workshop_demo/code/)
- [sources/](evidence_agents_mcp_evals_workshop_demo/sources/), including [rq/](evidence_agents_mcp_evals_workshop_demo/sources/rq/)
