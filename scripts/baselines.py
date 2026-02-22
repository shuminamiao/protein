"""Simple baseline models for perturbation prediction benchmarks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
from sklearn.linear_model import Ridge


@dataclass
class BaselineOutputs:
    ate_vector: np.ndarray
    mean_vector: np.ndarray
    linear_vector: np.ndarray


def ate_baseline(control_expr: np.ndarray, treated_expr: np.ndarray) -> np.ndarray:
    """Average Treatment Effect baseline: mean(treated - control)."""
    return treated_expr.mean(axis=0) - control_expr.mean(axis=0)


def mean_baseline(treated_expr: np.ndarray) -> np.ndarray:
    """Conditional mean baseline over observed treated cells."""
    return treated_expr.mean(axis=0)


def linear_baseline(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_query: np.ndarray,
    alpha: float = 1.0,
) -> np.ndarray:
    """Ridge regression baseline for expression prediction."""
    model = Ridge(alpha=alpha)
    model.fit(x_train, y_train)
    return model.predict(x_query)


def run_all_baselines(
    control_expr: np.ndarray,
    treated_expr: np.ndarray,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_query: np.ndarray,
) -> Dict[str, np.ndarray]:
    return {
        "ate": ate_baseline(control_expr, treated_expr),
        "mean": mean_baseline(treated_expr),
        "linear": linear_baseline(x_train, y_train, x_query),
    }
