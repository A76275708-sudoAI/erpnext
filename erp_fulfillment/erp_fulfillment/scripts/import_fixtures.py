"""Bench-executable wrapper.

bench --site <site> execute erp_fulfillment.scripts.import_fixtures.run
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_standalone():
    # Prefer the standalone script next to the app root (erp_fulfillment/scripts/)
    standalone = Path(__file__).resolve().parents[2] / "scripts" / "import_fixtures.py"
    if standalone.is_file():
        spec = importlib.util.spec_from_file_location(
            "erp_fulfillment_import_fixtures_standalone", standalone
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        return mod
    raise ImportError(f"standalone import_fixtures.py not found at {standalone}")


def run(fixtures_dir: str | None = None):
    return _load_standalone().run(fixtures_dir=fixtures_dir)
