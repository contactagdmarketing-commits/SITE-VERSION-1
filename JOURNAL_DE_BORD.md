# 📓 JOURNAL DE BORD — Projet Candidalib

> Fichier maître du projet. À lire EN PREMIER au début de chaque session.
> **Règle d'or : on n'efface jamais, on ne réécrit jamais. On ajoute uniquement, en bas.**
> Si une info change, on ajoute une nouvelle entrée datée qui dit ce qui a changé.

---

# PARTIE 1 — MANIFESTE

## 🟢 ÉTAT ACTUEL au 2026-06-26

Le projet a **deux volets** qui vivent dans le même dépôt `SITE-VERSION-1/` :

1. **Le site web `candidalib.fr`** (racine du repo) — 12 pages HTML statiques, opérationnel.
   Depuis aujourd'hui, il est **instrumenté pour le suivi de trafic** (Analytics) et dispose
   d'une **page « Appeler / Être rappelé »**.
2. **L'équipe d'agents IA Community Manager** (`agents-cm/`) — génère et gère le contenu
   réseaux sociaux. 5 agents + orchestrateur opérationnels.

**Ce qui est branché et fonctionne aujourd'hui :**
- Tracking site : **Google Analytics 4 (`G-P1VV14CR0E`) + Microsoft Clarity (`xcyzchjdx6`)** actifs,
  derrière un bandeau de consentement RGPD. Suivi auto des clics « Appeler ».
- Page contact refondue : bouton d'appel + formulaire « Être rappelé ».
- Agents : Stratège, Rédacteur, Designer, CM Social, Orchestrateur — tous fonctionnels.

