# zero-to-trade

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md) · [Português](README_PT.md) · **Français** · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · [Bahasa Indonesia](README_ID.md)

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**Sept étapes, de « mais quel pays je choisis ? » à « l'argent est arrivé ». Plus quatorze scripts Python qui s'occupent des parties ennuyeuses, et un site web avec quatre outils qui tournent directement dans votre navigateur. Aucune expérience requise. C'est tout l'intérêt.**

> Vous avez envoyé 200 e-mails à froid et reçu zéro réponse. Ce n'est pas votre anglais. C'est l'ordre dans lequel vous faites les choses.
>
> Ce dépôt transforme « se lancer à l'export » en quelque chose de concret : quel site ouvrir cet après-midi, quoi y taper, et quel résultat signifie que c'est validé.

> La règle qui sous-tend tout le reste : **l'IA fait le gros du travail, c'est vous qui décidez.**

Pas de formation à acheter. Pas de version payante. Pas de mur d'inscription par e-mail. Licence MIT, V20.

> Les PR sont les bienvenues, surtout de la part de ceux qui vendent sur un marché dont ce dépôt n'a jamais entendu parler. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Démo en 7 étapes : classez une vraie liste et rédigez votre premier message de prospection en 2 minutes

Inutile de lire la documentation d'abord. Sept étapes, une ligne chacune, une commande à copier-coller chacune — environ 2 minutes du début à la fin. Les sept commandes ci-dessous ont réellement été exécutées dans ce dépôt (2026-11-22, Python 3.x, bibliothèque standard uniquement). Les données d'exemple sont fictives ; les noms d'entreprise portent le préfixe 【示例】 (« exemple »).

| Étape | En une ligne | Commande (à copier-coller) |
|---|---|---|
| 1 Récupérer une liste | Copiez l'exemple dans votre propre fichier ; vos vrais prospects ne vont que dans cette copie | `cp examples/leads_example.csv my_leads.csv` |
| 2 La classer | 10 prospects répartis de T0 à T3 ; appelez-en 2 aujourd'hui | `python scripts/lead_score.py my_leads.csv` |
| 3 Vérifier les T0 | Assurez-vous qu'un T0 n'est pas une société écran avant d'écrire ; tout ce que vous n'avez pas fourni revient marqué « à vérifier » | `python scripts/due_diligence.py --company "【示例】海湾轮胎贸易"` |
| 4 Rédiger le premier contact | Brouillon de prospection pour le niveau T0, l'anglais à envoyer, le chinois pour votre relecture | `python scripts/outreach_gen.py my_leads.csv --tier T0` |
| 5 Planifier les relances | Rythme D0/D2/D5 : 3 contacts en 6 jours, on arrête après le troisième silence | `python scripts/followup_plan.py --tier T0 --start 2026-11-22 --csv my_leads.csv` |
| 6 Chiffrer quand ils répondent | Coût + fret + marge → fourchette FOB/CIF + une échelle de concessions en trois paliers | `python scripts/quote_engine.py --cost 28 --freight 6 --margin 15` |
| 7 Relancer quand ils se taisent | 7 jours après le devis sans réponse, demandez où ils en sont — ferme, pas désespéré | `python scripts/nudge.py --day D7 --scenario quoted` |

Après l'étape 4, vous avez en main un e-mail de premier contact réellement envoyable ; après l'étape 5, vous savez quoi faire chaque jour pendant les 6 jours suivants.

Pas de Python ? Ouvrez le site, [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/) (ou double-cliquez sur [`index.html`](index.html) dans une copie locale). Il propose quatre outils qui tournent dans le navigateur — scoring des prospects, prospection, plan de relance et devis — avec les mêmes règles que les scripts, et l'interface existe en 12 langues (menu en haut à droite). Chargez la liste d'exemple → notez-la et repérez vos T0 → générez le message de premier contact et copiez-le → remplacez les champs `[ ]` par votre nom, votre entreprise et votre WhatsApp → planifiez les relances D0/D2/D5 → chiffrez quand ils répondent. Rien n'est envoyé nulle part : votre liste ne quitte jamais le navigateur. Sur le site, le texte de premier contact est en anglais avec une référence en chinois ; pour un texte en espagnol, en portugais ou en arabe, utilisez `outreach_gen.py --lang es/pt/ar`.

