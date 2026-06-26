"""
Orchestrateur — Candidalib
Lance toute la chaîne de production de contenu en une seule commande.

Chaîne complète :
  1. Agent Stratège   → génère le calendrier mensuel
  2. Agent Rédacteur  → rédige les posts par semaine
  3. Agent Designer   → génère les images pour chaque post
  4. Agent CM Social  → génère les réponses aux interactions + demandes d'avis

Usage :
  python3 orchestrateur.py juillet 2026               → chaîne complète
  python3 orchestrateur.py juillet 2026 --semaines 1,2 → semaines spécifiques
  python3 orchestrateur.py juillet 2026 --etape stratege
  python3 orchestrateur.py juillet 2026 --etape redacteur --semaines 1
  python3 orchestrateur.py juillet 2026 --etape designer --semaines 1
  python3 orchestrateur.py --etape cm
  python3 orchestrateur.py --status                   → état du projet
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Ajoute les agents au path
sys.path.insert(0, str(BASE_DIR / "agents" / "stratege"))
sys.path.insert(0, str(BASE_DIR / "agents" / "redacteur"))
sys.path.insert(0, str(BASE_DIR / "agents" / "designer"))
sys.path.insert(0, str(BASE_DIR / "agents" / "community-manager"))

ETAPES = ["stratege", "redacteur", "designer", "cm"]

LOG_DIR = BASE_DIR / "outputs" / "logs"


def log(message: str, niveau: str = "INFO"):
    """Affiche et sauvegarde un log."""
    horodatage = datetime.now().strftime("%H:%M:%S")
    prefixes = {"INFO": "  ", "OK": "✓ ", "WARN": "! ", "ERR": "✗ ", "TITRE": ""}
    prefixe = prefixes.get(niveau, "  ")
    print(f"[{horodatage}] {prefixe}{message}")


def separateur(titre: str = ""):
    largeur = 52
    print(f"\n{'='*largeur}")
    if titre:
        print(f"  {titre}")
        print(f"{'='*largeur}")


def afficher_status(mois: str = None, annee: int = None):
    """Affiche l'état du projet : fichiers générés, manquants."""
    separateur("STATUS DU PROJET — Candidalib CM")

    drafts_dir = BASE_DIR / "outputs" / "drafts"
    images_dir = BASE_DIR / "outputs" / "images"
    cm_dir = BASE_DIR / "outputs" / "cm"

    # Calendriers
    calendriers = list(drafts_dir.glob("calendrier-*.md")) if drafts_dir.exists() else []
    log(f"Calendriers generes : {len(calendriers)}", "INFO")
    for c in calendriers:
        log(f"  - {c.name}", "OK")

    # Drafts
    drafts = list(drafts_dir.glob("semaine*.md")) if drafts_dir.exists() else []
    log(f"Drafts rediges : {len(drafts)}", "INFO")
    for d in sorted(drafts):
        log(f"  - {d.name}", "OK")

    # Images
    total_images = 0
    if images_dir.exists():
        for f in images_dir.rglob("*.jpg"):
            total_images += 1
        for f in images_dir.rglob("*.png"):
            total_images += 1
    log(f"Images generees : {total_images}", "INFO")

    # Rapports CM
    rapports = list(cm_dir.glob("rapport-cm-*.md")) if cm_dir.exists() else []
    log(f"Rapports CM : {len(rapports)}", "INFO")

    # Si mois/annee fournis : détail semaines
    if mois and annee:
        separateur(f"Semaines {mois.capitalize()} {annee}")
        for sem in range(1, 5):
            draft = drafts_dir / f"semaine{sem}-{mois.lower()}{annee}.md"
            img_dir = images_dir / f"{mois.lower()}{annee}" / f"semaine{sem}"
            nb_imgs = len(list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))) if img_dir.exists() else 0
            statut_draft = "OK" if draft.exists() else "WARN"
            log(f"Semaine {sem} : draft={'oui' if draft.exists() else 'non'} | images={nb_imgs}", statut_draft)

    print()


def run_stratege(mois: str, annee: int, events: str = ""):
    """Lance l'Agent Stratège."""
    separateur(f"ETAPE 1 — Agent Stratege")
    log(f"Mois cible : {mois.capitalize()} {annee}")

    # Vérifie si le calendrier existe déjà
    calendrier = BASE_DIR / "outputs" / "drafts" / f"calendrier-{mois.lower()}{annee}.md"
    if calendrier.exists():
        log(f"Calendrier deja present : {calendrier.name} — skip", "OK")
        return True

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "stratege",
            BASE_DIR / "agents" / "stratege" / "agent.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.run(mois, annee, events)
        log("Calendrier genere avec succes", "OK")
        return True
    except Exception as e:
        log(f"Erreur Agent Stratege : {e}", "ERR")
        return False


def run_redacteur(mois: str, annee: int, semaines: list[int]):
    """Lance l'Agent Rédacteur pour les semaines demandées."""
    separateur(f"ETAPE 2 — Agent Redacteur")
    log(f"Semaines : {semaines}")

    # Filtre les semaines déjà rédigées
    semaines_a_faire = []
    for s in semaines:
        draft = BASE_DIR / "outputs" / "drafts" / f"semaine{s}-{mois.lower()}{annee}.md"
        if draft.exists():
            log(f"Semaine {s} deja redigee — skip", "OK")
        else:
            semaines_a_faire.append(s)

    if not semaines_a_faire:
        log("Toutes les semaines sont deja redigees", "OK")
        return True

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "redacteur",
            BASE_DIR / "agents" / "redacteur" / "agent.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.run(mois, annee, semaines_a_faire)
        log(f"{len(semaines_a_faire)} semaine(s) redigee(s)", "OK")
        return True
    except Exception as e:
        log(f"Erreur Agent Redacteur : {e}", "ERR")
        return False