**Ce qui reste en suspens (voir Roadmap) :**
- ⏳ **Meta Pixel** : non créé (blocage structurel Meta — voir entrée 2026-06-26 et Points d'attention).
- ⏳ **Clé Web3Forms** : le formulaire « Être rappelé » est en ligne mais n'enverra les emails
  qu'une fois la clé posée (placeholder `VOTRE_CLE_WEB3FORMS` dans `contact.html`).
- ⏳ Mention RGPD des 3 outils de tracking à ajouter dans `confidentialite.html`.

---

## 🎯 Vision (le projet en 3 lignes)

Candidalib aide à passer le permis **en candidat libre** à Toulouse (véhicule double commande +
accompagnateur). Objectif business : **faire sonner le téléphone tous les jours** via du contenu
réseaux sociaux régulier + des pubs ciblées + un site qui convertit la visite en appel.
Candidalib **N'EST PAS une auto-école** (contrainte légale majeure).

## 📜 Doctrine / Règles permanentes

- **JAMAIS le mot « formation »** seul, ni « moniteur », « leçon de conduite », « cours de conduite ».
  Utiliser : « accompagnement », « préparation à l'examen », « support d'aide à la préparation ».
- **Zéro emoji / émoticône dans les visuels générés** (ça fait IA). Max 1-2 dans le texte des posts.
- **Prix** : Candidalib 45 €/h, forfait 10h = 400 €, jour J = 80 €. Auto-école (comparatif) = **55-70 €/h**.
- **Nommage images/drafts** : `[jour]-[date]-[mois]-[réseau].jpg` (ex : `lundi-29-juin-instagram.jpg`),
  avec date précise obligatoire. La section du draft doit matcher (`## LUNDI 29 JUIN — Instagram`).
- **Sécurité** : ne jamais créer de comptes, saisir de mots de passe, accepter des CGU ni supprimer
  de données à la place de l'utilisateur. On récupère seulement des IDs publics.
- **Ce journal** : lu en début de session, complété en fin d'avancée, jamais réécrit.

## 🏗️ Architecture en 1 minute

**Site (`/` racine)** — HTML statique, pas de build.
- Pages partagent `styles.css` + `script.js`. Palette : bleu `#3b82f6`/`#1e3a8a`, orange `#f97316`, police Inter.
- `tracking.js` (nouveau) : consentement RGPD + GA4 + Clarity + Meta Pixel, chargés après accord.
  Inerte tant que les IDs valent `XXXX`. Fournit `window.candidalibTrack(nom)` et suit les liens `tel:`.
- `contact.html` = page de conversion (appel + formulaire rappel via Web3Forms).

**Agents (`agents-cm/`)** — scripts Python appelant l'API Claude (+ Gemini/Nano Banana pour les images).
Chaîne : Stratège → Rédacteur → Designer → CM Social, pilotée par `orchestrateur.py`.
Tous lisent les `skills/` avant de produire (garantit le respect de la doctrine).

## 🗺️ Roadmap (ce qui reste à faire)

| Priorité | Tâche | Détail |
|---|---|---|
| Rapide | Clé Web3Forms | Activer la réception des demandes de rappel par email |
| Rapide | RGPD | Citer GA4/Clarity/Meta dans `confidentialite.html` |
| Quand pubs | Meta Pixel | Débloquer (cf. Points d'attention) puis créer + coller l'ID |
| Moyen | Contenu juillet | Générer semaines 2, 3, 4 (semaine 1 faite) |
| Moyen | Publication auto | Connecter Meta API / Buffer pour poster automatiquement |
| Plus tard | Agents Ads + Analyste | Pubs payantes + lecture des données de tracking |
| Plus tard | Agent Vidéo | Reels/TikTok (scripts déjà produits par le Rédacteur) |

## ⚠️ Points d'attention

- **Meta Pixel bloqué (structurel)** : la Page `Candidalib'` (FB ID `143272228880264`) est dans le
  portefeuille business **« Edhy Delaprez »** (`business_id 261567370285820`), qui a **0 compte publicitaire**.
  Les outils de création de Pixel (Events Manager) exigent un compte pub. Le compte pub vu
  (`1164645334901417`) est dans **un autre** des 4 portefeuilles. → Avant de créer le Pixel, il faudra
  régler cette organisation (mettre/partager un compte pub dans le portefeuille de Candidalib).
  Le wizard « Web → Suivant » d'Events Manager **bugue** en plus (se referme) ; passer par un autre chemin.
- **Measurement ID GA4** : lu à l'écran `G-P1VV14CR0E` (le caractère avant le E final est un **zéro**).
  À revérifier si GA ne remonte pas (Analytics → Admin → Flux de données).
- **Clés API** : `agents-cm/.env` (Anthropic + Gemini) — hors git (.gitignore). Ne jamais committer.
- **Réseaux Candidalib** : Facebook 0 abonné, Instagram 45 abonnés. La portée organique est donc
  quasi nulle au départ → les appels viendront surtout des **pubs**, pas du seul organique.

## 📁 Fichiers / dossiers clés

| Chemin | Rôle |
|---|---|
| `JOURNAL_DE_BORD.md` | Ce fichier — carnet + index maître |
| `index.html` … (12 pages) | Le site candidalib.fr |
| `styles.css` / `script.js` | Styles + JS partagés par toutes les pages |
| `tracking.js` | Consentement RGPD + GA4 + Clarity + Meta Pixel + suivi conversions |
| `contact.html` | Page « Appeler / Être rappelé » (conversion) |
| `CONFIGURATION-TRACKING.md` | Guide : où coller les IDs de tracking + clé Web3Forms |
| `agents-cm/orchestrateur.py` | Lance toute la chaîne d'agents |
| `agents-cm/agents/*/agent.py` | Stratège, Rédacteur, Designer, CM Social |
| `agents-cm/skills/*.md` | ADN marque, copywriting, calendrier, GEO/avis |
| `agents-cm/outputs/` | drafts, images, rapports CM générés |
| `agents-cm/.env` | Clés API (hors git) |

---

# PARTIE 2 — ENTRÉES CHRONOLOGIQUES

> Du plus ancien au plus récent. Ne jamais modifier une entrée existante ; ajouter en dessous.

## 2026-06-06 — Audit SEO/GEO + refonte front du site (catégorie : Front / SEO) [par : Claude + Edhy]
**Quoi** : Suppression systématique du mot « formation » (et requalification sémantique) sur tout
le site. Ajout schema.org (LocalBusiness, FAQPage), page `methode.html` (23 modules), `guide-candidat-libre.html`.
Nombreux ajustements front : hero, header sticky, nav, logo (JPG→PNG transparent), footer (retrait réseaux).
**Pourquoi** : Conformité légale (Candidalib ≠ auto-école) + optimisation pour citation par les IA (GEO)
+ repositionnement « accompagnement à la préparation du permis en candidat libre ».
**Où** : `index.html`, `cgu.html`, `mentions-legales.html`, `methode.html`, `guide-candidat-libre.html`, `styles.css`.
**Comment** : Commits `0416bf4` → `d7f1f9e`. Itérations multiples sur le hero (voir git log).

## 2026-06-08 — Création de l'équipe d'agents CM + contenu juin/juillet (catégorie : Back / Agents) [par : Claude + Edhy]
**Quoi** : Mise en place de `agents-cm/` : skills (ADN marque, copywriting, calendrier, GEO/avis),
Agent Stratège (calendrier mensuel), Agent Rédacteur (textes + UTM), Agent Designer (images via
Nano Banana/Gemini). Calendrier juillet 2026 + semaine 1 juin & juillet (posts + images + tracking UTM).
Convention de nommage avec date précise. Règle no-emoji dans les visuels.
**Pourquoi** : Industrialiser la production de contenu réseaux sociaux dans le respect de la doctrine.
**Où** : `agents-cm/agents/{stratege,redacteur,designer}/agent.py`, `agents-cm/skills/*.md`,
`agents-cm/outputs/`, `agents-cm/.env` (clés).
**Comment** : Commits `0a3c677` → `097ffea`. Nano Banana MCP patché (bon modèle Gemini + dossier de sortie).
SDK images : `google-genai` (part.inline_data en bytes bruts, détection JPEG).

## 2026-06-26 — Corrections des visuels de juin (catégorie : Design) [par : Claude + Edhy]
**Quoi** : Édition de `jeudi-11-juin-instagram.png` (prix 60-80 → **55-70 €/h**, « Attente moniteur » →
« Plusieurs moniteurs », « Disponible maintenant » → « Accompagnateur unique », retrait des coches vertes,
fond bleu marine harmonisé avec la charte). Retrait des emojis sur `samedi-13-juin-instagram-story.png`.
**Pourquoi** : Exactitude des prix, conformité légale (éviter « moniteur » côté Candidalib), cohérence visuelle.
**Où** : `agents-cm/outputs/images/jeudi-11-juin-instagram.png`, `samedi-13-juin-instagram-story.png`.
**Comment** : via `mcp__nano-banana__edit_image`, plusieurs passes ; fichiers édités renommés sur les originaux.

## 2026-06-26 — Agent CM Social (catégorie : Back / Agents) [par : Claude]
**Quoi** : Création de l'Agent CM Social : lit les interactions (commentaires/DM), génère des réponses
dans le ton de marque, et des demandes d'avis Google. Mode simulation (fichier JSON) ou API Meta.
**Pourquoi** : Compléter la chaîne — répondre vite aux leads (un commentaire/DM sans réponse = lead perdu).
**Où** : `agents-cm/agents/community-manager/agent.py` + `interactions-sample.json`.
**Comment** : `python3 agent.py [simulation|meta] [repondre|avis|tout]`. Sorties dans `outputs/cm/` (JSON + MD).

## 2026-06-26 — Orchestrateur (catégorie : Back / Agents) [par : Claude]
**Quoi** : Script central qui enchaîne Stratège → Rédacteur → Designer → CM en une commande, avec
gestion du « déjà fait » (skip), statut du projet, et logs.
**Pourquoi** : Lancer toute la production sans piloter chaque agent à la main.
**Où** : `agents-cm/orchestrateur.py`.
**Comment** : `python3 orchestrateur.py juillet 2026 [--semaines 1,2] [--etape ...] [--status]`.
Piège corrigé : `importlib.util.module_from_spec` (et non `load_module_from_spec`).

## 2026-06-26 — Cadrage de l'équipe marketing (catégorie : Décision / Stratégie) [par : Claude + Edhy]
**Quoi** : Exploration d'une « agence » à 16 agents (avec pôle Qualité/contrôle), puis recentrage sur
l'objectif réel : **des appels chaque jour**. Conclusion : l'organique seul ne suffit pas (10 abonnés) ;
le levier = pubs ciblées + site qui convertit + réponse rapide. Équipe utile resserrée.
**Pourquoi** : Éviter la sur-ingénierie ; aligner les moyens sur l'objectif business.
**Où** : décision (pas de fichier). Recherche web sourcée (agences social media 2026 + patterns multi-agents).
**Comment** : Reste à construire : Publisheur, Agent Ads, Agent Analyste (cf. Roadmap). Idée d'Agent Vidéo
(Option C : script + voix off ElevenLabs + images + montage moviepy).

## 2026-06-26 — Infrastructure de suivi de trafic du site (catégorie : Front / Analytics) [par : Claude]
**Quoi** : Création de `tracking.js` : bandeau de consentement RGPD + chargement conditionnel de
GA4 + Microsoft Clarity + Meta Pixel (inertes tant que les IDs valent `XXXX`), suivi auto des clics
`tel:`, et fonction `window.candidalibTrack(nom)`. Ajout de la balise sur les **11 pages** HTML.
Refonte de `contact.html` en page « Appeler / Être rappelé » avec formulaire (Web3Forms) qui déclenche
une conversion. Ajout d'un vrai composant de formulaire `.callback-*` dans `styles.css` (charte). Guide
`CONFIGURATION-TRACKING.md`.
**Pourquoi** : Aucun tracking n'existait → impossible de savoir qui visite/clique. C'est le préalable à
toute « stratégie d'analyse ». Et transformer la visite en appel.
**Où** : `tracking.js` (nouveau), `contact.html`, `styles.css` (composant `.callback-*` en fin de fichier),
les 11 `*.html`, `CONFIGURATION-TRACKING.md`.
**Comment** : Site statique → tracking.js injecté avant `</head>` partout (le fichier vide
`google485623...html` est ignoré). Bandeau auto-injecté en JS (1 seule balise par page). Vérifié en
preview locale (`python3 -m http.server 8000`), aucune erreur console. ⚠️ Non encore committé.

## 2026-06-26 — Récupération des IDs de tracking via Chrome (catégorie : Config / Analytics) [par : Claude + Edhy]
**Quoi** : Pilotage de Chrome (Claude in Chrome) pour récupérer/coller les IDs. **Clarity** : projet
« Candidalib » créé → ID `xcyzchjdx6`. **GA4** : propriété déjà existante → Measurement ID `G-P1VV14CR0E`.
Les deux collés dans `tracking.js`. **Meta Pixel** : NON créé (blocage, voir ci-dessous).
**Pourquoi** : Activer la mesure réelle du trafic.
**Où** : `tracking.js` (lignes `GA4_ID`, `CLARITY_ID`).
**Comment** : L'utilisateur reste connecté ; je lis seulement les IDs (jamais de mot de passe). Pour le
Pixel : la Page Candidalib' est dans le portefeuille « Edhy Delaprez » (0 compte pub) → impossible de
créer le Pixel sans compte pub ; + le wizard Web bugue. **Décision : Pixel parqué jusqu'au lancement des
pubs** (il ne sert qu'à ça). Voir Points d'attention pour les IDs Meta (page `143272228880264`, portefeuille
`261567370285820`, compte pub `1164645334901417` dans un autre portefeuille).

## 2026-06-26 — Mise en place du Journal de bord (catégorie : Process) [par : Claude + Edhy]
**Quoi** : Création de ce fichier `JOURNAL_DE_BORD.md` (manifeste + état actuel + historique consolidé
depuis le début), avec recensement de la conversation et du repo (git log, fichiers).
**Pourquoi** : Mémoire persistante du projet, indépendante des sessions IA — « le seau, pas la passoire ».
**Où** : `JOURNAL_DE_BORD.md` (racine).
**Comment** : Règle permanente : lire l'état actuel en début de session, ajouter en bas à chaque avancée,
ne jamais réécrire. À committer dans git.

## 2026-06-26 — Sauvegarde Git du travail de la session (catégorie : Process) [par : Claude + Edhy]
**Quoi** : Commit + push sur `main` de tout le travail de la session (tracking, page Appeler/Être rappelé,
Agent CM, Orchestrateur, corrections visuels, ce journal).
**Pourquoi** : Rien ne se perd ; point de contrôle permanent. Vérification préalable : `.env` (clés API)
bien exclu par `.gitignore`, aucun secret dans `.nano-banana-config.json` ni `.claude/`.
**Où** : commit `79722be` (`097ffea..79722be main -> main`), remote `github.com/contactagdmarketing-commits/SITE-VERSION-1`.
**Comment** : `git add -A` puis commit + `git push`. Branche `main` (convention du repo : commits directs sur main).

## 2026-06-26 — Mention RGPD des outils de tracking (catégorie : Sécu / Légal) [par : Claude]
**Quoi** : Réécriture de la section 8 « Cookies » de `confidentialite.html` : distinction cookies
techniques / mesure d'audience, déclaration de Google Analytics 4 + Microsoft Clarity + Meta Pixel,
consentement préalable, transfert hors UE encadré, modalités de retrait du consentement. Date de mise
à jour passée à « Juin 2026 ».
**Pourquoi** : Obligation RGPD — déclarer les outils de tracking ajoutés le même jour (l'ancienne section
disait à tort que le site ne collectait pas de données).
**Où** : `confidentialite.html` (section 8).
**Comment** : Texte dans `.legal-content`. HTML validé (balises équilibrées). Reste à faire pour finir
la page contact : poser la clé Web3Forms (placeholder `VOTRE_CLE_WEB3FORMS` dans `contact.html`).
