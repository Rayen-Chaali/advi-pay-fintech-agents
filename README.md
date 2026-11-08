# 🤖 Advi-Pay : Enterprise AI Payment Advisor

**Advi-Pay** est une plateforme de démonstration FinTech innovante basée sur un système multi-agents. Elle illustre comment intégrer l'Intelligence Artificielle Générative (LLM) dans un processus de vente et de paiement B2C, tout en garantissant une sécurité déterministe absolue (Zero-Trust) face aux risques d'hallucination ou d'injection de prompt.

---

## ✨ Fonctionnalités Principales

* **Architecture Multi-Agents :** Un écosystème de 6 agents collaboratifs (Orchestrateur, Vente, Intelligence, Sécurité, Finance/Stratégie, Paiement).
* **Sécurité Déterministe (Zero-Trust) :** L'IA gère la conversation, mais le code Python strict gère les transactions. Les prix et les soldes ne peuvent pas être manipulés par des prompts malveillants.
* **Human-in-the-Loop (HITL) :** Interface Superviseur exigeant une validation humaine (CAPTCHA + Code PIN) avant de finaliser toute transaction financière.
* **Résilience et Tolérance aux Pannes :** Système de *Fallback* (secours) local intégré. Si l'API LLM atteint sa limite de quota (Erreur 429) ou subit une coupure réseau, la plateforme continue de fonctionner de manière fluide.
* **Dashboard Stratégique IA :** Analyse du profil financier du client en temps réel pour lui fournir des recommandations d'optimisation budgétaire.

---

## 🏗️ Architecture du Système (Les 6 Agents)

1. **Orchestrator (`orchestrator.py`)** : Le routeur central qui gère les états de la transaction et dirige les requêtes vers les bons agents.
2. **Agent de Vente (`sales_agent.py`)** : Connecté à Gemini 1.5, il analyse les besoins et propose dynamiquement des formations issues d'un catalogue B2C.
3. **Agent d'Intelligence (`intelligence_agent.py`)** : Analyse la sémantique de l'intention du client (simple curiosité vs intention d'achat claire).
4. **Agent de Sécurité (`security_agent.py`)** : Pare-feu déterministe qui bloque toute tentative de manipulation de prix ou de contournement des règles de paiement.
5. **Agent Finance/Stratégie (`strategy_agent.py`)** : Fournit des recommandations B2C pour optimiser le budget formation du client.
6. **Agent de Paiement (`payment_agent.py`)** : Valide mathématiquement le solde en Dinars Tunisiens (TND) et effectue la transaction sécurisée.

---

## 🛠️ Prérequis et Installation

### 1. Cloner le projet et préparer l'environnement
Il est recommandé d'utiliser un environnement virtuel Python.
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Activer l'environnement (Mac/Linux)
source venv/bin/activate
```

### 2. Installer les dépendances
```bash
pip install streamlit google-generativeai python-dotenv
```

### 3. Configuration de la clé API (Environnement)
Créez un fichier nommé exactement `.env` à la racine de votre projet et ajoutez-y vos identifiants Google Gemini :
```text
GEMINI_API_KEY=Votre_Cle_API_Google_Ici
GEMINI_MODEL=gemini-1.5-flash
```
*(Note : L'application fonctionnera en mode "Secours" si la clé est manquante ou si le quota gratuit de l'API est dépassé).*

---

## 🚀 Utilisation et Démonstration

Pour lancer l'application, exécutez la commande suivante dans votre terminal :
```bash
python -m streamlit run app.py
```

### Scénario de Démo Typique :
1. **Onglet 1 (Conversation) :** Demandez au chatbot de vous présenter le catalogue ("Quelles sont vos formations ?"), puis demandez conseil ("Quelle est la meilleure formation pour la maîtrise de l'IA ?").
2. **Attaque Contrôlée :** Cliquez sur le bouton "Lancer : Attaque contrôlée" dans la barre latérale pour prouver que le système résiste aux injections (Prompt Injection) bloquant l'achat à 1 TND.
3. **Confirmation :** Confirmez l'achat proposé par le bot (ex: "Je valide l'achat").
4. **Onglet 2 (Approbations) :** Le système bascule en attente de validation. Entrez la réponse au CAPTCHA et utilisez le code PIN par défaut **`1234`** pour approuver.
5. **Onglet 3 (Dashboard) :** Consultez les métriques générées, le journal d'audit des transactions, et les conseils d'optimisation financière générés par l'Agent Stratégique.

---

## 📁 Structure du Projet

```text
📁 /
├── 📄 app.py                  # Point d'entrée Streamlit (Interface UI)
├── 📄 orchestrator.py         # Logique de routage central
├── 📄 database.py             # Fausse base de données, catalogue et logs
├── 📄 .env                    # Variables d'environnement (API Key)
├── 📄 .gitignore              # Exclusion des fichiers sensibles pour Git
├── 📄 journal.txt             # Audit de sécurité généré automatiquement
└── 📁 agents/
    ├── 📄 finance_agent.py
    ├── 📄 intelligence_agent.py
    ├── 📄 payment_agent.py
    ├── 📄 sales_agent.py
    ├── 📄 security_agent.py
    └── 📄 strategy_agent.py
```