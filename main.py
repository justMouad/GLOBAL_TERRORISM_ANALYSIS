"""Pipeline complet : chargement -> nettoyage -> tables -> figures -> rapport.

Usage:
    python main.py --data data/raw/globalterrorismdb_0718dist.csv
"""
import argparse
from pathlib import Path
from src.gtd import analyze as A
from src.gtd.clean import clean
from src.gtd.load import load_raw
from src.gtd.plots import make_all


def main():
    p = argparse.ArgumentParser(description="Analyse de la Global Terrorism Database")
    p.add_argument("--data", default="data/raw/globalterrorismdb_0718dist.csv")
    p.add_argument("--out", default="outputs")
    a = p.parse_args()

    out = Path(a.out); tables = out / "tables"; figs = out / "figures"
    tables.mkdir(parents=True, exist_ok=True)

    print("Chargement…"); raw = load_raw(a.data)
    print("Nettoyage…"); df = clean(raw)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/processed/gtd_clean.csv", index=False)

    ov = A.overview(df)
    ov.to_csv(tables / "overview.csv", header=["valeur"])
    A.by_year(df).to_csv(tables / "by_year.csv")
    A.by_region_decade(df).to_csv(tables / "region_by_decade.csv")
    A.top(df, "country", 20).to_csv(tables / "top_countries.csv")
    A.top(df, "region", 20).to_csv(tables / "top_regions.csv")
    A.top(df, "group", 20, exclude_unknown=True).to_csv(tables / "top_groups.csv")
    A.top(df, "attack_type", 20).to_csv(tables / "top_attack_types.csv")
    A.top(df, "target_type", 25).to_csv(tables / "top_target_types.csv")
    A.top(df, "weapon_type", 20).to_csv(tables / "top_weapon_types.csv")

    print("Figures…"); make_all(df, figs)

    y = A.by_year(df)
    peak = y.attacks.idxmax()
    top_c = A.top(df, "country", 5)
    top_g = A.top(df, "group", 5, exclude_unknown=True)
    lines = ["# Rapport automatique – GTD", "", "## Vue d'ensemble", ""]
    lines += [f"- **{k}** : {v}" for k, v in ov.items()]
    lines += ["", f"## Points clés", "",
              f"- Année la plus active : **{peak}** ({int(y.attacks.max())} attentats).",
              f"- Année la plus meurtrière : **{y.killed.idxmax()}** ({int(y.killed.max())} morts).",
              "", "### Top 5 pays", "", top_c[["attacks", "killed"]].to_markdown(),
              "", "### Top 5 groupes identifiés", "", top_g[["attacks", "killed"]].to_markdown(),
              "", "Figures : `outputs/figures/`, tables : `outputs/tables/`."]
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Terminé -> {out}/")


if __name__ == "__main__":
    main()
