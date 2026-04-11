"""Nettoyage et enrichissement."""
import numpy as np
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates(subset="eventid")

    # Renommage lisible
    df = df.rename(columns={
        "iyear": "year", "imonth": "month", "iday": "day",
        "country_txt": "country", "region_txt": "region",
        "attacktype1_txt": "attack_type", "targtype1_txt": "target_type",
        "weaptype1_txt": "weapon_type", "gname": "group",
    })

    # Mois/jour = 0 -> inconnu
    df["month"] = df["month"].replace(0, np.nan)
    df["day"] = df["day"].replace(0, np.nan)

    # Victimes : NaN -> 0 pour les agrégats, on garde un indicateur d'inconnu
    df["casualties_known"] = df[["nkill", "nwound"]].notna().any(axis=1)
    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)
    df["casualties"] = df["nkill"] + df["nwound"]

    # Coordonnées valides uniquement
    df.loc[~df["latitude"].between(-90, 90), "latitude"] = np.nan
    df.loc[~df["longitude"].between(-180, 180), "longitude"] = np.nan

    # Catégories textuelles
    for c in ["country", "region", "attack_type", "target_type", "weapon_type", "group"]:
        df[c] = df[c].astype("string").str.strip()
    df["group"] = df["group"].fillna("Unknown")

    # Variables dérivées
    df["decade"] = (df["year"] // 10 * 10).astype(int)
    df["is_unknown_group"] = df["group"].eq("Unknown")
    df["deadly"] = df["nkill"] > 0
    df["success"] = df["success"].astype("Int8")
    df["suicide"] = df["suicide"].astype("Int8")
    return df.reset_index(drop=True)
