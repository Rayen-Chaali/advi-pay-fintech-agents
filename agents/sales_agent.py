import json
import os
import google.generativeai as genai
from database import CATALOGUE_FICTIF, journaliser_evenement

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

CATALOGUE_STR = json.dumps(CATALOGUE_FICTIF, ensure_ascii=False)
PROMPT = f"""Tu es conseiller. Catalogue: {CATALOGUE_STR}. 
Analyse le besoin du client et propose la formation la plus adaptée. 
Retourne uniquement un objet JSON pur (sans balises markdown) avec: reply (ta réponse), intent (inquiry ou purchase_intent), offer_id (ID de l'offre, ex: FORM-CYBER)."""

def simuler_appel_api_llm(message_client):
    print(f"➡️ Envoi à Gemini : {message_client}")
    try:
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
        resp = model.generate_content(
            f"{PROMPT}\nMessage: {message_client}", 
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Nettoyage robuste pour éviter les plantages si Gemini renvoie du Markdown
        texte_brut = resp.text.strip()
        if texte_brut.startswith("```"):
            # On retire les balises ```json et ```
            texte_brut = texte_brut.strip("`").replace("json\n", "", 1).strip()
            
        print("✅ Réponse traitée avec succès !")
        return json.loads(texte_brut)
        
    except Exception as e:
        print(f"❌ Erreur API (Quota/Réseau) : {e}")
        journaliser_evenement("ERREUR_LLM", f"Bascule sur le système de secours local. Erreur: {str(e)}")
        
        # Mode de secours intelligent (sans IA) pour sauver la démo
        texte_min = message_client.lower()
        if "llm" in texte_min:
            return {"reply": "Très bon choix. Souhaitez-vous valider la formation 'Maîtrise des LLMs' à 2500 TND ?", "intent": "inquiry", "offer_id": "FORM-LLM"}
        elif "cyber" in texte_min:
            return {"reply": "Excellent. Souhaitez-vous valider 'Cybersécurité & Défense' à 3200 TND ?", "intent": "inquiry", "offer_id": "FORM-CYBER"}
        elif "machine" in texte_min or "ml" in texte_min:
            return {"reply": "Parfait. Souhaitez-vous valider 'Machine Learning Avancé' à 2950 TND ?", "intent": "inquiry", "offer_id": "FORM-ML"}
        elif "deep" in texte_min or "dl" in texte_min:
            return {"reply": "Je vous propose 'Deep Learning & Vision' à 3100 TND. Confirmez-vous ?", "intent": "inquiry", "offer_id": "FORM-DL"}
        
        # Par défaut si aucun mot clé n'est trouvé
        return {
            "reply": "D'après votre demande, je recommande notre 'Bootcamp Agentic AI' à 2890 TND. Souhaitez-vous valider cette offre ?",
            "intent": "inquiry",
            "offer_id": "FORM-IA-PRO"
        }

def generer_reponse_commerciale(message):
    return simuler_appel_api_llm(message)