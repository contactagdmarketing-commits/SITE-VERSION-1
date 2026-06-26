"""
Agent CM Social — Candidalib
Rôle : Gère les interactions sociales de Candidalib
  - Lit les commentaires et DM en attente (depuis un fichier de simulation ou API Meta)
  - Génère des réponses adaptées via Claude (ton de marque, règles légales)
  - Génère des messages de demande d'avis Google
  - Sauvegarde les réponses dans outputs/cm/ pour validation manuelle avant envoi

Mode : simulation (fichier JSON) ou API Meta réelle (si token configuré)
"""

import anthropic
import json
import os
from datetime import datetime
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent.parent.parent
SKILLS_DIR = BASE_DIR / "skills"
CM_DIR = BASE_DIR / "outputs" / "cm"
CONFIG_DIR = BASE_DIR / "config"


def lire_skills() -> str:
    """Charge les skills pertinents pour le CM."""
    contenu = ""
    for skill_file in sorted(SKILLS_DIR.glob("*.md")):
        contenu += f"\n\n{'='*60}\n"
        contenu += f"SKILL : {skill_file.name}\n"
        contenu += f"{'='*60}\n"
        contenu += skill_file.read_text(encoding="utf-8")
    return contenu


def lire_interactions(source: str = "simulation") -> list[dict]:
    """
    Charge les interactions à traiter.
    - source="simulation" : lit le fichier interactions-sample.json
    - source="meta" : appel API Meta (nécessite token)
    """
    if source == "simulation":
        sample_file = Path(__file__).parent / "interactions-sample.json"
        if sample_file.exists():
            return json.loads(sample_file.read_text(encoding="utf-8"))
        else:
            print("Fichier interactions-sample.json introuvable.")
            print("Lance : python3 agent.py --generer-sample")
            return []

    elif source == "meta":
        token = os.environ.get("META_ACCESS_TOKEN")
        page_id = os.environ.get("META_PAGE_ID")
        if not token or not page_id:
            raise ValueError(
                "META_ACCESS_TOKEN et META_PAGE_ID requis dans .env\n"
                "Génère un token sur : https://developers.facebook.com/"
            )
        return _fetch_meta_interactions(token, page_id)

    return []


def _fetch_meta_interactions(token: str, page_id: str) -> list[dict]:
    """Récupère commentaires et messages via l'API Meta Graph."""
    import httpx
    interactions = []

    # Commentaires sur les posts Facebook/Instagram récents
    url_comments = (
        f"https://graph.facebook.com/v19.0/{page_id}/feed"
        f"?fields=id,message,comments{{id,message,from,created_time}}"
        f"&access_token={token}"
    )
    try:
        r = httpx.get(url_comments, timeout=10)
        data = r.json()
        for post in data.get("data", []):
            for comment in post.get("comments", {}).get("data", []):
                interactions.append({
                    "id": comment["id"],
                    "type": "commentaire_facebook",
                    "plateforme": "facebook",
                    "auteur": comment.get("from", {}).get("name", "Anonyme"),
                    "message": comment["message"],
                    "date": comment["created_time"],
                    "post_id": post["id"]
                })
    except Exception as e:
        print(f"  [WARN] Erreur fetch commentaires Facebook : {e}")

    # Messages privés (Messenger)
    url_messages = (
        f"https://graph.facebook.com/v19.0/{page_id}/conversations"
        f"?fields=messages{{message,from,created_time}}"
        f"&access_token={token}"
    )
    try:
        r = httpx.get(url_messages, timeout=10)
        data = r.json()
        for conv in data.get("data", []):
            for msg in conv.get("messages", {}).get("data", []):
                if msg.get("from", {}).get("id") != page_id:
                    interactions.append({
                        "id": msg.get("id", ""),
                        "type": "message_prive",
                        "plateforme": "messenger",
                        "auteur": msg.get("from", {}).get("name", "Anonyme"),
                        "message": msg["message"],
                        "date": msg["created_time"]
                    })
    except Exception as e:
        print(f"  [WARN] Erreur fetch messages Messenger : {e}")

    return interactions


