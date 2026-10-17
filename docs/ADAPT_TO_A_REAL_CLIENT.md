# Adapt this to a real client

Short version. Do the discovery questions in [DISCOVERY.md](DISCOVERY.md) first. Keep the synthetic depot until their read-only lookup is boringly correct.

1. Replace the handlers in `tools/execute.py` with a read of their system. Leave `authorize_tool` in front. Do not let the model hold a credential; the process should.
2. Keep writes off the first milestone. If a write is required, the grant has to come from their approval system, not from a string the model can emit.
3. Replay a cassette of their sanitized transcripts through the same invariant gate before any live flag is turned on. Strip personal data before it lands in this repo; better, keep the cases in their private repo.
4. Change the money cap and the price source. Delete the simulated constant from any slide that talks about their bill. Cite their provider's public pricing page with the date.
5. Add a vendor-specific lesson only from public docs, with the URL and the access date, and do not call it from CI.
6. Agree who updates golden cases. If that name is missing, stop.

This file is not a proposal and it does not name a client, because none is in scope.
