# xAI spend (this video: agents_mcp_evals_workshop_demo_en)
- TTS (voice leo, speed 1.08): 1701 characters (first draft, discarded as too long) + 1393 (second draft) + 801 (4 scenes re-generated to shorten) + 198 (1 scene re-generated for pronunciation) = 4093 characters x US$15 / 1M = about US$0.061. Estimated from character counts at the listed rate; the API response did not include a cost field.
- STT check (grok-voice-transcribe-2.0, US$0.10/h): 2 transcriptions of about 105 s = about US$0.006 (estimated from duration).
- Live model calls (LLM): none. The workshop's live provider and `llm-judge` are off by default and were not enabled. The run is fully offline; the badge on screen says so. XAI_API_KEY was removed from the terminal environment of the take and was not written to any file.
- Total for this video: about US$0.07 (estimated).
