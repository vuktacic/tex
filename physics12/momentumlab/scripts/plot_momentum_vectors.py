#!/usr/bin/env python3
import os
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
OUT_DIR = os.path.join(ROOT, 'images')
os.makedirs(OUT_DIR, exist_ok=True)

CSV_INITIAL = os.path.join(DATA_DIR, 'results-momentum-initial.csv')
CSV_FINAL = os.path.join(DATA_DIR, 'results-momentum-final.csv')

def read_csv_as_dict(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def plot_tip_to_tail(p1, p2, sys_p, title, fname):
    fig, ax = plt.subplots(figsize=(6,6))
    # p1 from origin
    ax.arrow(0, 0, p1[0], p1[1], head_width=0.08, head_length=0.12, fc='C0', ec='C0', length_includes_head=True)
    # p2 from tip of p1
    ax.arrow(p1[0], p1[1], p2[0], p2[1], head_width=0.08, head_length=0.12, fc='C1', ec='C1', length_includes_head=True)
    # system momentum from origin (resultant)
    ax.arrow(0, 0, sys_p[0], sys_p[1], head_width=0.08, head_length=0.12, fc='C2', ec='C2', linestyle='--', length_includes_head=True)
    # dashed line showing tip-to-tail resultant from origin to tip of (p1+p2)
    resultant = (p1[0] + p2[0], p1[1] + p2[1])
    ax.plot([0, resultant[0]], [0, resultant[1]], color='C3', linestyle=':', label='p1+p2 (tip-to-tail)')
    # markers
    ax.scatter([0, p1[0], resultant[0], sys_p[0]], [0, p1[1], resultant[1], sys_p[1]], c=['k','C0','C3','C2'])
    ax.set_aspect('equal', adjustable='box')
    xs = [0, p1[0], resultant[0], sys_p[0]]
    ys = [0, p1[1], resultant[1], sys_p[1]]
    margin = max(0.5, 0.1 * max(abs(x) for x in xs+ys))
    ax.set_xlim(min(xs)-margin, max(xs)+margin)
    ax.set_ylim(min(ys)-margin, max(ys)+margin)
    ax.grid(True)
    ax.legend(['p1', 'p2 (from tip of p1)', 'p_sys', 'p1+p2 (tip-to-tail)'])
    ax.set_title(title)
    plt.savefig(fname, bbox_inches='tight', dpi=150)
    plt.close()

def to_float_pair(d, kx, ky):
    return (float(d[kx]), float(d[ky]))

def find_row(rows, collision_name):
    for r in rows:
        if r.get('Collision') == collision_name:
            return r
    raise KeyError(f'Collision not found: {collision_name}')

def main():
    rows_i = read_csv_as_dict(CSV_INITIAL)
    rows_f = read_csv_as_dict(CSV_FINAL)

    collision = 'Elastic 2'
    row_i = find_row(rows_i, collision)
    row_f = find_row(rows_f, collision)

    p1_i = to_float_pair(row_i, 'p1_i_x', 'p1_i_y')
    p2_i = to_float_pair(row_i, 'p2_i_x', 'p2_i_y')
    p_sys_i = to_float_pair(row_i, 'p_sys_i_x', 'p_sys_i_y')

    p1_f = to_float_pair(row_f, 'p1_f_x', 'p1_f_y')
    p2_f = to_float_pair(row_f, 'p2_f_x', 'p2_f_y')
    p_sys_f = to_float_pair(row_f, 'p_sys_f_x', 'p_sys_f_y')

    out_initial = os.path.join(OUT_DIR, 'momentum_elastic2_initial.png')
    out_final = os.path.join(OUT_DIR, 'momentum_elastic2_final.png')

    plot_tip_to_tail(p1_i, p2_i, p_sys_i, f'{collision} — Initial momenta (tip-to-tail)', out_initial)
    plot_tip_to_tail(p1_f, p2_f, p_sys_f, f'{collision} — Final momenta (tip-to-tail)', out_final)
    print('Saved:', out_initial, out_final)

if __name__ == '__main__':
    main()