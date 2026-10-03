"""Calcula la matriz de decisión ponderada y genera img/matriz.png (matplotlib)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
criterios = ["Seguridad\n(25%)", "Interoperab.\n(20%)", "Tiempo de\nentrega (20%)",
             "Costo\noperativo (15%)", "Simplicidad\noperativa (10%)", "Modificab.\n(10%)"]
pesos = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
alternativas = {
    "A. Monolito en capas": [3, 2, 5, 5, 5, 2],
    "B. Monolito modular": [4, 4, 4, 5, 4, 4],
    "C. Microservicios": [3, 4, 2, 2, 1, 5],
}
colores = ["#9E9E9E", "#2E7D32", "#2B5797"]

assert abs(sum(pesos) - 1.0) < 1e-9, "Los pesos deben sumar 100 %"
totales = {n: round(sum(p * s for p, s in zip(pesos, v)), 2) for n, v in alternativas.items()}
for n, t in totales.items():
    print(n + ": " + f"{t:.2f}".replace(".", ","))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={"width_ratios": [1.6, 1]})
ancho = 0.26
for i, (n, v) in enumerate(alternativas.items()):
    ax1.bar([x + (i - 1) * ancho for x in range(len(criterios))], v, ancho, label=n, color=colores[i])
ax1.set_xticks(range(len(criterios)))
ax1.set_xticklabels(criterios, fontsize=8)
ax1.set_ylabel("Puntaje (1-5)")
ax1.set_ylim(0, 5.5)
ax1.set_title("Puntaje por criterio")
ax1.legend(fontsize=8, ncol=3, loc="upper center")
ax1.spines[["top", "right"]].set_visible(False)

nombres = list(totales)[::-1]
valores = [totales[n] for n in nombres]
ax2.barh(nombres, valores, color=colores[::-1])
for y, v in enumerate(valores):
    ax2.text(v + 0.05, y, str(v).replace(".", ","), va="center", fontweight="bold")
ax2.set_xlim(0, 5)
ax2.set_title("Puntaje ponderado total")
ax2.spines[["top", "right"]].set_visible(False)

fig.suptitle("BiblioUNSA - Matriz de decisión ponderada", fontsize=11)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "img"), exist_ok=True)
fig.savefig(os.path.join(HERE, "img", "matriz.png"), dpi=150)
