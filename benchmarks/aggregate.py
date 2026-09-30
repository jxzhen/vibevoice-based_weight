"""
Aggregate per-system benchmark JSONs into a single comparison table.

Usage:
    python benchmarks/aggregate.py --results benchmarks/results/ --out benchmarks/summary.md

Output:
    - benchmarks/summary.md  (Markdown table for the README / web demo)
    - benchmarks/summary.json (machine-readable, used by the web demo)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any


def load_results(results_dir: Path) -> List[Dict[str, Any]]:
    out = []
    for p in sorted(results_dir.glob("*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                out.append(json.load(f))
        except Exception as e:
            print(f"[warn] failed to read {p}: {e}")
    return out


def render_markdown(results: List[Dict[str, Any]]) -> str:
    if not results:
        return "# ASR Comparison Results\n\n_No results yet._\n"
    lines = []
    lines.append("# ASR Comparison Results")
    lines.append("")
    lines.append("| Audio | System | Lang | Audio s | Gen s | RTF | Params B | Transcript excerpt |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        excerpt = (r.get("transcript") or "").replace("\n", " ")[:80]
        lines.append(
            f"| `{Path(r['audio']).name}` "
            f"| {r['system']} "
            f"| {r.get('language', '?')} "
            f"| {r['audio_seconds']:.2f} "
            f"| {r['generation_seconds']:.2f} "
            f"| {r['rtf']:.2f} "
            f"| {r['n_params_B']:.2f} "
            f"| {excerpt} |"
        )
    lines.append("")
    lines.append(f"_Total runs: {len(results)}._")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=str, required=True, help="Directory of per-system JSON files")
    parser.add_argument("--out", type=str, default="benchmarks/summary.md")
    args = parser.parse_args()

    results_dir = Path(args.results)
    out_md = Path(args.out)
    out_json = out_md.with_suffix(".json")

    results = load_results(results_dir)
    md = render_markdown(results)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md, encoding="utf-8")
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[aggregate] Wrote {out_md}")
    print(f"[aggregate] Wrote {out_json}  ({len(results)} entries)")


if __name__ == "__main__":
    main()