---

## Ce que ce dépôt règle vraiment

Tapez « comment se lancer à l'export » sur Google. Vous tombez sur la success story d'un type, deux cents articles SEO, l'aperçu gratuit d'une formation payante et une miniature YouTube qui promet de l'argent rapide. Vous lisez tout, vous vous sentez informé, et le lendemain matin vous fixez un site de données douanières sans avoir la moindre idée de ce qu'il faut mettre dans le premier champ.

Ce n'est pas un manque d'information. C'est de l'information mal façonnée : hachée en fragments, écrite du point de vue des gagnants, et qui s'arrête pile avant le moment où il faut agir.

Voici comment la plupart des tutoriels s'y prennent. *« Vous devriez vous renseigner sur vos clients. »* Puis : *« Se renseigner est important. »* Puis plus rien. Vous ne savez toujours pas quels champs, quels sites, à quoi ressemble un signal d'alerte, ni quand vous en avez assez vérifié.

Ce dépôt fait l'inverse : **prendre une tâche et la découper jusqu'à ce qu'elle devienne une action.**

| Ce que dit un tutoriel | Ce que dit ce dépôt |
|---|---|
| « Renseignez-vous sur vos clients » | Filtre L1, trois contrôles : le site existe-t-il, depuis quand l'entreprise est-elle immatriculée, les comptes sociaux sont-ils actifs. Un seul échec, et le prospect est mort. |
| « La qualité compte plus que la quantité » | 10 prospects répartis en T0/T1/T2/T3, chaque niveau avec son action suivante et son propre budget temps. |
| « Relancez-les » | Jours 1, 3, 5, 7. Un angle différent à chaque fois, et le jour 7 se termine par une décision : insister ou abandonner. |
| « L'IA transforme le commerce » | Quatorze scripts Python en bibliothèque standard pure (treize scripts métier, dont un moteur de devis, plus un garde-fou de confidentialité). `python scripts/lead_score.py examples/leads_example.csv` et vous avez le classement complet en une trentaine de secondes. |

Même information. **Granularité** différente. Toute la différence est là. Chaque affirmation ici doit survivre à une seule question : qu'est-ce que j'ouvre cet après-midi, et qu'est-ce que je tape ?

Donc non, ce n'est pas de la motivation. C'est une checklist et quatorze fichiers de scripts (treize scripts métier + un garde-fou de confidentialité).

---

## Les sept étapes

Une seule chaîne, du début à la fin : choisir un pays, finir avec l'argent sur le compte. Un document par étape, et chaque document se termine par quelque chose que vous pouvez réellement utiliser.

| Étape | Ce que vous faites | Livrable |
|---|---|---|
| **01 Choisir un marché** | Notez-le sur la langue, la demande et les barrières | 1 premier marché + 3 raisons de le défendre |
| **02 Trouver des prospects** | Quatre voies : données douanières, réseaux sociaux, recherche, salons | ≥20 prospects vérifiés par jour |
| **03 Vérifier l'acheteur** | Filtre L1 → standard L2 → analyse approfondie L3 | Note A/B/C ; escrocs écartés |
| **04 Prendre contact** | Classez les prospects de T0 à T3 ; activez trois canaux au premier contact | Liste classée + plan de relance D0/D2/D5 (3 contacts en 6 jours) |
| **05 Parler spécifications** | Petites demandes d'abord. Le prix vient toujours en dernier | Spécification / quantité / port de destination |
| **06 Chiffrer et négocier** | Discipline du devis : chaque concession s'obtient en échange de quelque chose | Devis + échelle de concessions + argumentaires |
| **07 Livrer la commande** | Contrat, production, inspection, documents, paiement, fret | Boucle de livraison bouclée + plan de réachat |

Les documents d'étape se trouvent dans `docs/`, un fichier par étape, tous construits sur la même structure en six parties (voir [CONTRIBUTING.md](CONTRIBUTING.md)) : **à quoi sert cette étape → comment faire, pas à pas → les critères de réussite → les erreurs classiques → les modèles à copier-coller → les prompts IA de cette étape.**

