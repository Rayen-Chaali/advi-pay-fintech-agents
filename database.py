import uuid
import datetime
import random

CATALOGUE_FICTIF = {
    "FORM-IA-PRO": {"nom": "Bootcamp Agentic AI", "prix": 2890.0},
    "FORM-CYBER": {"nom": "Cybersécurité & Défense", "prix": 3200.0},
    "FORM-ML": {"nom": "Machine Learning Avancé", "prix": 2950.0},
    "FORM-DL": {"nom": "Deep Learning & Vision", "prix": 3100.0},
    "FORM-LLM": {"nom": "Maîtrise des LLMs", "prix": 2500.0},
}

def creer_dossier_initial(id_session):
    return {
        "id_client": f"CL-{str(uuid.uuid4())[:8].upper()}",
        "session": id_session,
        "date_creation": datetime.datetime.now().isoformat(),
        "statut_dossier": "NOUVEAU",
        # Le solde est généré aléatoirement pour tester les cas de refus et de succès
        "solde_client": random.choice([2000.0, 3500.0, 5000.0]), 
        "ajouts_agents": {},
        "alertes": []
    }

def journaliser_evenement(type_evenement, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("journal.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {type_evenement} - {details}\n")