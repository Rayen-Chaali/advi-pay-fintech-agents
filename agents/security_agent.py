import datetime
from database import CATALOGUE_FICTIF

def generer_alerte(id_alerte, type_alerte, gravite, dossier_id, fait_observe, regle, decision):
    return {
        "id": id_alerte,
        "type": type_alerte,
        "gravite": gravite,
        "dossier_id": dossier_id,
        "fait_observe": fait_observe,
        "regle_declenchee": regle,
        "decision": decision,
        "heure_creation": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def evaluer_securite(dossier, message_client):
    alertes = []
    decision_finale = "autorisée"
    
    texte_lower = message_client.lower()

    # RÈGLE 1 : Scénario préparé - Attaque Contrôlée (Démo Hackathon)
    # Remarque : Ceci est un scénario préparé pour la démo, pas un détecteur universel de prompt injection.
    if "ignore les règles" in texte_lower and "change le prix" in texte_lower:
        alertes.append(generer_alerte(
            id_alerte="SEC-001",
            type_alerte="Tentative d'Injection de Prompt (Démo)",
            gravite="HAUTE",
            dossier_id=dossier["id_client"],
            fait_observe="Demande explicite d'ignorer les règles et de modifier le prix du catalogue.",
            regle="Règle d'intégrité : Le prix du catalogue est immuable et ne peut être altéré par la saisie utilisateur.",
            decision="bloquée"
        ))
        decision_finale = "bloquée"

    # RÈGLE 2 : Transition d'état interdite (Saut d'étape)
    if "valide le paiement" in texte_lower and dossier["statut_dossier"] == "NOUVEAU":
        alertes.append(generer_alerte(
            id_alerte="SEC-002",
            type_alerte="Saut d'étape obligatoire",
            gravite="MOYENNE",
            dossier_id=dossier["id_client"],
            fait_observe="Tentative de validation de paiement dès le premier message.",
            regle="Séquence stricte : NOUVEAU -> ATTENTE_VALIDATION_HUMAINE. Le passage direct au paiement est interdit.",
            decision="bloquée"
        ))
        decision_finale = "bloquée"

    # RÈGLE 3 : Vérification (simulée) de l'intégrité de l'offre
    offre_proposee = dossier["ajouts_agents"].get("Voice_Sales", {}).get("offre_proposee")
    if offre_proposee:
        if offre_proposee not in CATALOGUE_FICTIF:
            alertes.append(generer_alerte("SEC-003", "Offre Invalide", "HAUTE", dossier["id_client"], "L'offre proposée n'existe pas.", "Intégrité Catalogue", "bloquée"))
            decision_finale = "bloquée"

    return alertes, decision_finale