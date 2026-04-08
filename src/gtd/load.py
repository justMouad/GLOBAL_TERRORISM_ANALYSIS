"""Chargement du fichier CSV brut GTD."""
from pathlib import Path
import pandas as pd

# Colonnes utiles (présentes dans toutes les versions récentes de la GTD)
USECOLS = [
    "eventid", "iyear", "imonth", "iday", "country_txt", "region_txt",
    "provstate", "city", "latitude", "longitude", "success", "suicide",
    "attacktype1_txt", "targtype1_txt", "weaptype1_txt", "gname",
    "nkill", "nwound", "property", "ishostkid", "multiple",
]


def load_raw(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} introuvable. Voir data/README.md pour télécharger la GTD."
        )
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
        cols = [c for c in USECOLS if c in df.columns]
        return df[cols]
    # Le CSV officiel est encodé en latin-1
    header = pd.read_csv(path, encoding="latin-1", nrows=0).columns
    cols = [c for c in USECOLS if c in header]
    return pd.read_csv(path, encoding="latin-1", usecols=cols, low_memory=False)
