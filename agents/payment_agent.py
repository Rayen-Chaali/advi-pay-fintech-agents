from database import journaliser_evenement

def simuler_paiement(dossier):
    approbation = dossier.get("approbation_humaine", {})
    if not approbation.get("approuve"):
        return {"statut_paiement": "REFUSÉ_NON_APPROUVÉ", "montant_traite": 0.0}

    prix = approbation.get("prix_approuve", 0.0)
    solde = dossier.get("solde_client", 0.0)
    
    journaliser_evenement("TENTATIVE_PAIEMENT", f"Montant requis : {prix} TND | Solde client : {solde} TND")

    # VÉRIFICATION DU SOLDE (La logique métier reste 100% en Python, hors de portée de l'IA)
    if solde < prix:
        journaliser_evenement("ECHEC_PAIEMENT", "Fonds insuffisants.")
        return {
            "statut_paiement": "REFUSÉ_SOLDE_INSUFFISANT",
            "montant_traite": 0.0,
            "raison": "Votre solde est insuffisant pour finaliser cette transaction."
        }

    # Simulation réussite
    dossier["solde_client"] -= prix
    journaliser_evenement("PAIEMENT_REUSSI", f"Montant traité: {prix} TND. Nouveau solde: {dossier['solde_client']} TND.")
    
    return {
        "statut_paiement": "RÉUSSI",
        "montant_traite": prix,
        "nouveau_solde": dossier["solde_client"]
    }