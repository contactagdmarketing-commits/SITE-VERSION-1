# CANDIDALIB — Équipe d'agents Community Manager

## Contexte du projet
Ce projet contient l'équipe d'agents IA dédiée à la gestion des réseaux sociaux de Candidalib.
Site : candidalib.fr — Solution d'accompagnement à la préparation du permis en candidat libre à Toulouse.

## Structure du projet
```
CANDIDALIB-AGENTS/
├── skills/                          ← Les skills (lire avant tout contenu)
│   ├── skill-candidalib.md          ← ADN de la marque (LIRE EN PREMIER)
│   ├── skill-copywriting-reseaux.md ← Règles de rédaction par réseau
│   ├── skill-calendrier-editorial.md← Logique de calendrier et saisonnalité
│   └── skill-geo-avis.md            ← Optimisation GEO et gestion des avis
├── agents/
│   ├── stratege/                    ← Génère le calendrier mensuel
│   ├── redacteur/                   ← Rédige les posts par réseau
│   ├── publisheur/                  ← Programme et poste
│   └── community-manager/           ← Répond aux commentaires et avis
├── config/
│   └── reseaux.json                 ← Credentials et config des APIs réseaux
├── outputs/
│   ├── drafts/                      ← Posts rédigés en attente de validation
│   └── published/                   ← Archive des posts publiés
```

## Règle absolue
Ne JAMAIS utiliser le mot "formation" seul. Toujours utiliser :
- "préparation à l'examen de conduite"
- "accompagnement à la préparation du permis"
- "support d'aide à la préparation"

Candidalib n'est PAS une auto-école agréée. Ne jamais dire "moniteur", "leçon de conduite", "cours de conduite".

## Workflow standard
1. L'Agent Stratège génère le calendrier du mois
2. L'Agent Rédacteur produit les posts (toujours en lisant les skills)
3. Les drafts sont sauvegardés dans outputs/drafts/
4. Validation manuelle ou automatique selon le niveau de confiance
5. L'Agent Publisheur poste via les APIs
6. L'Agent CM surveille et répond

## Pour générer du contenu
Toujours commencer par : "Lis les skills dans /skills/ puis génère..."
