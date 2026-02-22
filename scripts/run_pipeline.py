"""Entry point for the perturbation prediction closed-loop demo."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import yaml


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dirs(output_dir: str) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    return out


def save_run_metadata(config: dict, out_dir: Path) -> None:
    metadata = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project": config.get("project", {}),
        "paths": config.get("paths", {}),
        "models": config.get("models", {}),
        "baselines": config.get("baselines", {}),
        "metrics": config.get("metrics", []),
    }
    with open(out_dir / "run_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    out_dir = ensure_dirs(config["paths"]["output_dir"])
    save_run_metadata(config, out_dir)

    if args.dry_run:
        print("[DRY-RUN] Config loaded and metadata written.")
        print(f"Output directory: {out_dir.resolve()}")
        return

    # TODO: Integrate real data loading + model training/eval loops for GEARS/scGen.
    # Recommended structure:
    # 1) Load h5ad datasets
    # 2) Build holdout gene split
    # 3) Train models and baselines
    # 4) Evaluate on internal + external sets
    # 5) Export prediction tables for qPCR panel mapping
    print("Pipeline scaffold is ready. Replace TODO with full training/evaluation logic.")


if __name__ == "__main__":
    main()
