"""Genera las figuras y cifras del informe de semana 8 a partir de semana08_pacientes_agregados.ipynb
(mismo código y semilla). Ejecutar desde la raíz del repositorio: python informe/figuras_semana8.py"""
import json, warnings; warnings.filterwarnings("ignore")
import nbformat, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

nb = nbformat.read("semana08_pacientes_agregados.ipynb", 4)
g = {"display": lambda *a, **k: None}
for c in nb.cells:
    if c.cell_type == "code":
        exec(c.source.replace("plt.show()", "plt.close('all')"), g)
X, dev, test, best, winner = g["X"], g["dev"], g["test"], g["best"], g["winner"]
xx, yy, dens, level50, db_labels = g["xx"], g["yy"], g["dens"], g["level50"], g["db_labels"]
XLIM, YLIM = g["XLIM"], g["YLIM"]

INK, INK2, GRID = "#1f1f1e", "#52514e", "#e4e3df"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
GRAY = "#b9b8b3"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.titlesize": 9.5, "axes.titlecolor": INK, "figure.dpi": 220})

# ---- nombres de las componentes GMM por regla sobre su perfil
dev["gmm"] = best.predict(X)
st = dev.groupby("gmm").agg(n=("edad", "size"), multi=("n_encuentros", lambda s: (s > 1).mean()),
                            meds=("meds_medio", "median"), enc=("n_encuentros", "median"), hosp=("hosp_prev_max", "median"),
                            est=("estancia_media", "median"), diag=("diag_medio", "median"), edad=("edad", "median"),
                            r1=("readm30_primero", "mean"), ra=("readm30_alguna", "mean"))
st["share"] = st.n / st.n.sum()
test["gmm"] = best.predict(g["Xt"])
st["share_test"] = test.gmm.value_counts(normalize=True)
st["r1_test"] = test.groupby("gmm").readm30_primero.mean()
order = st.sort_values("multi", ascending=False).index.tolist()
names = {order[0]: "Muy recurrentes", order[1]: "Recurrentes", order[2]: "En transición", order[3]: "Frontera cresta–abanico"}
rest = order[4:]
tip = st.loc[rest, "n"].idxmin(); names[tip] = "Punta de la cresta (ajuste técnico)"; rest.remove(tip)
for nm, idx in zip(["Un solo ingreso, complejo", "Un solo ingreso, moderado", "Un solo ingreso, breve"],
                   st.loc[rest].sort_values("meds", ascending=False).index):
    names[idx] = nm
st["nombre"] = st.index.map(names)

# ---- Figura 1: tres mapas con los mismos ejes
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.75), sharex=True, sharey=True)
lab = best.predict(X)
colmap = {k: CAT[i % 8] for i, k in enumerate(st.sort_values("share", ascending=False).index)}
axes[0].scatter(*X.T, c=[colmap[l] for l in lab], s=1.2, alpha=.45, linewidths=0)
for k, mean in enumerate(best.means_):
    vals, vecs = np.linalg.eigh(best.covariances_[k]); ang = np.degrees(np.arctan2(vecs[1, -1], vecs[0, -1]))
    axes[0].add_patch(Ellipse(mean, 2*np.sqrt(5.991*vals[-1]), 2*np.sqrt(5.991*vals[0]), angle=ang, fc="none", ec=colmap[k], lw=1))
axes[0].set_title(f"GMM · {int(winner.k)} componentes", loc="left")
axes[1].pcolormesh(xx, yy, np.log(dens + 1e-12), shading="auto", cmap="Blues", vmin=-9, vmax=0, rasterized=True)
axes[1].contour(xx, yy, dens, levels=[level50], colors=INK, linewidths=.9)
axes[1].set_title(f"KDE · h = {g['best_h']:g}", loc="left")
axes[2].scatter(*X[db_labels == -1].T, s=1.2, color=GRAY, linewidths=0, label="ruido")
axes[2].scatter(*X[db_labels == 0].T, s=1.2, color=CAT[0], linewidths=0, label="masa principal")
axes[2].scatter(*X[db_labels > 0].T, s=4, color=CAT[1], linewidths=0, label="grupo pequeño")
axes[2].legend(frameon=False, fontsize=6.5, markerscale=4, loc="upper left")
axes[2].set_title(f"DBSCAN · eps = {g['CHOSEN_EPS']}, m = {g['CHOSEN_M']}", loc="left")
for ax in axes:
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM); ax.set_aspect("equal", adjustable="box"); ax.set_xlabel("CP1 · carga clínica (d.e.)")
axes[0].set_ylabel("CP2 · recurrencia (d.e.)")
axes[1].annotate("cresta: pacientes\nde un solo ingreso", (-1.7, -.3), xytext=(-4.6, -3.2), fontsize=6.5, color=INK,
                 arrowprops=dict(arrowstyle="-", color=INK, lw=.6))
axes[1].annotate("abanico:\nrecurrentes", (1.6, 1.9), xytext=(2.2, 4.1), fontsize=6.5, color=INK,
                 arrowprops=dict(arrowstyle="-", color=INK, lw=.6))
fig.tight_layout(w_pad=.4); fig.savefig("informe/figuras/f1_mapas.png", bbox_inches="tight", facecolor="white"); plt.close(fig)

# ---- Figura 2: segmentos (sin la pieza técnica), readmisión en el primer ingreso (medida menos circular)
s2 = st[st.nombre != "Punta de la cresta (ajuste técnico)"].sort_values("r1")
base1 = dev.readm30_primero.mean()
fig, ax = plt.subplots(figsize=(7.2, 2.6))
bars = ax.barh(s2.nombre, s2.r1, color=[CAT[0] if v > base1 else GRAY for v in s2.r1], height=.62)
ax.axvline(base1, ls="--", lw=.9, color=INK2, zorder=1); ax.text(base1 + .003, len(s2) - .45, f"promedio {base1:.1%}", fontsize=7, color=INK2)
for b_, v, sh in zip(bars, s2.r1, s2.share):
    ax.text(v + .004, b_.get_y() + b_.get_height() / 2, f"{v:.1%}  ·  {sh:.0%} de los pacientes", va="center", fontsize=7.5, color=INK,
            bbox=dict(fc="white", ec="none", pad=1.2), zorder=3)
from matplotlib.ticker import PercentFormatter
ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0)); ax.set_xlim(0, .40); ax.set_ylim(-.6, len(s2) - .1)
ax.set_xlabel("Readmisión < 30 días en el primer ingreso (desarrollo)"); ax.grid(axis="x", color=GRID, lw=.6); ax.set_axisbelow(True)
ax.set_title("El riesgo se concentra en los segmentos que vuelven al hospital", loc="left")
fig.tight_layout(); fig.savefig("informe/figuras/f2_segmentos.png", bbox_inches="tight", facecolor="white"); plt.close(fig)

out = dict(base1=float(base1), basea=float(dev.readm30_alguna.mean()),
           segmentos=json.loads(st.set_index("nombre").round(4).to_json(orient="index")),
           dbscan_sens=g["db_sens"].round(3).to_dict(orient="records"), kde_cv=g["kde_cv"].round(4).to_dict(orient="records"),
           ext=g["ext"].round(3).to_dict(orient="records"), sens=g["sens"].to_dict(orient="records"))
json.dump(out, open("informe/figuras/insumos_semana8.json", "w"), ensure_ascii=False, indent=1)
print(st[["nombre", "share", "share_test", "multi", "enc", "hosp", "est", "meds", "diag", "edad", "r1", "ra", "r1_test"]].round(3).to_string())
print(g["sens"].to_string())
