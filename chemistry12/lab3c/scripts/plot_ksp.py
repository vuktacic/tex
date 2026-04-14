#!/usr/bin/env python3
"""Generate Ksp(x) model plot and overlay measured points from metadata.csv.

Saves output to ../images/ksp_plot.png (relative to this script's directory).
"""
from __future__ import annotations

import csv
from pathlib import Path
import math

import numpy as np
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "metadata.csv"
OUT_PNG = ROOT / "images" / "ksp_plot.png"


def ksp(x_ml: float) -> float:
    """Calculate Ksp as a function of added KI volume x in mL.

    Formula from the lab:
    Ksp(x) = (0.0020 * 50/(50+x)) * (0.020 * x/(50+x))**2
    """
    v0 = 50.0
    # concentrations
    denom = v0 + x_ml
    pb = 0.0020 * (v0 / denom)
    i = 0.020 * (x_ml / denom)
    return pb * (i ** 2)


def read_dv_values(path: Path) -> list[float]:
    dv = []
    with path.open() as fh:
        r = csv.reader(fh)
        header = next(r, None)
        for row in r:
            if not row:
                continue
            try:
                dv.append(float(row[0]))
            except Exception:
                # skip malformed rows
                continue
    return dv


def main() -> None:
    dv_vals = read_dv_values(DATA_CSV)
    if not dv_vals:
        raise SystemExit("No dv values found in metadata.csv")

    xs = np.linspace(0.1, max(20.0, max(dv_vals) + 1.0), 400)
    ys = [ksp(x) for x in xs]

    measured_x = dv_vals
    measured_y = [ksp(x) for x in measured_x]

    # Replace exact zeros for plotting on log scale
    plot_measured_y = [y if y > 0 else 1e-12 for y in measured_y]

    plt.figure(figsize=(6.5, 4.5))
    plt.semilogy(xs, ys, label="Model: Ksp(x)", color="tab:blue")
    plt.scatter(measured_x, plot_measured_y, color="tab:orange", zorder=5, label="Measured dv values")

    # Annotate measured points with dv and Ksp (2 significant figures)
    for x, y, raw_y in zip(measured_x, plot_measured_y, measured_y):
        label = f"{x} mL: {raw_y:.2g}"
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(6, -8), fontsize=8)

    plt.xlabel("Added KI volume x (mL)")
    plt.ylabel(r"K$_{sp}$ (PbI$_2$)")
    plt.title("Modeled Ksp(x) and measured dv points")
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200)
    print(f"Saved plot to: {OUT_PNG}")


if __name__ == "__main__":
    main()