**Vous partez de zéro ?** [`docs/00-getting-started.md`](docs/00-getting-started.md) ne suppose ni git ni Python, et vous met en route en une dizaine de minutes. Plutôt pressé ? [`docs/fast-path.md`](docs/fast-path.md), c'est sept jours de zéro à votre première réponse.

---

## Démarrage en 30 secondes

**Vous ne voulez pas installer Python ?** Ouvrez le site : [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). Quatre outils dans le navigateur — scoring des prospects, prospection, plan de relance et devis — avec une interface en 12 langues. Collez un CSV, obtenez le classement T0-T3, puis le premier contact, les dates de relance et le devis. Rien à installer, et rien ne quitte votre navigateur.

Quatorze fichiers de scripts : treize scripts métier, dont le moteur de devis, plus un script garde-fou de confidentialité (`check_private_data.py`, qui recherche de vraies données clients avant chaque commit). Bibliothèque standard uniquement. Python 3.10+.

```bash
# 1. Classez vos prospects. Un CSV en entrée, T0-T3 en sortie, chaque niveau avec son action suivante.
python scripts/lead_score.py examples/leads_example.csv

# 2. Rédigez le texte de prospection pour un niveau, anglais et 中文 côte à côte.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Construisez le plan de relance. Trois contacts, des dates réelles.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. Devis : coût + fret + marge -> fourchette FOB/CIF + une échelle de concessions en 3 paliers.
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

Voici ce qu'affiche réellement la première commande sur 10 prospects d'exemple. Le script répond en chinois ; 【示例】 est simplement une étiquette qui signifie « exemple », et la dernière colonne est traduite ici :

| Niveau | Entreprise | Pays | Score | Action suivante |
|---|---|---|---|---|
| T0 | 【示例】海湾轮胎贸易 | Arabie saoudite | 95 | envoyer le premier contact aujourd'hui, sans attendre |
| T0 | 【示例】三角洲轮胎 | Arabie saoudite | 88 | envoyer le premier contact aujourd'hui, sans attendre |
| T1 | 【示例】阿曼蓝海 | Oman | 77 | cette semaine ; préparer le texte aujourd'hui |
| T1 | 【示例】半岛汽车 | Arabie saoudite | 71 | cette semaine ; préparer le texte aujourd'hui |
| T1 | 【示例】尼罗河商贸 | Égypte | 67 | cette semaine ; préparer le texte aujourd'hui |
| T1 | 【示例】迪拜轮毂行 | EAU | 65 | cette semaine ; préparer le texte aujourd'hui |
| T1 | 【示例】利雅得汽配 | Arabie saoudite | 60 | cette semaine ; préparer le texte aujourd'hui |
| T2 | 【示例】尼日利亚先锋 | Nigeria | 46 | vivier froid, à passer en revue une fois par jour |
| T3 | 【示例】黎凡特供配 | Liban | 20 | infos insuffisantes, trouver d'abord contact + besoin |
| T3 | 【示例】利雅得零件店 | Arabie saoudite | 10 | infos insuffisantes, trouver d'abord contact + besoin |

Résumé : **T0:2 / T1:5 / T2:1 / T3:2**. À contacter aujourd'hui : 【示例】海湾轮胎贸易, 【示例】三角洲轮胎. Cette semaine : 【示例】阿曼蓝海, 【示例】半岛汽车, 【示例】尼罗河商贸, 【示例】迪拜轮毂行, 【示例】利雅得汽配. À laisser de côté pour l'instant : 【示例】黎凡特供配, 【示例】利雅得零件店.

En-tête CSV :

```
company,country,product,source,email,phone,years,contact,note
```

Seule la colonne `company` est obligatoire. Tout le reste peut rester vide, et un champ vide reçoit le score plancher. C'est `source` qui pèse le plus : `referral` / `trade_show` / `customs` / `linkedin` / `search`.

Les quatorze scripts acceptent `--help`. `lead_score.py` propose aussi `--format json` et les filtres `--country` / `--product`, si vous voulez envoyer le résultat dans un tableur.

Les scripts ne tranchent que ce qu'une machine peut trancher : y a-t-il un e-mail, y a-t-il un site, le prospect passe-t-il la barre du T0. Savoir si un prospect mérite votre après-midi, c'est dans la documentation que ça se joue — et dans votre tête.

---

## Organisation du dépôt

```
zero-to-trade/
├── README.md              # Version chinoise complète
├── README_EN.md           # Version anglaise (la référence de toutes les traductions)
├── README_ES.md / README_PT.md / README_FR.md / README_AR.md / README_RU.md
├── README_DE.md / README_JA.md / README_KO.md / README_TR.md / README_ID.md
│                          # Espagnol, portugais, français, arabe (RTL), russe, allemand, japonais, coréen, turc, indonésien
├── index.html             # Le site : 4 outils dans le navigateur, 12 langues d'interface, zéro dépendance (GitHub Pages)
├── MANIFESTO.md           # Anonyme, pas de formation payante : la position de la marque
├── GITHUB_LAUNCH.md       # Checklist de lancement + promotion (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # Comment contribuer + conventions de documentation et de code
├── CHANGELOG.md           # Journal des modifications : ce qui a changé à chaque fois
├── ROADMAP.md             # Feuille de route : la suite des versions
├── LICENSE                # MIT
├── docs/                  # Un fichier par étape
│   ├── 00-getting-started.md
│   ├── fast-path.md       # 7 jours de zéro à la première réponse
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md # Un exemple réaliste de première affaire, pas à pas
├── scripts/               # Python exécutable, bibliothèque standard uniquement
│   ├── lead_score.py      # Classe les prospects de T0 à T3
│   ├── outreach_gen.py    # Textes de prospection par niveau (EN/ZH + ES/PT/AR avec référence anglaise, V13)
│   ├── followup_plan.py   # Plan de relance D0/D2/D5 (3 contacts en 6 jours)
│   ├── quote_engine.py    # Moteur de devis : fourchette FOB/CIF + échelle de concessions en 3 paliers
│   ├── due_diligence.py   # V11, agent de vérification : L1/L2/L3 + note A/B/C + signaux d'alerte
│   ├── tire_pack.py       # V12, pack secteur pneus : dimension + marché → points GCC + documents de dédouanement + notes marché
│   ├── landed_cost.py     # Coût rendu, V14 : FOB + fret + assurance → CIF, plus droits + frais à destination → DDP
│   ├── trade_show.py      # Salon, V15 : exposants collectés sur le salon → plan de relance sous 24 h (remerciement sous 2 h, piste de devis sous 12 h, relance appel/WhatsApp sous 24 h)
│   ├── nudge.py           # Bibliothèque de relances, V16 : D3/D7/D14/D30 × devis envoyé/échantillon envoyé/en négociation → version WhatsApp courte + version e-mail plus longue (anglais + chinois)
│   ├── anchor_price.py    # Prix de référence concurrent, V18 : fourchette de prix concurrents issue des données douanières + votre coût → paliers CIF agressif/médian/prudent + checklist en 5 points
│   ├── fast_path.py     # V19, parcours express interactif de 7 jours : --day N affiche les tâches, --done N les coche, --progress fait le bilan (aligné sur docs/fast-path.md)
│   ├── market_rules.py    # Règles marché : marchés cibles, barrières Turquie/Brésil, exclusions Mexique/États-Unis/UE
│   ├── daily_video_list.py  # Liste quotidienne de 5 vidéos (3 le matin, 2 l'après-midi) avec dimension, marché, argument de vente et contrôle des plans
│   └── check_private_data.py  # Garde-fou de confidentialité : recherche de vraies données clients avant commit
├── examples/
│   ├── leads_example.csv  # Données d'exemple, exécutables telles quelles
│   ├── leads_example_lighting.csv  # Exemple hors pneus : 8 prospects en éclairage LED
│   └── trade_show_example.csv  # Exposants d'exemple, un par niveau d'intérêt
├── tests/                 # 452 tests en bibliothèque standard
├── prompts/
│   └── AI_PROMPTS.md      # 40 prompts à copier-coller (28 essentiels + 12 avancés), regroupés par étape
└── assets/                # Captures d'écran, schémas
```

---

## Pourquoi des scripts, et pas seulement un document de méthode

La plupart des dépôts « IA pour le business » font la même chose : prendre la méthodologie, la coller dans un prompt, et publier. Celui-ci fonctionne à l'envers. **La discipline d'abord, les outils ensuite.**

Pourquoi : **être bon en prompts, ce n'est pas être bon en commerce.** Mon pari, c'est que ce ne sont pas les mots qui vous manquent. C'est une façon de décider. Donc :

- **Ici, les règles sont le produit.** Un T0 reçoit un e-mail aujourd'hui. Un T3 reste au tiroir pendant trois mois. Une concession qui ne rapporte rien en retour est un cadeau, pas une négociation. Aucun modèle ne prend ces décisions à votre place.
- **Le volume, c'est pour l'IA.** Filtrer 8 prospects d'un coup, rédiger trois niveaux de vérification sur 50 entreprises, décliner sept jours de variantes de relance. Des heures de travail, presque aucun jugement dedans.
- **Tout ce qui se répète devient un script.** Si le classement relève du ressenti, ce n'est pas un standard. C'est donc un script de moins de 200 lignes, sans aucune dépendance, et deux personnes qui le lancent arrivent au même résultat.

Où passe la frontière : **ça tient dans un `if/else` ? Dans un script. Ça demande un arbitrage ? Dans la documentation. Ça doit sonner comme écrit par un humain ? Dans `prompts/`.**

Pas de pandas, pas de SDK OpenAI, et c'est voulu. La configuration de l'environnement, c'est là que les débutants abandonnent. Quelqu'un qui découvre l'export perdra plus d'heures sur `pip install` qu'à trouver des clients, et c'est un endroit stupide pour les perdre.

---

## Feuille de route

> Feuille de route complète : [ROADMAP.md](ROADMAP.md) ; historique des modifications : [CHANGELOG.md](CHANGELOG.md).

| Version | Statut | Contenu |
|---|---|---|
| **V13** | ✅ Livrée (2026-11-07) | Prospection multilingue (`scripts/outreach_gen.py --lang es/pt/ar` : texte en espagnol/portugais/arabe + original anglais après chaque brouillon ; modèles calqués un pour un sur les T0/T1/T2 anglais, un seul dictionnaire intégré au script) + nouvelle section dans `docs/04-outreach.md` (utilisation + 3 sorties réelles collées telles quelles) + `tests/` 80 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 7 fichiers de scripts |
| **V18** | ✅ Livrée (2026-11-07) | Prix de référence concurrent (`scripts/anchor_price.py` : fourchette de prix concurrents issue des données douanières + votre coût → paliers CIF agressif/médian/prudent, chacun avec marge disponible, taux de marge, équivalent FOB, majoration implicite et cas d'usage ; une checklist en 5 points — coût, fret, change, conditions de paiement, validité — avant de chiffrer, tout point non coché étant signalé ; alerte sous le coût « sous le coût, ne prenez pas la commande, négociez d'abord le volume contre le prix » ; médiane manquante estimée à (bas + haut) / 2 et marquée comme estimation ; `--format json` / `--audience client`) + `docs/anchor-price.md` (utilisation + guide du prix de référence + 2 sorties réelles collées telles quelles) + une ligne dans `docs/06-quote.md` (prix de référence avant de chiffrer) + `tests/` 187 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 11 fichiers de scripts |
| **V20** | ✅ Actuelle (2026-11-14) | Fusion des incréments locaux + 10 tours de durcissement : points d'entrée CLI unifiés (erreurs en langage clair, codes de sortie harmonisés) + tests renforcés (mode message unique, alias `--start-date`, journaux d'exécution) + chiffres de la documentation alignés + exemple hors pneus (8 prospects en éclairage LED) + page de démo synchronisée avec la V19 + erreurs claires pour les CSV défectueux (colonne manquante / fichier vide / guillemet non fermé ne provoquent plus de traceback) + alignement des prompts (la commande de relance P04-4 gagne `--avoid-weekend`, la fenêtre de P10-2 unifiée à 48 heures) + traçage des exécutions en place (`logs/trace-YYYY-MM-DD.jsonl`, une ligne par exécution des trois scripts principaux) + nettoyage du code (fonctions utilitaires partagées regroupées en un seul endroit, −151 lignes nettes ; deux fonctions mortes supprimées) + `tests/` 452 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 14 fichiers de scripts |
| **V19** | ✅ Livrée (2026-11-07) | Parcours express interactif de 7 jours (`scripts/fast_path.py` : `--day N` affiche les tâches du jour — nom de la tâche + livrable + script/document à utiliser ; `--done N` coche une journée avec horodatage, écrit dans le fichier JSON `--state`, un second pointage indique que c'est déjà fait et n'est pas enregistré deux fois ; `--progress` fait le total fait / restant / en retard (en retard = date prévue antérieure à aujourd'hui et non cochée, date prévue = jour 1 de `--start` + (N-1) jours ; sans `--start`, pas de décompte des retards, et c'est dit clairement) ; `--list` affiche les 7 jours ; tâches alignées ligne par ligne sur `docs/fast-path.md`, aucune seconde liste inventée ; `--help` contient de vrais exemples, un jour ou une date invalide donne une erreur en langage clair) + `docs/fast-path-interactive.md` (utilisation + format du fichier d'état + règle de retard + vue d'ensemble des 7 jours + 2 sorties réelles collées telles quelles) + une ligne en tête de `docs/fast-path.md` (point d'entrée interactif) + une ligne dans `docs/00-getting-started.md` étape B5 (8 scripts restants → 9) + `tests/` 226 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 12 fichiers de scripts |
| **V17** | ✅ Livrée (2026-11-07) | README complets en portugais et en arabe (nouveaux `README_PT.md` en portugais du Brésil et `README_AR.md` en arabe avec mise en page RTL, tous deux traduits intégralement et alignés sur README_EN.md : mêmes sections, tableaux, commandes, noms de scripts, noms de fichiers, version et chiffres ; toutes les entreprises/prix/contacts d'exemple sont fictifs, marqués 【示例】 avec le domaine réservé sample.example) + `tests/` 167 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 10 fichiers de scripts |
| **V16** | ✅ Livrée (2026-11-07) | Bibliothèque de relances (`scripts/nudge.py` : D3/D7/D14/D30 × devis envoyé/échantillon envoyé/en négociation, 12 brouillons au total, version WhatsApp courte + version e-mail plus longue, l'anglais d'abord avec la traduction chinoise après chaque brouillon ; gradation du ton — D3 rappel léger, D7 demande d'avancement, D14 trois options pour sauver la face (prix plus bas / autre spécification / délai de paiement plus long), D30 dernier message qui laisse la porte ouverte ; le jour 0 est le jour d'envoi du devis/de l'échantillon/de la discussion de prix, un repère différent du rythme de premier contact de followup_plan, un fil ne suit qu'une seule piste ; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (utilisation + articulation avec followup_plan + 2 sorties réelles collées telles quelles) + une ligne dans `docs/00-getting-started.md` (liste des scripts 6 → 7) + `tests/` 152 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 10 fichiers de scripts |
| **V15** | ✅ Livrée (2026-11-07) | Relance après salon (`scripts/trade_show.py` : exposants collectés sur le salon classés par intérêt dans un plan de relance sous 24 heures — remerciement + documentation sous 2 h, piste de devis sous 12 h, relance appel/WhatsApp sous 24 h ; `--add` un par un + `--csv` par lot, `--format json` / `--out` ; le brouillon de premier contact suit le modèle T0/T1/T2 d'outreach_gen) + `docs/trade-show.md` (utilisation + 1 sortie réelle collée telle quelle) + `examples/trade_show_example.csv` (3 exposants d'exemple, un par niveau d'intérêt) + une ligne dans `docs/00-getting-started.md` et une dans `docs/02-find-leads.md` (que faire des prospects après le salon) + `tests/` 127 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 9 fichiers de scripts |
| **V14** | ✅ Livrée (2026-11-07) | Estimation du coût rendu (`scripts/landed_cost.py` : FOB + fret + assurance → CIF, plus droits + frais au port de destination → DDP ; coût unitaire + totaux + marge disponible si un prix de vente est indiqué ; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (utilisation + tableau des formules + 2 sorties réelles collées telles quelles) + une ligne dans `docs/00-getting-started.md` et une dans `docs/06-quote.md` (chiffrer d'abord le FOB/CIF avec quote_engine, puis calculer le coût rendu complet avec landed_cost) + `tests/` 97 tests en bibliothèque standard + 40 prompts inchangés (28 essentiels + 12 avancés) + 8 fichiers de scripts |
| **V12** | ✅ Livrée (2026-11-07) | Pack secteur pneus (`scripts/tire_pack.py` : dimension + marché → points de certification GCC + documents de dédouanement au port de destination + notes marché ; 4 dimensions TBR × 8 marchés) + `docs/tire-pack.md` (utilisation + 2 sorties réelles collées telles quelles) + liste des scripts mise à jour dans `docs/00-getting-started.md` + `tests/` 68 tests en bibliothèque standard + 40 prompts (28 essentiels + 12 avancés) + 7 fichiers de scripts |
| **V11** | ✅ Livrée (2026-11-07) | Agent de vérification (`scripts/due_diligence.py` : L1/L2/L3 + note A/B/C + checklist des signaux d'alerte + vue client + sortie JSON) + section 13 de `docs/03-due-diligence.md` (sortie réelle collée telle quelle) + prompt P03-5 + `tests/` 52 tests en bibliothèque standard + 40 prompts (28 essentiels + 12 avancés) + 6 fichiers de scripts |
| **V10** | ✅ Livrée (2026-11-07) | 6 modules avancés (08 site autonome / 09 matrice de réseaux sociaux / 10 salons / 11 logistique et paiement / 12 risques et conformité / 13 grands comptes) + 3 parcours d'apprentissage + dépannage et workflow des contributeurs + moteur de devis durci (isolation de la vue client, contrôles des limites) + `tests/` 30 tests en bibliothèque standard + 39 prompts (27 essentiels + 12 avancés) + scoring de la démo navigateur aligné sur Python |
| **v0.1.5** | Publiée | Démo navigateur sans installation (index.html) + moteur de devis v0.2 en alpha (quote_engine.py) + manifeste de la marque (MANIFESTO) + checklist de lancement/promotion (GITHUB_LAUNCH) + Fast Path + exemple d'affaire pas à pas |
| **v0.1** | Publiée | 7 documents d'étape, 4 scripts métier en bibliothèque standard, 27 prompts, README bilingue |
| **v0.2** | ✅ Livrée (alpha) | **Moteur de devis IA** : `scripts/quote_engine.py` est en ligne — coûts + marché + prix de référence concurrent en entrée → fourchette FOB/CIF + une échelle de concessions en trois paliers (chaque palier doit rapporter quelque chose) ; isolation de la vue client et contrôles des limites durcis (voir `tests/test_quote_engine.py`) |
| **Prochaine version** | À décider | Prochaine orientation à décider (le parcours express interactif de 7 jours est arrivé avec la V19) |
| **Long terme** | — | Packs sectoriels (pneus, matériaux de construction, machines, quincaillerie) ; textes de prospection en français/russe (espagnol, portugais et arabe arrivés avec la V13) ; jeux de données publics de prospects anonymisés ; connexion du moteur de devis aux données douanières pour un prix de référence concurrent automatique |

La V20 n'attend pas la prochaine version : les 10 tours de durcissement sont utilisables dès maintenant (les CSV défectueux donnent des erreurs en langage clair au lieu de tracebacks, chaque exécution écrit une ligne de trace, les fonctions utilitaires partagées sont regroupées en un seul endroit). Inutile d'attendre la prochaine version — les scripts sont déjà dans le dépôt, avec 452 tests tous au vert.

---

## Contribuer

Ce qui manque ici, ce n'est pas la documentation. C'est **le détail terrain propre à chaque pays.** Je sais comment se passe une première commande de pneus vers le Moyen-Orient. Je n'ai aucune idée de la façon dont fonctionne la distribution de matériaux de construction en Équateur, ni des documents que la douane nigériane exige réellement. Seuls ceux qui vendent là-bas peuvent combler ce vide.

Trois façons de participer, de la plus simple à la plus exigeante :

1. **Corriger quelque chose.** Une coquille, un fait dépassé, une règle qui ressemble à de la bouillie. Ouvrez une issue. Une phrase vaut mieux que le silence. Le modèle pose trois questions : à quelle ligne vous avez décroché, quel chiffre n'a pas de source, quelle règle ne tient pas dans votre secteur.
2. **Traduire une étape.** Espagnol, arabe, portugais, russe, français, vietnamien — la langue que vous parlez vraiment. Gardez la structure en six parties, changez la langue, alignez les termes sur [GLOSSARY.md](GLOSSARY.md).
3. **Ajouter votre pays ou votre secteur.** C'est la pièce manquante. Écrivez ce que vous avez fait, pas ce que vous pensez qu'il faudrait faire. Noms de champs, noms de documents, comment le canal se construit, comment les gens paient, et pourquoi ils refusent de payer.

Le code aussi, avec une règle stricte : **Python 3.10+, bibliothèque standard uniquement.** L'explication se trouve dans [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Pour les développeurs : modifiable à souhait, et sans aucune dépendance

Les treize scripts métier (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list`, plus le garde-fou de confidentialité `check_private_data.py`) n'utilisent que la bibliothèque standard. Il n'y a aucun `pip install`. Forkez, modifiez, intégrez-les à vos propres outils :

