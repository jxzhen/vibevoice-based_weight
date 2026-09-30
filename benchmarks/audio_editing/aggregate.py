"""
Aggregate per-system audio-editing benchmark JSONs into a single comparison table.

Usage:
    python benchmarks/audio_editing/aggregate.py \\
        --results benchmarks/audio_editing/results/ \\
        --out benchmarks/audio_editing/summary.md
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


def fmt(v, digits=2):
    if v is None or (isinstance(v, float) and v != v):  # NaN check
        return "--"
    return f"{v:.{digits}f}"


def render_markdown(results: List[Dict[str, Any]]) -> str:
    if not results:
        return "# Audio Editing Comparison\n\n_No results yet._\n"
    lines = []
    lines.append("# Audio Editing Comparison")
    lines.append("")
    lines.append("Aligned with ICASSP 2027 AEC metrics. Higher is better for "
                 "SI-SDR / PESQ / STOI; lower is better for Mel L1 / LSD.")
    lines.append("")
    lines.append("| System | Audio | Text | Region | SI-SDR | PESQ | STOI | Mel L1 | LSD | Params B |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in results:
        region = f"[{fmt(r.get('region_start'))}, {fmt(r.get('region_end'))}] s"
        lines.append(
            f"| {r['system']} "
            f"| `{Path(r['audio']).name}` "
            f"| {r.get('text_instruction', '')[:40]} "
            f"| {region} "
            f"| {fmt(r.get('si_sdr'))} "
            f"| {fmt(r.get('pesq'))} "
            f"| {fmt(r.get('stoi'))} "
            f"| {fmt(r.get('mel_l1'))} "
            f"| {fmt(r.get('lsd'))} "
            f"| {fmt(r.get('n_params_B_total'))} |"
        )
    lines.append("")
    lines.append(f"_Total runs: {len(results)}._")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=str, required=True)
    parser.add_argument("--out", type=str, default="benchmarks/audio_editing/summary.md")
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