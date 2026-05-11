import requests
import json
from datetime import datetime
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DiscordNotifier")

# Il est préférable d'utiliser une variable d'environnement pour la sécurité
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1502639151034404999/wP9lUn1qgL7QCVeaLp-2OwgNYjc8oXddz7Z2b5z2IQaaOhZGm-zKPbN2qhhHGvuV74LG")

#WEBHOOK_URL = "https://discord.com/api/webhooks/1502639151034404999/wP9lUn1qgL7QCVeaLp-2OwgNYjc8oXddz7Z2b5z2IQaaOhZGm-zKPbN2qhhHGvuV74LG"

#def notify_discord(message, level="info"):
#def notify_discord(message, level="info", task_name="Training"):
"""def notify_discord(message, metrics=None, level="success",task_name="Training"):
    " ""
    Envoie une notification enrichie sur Discord.
    level: 'info', 'success', 'error', 'warning'
    "" "
    colors = {
        "info": 3447003,      # Bleu
        "success": 3066993,   # Vert
        "warning": 16776960,  # Jaune
        "error": 15158332     # Rouge
    }
    # Transformation des métriques en texte lisible
    metrics_text = "N/A"
    if metrics:
        metrics_text = "\n".join([f"**{k}:** `{v:.4f}`" for k, v in metrics.items()])

    emoji = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}
    #emoji = {"info": "ℹ️", "success": "✅", "error": "❌"}
    
    payload = {
        "username": "MLOps Watcher",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
        "embeds": [{
            "title": f"{emoji.get(level, '➡️')} {task_name.upper()}",
            "description": message,
            "color": colors.get(level, 3447003),
            "fields": [
                {
                    "name": "Environnement-Model",
                    "value": "`Production/Lab`",
                    "inline": True
                },
                {
                    "name": "Auteur",
                    "value": "`ING.LABIADH LINA`",
                    "inline": True
                },
                {
                    "name": "Horodatage",
                    "value": datetime.now().strftime("%H:%M:%S"),
                    "inline": True
                },
                
                {
                    "name": "📊 Métriques",
                    "value": metrics_text,
                    "inline": False
                },
                {
                    "name": "🔗 MLflow UI",
                    "value": "[Accéder à l'interface](http://localhost:5000)",
                    "inline": False
                }
            ],
            "thumbnail": {
                "url": "https://cdn-icons-png.flaticon.com/512/4712/4712139.png" # Icône de fusée/IA
            },
            "footer": {
                "text": "Système de Monitoring MLOps - iTeam Univ"
            },
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
"""
    
def notify_discord(message, run_id="N/A", metrics=None, level="success", task_name="Training"):
    """
    Notification Discord Optimisée - Style iTeam Univ
    """
    colors = {
        "info": 3447003, "success": 3066993, "warning": 16776960, "error": 15158332
    }
    
    metrics_text = "N/A"
    if metrics:
        metrics_text = "\n".join([f"**{k}:** `{v:.4f}`" for k, v in metrics.items()])

    emoji = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}
    
    payload = {
        "username": "MLOps Watcher",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
        "embeds": [{
            "title": f"{emoji.get(level, '➡️')} {task_name.upper()}",
            "description": message,
            "color": colors.get(level, 3447003),
            "fields": [
                {"name": "🌍 Environnement", "value": "`Production/Lab`", "inline": True},
                {"name": "👤 Auteur", "value": "`ING. LABIADH LINA`", "inline": True},
                {"name": "🆔 Run ID", "value": f"`{run_id}`", "inline": True},
                {"name": "📊 Métriques", "value": metrics_text, "inline": False},
                {"name": "🔗 MLflow UI", "value": "[Accéder à l'interface](http://localhost:5000)", "inline": False}
            ],
            "thumbnail": {"url": "https://cdn-icons-png.flaticon.com/512/4712/4712139.png"},
            "footer": {"text": "Système de Monitoring MLOps - iTeam Univ"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL, 
            data=json.dumps(payload), 
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        response.raise_for_status()
        logger.info(f"Notification Discord envoyée avec succès : {level}")
    except requests.exceptions.HTTPError as err:
        logger.error(f"Erreur HTTP Discord : {err}")
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'envoi Discord : {e}")

if __name__ == "__main__":
    # Test rapide
    notify_discord("Pipeline MLOps démarré avec succès sur Docker.",
                   metrics={"R2_Score": 0.8942},
                   level="success",
                   task_name="Training"
                   )