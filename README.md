# Analyse de la Global Terrorism Database (GTD)

Pipeline d'analyse exploratoire des attentats recensés par la GTD (START, Université du Maryland, 1970–2017+).

## Contenu
- Nettoyage (doublons, dates inconnues, coordonnées invalides, victimes manquantes)
- Indicateurs : attentats, morts, blessés, taux de succès, part d'attentats-suicides
- Analyses : évolution annuelle, régions, pays, groupes, types d'attaque/armes/cibles, létalité, saisonnalité, région × décennie
- 10 figures + 9 tables CSV + rapport Markdown automatique

## Structure
```
main.py              # pipeline complet
src/gtd/             # load, clean, analyze, plots
data/raw/            # y placer le CSV GTD (ignoré par git)
outputs/figures/     # graphiques PNG
outputs/tables/      # tables CSV
outputs/report.md    # rapport généré
```

## Utilisation
```bash
pip install -r requirements.txt
# placer globalterrorismdb_0718dist.csv dans data/raw/ (voir data/README.md)
python main.py --data data/raw/globalterrorismdb_0718dist.csv
```

## Notes méthodologiques
- Victimes inconnues (`nkill`/`nwound` manquants) comptées comme 0 → les totaux sont des minorants.
- « Unknown » est exclu du classement des groupes.
- La GTD n'a pas de données pour 1993 (perdues) : creux artificiel dans les séries.

## Source
National Consortium for the Study of Terrorism and Responses to Terrorism (START). Global Terrorism Database. https://www.start.umd.edu/gtd
