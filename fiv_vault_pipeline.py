#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

STEPS = [
    ["python3", "extract_world_sailing_results.py"],
    ["python3", "extract_world_sailing_european_results.py"],
    ["python3", "extract_world_sailing_major_regattas.py"],
    ["python3", "extract_world_sailing_youth_para_results.py"],
    ["python3", "build_federvela_news_archive.py"],
    ["python3", "build_sportvela_news_archive.py"],
    ["python3", "update_fiv_convocazioni_bodrato.py"],
    ["python3", "build_obsidian_connective_layer.py"],
    # NOTA: audit_content_integrity.py e clean_editorial_residue.py sono stati
    # rimossi da questa pipeline il 2026-08-22: i file con quel nome in questa
    # cartella condivisa appartengono al progetto guida-vini, non al vault FIV
    # (path hardcoded su "guida-vini-site-local-ux-complete"). Se in futuro si
    # vogliono un audit/pulizia dedicati al vault FIV, vanno scritti da zero.
]


def run_step(cmd: list[str]) -> None:
    print(f"\n==> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    for cmd in STEPS:
        run_step(cmd)
    print("\nPipeline completata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