- Les pondérations vous semblent fausses ? Quatre constantes en tête de `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Le plafond reste à 100.
- Vous avez vos propres données douanières ? Respectez l'en-tête (`company,country,product,source,email,phone,years,contact,note`) et injectez-les.
- Vous voulez l'intégrer à votre propre outil ? Chaque script s'importe proprement. `score_lead()`, `render()`, `plan_followups()`, `build_quote()` sont des fonctions pures qui renvoient des dictionnaires et des listes. Pas de réseau, aucun fichier écrit.
- La CI exécute `py_compile` plus la suite de tests (Python 3.10–3.13) plus un contrôle de confidentialité sur chaque PR, pour qu'une mauvaise modification ne passe pas en douce.

> Le parti pris ici : **le vérifiable plutôt que l'astucieux.** Ne me croyez pas sur parole : lancez `python scripts/lead_score.py examples/leads_example.csv` et lisez ce qui sort.

---

## Si ce dépôt vous a évité un faux pas

Mettez une étoile. En haut à droite. C'est tout ce que je demande. C'est aussi comme ça que vous le retrouverez dans six mois, quand vous aurez oublié le nom et qu'il vous faudra le plan de relance à 23 h.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[Voir le graphique complet de l'historique des étoiles](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Traductions

Le README existe en 12 langues, tout comme l'interface du site. L'anglais est le texte de référence.

- [中文](README.md) (chinois, complet)
- [Español](README_ES.md) (espagnol, version de départ, relecteurs recherchés)
- [Português](README_PT.md) (portugais du Brésil, complet)
- [Français](README_FR.md) (version française complète)
- [العربية](README_AR.md) (arabe, complet, RTL)
- [Русский](README_RU.md) (russe, complet)
- [Deutsch](README_DE.md) (allemand, complet)
- [日本語](README_JA.md) (japonais, complet)
- [한국어](README_KO.md) (coréen, complet)
- [Türkçe](README_TR.md) (turc, complet)
- [Bahasa Indonesia](README_ID.md) (indonésien, complet)

Les documents d'étape de `docs/` n'existent encore qu'en chinois. Traduisez une étape dans une langue que vous maîtrisez ; gardez la structure en six parties et alignez les termes sur le [GLOSSARY.md](GLOSSARY.md). Les locuteurs natifs capables de relire un README sont aussi les très bienvenus. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Licence

[MIT](LICENSE) © 2026 zero-to-trade contributors

Utilisez-le, modifiez-le, vendez avec. Gardez la mention de crédit. Une réserve : rien de tout cela ne vous garantit de décrocher une affaire. Ce qui est garanti, en revanche, c'est que vous ne resterez pas bloqué faute de connaître l'étape suivante.

---

## Questions et contributions

**Ouvrez une issue : https://github.com/6hn68/zero-to-trade/issues**

Quelque chose est faux ici ? Dites-le, ça compte comme une contribution. Vous vendez sur un marché dont ce dépôt n'a jamais entendu parler ? C'est exactement le genre de PR que j'attends. Vous pensez que toute la méthode est à côté de la plaque ? Venez en débattre dans une issue, je préfère avoir tort à voix haute.

Pas de biographie de l'auteur, et c'est voulu. **C'est le contenu qui doit vous convaincre, pas son auteur.** Pour me joindre : mentionnez le mainteneur avec @ dans une issue, ou laissez un message via le formulaire en bas du site. Dans les deux cas, votre message arrive jusqu'à l'auteur.
