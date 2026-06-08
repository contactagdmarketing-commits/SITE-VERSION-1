"""
Agent Rédacteur — Candidalib
Rôle : Lit le calendrier généré par l'Agent Stratège et rédige les textes
complets de chaque post (légende, hashtags, script TikTok, texte Google Business).
Sauvegarde les drafts prêts à publier dans outputs/drafts/semaine[N]-[mois][année].md
"""

import anthropic
import json
import re
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
    for skill_file in sorted(SKILLS_DIR.glob("*.md")):
        contenu += f"\n\n{'='*60}\n"
        contenu += f"SKILL : {skill_file.name}\n"
        contenu += f"{'='*60}\n"
        contenu += skill_file.read_text(encoding="utf-8")
    return contenu


def lire_calendrier(mois: str, annee: int) -> str:
    """Charge le calendrier généré par l'Agent Stratège."""
    nom_fichier = f"calendrier-{mois.lower()}{annee}.md"
    chemin = DRAFTS_DIR / nom_fichier
    if not chemin.exists():
        raise FileNotFoundError(f"Calendrier introuvable : {chemin}\nLance d'abord l'Agent Stratège.")
    return chemin.read_text(encoding="utf-8")


def lire_utm_config() -> dict:
    """Charge la configuration des liens UTM."""
    utm_file = CONFIG_DIR / "utm-tracking.json"
    if utm_file.exists():
        return json.loads(utm_file.read_text(encoding="utf-8"))
    return {}


def rediger_semaine(semaine_num: int, calendrier: str, skills: str, utm: dict) -> str:
    """Rédige tous les posts d'une semaine via Claude."""
    client = anthropic.Anthropic()

    prompt = f"""Tu es l'Agent Rédacteur de Candidalib. Tu reçois le calendrier éditorial du mois et tu rédiges les textes complets de chaque post pour la semaine {semaine_num}.

SKILLS À APPLIQUER OBLIGATOIREMENT :
{skills}

CONFIGURATION UTM :
{json.dumps(utm, ensure_ascii=False, indent=2)}

CALENDRIER DU MOIS (contexte complet) :
{calendrier}

TA MISSION : Rédige les textes complets de tous les posts de la SEMAINE {semaine_num} uniquement.

Pour chaque post, produis :
1. Le texte complet de la légende (ou script TikTok, ou post Google Business)
2. Les hashtags adaptés au réseau (Instagram uniquement)
3. Le lien UTM tracké (déjà dans le calendrier, à reprendre tel quel)
4. Le nom de l'image associée (convention : jour-réseau.png)
5. Un brief visuel détaillé pour l'Agent Designer (description précise de l'image à générer, SANS emojis ni émoticônes)

RÈGLES STRICTES :
- ZÉRO emoji dans les briefs visuels
- Respect du ton par profil (tutoiement jeunes / vouvoiement parents)
- NE JAMAIS écrire "formation" — toujours "préparation à l'examen" ou "accompagnement"
- Chaque post doit finir par un appel à l'action clair
- Les briefs visuels doivent être en anglais (pour Nano Banana / Gemini)

Format de sortie : fichier Markdown structuré, une section par post, prêt à copier-coller.
"""

    print(f"  Rédaction semaine {semaine_num}...")

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8096,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def sauvegarder_semaine(contenu: str, semaine_num: int, mois: str, annee: int) -> Path:
    """Sauvegarde le draft de la semaine dans outputs/drafts/."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    nom_fichier = f"semaine{semaine_num}-{mois.lower()}{annee}.md"
    chemin = DRAFTS_DIR / nom_fichier

    header = f"""# Semaine {semaine_num} — {mois.capitalize()} {annee}
*Rédigé par l'Agent Rédacteur le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*
*Statut : En attente de validation → Agent Designer*

---

"""
    chemin.write_text(header + contenu, encoding="utf-8")
    print(f"  Sauvegarde : {nom_fichier}")
    return chemin


def run(mois: str, annee: int, semaines: list = None):
    """
    Point d'entrée de l'agent.

    Args:
        mois: Mois cible (ex: "juillet")
        annee: Année (ex: 2026)
        semaines: Liste des semaines à rédiger (ex: [1, 2]). Par défaut toutes (1-4).
    """
    if semaines is None:
        semaines = [1, 2, 3, 4]

    print(f"\n{'='*50}")
    print(f"  AGENT RÉDACTEUR — Candidalib")
    print(f"  Mois : {mois} {annee} | Semaines : {semaines}")
    print(f"{'='*50}\n")

    skills = lire_skills()
    utm = lire_utm_config()

    print("Chargement du calendrier...")
    calendrier = lire_calendrier(mois, annee)
    print(f"Calendrier chargé ({len(calendrier)} caractères)\n")

    fichiers_generes = []
    for num in semaines:
        print(f"Semaine {num} en cours...")
        contenu = rediger_semaine(num, calendrier, skills, utm)
        chemin = sauvegarder_semaine(contenu, num, mois, annee)
        fichiers_generes.append(chemin)

    print(f"\n{'='*50}")
    print(f"  {len(fichiers_generes)} semaine(s) rédigée(s)")
    for f in fichiers_generes:
        print(f"  - {f.name}")
    print(f"\n  Prochaine étape : Agent Designer")
    print(f"{'='*50}\n")

    return fichiers_generes


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage : python3 agent.py [mois] [annee] [semaines optionnelles: 1,2,3,4]")
        print("Exemple : python3 agent.py juillet 2026")
        print("Exemple : python3 agent.py juillet 2026 1,2")
        sys.exit(1)

    mois = sys.argv[1]
    annee = int(sys.argv[2])
    semaines = [int(s) for s in sys.argv[3].split(",")] if len(sys.argv) > 3 else None

    run(mois, annee, semaines)
