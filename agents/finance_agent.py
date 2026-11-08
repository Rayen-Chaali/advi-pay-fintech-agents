# agents/finance_agent.py

def calculer_metriques(liste_dossiers):
    """
    Calcule les indicateurs financiers de manière déterministe (sans LLM).
    """
    interactions = len(liste_dossiers)
    prospects_interesses = 0
    paiements_reussis = 0
    paiements_refuses = 0
    paiements_attente = 0
    revenus_simules = 0.0
    objections = []

    for dossier in liste_dossiers:
        # 1. Analyse des intérêts et objections
        intel = dossier.get("ajouts_agents", {}).get("Customer_Intelligence", {})
        if intel:
            if intel.get("interest") in ["High", "Élevé", "Moyen"]:
                prospects_interesses += 1
            if intel.get("objections"):
                objections.append(intel.get("objections"))

        # 2. Analyse des paiements
        paiement = dossier.get("ajouts_agents", {}).get("Payment_Agent", {})
        if paiement:
            statut = paiement.get("statut_paiement")
            if statut == "RÉUSSI":
                paiements_reussis += 1
                revenus_simules += paiement.get("montant_traite", 0.0)
            elif statut == "REFUSÉ":
                paiements_refuses += 1
            elif statut == "EN_ATTENTE":
                paiements_attente += 1

    # 3. Calcul du taux de conversion
    taux_conversion = (paiements_reussis / interactions * 100) if interactions > 0 else 0.0
    formule = f"Taux de conversion = ({paiements_reussis} Paiements Réussis / {interactions} Total Interactions) * 100"

    return {
        "interactions": interactions,
        "prospects_interesses": prospects_interesses,
        "taux_conversion_pourcentage": round(taux_conversion, 2),
        "formule_conversion": formule,
        "paiements": {
            "reussis": paiements_reussis,
            "refuses": paiements_refuses,
            "en_attente": paiements_attente
        },
        "revenus_simules": revenus_simules,
        "objections_recueillies": objections
    }