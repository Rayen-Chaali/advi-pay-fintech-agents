import json
import os
import google.generativeai as genai
from database import journaliser_evenement

def generer_recommandations(metriques):
    try:
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
        # Le prompt est maintenant orienté B2C / Client
        prompt = f"""Tu es un conseiller financier et stratégique pour nos clients.
        Analyse ce dossier client : {json.dumps(metriques)}.
        Propose 3 recommandations pour l'aider à optimiser son budget de formation, maximiser son retour sur investissement d'apprentissage, et gérer son solde.
        Format attendu STRICTEMENT en JSON : {{"recommendations": [{{"observation": "...", "action_suggeree": "...", "indicateur_a_suivre": "..."}}]}}"""
        
        resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        
        texte_brut = resp.text.strip()
        if texte_brut.startswith("```"):
            texte_brut = texte_brut.strip("`").replace("json\n", "", 1).strip()
            
        return json.loads(texte_brut)
        
    except Exception as e:
        journaliser_evenement("ERREUR_STRATEGIE", str(e))
        # Recommandations de secours orientées client si l'API est en panne de quota
        return {
            "recommendations": [
                {
                    "observation": "Solde disponible pour de futures formations.",
                    "action_suggeree": "Envisager un bundle avec des certifications complémentaires.",
                    "indicateur_a_suivre": "Budget restant"
                },
                {
                    "observation": "Engagement sur un parcours technique.",
                    "action_suggeree": "Rejoindre notre communauté d'alumni pour networker.",
                    "indicateur_a_suivre": "Taux de complétion"
                },
                {
                    "observation": "Besoin de maîtrise pratique.",
                    "action_suggeree": "Pratiquer sur des projets réels (Kaggle, GitHub) en parallèle.",
                    "indicateur_a_suivre": "Portfolio personnel"
                }
            ]
        }