def generer_reponses(interactions: list[dict], skills: str) -> list[dict]:
    """Génère une réponse pour chaque interaction via Claude."""
    client = anthropic.Anthropic()
    resultats = []

    for i, interaction in enumerate(interactions, 1):
        print(f"  [{i}/{len(interactions)}] {interaction['type']} de {interaction['auteur']}")

        prompt = f"""Tu es l'Agent CM de Candidalib. Tu dois répondre à une interaction sur les réseaux sociaux.

RÈGLES DE LA MARQUE (skills) :
{skills}

INTERACTION À TRAITER :
- Plateforme : {interaction['plateforme']}
- Type : {interaction['type']}
- Auteur : {interaction['auteur']}
- Message : {interaction['message']}
- Date : {interaction.get('date', 'inconnue')}

TA MISSION :
Rédige une réponse adaptée en respectant :
1. Le ton Candidalib (direct, rassurant, professionnel)
2. Le profil probable de l'auteur (jeune candidat libre ou parent ?)
3. Règles légales strictes : ne JAMAIS dire "formation", "moniteur", "cours de conduite"
4. Maximum 3-4 phrases pour un commentaire, 5-6 pour un message privé
5. Finir par un appel à l'action si pertinent (lien site, numéro de téléphone)
6. ZÉRO emoji dans la réponse
7. Si l'interaction est négative ou agressive : réponse calme, empathique, proposer de continuer en privé

RÉPONSE (texte uniquement, prête à copier-coller) :"""

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )

        reponse = message.content[0].text.strip()

        resultats.append({
            **interaction,
            "reponse_suggeree": reponse,
            "statut": "en_attente_validation",
            "genere_le": datetime.now().isoformat()
        })

        print(f"     Reponse generee ({len(reponse)} caracteres)")

    return resultats


