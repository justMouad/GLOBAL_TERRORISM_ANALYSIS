"""Visualisations -> outputs/figures/*.png"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from . import analyze as A

sns.set_theme(style="whitegrid", context="notebook")


def _save(fig, outdir: Path, name: str):
    fig.tight_layout()
    fig.savefig(outdir / f"{name}.png", dpi=150)
    plt.close(fig)


def make_all(df, outdir: Path) -> list[str]:
    outdir.mkdir(parents=True, exist_ok=True)
    names = []

    # 1. Évolution annuelle
    y = A.by_year(df)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(y.index, y.attacks, color="#c0392b", lw=2, label="Attentats")
    ax2 = ax.twinx()
    ax2.plot(y.index, y.killed, color="#2c3e50", lw=2, ls="--", label="Morts")
    ax.set(title="Attentats et morts par année", xlabel="Année", ylabel="Attentats")
    ax2.set_ylabel("Morts"); ax2.grid(False)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left")
    _save(fig, outdir, "01_evolution_annuelle"); names.append("01_evolution_annuelle")

    # 2. Régions
    r = df.region.value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(9, 6))
    r.plot.barh(ax=ax, color="#2980b9")
    ax.set(title="Attentats par région", xlabel="Nombre d'attentats", ylabel="")
    _save(fig, outdir, "02_regions"); names.append("02_regions")

    # 3. Top pays
    c = A.top(df, "country", 15).attacks.sort_values()
    fig, ax = plt.subplots(figsize=(9, 6))
    c.plot.barh(ax=ax, color="#8e44ad")
    ax.set(title="Top 15 pays par nombre d'attentats", xlabel="Attentats", ylabel="")
    _save(fig, outdir, "03_top_pays"); names.append("03_top_pays")

    # 4. Types d'attaque / armes
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    df.attack_type.value_counts().sort_values().plot.barh(ax=axes[0], color="#e67e22")
    axes[0].set(title="Types d'attaque", xlabel="Attentats", ylabel="")
    df.weapon_type.value_counts().head(8).sort_values().plot.barh(ax=axes[1], color="#16a085")
    axes[1].set(title="Types d'armes (top 8)", xlabel="Attentats", ylabel="")
    _save(fig, outdir, "04_attaques_armes"); names.append("04_attaques_armes")

    # 5. Heatmap région x décennie
    h = A.by_region_decade(df)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(h, annot=True, fmt="d", cmap="Reds", ax=ax, cbar_kws={"label": "Attentats"})
    ax.set(title="Attentats par région et décennie", xlabel="Décennie", ylabel="")
    _save(fig, outdir, "05_heatmap_region_decennie"); names.append("05_heatmap_region_decennie")

    # 6. Groupes les plus actifs (hors inconnus)
    g = A.top(df, "group", 12, exclude_unknown=True).attacks.sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    g.plot.barh(ax=ax, color="#d35400")
    ax.set(title="Groupes les plus actifs (hors « Unknown »)", xlabel="Attentats", ylabel="")
    _save(fig, outdir, "06_top_groupes"); names.append("06_top_groupes")

    # 7. Létalité par type d'attaque
    l = A.lethality_by(df, "attack_type", 100).killed_per_attack.sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    l.plot.barh(ax=ax, color="#34495e")
    ax.set(title="Létalité moyenne par type d'attaque", xlabel="Morts par attentat", ylabel="")
    _save(fig, outdir, "07_letalite_type_attaque"); names.append("07_letalite_type_attaque")

    # 8. Saisonnalité
    s = A.seasonality(df)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(s.index.astype(int), s.values, color="#27ae60")
    ax.set(title="Saisonnalité des attentats (mois connus)", xlabel="Mois", ylabel="Attentats",
           xticks=range(1, 13))
    _save(fig, outdir, "08_saisonnalite"); names.append("08_saisonnalite")

    # 9. Attentats-suicides
    sb = A.suicide_by_year(df)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(sb.index, sb.suicide_attacks, color="#c0392b", alpha=.6)
    ax.set(title="Attentats-suicides par année", xlabel="Année", ylabel="Attentats")
    _save(fig, outdir, "09_attentats_suicides"); names.append("09_attentats_suicides")

    # 10. Carte (nuage de points lon/lat)
    geo = df.dropna(subset=["latitude", "longitude"])
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.scatter(geo.longitude, geo.latitude, s=2, alpha=.25, color="#c0392b")
    ax.set(title="Localisation des attentats", xlabel="Longitude", ylabel="Latitude",
           xlim=(-180, 180), ylim=(-60, 85))
    _save(fig, outdir, "10_carte_attentats"); names.append("10_carte_attentats")
    return names
