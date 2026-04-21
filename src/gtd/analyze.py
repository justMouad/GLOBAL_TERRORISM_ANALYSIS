"""Tables d'analyse (retournent des DataFrames)."""
import pandas as pd


def overview(df: pd.DataFrame) -> pd.Series:
    return pd.Series({
        "attentats": len(df),
        "période": f"{df.year.min()}-{df.year.max()}",
        "pays": df.country.nunique(),
        "morts": int(df.nkill.sum()),
        "blessés": int(df.nwound.sum()),
        "taux_succès_%": round(df.success.mean() * 100, 1),
        "part_suicide_%": round(df.suicide.mean() * 100, 1),
        "part_groupe_inconnu_%": round(df.is_unknown_group.mean() * 100, 1),
    })


def by_year(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("year").agg(
        attacks=("eventid", "count"), killed=("nkill", "sum"),
        wounded=("nwound", "sum"), success_rate=("success", "mean"),
    )
    g["killed_per_attack"] = g.killed / g.attacks
    return g


def by_region_decade(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="region", columns="decade",
                          values="eventid", aggfunc="count", fill_value=0)


def top(df: pd.DataFrame, col: str, n: int = 15, exclude_unknown: bool = False) -> pd.DataFrame:
    d = df[~df.is_unknown_group] if exclude_unknown and col == "group" else df
    t = d.groupby(col).agg(attacks=("eventid", "count"), killed=("nkill", "sum"),
                           wounded=("nwound", "sum"))
    t["killed_per_attack"] = (t.killed / t.attacks).round(2)
    return t.sort_values("attacks", ascending=False).head(n)


def lethality_by(df: pd.DataFrame, col: str, min_events: int = 100) -> pd.DataFrame:
    t = df.groupby(col).agg(attacks=("eventid", "count"), killed=("nkill", "sum"))
    t = t[t.attacks >= min_events]
    t["killed_per_attack"] = t.killed / t.attacks
    return t.sort_values("killed_per_attack", ascending=False)


def seasonality(df: pd.DataFrame) -> pd.Series:
    return df.dropna(subset=["month"]).groupby("month").size()


def suicide_by_year(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("year").agg(suicide_attacks=("suicide", "sum"),
                                  share=("suicide", "mean"))
