# Configuration du suivi de trafic — Candidalib

Tout est installé et fonctionne. Il reste **4 valeurs à remplacer** quand tes comptes sont créés.
Tant qu'elles ne sont pas remplies, le site fonctionne normalement — les outils restent simplement désactivés.

---

## 1. Les 3 IDs de suivi → fichier `tracking.js` (tout en haut)

```js
const CANDIDALIB_TRACKING = {
  GA4_ID:        "G-XXXXXXXXXX",   // ← Google Analytics 4
  CLARITY_ID:    "XXXXXXXXXX",     // ← Microsoft Clarity
  META_PIXEL_ID: "XXXXXXXXXX"      // ← Meta Pixel
};
```

| Valeur | Où la créer (gratuit) | Format attendu |
|---|---|---|
| `GA4_ID` | https://analytics.google.com | `G-A1B2C3D4E5` |
| `CLARITY_ID` | https://clarity.microsoft.com | suite de chiffres/lettres |
| `META_PIXEL_ID` | Meta Business Manager → Pixel | suite de chiffres |

> Ne me donne JAMAIS tes mots de passe. Seulement ces identifiants publics.

---

## 2. La clé du formulaire « Être rappelé » → fichier `contact.html`

Cherche `VOTRE_CLE_WEB3FORMS` et remplace-la.

```html
<input type="hidden" name="access_key" value="VOTRE_CLE_WEB3FORMS">
```

- Va sur https://web3forms.com (gratuit, pas de compte requis)
- Saisis l'email où tu veux **recevoir les demandes de rappel**
- Web3Forms t'envoie une clé d'accès → colle-la à la place de `VOTRE_CLE_WEB3FORMS`

---

## Ce qui marche DÉJÀ, sans rien configurer

- ✅ Le bandeau de consentement cookies (RGPD) s'affiche sur toutes les pages
- ✅ Le bouton « Appeler » fonctionne partout (lien `tel:`)
- ✅ Le formulaire « Être rappelé » est en ligne (il enverra les leads une fois la clé Web3Forms posée)
- ✅ Le suivi des clics « Appeler » est prêt (il enverra les données une fois les IDs posés)

## Ce que tu auras APRÈS configuration

| Outil | Ce que tu verras |
|---|---|
| **Microsoft Clarity** | Enregistrements vidéo des visites : qui clique où, combien de temps il reste, où il abandonne |
| **Google Analytics 4** | D'où viennent les visiteurs (pub, Insta, Google), combien, quelles pages |
| **Meta Pixel** | Quelle pub a généré la visite, le clic « Appeler » et la demande de rappel |

---

## À ne pas oublier (légal)

Ta page `confidentialite.html` doit mentionner l'usage de Google Analytics, Microsoft Clarity et Meta Pixel
(obligation RGPD). Demande-moi de l'ajouter quand tu veux — c'est une mise à jour de 5 minutes.
