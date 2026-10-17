# Slides outline

Design only. There is no deck in this repo, no exported file, and no hosted player.

If someone builds a deck later, the slides are an outline of the modules, not a second source of truth. The commands in the README win when they disagree.

| # | Slide | Must say | Must not say |
| --- | --- | --- | --- |
| 1 | Title | Offline class. Fake provider. Synthetic depot. | That a team already runs this in production |
| 2 | The loop | Propose, gate, effect, stop | A vendor architecture diagram |
| 3 | Stop rules | `final` beats the cap | An infinite loop "until the model is done" |
| 4 | Tools | Types, least privilege, human grant | "The prompt is the policy" |
| 5 | MCP frames | Three methods, stdio, read-only export | "This is the official SDK" |
| 6 | Invariants | Two tool orders, one gate | An exact tool trace as the oracle |
| 7 | Money | Simulated rate, cap can be zero | A vendor price without a URL and a date |
| 8 | Injection | Quote is allowed. Write is not | "We filter the phrase so we are safe" |
| 9 | Capstone | Green eval | A live API key on the slide |
| 10 | Red on purpose | Exit code 1 is the point | A screenshot of a green regression |

Vendor-specific slides (a particular host's request format) are out of scope. If a later outline adds them, it has to use only that vendor's public docs, with the URL and the date accessed, and it stays design-only relative to CI.