def generer_demandes_avis(nb: int = 3) -> list[dict]:
    """
    Génère des messages types pour demander des avis Google
    à envoyer après une session d'accompagnement.
    """
    client = anthropic.Anthropic()
    skills = lire_skills()

    prompt = f"""Tu es l'Agent CM de Candidalib. Génère {nb} variantes de message pour demander un avis Google à un client qui vient de terminer une session d'accompagnement avec Candidalib.

RÈGLES :
{skills}

CONTRAINTES :
- Ton chaleureux mais professionnel
- Court : 3-4 phrases maximum
- Inclure le lien Google : https://g.page/r/candidalib/review (placeholder)
- ZÉRO emoji
- Ne pas être insistant ni donner l'impression de "forcer"
- Rappeler brièvement la valeur apportée

Produis {nb} variantes numérotées, chacune avec un ton légèrement différent (neutre / enthousiaste / reconnaissant).
Format : chaque variante séparée par ---"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    texte = message.content[0].text.strip()
    variantes = [v.strip() for v in texte.split("---") if v.strip()]

    return [
        {
            "type": "demande_avis_google",
            "variante": i + 1,
            "message": v,
            "statut": "en_attente_validation",
            "genere_le": datetime.now().isoformat()
        }
        for i, v in enumerate(variantes)
    ]


def sauvegarder(resultats: list[dict], nom_fichier: str):
    """Sauvegarde les résultats en JSON + Markdown lisible."""
    CM_DIR.mkdir(parents=True, exist_ok=True)

    # JSON brut (pour intégration future)
    chemin_json = CM_DIR / f"{nom_fichier}.json"
    chemin_json.write_text(
        json.dumps(resultats, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # Markdown lisible pour validation manuelle
    chemin_md = CM_DIR / f"{nom_fichier}.md"
    lignes = [
        f"# Rapport CM — {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
        f"*{len(resultats)} interaction(s) traitée(s)*\n",
        "---\n"
    ]

    for item in resultats:
        if item["type"] == "demande_avis_google":
            lignes.append(f"## Demande d'avis Google — Variante {item['variante']}")
            lignes.append(f"\n{item['message']}\n")
        else:
            lignes.append(f"## {item['type'].replace('_', ' ').title()} — {item['auteur']}")
            lignes.append(f"**Plateforme** : {item['plateforme']}")
            lignes.append(f"**Message recu** : {item['message']}")
            lignes.append(f"\n**Reponse suggeree** :\n> {item['reponse_suggeree']}\n")
            lignes.append(f"*Statut : {item['statut']}*")
        lignes.append("\n---\n")

    chemin_md.write_text("\n".join(lignes), encoding="utf-8")

    print(f"\n  Sauvegarde : {chemin_json.relative_to(BASE_DIR)}")
    print(f"  Sauvegarde : {chemin_md.relative_to(BASE_DIR)}")


def generer_sample():
    """Génère un fichier d'interactions de test."""
    sample = [
        {
            "id": "cmnt_001",
            "type": "commentaire_facebook",
            "plateforme": "facebook",
            "auteur": "Lucas Martin",
            "message": "Bonjour, c'est quoi exactement la différence avec une auto-école classique ?",
            "date": "2026-06-08T10:23:00"
        },
        {
            "id": "cmnt_002",
            "type": "commentaire_instagram",
            "plateforme": "instagram",
            "auteur": "amelie_toulouse31",
            "message": "J'ai passé mon permis avec vous en mars, merci beaucoup ! Je le recommande a tout le monde",
            "date": "2026-06-08T14:05:00"
        },
        {
            "id": "msg_001",
            "type": "message_prive",
            "plateforme": "messenger",
            "auteur": "Marie Dupont",
            "message": "Bonjour, mon fils a 18 ans et vient d'avoir son NEPH. Il a validé le code il y a 2 mois. Est-ce que vous pouvez l'aider pour la pratique ? Quels sont vos tarifs ?",
            "date": "2026-06-08T09:10:00"
        },
        {
            "id": "cmnt_003",
            "type": "commentaire_instagram",
            "plateforme": "instagram",
            "auteur": "kevin_permis",
            "message": "C'est nul, j'ai raté mon examen après 5h avec vous...",
            "date": "2026-06-07T18:42:00"
        }
    ]

    chemin = Path(__file__).parent / "interactions-sample.json"
    chemin.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fichier sample genere : {chemin}")
    return chemin


def run(mode: str = "simulation", action: str = "repondre"):
    """
    Point d'entrée de l'agent.

    Args:
        mode: "simulation" (fichier JSON) ou "meta" (API réelle)
        action: "repondre" | "avis" | "tout"
    """
    print(f"\n{'='*50}")
    print(f"  AGENT CM SOCIAL — Candidalib")
    print(f"  Mode : {mode} | Action : {action}")
    print(f"{'='*50}\n")

    skills = lire_skills()
    horodatage = datetime.now().strftime("%Y%m%d-%H%M")
    tous_resultats = []

    if action in ("repondre", "tout"):
        print("Chargement des interactions...")
        interactions = lire_interactions(mode)
        print(f"{len(interactions)} interaction(s) a traiter\n")

        if interactions:
            print("Generation des reponses...")
            reponses = generer_reponses(interactions, skills)
            tous_resultats.extend(reponses)

    if action in ("avis", "tout"):
        print("\nGeneration des demandes d'avis Google...")
        avis = generer_demandes_avis(nb=3)
        tous_resultats.extend(avis)
        print(f"  {len(avis)} variante(s) generee(s)")

    if tous_resultats:
        sauvegarder(tous_resultats, f"rapport-cm-{horodatage}")

    print(f"\n{'='*50}")
    print(f"  {len(tous_resultats)} element(s) genere(s)")
    print(f"  Dossier : outputs/cm/")
    print(f"  Valide les reponses avant envoi manuel ou auto")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    if "--generer-sample" in args:
        generer_sample()
        sys.exit(0)

    mode = "simulation"
    action = "tout"

    for arg in args:
        if arg in ("simulation", "meta"):
            mode = arg
        if arg in ("repondre", "avis", "tout"):
            action = arg

    run(mode, action)
