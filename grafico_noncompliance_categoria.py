import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import FancyBboxPatch
import numpy as np

df = dataset.copy()
df = df[df["Fora_Politica"] == "S"]
df = df.groupby("Categoria", as_index=False)["Valor"].sum()

total = df["Valor"].sum()
df["Perc"] = (df["Valor"] / total) * 100
df = df.sort_values("Valor", ascending=True)

bg      = "#F7F9FC"
card_bg = "#EEF2F8"
azul    = "#1A4F8A"
texto   = "#1A2A3A"
texto2  = "#6B7A8D"
borda   = "#D0DAE8"

plt.rcParams["font.family"] = "DejaVu Sans"

fig = plt.figure(figsize=(14, 7))
fig.patch.set_facecolor(bg)

gs = fig.add_gridspec(1, 2, width_ratios=[3.2, 1], wspace=0.06)
ax   = fig.add_subplot(gs[0])
ax_r = fig.add_subplot(gs[1])

ax.set_facecolor(bg)
ax_r.set_facecolor(bg)
ax_r.axis("off")

# --- Cards ---
n = len(df)
maior_cat = df.sort_values("Valor", ascending=False).iloc[0]["Categoria"]

cards = [
    ("Total fora\nda política", f"R$ {total/1000:.1f}k".replace(".", ",")),
    ("Categorias\navaliadas",   str(n)),
    ("Maior\ncategoria",        maior_cat),
]

for i, (label, value) in enumerate(cards):
    y0 = 0.96 - i * 0.35
    rect = FancyBboxPatch(
        (0.04, y0 - 0.27), 0.92, 0.28,
        boxstyle="round,pad=0.03",
        transform=ax_r.transAxes,
        facecolor=card_bg, edgecolor=borda, linewidth=0.8,
        clip_on=False
    )
    ax_r.add_patch(rect)
    ax_r.text(0.5, y0 - 0.05, label,
              transform=ax_r.transAxes,
              ha="center", va="top",
              fontsize=8.5, color=texto2)
    ax_r.text(0.5, y0 - 0.16, value,
              transform=ax_r.transAxes,
              ha="center", va="top",
              fontsize=13 if i < 2 else 10.5,
              color=azul, fontweight="bold")

# --- Barras ---
max_val    = df["Valor"].max()
n_bars     = len(df)
altura     = 0.52
categorias = df["Categoria"].tolist()
valores    = df["Valor"].tolist()
percs      = df["Perc"].tolist()

cores = [plt.cm.colors.to_hex(c)
         for c in plt.cm.Blues(np.linspace(0.42, 0.82, n_bars))]

y_positions = np.arange(n_bars)

ax.set_xlim(0, max_val * 1.42)
ax.set_ylim(-0.6, n_bars - 0.4)
ax.set_yticks(y_positions)
ax.set_yticklabels(categorias, fontsize=9.5, color=texto)

# Renderiza barras primeiro (sem anotações)
for i, (val, cor) in enumerate(zip(valores, cores)):
    h   = altura
    y   = i - h / 2
    rad = h * 0.38

    bar = FancyBboxPatch(
        (0, y), val, h,
        boxstyle=f"round,pad=0,rounding_size={rad}",
        facecolor=cor,
        edgecolor="none",
        zorder=3,
        clip_on=True
    )
    ax.add_patch(bar)

# Renderiza o gráfico uma vez para poder medir textos
fig.canvas.draw()

#  mede largura real do texto do valor, posiciona % logo após
gap = max_val * 0.012  # espaço entre barra e texto
espacamento = max_val * 0.008  # espaço entre valor e %

for i, (val, perc) in enumerate(zip(valores, percs)):
    val_txt  = f"R$ {val/1000:.1f}k".replace(".", ",")
    perc_txt = f"({perc:.1f}%)".replace(".", ",")

    # Texto do valor
    t_val = ax.text(
        val + gap, i,
        val_txt,
        va="center", ha="left",
        fontsize=9.5, color=texto, fontweight="bold"
    )

    # Mede a largura do texto do valor em coordenadas de dados
    fig.canvas.draw()
    bbox = t_val.get_window_extent(renderer=fig.canvas.get_renderer())
    # Converte pixels → coordenadas de dados
    x1_display = bbox.x1
    x1_data = ax.transData.inverted().transform((x1_display, 0))[0]

    # Texto do % logo após o valor
    ax.text(
        x1_data + espacamento, i,
        perc_txt,
        va="center", ha="left",
        fontsize=9, color=texto2
    )

# Grid e eixos
ax.xaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f"R$ {int(x/1000)}k")
)
ax.grid(axis="x", linestyle="--", alpha=0.2, color="#9AAEC0", zorder=0)
ax.set_axisbelow(True)

for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(borda)
ax.spines["bottom"].set_linewidth(0.8)

ax.tick_params(axis="y", length=0, labelsize=9.5, colors=texto)
ax.tick_params(axis="x", labelsize=8.5, colors=texto2)

#  Título 
ax.set_title("")  # limpa título nativo

# Descobre posição do topo do ax em coordenadas de figura
fig.canvas.draw()
ax_pos = ax.get_position()  # [x0, y0, width, height] em fração da figura

titulo_y    = ax_pos.y1 + 0.055
subtitulo_y = ax_pos.y1 + 0.025

fig.text(ax_pos.x0, titulo_y,
         "Non-Compliance por Categoria",
         fontsize=14, color=texto, fontweight="bold", ha="left", va="bottom")

fig.text(ax_pos.x0, subtitulo_y,
         "Valor fora da política (R$ mil)  ·  filtro: Fora_Politica = \"S\"",
         fontsize=8.5, color=texto2, ha="left", va="bottom")

# Rodapé
fig.text(0.05, 0.01,
         f"Total fora da política: R$ {total/1000:.1f}k  ·  {n} categorias avaliadas".replace(".", ","),
         ha="left", fontsize=8, color=texto2, style="italic")

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.show()
