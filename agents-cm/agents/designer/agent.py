"""
Agent Designer — Candidalib
Rôle : Lit les briefs visuels dans les drafts rédigés par l'Agent Rédacteur
et génère les images via Nano Banana (MCP Gemini).
Sauvegarde les images dans outputs/images/[mois][annee]/semaine[N]/
"""

import anthropic
import re
import os
import base64
import httpx
from datetime import datetime
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent.parent.parent
DRAFTS_DIR = BASE_DIR / "outputs" / "drafts"
IMAGES_DIR = BASE_DIR / "outputs" / "images"
SKILLS_DIR = BASE_DIR / "skills"


def lire_skill_candidalib() -> str:
    """Charge le skill de base pour respecter les règles visuelles."""
    skill_file = SKILLS_DIR / "skill-candidalib.md"
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    return ""


def extraire_briefs(draft_path: Path) -> list[dict]:
    """
    Extrait tous les briefs visuels d'un fichier draft.
    Retourne une liste de dicts : {nom_image, brief_en, reseau, jour}
    """
    contenu = draft_path.read_text(encoding="utf-8")
    briefs = []

    # Cherche chaque section de post
    sections = re.split(r'\n## ', contenu)

    for section in sections:
        # Trouve le nom de l'image
        nom_match = re.search(r'\*\*Nom image\*\*\s*:\s*`([^`]+)`', section)
        if not nom_match:
            continue
        nom_image = nom_match.group(1)

        # Trouve le brief visuel (EN)
        brief_match = re.search(
            r'### Brief visuel \(EN\)\s*\n(.*?)(?=\n---|\n## |\Z)',
            section,
            re.DOTALL
        )
        if not brief_match:
            continue
        brief = brief_match.group(1).strip()

        # Extrait le réseau et le jour depuis le titre de section
        titre_match = re.match(r'([A-ZÉÀÂ]+\s+\d+\s+\w+)\s*[—-]\s*(\w+)', section)
        jour = titre_match.group(1).strip() if titre_match else "inconnu"
        reseau = titre_match.group(2).strip().lower() if titre_match else "inconnu"

        briefs.append({
            "nom_image": nom_image,
            "brief": brief,
            "jour": jour,
            "reseau": reseau
        })

    # Déduplique par nom d'image (garde le premier)
    vus = set()
    briefs_uniques = []
    for b in briefs:
        if b["nom_image"] not in vus:
            vus.add(b["nom_image"])
            briefs_uniques.append(b)

    return briefs_uniques


def generer_image_gemini(brief: str, nom_image: str, output_dir: Path) -> Path | None:
    """
    Génère une image via l'API Gemini (nouveau SDK google.genai).
    Retourne le chemin de l'image sauvegardée.
    """
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY non définie dans l'environnement")

    client = genai.Client(api_key=api_key)

    # Prompt enrichi avec les règles de la marque
    prompt_final = f"""Generate a professional social media image for Candidalib, a French driving school service in Toulouse.

Brand rules:
- Colors: deep blue gradient (#1e3a8a to #1e40af), white text
- Style: clean, minimal, professional
- NO emojis, NO emoticons in the image
- Text must be in French
- Always include "candidalib.fr" or "Candidalib" branding

Visual brief:
{brief}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-image",
        contents=prompt_final,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"]
        )
    )

    # Sauvegarde l'image
    output_dir.mkdir(parents=True, exist_ok=True)
    chemin_image = output_dir / nom_image

    for part in response.parts:
        if part.inline_data is not None:
            data = part.inline_data.data
            # Les données sont déjà en bytes bruts (JPEG/PNG)
            image_data = data if isinstance(data, bytes) else base64.b64decode(data)
            # Sauvegarde en .jpg si JPEG détecté
            if image_data[:2] == b'\xff\xd8':
                chemin_image = chemin_image.with_suffix('.jpg')
            chemin_image.write_bytes(image_data)
            return chemin_image

    return None


def generer_image_anthropic(brief: str, nom_image: str, output_dir: Path) -> Path | None:
    """
    Fallback : génère via l'API Anthropic (claude + description).
    Utilisé si Gemini n'est pas disponible.
    """
    # Anthropic ne génère pas d'images nativement — on log et on skip
    print(f"    [INFO] Génération image non disponible sans Gemini API — brief sauvegardé")
    return None


def run(mois: str, annee: int, semaine_num: int):
    """
    Point d'entrée de l'agent.

    Args:
        mois: ex "juillet"
        annee: ex 2026
        semaine_num: numéro de semaine (1-4)
    """
    print(f"\n{'='*50}")
    print(f"  AGENT DESIGNER — Candidalib")
    print(f"  Mois : {mois} {annee} | Semaine : {semaine_num}")
    print(f"{'='*50}\n")

    # Chemin du draft
    draft_path = DRAFTS_DIR / f"semaine{semaine_num}-{mois.lower()}{annee}.md"
    if not draft_path.exists():
        print(f"Draft introuvable : {draft_path}")
        print("Lance d'abord l'Agent Rédacteur.")
        return

    # Dossier de sortie des images
    output_dir = IMAGES_DIR / f"{mois.lower()}{annee}" / f"semaine{semaine_num}"

    # Extraction des briefs
    print(f"Lecture du draft : {draft_path.name}")
    briefs = extraire_briefs(draft_path)
    print(f"{len(briefs)} image(s) à générer\n")

    if not briefs:
        print("Aucun brief visuel trouvé dans le draft.")
        return

    # Génération des images
    images_generees = []
    images_skippees = []

    for i, item in enumerate(briefs, 1):
        print(f"[{i}/{len(briefs)}] {item['nom_image']} ({item['jour']} - {item['reseau']})")

        # Vérifie si l'image existe déjà
        chemin_existant = output_dir / item["nom_image"]
        if chemin_existant.exists():
            print(f"    Déjà générée — skip")
            images_skippees.append(item["nom_image"])
            continue

        try:
            chemin = generer_image_gemini(item["brief"], item["nom_image"], output_dir)
            if chemin:
                print(f"    Sauvegardée : {chemin.relative_to(BASE_DIR)}")
                images_generees.append(chemin)
            else:
                print(f"    Echec génération")
        except ImportError:
            print(f"    [ATTENTION] google-generativeai non installé")
            print(f"    Installe avec : pip3 install google-generativeai")
            break
        except Exception as e:
            print(f"    Erreur : {e}")

    # Résumé
    print(f"\n{'='*50}")
    print(f"  Généré : {len(images_generees)} image(s)")
    print(f"  Skippé : {len(images_skippees)} image(s)")
    print(f"  Dossier : outputs/images/{mois.lower()}{annee}/semaine{semaine_num}/")
    print(f"\n  Prochaine étape : validation manuelle puis publication")
    print(f"{'='*50}\n")

    return images_generees


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage : python3 agent.py [mois] [annee] [semaine]")
        print("Exemple : python3 agent.py juillet 2026 1")
        sys.exit(1)

    mois = sys.argv[1]
    annee = int(sys.argv[2])
    semaine = int(sys.argv[3])

    run(mois, annee, semaine)
