"""Utilidades de carga y figuras. Los algoritmos se implementan en los notebooks."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.metrics import silhouette_score

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'datasets/semana-08').is_dir())
DATA = ROOT / 'datasets/semana-08'
FIGURES = ROOT / 'assets/semana-08'
RESULTS = ROOT / 'notebooks/semana-08/docente/resultados'
COLORS = ['#087f8c', '#d57927', '#7856a5', '#c94d61', '#418650', '#b49b24', '#547ba5', '#7a5342']


def load_data(kind='desarrollo'):
    names = {'desarrollo': 'recogidas_desarrollo.csv', 'test': 'recogidas_test_temporal.csv',
             'jerarquico': 'recogidas_jerarquico.csv'}
    return pd.read_csv(DATA / names[kind], parse_dates=['pickup_datetime'])


def setup():
    plt.rcParams.update({'figure.dpi': 110, 'savefig.dpi': 160, 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.titleweight': 'bold', 'axes.labelcolor': '#172029',
                         'figure.facecolor': 'white', 'axes.prop_cycle': plt.cycler(color=COLORS)})


def spatial_axes(ax, X, title):
    ax.set(title=title, xlabel='Este relativo (km)', ylabel='Norte relativo (km)')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(X[:,0].min()-0.5, X[:,0].max()+0.5)
    ax.set_ylim(X[:,1].min()-0.5, X[:,1].max()+0.5)


def savefig(fig, name):
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f'{name}.png', bbox_inches='tight')
    plt.show()
    plt.close(fig)


def save_table(frame, name):
    RESULTS.mkdir(parents=True, exist_ok=True)
    frame.to_csv(RESULTS / f'{name}.csv', index=False)


def ellipses(ax, model):
    for k, mean in enumerate(model.means_):
        covariance = model.covariances_[k]
        if model.covariance_type == 'diag':
            covariance = np.diag(covariance)
        values, vectors = np.linalg.eigh(covariance)
        angle = np.degrees(np.arctan2(vectors[1, -1], vectors[0, -1]))
        # Radio sqrt(chi2.ppf(.95, 2)); contorno de componente, no IC de su media.
        patch = Ellipse(mean, 2*np.sqrt(5.991*values[-1]), 2*np.sqrt(5.991*values[0]),
                        angle=angle, facecolor='none', edgecolor=COLORS[k % len(COLORS)], lw=2)
        ax.add_patch(patch)


def safe_silhouette(X, labels, cap=1000):
    mask = labels != -1
    x, lab = X[mask], np.asarray(labels)[mask]
    if len(x) < 3 or not 2 <= len(np.unique(lab)) < len(x):
        return np.nan
    rng = np.random.default_rng(42)
    ids = rng.choice(len(x), min(cap, len(x)), replace=False)
    if not 2 <= len(np.unique(lab[ids])) < len(ids):
        return np.nan
    return silhouette_score(x[ids], lab[ids])


def density_grid(X, size=140):
    gx = np.linspace(X[:,0].min()-0.5, X[:,0].max()+0.5, size)
    gy = np.linspace(X[:,1].min()-0.5, X[:,1].max()+0.5, size)
    xx, yy = np.meshgrid(gx, gy)
    return xx, yy, np.c_[xx.ravel(), yy.ravel()]