def run_designer(mois: str, annee: int, semaines: list[int]):
    """Lance l'Agent Designer pour les semaines demandées."""
    separateur(f"ETAPE 3 — Agent Designer")
    log(f"Semaines : {semaines}")

    succes = 0
    for s in semaines:
        log(f"Semaine {s}...")
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "designer",
                BASE_DIR / "agents" / "designer" / "agent.py"
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            images = mod.run(mois, annee, s)
            nb = len(images) if images else 0
            log(f"Semaine {s} : {nb} image(s) generee(s)", "OK")
            succes += 1
        except Exception as e:
            log(f"Erreur semaine {s} : {e}", "ERR")

    return succes == len(semaines)


def run_cm(mode: str = "simulation"):
    """Lance l'Agent CM Social."""
    separateur("ETAPE 4 — Agent CM Social")
    log(f"Mode : {mode}")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "cm",
            BASE_DIR / "agents" / "community-manager" / "agent.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.run(mode, "tout")
        log("Rapport CM genere", "OK")
        return True
    except Exception as e:
        log(f"Erreur Agent CM : {e}", "ERR")
        return False


def run_complet(mois: str, annee: int, semaines: list[int], events: str = "", cm_mode: str = "simulation"):
    """Lance la chaîne complète."""
    debut = datetime.now()

    separateur(f"ORCHESTRATEUR CANDIDALIB — {mois.upper()} {annee}")
    log(f"Semaines : {semaines}")
    log(f"Debut : {debut.strftime('%d/%m/%Y a %H:%M')}")

    resultats = {}

    # 1. Stratège
    resultats["stratege"] = run_stratege(mois, annee, events)
    if not resultats["stratege"]:
        log("Arret : echec Agent Stratege", "ERR")
        return resultats

    # 2. Rédacteur
    resultats["redacteur"] = run_redacteur(mois, annee, semaines)
    if not resultats["redacteur"]:
        log("Arret : echec Agent Redacteur", "ERR")
        return resultats

    # 3. Designer
    resultats["designer"] = run_designer(mois, annee, semaines)

    # 4. CM (ne bloque pas la chaîne si échec)
    resultats["cm"] = run_cm(cm_mode)

    # Bilan
    duree = (datetime.now() - debut).seconds
    separateur("BILAN FINAL")
    for etape, ok in resultats.items():
        niveau = "OK" if ok else "ERR"
        log(f"{etape.capitalize()} : {'OK' if ok else 'ECHEC'}", niveau)
    log(f"Duree totale : {duree}s")
    log(f"Outputs : agents-cm/outputs/")
    print()

    # Sauvegarde du log
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"run-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    log_file.write_text(
        json.dumps({
            "mois": mois,
            "annee": annee,
            "semaines": semaines,
            "resultats": resultats,
            "duree_secondes": duree,
            "timestamp": debut.isoformat()
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return resultats


def parse_args(args: list[str]) -> dict:
    """Parse les arguments CLI."""
    params = {
        "mois": None,
        "annee": None,
        "semaines": [1, 2, 3, 4],
        "etape": None,
        "events": "",
        "cm_mode": "simulation",
        "status": False
    }

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--status":
            params["status"] = True
        elif arg == "--semaines" and i + 1 < len(args):
            params["semaines"] = [int(s) for s in args[i + 1].split(",")]
            i += 1
        elif arg == "--etape" and i + 1 < len(args):
            params["etape"] = args[i + 1]
            i += 1
        elif arg == "--events" and i + 1 < len(args):
            params["events"] = args[i + 1]
            i += 1
        elif arg == "--cm-mode" and i + 1 < len(args):
            params["cm_mode"] = args[i + 1]
            i += 1
        elif params["mois"] is None and not arg.startswith("--"):
            params["mois"] = arg
        elif params["annee"] is None and not arg.startswith("--"):
            try:
                params["annee"] = int(arg)
            except ValueError:
                pass
        i += 1

    return params


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    # Affichage du status seul
    if args["status"]:
        afficher_status(args["mois"], args["annee"])
        sys.exit(0)

    # Vérification des paramètres obligatoires (sauf pour CM seul)
    if args["etape"] != "cm" and (not args["mois"] or not args["annee"]):
        print("\nUsage :")
        print("  python3 orchestrateur.py juillet 2026")
        print("  python3 orchestrateur.py juillet 2026 --semaines 1,2")
        print("  python3 orchestrateur.py juillet 2026 --etape stratege")
        print("  python3 orchestrateur.py juillet 2026 --etape redacteur --semaines 1")
        print("  python3 orchestrateur.py juillet 2026 --etape designer --semaines 1")
        print("  python3 orchestrateur.py --etape cm")
        print("  python3 orchestrateur.py --status")
        sys.exit(1)

    # Lancement d'une étape spécifique
    if args["etape"]:
        etape = args["etape"]
        if etape == "stratege":
            run_stratege(args["mois"], args["annee"], args["events"])
        elif etape == "redacteur":
            run_redacteur(args["mois"], args["annee"], args["semaines"])
        elif etape == "designer":
            run_designer(args["mois"], args["annee"], args["semaines"])
        elif etape == "cm":
            run_cm(args["cm_mode"])
        else:
            print(f"Etape inconnue : {etape}")
            print(f"Etapes disponibles : {', '.join(ETAPES)}")
            sys.exit(1)
    else:
        # Chaîne complète
        run_complet(
            args["mois"],
            args["annee"],
            args["semaines"],
            args["events"],
            args["cm_mode"]
        )
