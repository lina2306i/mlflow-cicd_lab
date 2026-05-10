import requests
import json
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1502639151034404999/wP9lUn1qgL7QCVeaLp-2OwgNYjc8oXddz7Z2b5z2IQaaOhZGm-zKPbN2qhhHGvuV74LG"

def notify_discord(message, level="info"):
    """
    Envoie une notification sur Discord via Webhook.
    level: 'info', 'success', 'error'
    """
    colors = {
        "info": 3447003,      # Bleu
        "success": 3066993,   # Vert
        "error": 15158332     # Rouge
    }
    
    emoji = {"info": "ℹ️", "success": "✅", "error": "❌"}
    
    payload = {
        "username": "Bot-ML-Notifier",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/4712/4712139.png",
        "embeds": [{
            "title": f"{emoji.get(level, '➡️')} Notification d'Entraînement ML",
            "description": message,
            "color": colors.get(level, 3447003),
            "footer": {
                "text": "ML Training Bot"
            },
            "thumbnail": {
                "url": "https://cdn-icons-png.flaticon.com/512/4712/4712139.png"
            },
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL, 
            data=json.dumps(payload), 
            headers={'Content-Type': 'application/json'},
            timeout=10 ,
            
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur lors de l'envoi Discord: {e}")
        

if __name__ == "__main__":
    notify_discord("Le module Discord est bien configuré !", "success")
    assert True, "Test de notification Discord réussi"
    
