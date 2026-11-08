from database import journaliser_evenement, CATALOGUE_FICTIF
from agents.sales_agent import generer_reponse_commerciale
from agents.intelligence_agent import analyser_intentions
from agents.security_agent import evaluer_securite

def traiter_message_client(message, dossier):
    dossier["message_original"] = message
    texte_min = message.lower()
    
    # 1. CONTRÔLE DE SÉCURITÉ IMMÉDIAT
    alertes, decision_securite = evaluer_securite(dossier, message)
    dossier["decision_securite"] = decision_securite
    
    if "alertes" not in dossier:
        dossier["alertes"] = []
    dossier["alertes"].extend(alertes)
    
    if decision_securite == "bloquée":
        dossier["statut_dossier"] = "ALERTE_SECURITE_BLOQUEE"
        journaliser_evenement("BLOCAGE_SECURITE", f"Demande bloquée (ID: {dossier['id_client']})")
        return dossier

    # NOUVEAUTÉ : Demande explicite du catalogue
    if any(mot in texte_min for mot in ["catalogue", "formations", "prix", "liste", "proposez"]):
        catalogue_texte = "Voici notre catalogue de formations :\n"
        for code, details in CATALOGUE_FICTIF.items():
            catalogue_texte += f"- **{details['nom']}** : {details['prix']} TND\n"
        
        dossier["ajouts_agents"]["Voice_Sales"] = {
            "reply": catalogue_texte + "\nLaquelle de ces formations vous intéresse ?",
            "intent": "inquiry",
            "offer_id": None
        }
        dossier["statut_dossier"] = "ATTENTE_CONFIRMATION_CLIENT"
        journaliser_evenement("INFO", "Affichage manuel du catalogue demandé par le client.")
        return dossier

    # 2. ÉTAPE : Attente de la réponse explicite du client
    if dossier["statut_dossier"] == "ATTENTE_CONFIRMATION_CLIENT":
        if any(mot in texte_min for mot in ["oui", "ok", "accepte", "d'accord", "je veux"]):
            dossier["client_confirme"] = True
            dossier["statut_dossier"] = "ATTENTE_VALIDATION_HUMAINE"
            journaliser_evenement("CONFIRMATION_CLIENT", "Le client a explicitement confirmé l'offre.")
            return dossier
        else:
            # CORRECTION : Si ce n'est pas un "oui", on repasse en mode NOUVEAU pour que Gemini réponde à la question
            dossier["statut_dossier"] = "NOUVEAU"

    # 3. ÉTAPE : Nouveau Client ou suite de la discussion (Appel Gemini)
    if dossier["statut_dossier"] == "NOUVEAU":
        resultat_sales = generer_reponse_commerciale(message)
        dossier["ajouts_agents"]["Voice_Sales"] = resultat_sales
        
        reponse_ia = resultat_sales.get("reply", "")
        
        # Sécurisation de l'appel à l'agent d'intelligence (si présent)
        try:
            resultat_intel = analyser_intentions(message, reponse_ia)
            dossier["ajouts_agents"]["Customer_Intelligence"] = resultat_intel
        except Exception as e:
            journaliser_evenement("ERREUR_INTEL", str(e))
        
        dossier["statut_dossier"] = "ATTENTE_CONFIRMATION_CLIENT"
        journaliser_evenement("CHANGEMENT_STATUT", "Passage à ATTENTE_CONFIRMATION_CLIENT")
    
    return dossier