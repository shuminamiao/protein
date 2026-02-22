"""Map model predictions into a qPCR validation panel template."""

from __future__ import annotations

import argparse
import pandas as pd


def build_qpcr_panel(pred_df: pd.DataFrame, top_k: int = 10) -> pd.DataFrame:
    """
    pred_df columns required:
      - gene
      - predicted_logfc
      - pathway (optional)
    """
    up = pred_df.sort_values("predicted_logfc", ascending=False).head(top_k // 2)
    down = pred_df.sort_values("predicted_logfc", ascending=True).head(top_k // 2)
    panel = pd.concat([up, down], ignore_index=True)
    panel["predicted_direction"] = panel["predicted_logfc"].apply(
        lambda x: "up" if x > 0 else "down"
    )
    panel["primer_fwd"] = ""
    panel["primer_rev"] = ""
    panel["is_housekeeping"] = False
    return panel[
        [
            "gene",
            "predicted_logfc",
            "predicted_direction",
            "pathway",
            "primer_fwd",
            "primer_rev",
            "is_housekeeping",
        ]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", required=True, help="CSV of model predictions")
    parser.add_argument("--out", required=True, help="Output qPCR panel CSV")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()

    pred_df = pd.read_csv(args.pred)
    if "pathway" not in pred_df.columns:
        pred_df["pathway"] = "NA"
    panel = build_qpcr_panel(pred_df, top_k=args.top_k)
    panel.to_csv(args.out, index=False)


if __name__ == "__main__":
    main()
