"""
Agent Stratège — Candidalib
Rôle : Génère le calendrier éditorial mensuel pour tous les réseaux sociaux.
Lit les skills, applique la saisonnalité, produit un fichier draft structuré.
"""

import anthropic
import json
import os
from datetime import datetime
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent.parent.parent
SKILLS_DIR = BASE_DIR / "skills"
DRAFTS_DIR = BASE_DIR / "outputs" / "drafts"
CONFIG_DIR = BASE_DIR / "config"


def lire_skills() -> str:
    """Charge tous les skills dans un seul contexte."""
    contenu = ""
    for skill_file in SKILLS_DIR.glob("*.md"):
        contenu += f"\n\n{'='*60}\n"
        contenu += f"SKILL : {skill_file.name}\n"
        contenu += f"{'='*60}\n"
        contenu += skill_file.read_text(encoding="utf-8")
    return contenu


def lire_utm_config() -> dict:
    """Charge la configuration des liens UTM."""
    utm_file = CONFIG_DIR / "utm-tracking.json"
    if utm_file.exists():
        return json.loads(utm_file.read_text(encoding="utf-8"))
    return {}


def generer_calendrier(mois: str, annee: int, evenements: str = "") -> str:
    """
    Appelle Claude pour générer le calendrier éditorial du mois.

    Args:
        mois: Nom du mois en français (ex: "juillet")
        annee: Année (ex: 2026)
        evenements: Événements spéciaux du mois (optionnel)

    Returns:
        Calendrier complet en Markdown
    """
    client = anthropic.Anthropic()

    skills_context = lire_skills()
    utm_config = lire_utm_config()

    prompt = f"""Tu es l'Agent Stratège de Candidalib, chargé de générer le calendrier éditorial mensuel.

Voici tous les skills du projet que tu dois appliquer :
{skills_context}

Configuration UTM :
{json.dumps(utm_config, ensure_ascii=False, indent=2)}

Ta mission : génère le calendrier éditorial complet pour **{mois} {annee}**.

Événements spéciaux ce mois : {evenements if evenements else "Aucun"}

Règles à respecter :
1. Respecte la convention de nommage des fichiers (skill-calendrier-editorial.md)
2. Génère 4 semaines complètes
3. Pour chaque post : jour, réseau, pilier éditorial, thème, accroche, nom image suggéré, lien UTM tracké
4. Respecte la répartition : Éducation 40% / Preuve sociale 25% / Coulisses 20% / Offre 15%
5. Adapte le contenu à la saisonnalité du mois
6. Ne jamais utiliser le mot "formation" — utiliser "préparation à l'examen" ou "accompagnement"

Format de sortie : un fichier Markdown structuré par semaine, prêt à être transmis à l'Agent Rédacteur.
"""

    print(f"🧠 Agent Stratège — Génération du calendrier {mois} {annee}...")

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8096,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def sauvegarder_calendrier(contenu: str, mois: str, annee: int) -> Path:
    """Sauvegarde le calendrier dans outputs/drafts/."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    nom_fichier = f"calendrier-{mois.lower()}{annee}.md"
    chemin = DRAFTS_DIR / nom_fichier

    header = f"""# Calendrier Éditorial — {mois.capitalize()} {annee}
*Généré par l'Agent Stratège le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*
*Statut : En attente de validation → Agent Rédacteur*

---

"""
    chemin.write_text(header + contenu, encoding="utf-8")
    print(f"✅ Calendrier sauvegardé : {chemin}")
    return chemin


def run(mois: str = None, annee: int = None, evenements: str = ""):
    """Point d'entrée de l'agent."""
    # Valeurs par défaut : mois suivant
    if not mois or not annee:
        now = datetime.now()
        mois_noms = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        prochain = now.month % 12
        mois = mois_noms[prochain]
        annee = now.year if prochain > 0 else now.year + 1

    print(f"\n{'='*50}")
    print(f"  AGENT STRATÈGE — Candidalib")
    print(f"  Mois cible : {mois} {annee}")
    print(f"{'='*50}\n")

    calendrier = generer_calendrier(mois, annee, evenements)
    chemin = sauvegarder_calendrier(calendrier, mois, annee)

    print(f"\n✅ Calendrier généré : {chemin.name}")
    print(f"📋 Prochaine étape : lancer l'Agent Rédacteur sur ce fichier\n")

    return chemin


if __name__ == "__main__":
    import sys

    mois = sys.argv[1] if len(sys.argv) > 1 else None
    annee = int(sys.argv[2]) if len(sys.argv) > 2 else None
    evenements = sys.argv[3] if len(sys.argv) > 3 else ""

    run(mois, annee, evenements)
