# Agent Stratège

## Rôle
Génère le calendrier éditorial mensuel pour tous les réseaux sociaux de Candidalib.
C'est le **premier agent de la chaîne** — son output alimente l'Agent Rédacteur.

## Ce qu'il fait
1. Lit tous les skills (`/skills/`)
2. Applique la saisonnalité Candidalib
3. Respecte la répartition des piliers éditoriaux
4. Génère 4 semaines de contenu structuré
5. Sauvegarde dans `outputs/drafts/calendrier-[mois][année].md`

## Lancer l'agent

### Mois suivant (par défaut)
```bash
python agent.py
```

### Mois spécifique
```bash
python agent.py juillet 2026
```

### Avec événements spéciaux
```bash
python agent.py juillet 2026 "Vacances d'été, pic de demande permis"
```

## Prérequis
```bash
pip install anthropic
export ANTHROPIC_API_KEY="ta-clé-api"
```

## Output
Fichier `outputs/drafts/calendrier-[mois][année].md` contenant :
- 4 semaines × 6 jours de posts
- Par post : réseau, pilier, thème, accroche, nom image, lien UTM
- Prêt à être transmis à l'Agent Rédacteur
