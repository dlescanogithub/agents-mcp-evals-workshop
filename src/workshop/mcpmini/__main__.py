"""stdio entrypoint: python -m workshop.mcpmini"""

from __future__ import annotations

from workshop.mcpmini.server import main

if __name__ == "__main__":
    raise SystemExit(main())
