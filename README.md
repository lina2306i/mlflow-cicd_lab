<div align="center">

# 🧬 MLOps Pipeline — Breast Cancer Classification

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/MLflow-3.1.4-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
<img src="https://img.shields.io/badge/DVC-Data_Versioning-945DD6?style=for-the-badge&logo=dvc&logoColor=white"/>
<img src="https://img.shields.io/badge/MinIO-S3_Storage-C72E49?style=for-the-badge&logo=minio&logoColor=white"/>

<br/>

> **Architecture MLOps complète** — de l'expérimentation jusqu'au versioning des données et à la notification temps réel.

**Cours DevOps - MLOps • iTeam University • Mai 2026**
**Auteur : Ing. LABIADH LINA**

</div>

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation & Lancement](#-installation--lancement)
- [Structure du projet](#-structure-du-projet)
- [Versioning des données — DVC](#-versioning-des-données--dvc)
- [Expérimentation — MLflow](#-expérimentation--mlflow)
- [Notifications Discord](#-notifications-discord)
- [Résultats](#-résultats)
- [Perspectives](#-perspectives)

---

## 🔭 Vue d'ensemble

Ce projet implémente un pipeline **MLOps end-to-end** pour la classification du cancer du sein (dataset Breast Cancer de scikit-learn). Il couvre l'ensemble du cycle de vie ML :

| Étape | Outil | Description |
|-------|-------|-------------|
| 📦 Containerisation | Docker Compose | 4 services orchestrés |
| 🗄️ Stockage metadata | PostgreSQL 14 | Backend store MLflow |
| 🪣 Stockage artefacts | MinIO (S3) | Modèles `.pkl` + données DVC |
| 📊 Tracking | MLflow 3.1.4 | Expériences, métriques, modèles |
| 🔁 Versioning données | DVC | Dataset versionné dans MinIO |
| 📡 Monitoring | Discord Webhook | Notifications temps réel |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  mlops_net  (réseau Docker interne)       │
│                                                          │
│   ┌─────────────┐      ┌──────────────┐                  │
│   │ PostgreSQL  │◄─────│  MLflow      │◄─── Jupyter Lab  │
│   │   :5432     │      │  Server:5000 │      :8888       │
│   └─────────────┘      └──────┬───────┘                  │
│                               │                          │
│                        ┌──────▼───────┐                  │
│                        │    MinIO     │                  │
│                        │  :9000/:9001 │                  │
│                        └─────────────┘                  │
└──────────────────────────────────────────────────────────┘
         │                                    │
    DVC remote                         Artifact store
   (dvcstore/)                        (runs/models/)
```

### Services Docker

| Container | Image | Port | Rôle |
|-----------|-------|------|------|
| `mlops_postgreslab` | postgres:14 | 5432 | Métadonnées MLflow |
| `mlops_miniolab` | minio/minio:latest | 9010 / 9001 | Stockage S3 local |
| `mlops_mlflowlab` | custom python:3.9 | 5000 | Tracking server |
| `mlops_jupyterlab` | custom datascience-notebook | 8888 | Environnement ML |

---

## ✅ Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ≥ 4.x
- Python ≥ 3.11
- [DVC](https://dvc.org/) (`pip install dvc[s3]`)
- Git

> **WSL 2 (Windows)** : configurer `~/.wslconfig` avec au moins `memory=8GB`

---

## 🚀 Installation & Lancement

### 1. Cloner le repo

```bash
git clone https://github.com/lina2306i/mlflow-cicd_lab.git
cd mlflow-cicd_lab
```

### 2. Configurer les variables d'environnement

```bash
# Créer un fichier .env (ne pas commiter !)
cp .env.example .env
```

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/TON_WEBHOOK
```

### 3. Démarrer l'infrastructure

```bash
docker-compose up -d --build
```

✅ Vérifier que les 5 containers sont actifs :

```bash
docker ps
```

### 4. Accéder aux interfaces

| Service | URL | Identifiants |
|---------|-----|--------------|
| 📓 Jupyter Lab | http://localhost:8888 | token : `mlflow` |
| 📊 MLflow UI | http://localhost:5000 | — |
| 🪣 MinIO Console | http://localhost:9001 | `root` / `root123456789` |

### 5. Récupérer les données (DVC)

```bash
dvc pull
```

### 6. Lancer l'expérimentation

Ouvrir dans Jupyter : `notebooks/01_experimentation.ipynb` et exécuter toutes les cellules.

---

## 📁 Structure du projet

```
mlflow-cicd_lab/
│
├── 📂 docker/
│   ├── Dockerfile.jupyter          # Image Jupyter + dépendances ML
│   └── Dockerfile.mlflow           # Image MLflow Tracking Server
│
├── 📂 notebooks/
│   └── 01_experimentation.ipynb    # Pipeline complet ML + Discord
│
├── 📂 src/
│   └── 📂 utils/
│       ├── __init__.py
│       └── discord_notify.py       # Bot de notifications Discord
│
├── 📂 data/
│   ├── dataset.csv                 # ⚠️ ignoré par Git (géré par DVC)
│   └── dataset.csv.dvc             # ✅ pointeur DVC versionné
│
├── 📂 .dvc/
│   └── config                      # Config remote MinIO
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .dvcignore
└── README.md
```

---

## 🔁 Versioning des données — DVC

DVC permet de versionner les datasets volumineux en dehors de Git, en les stockant dans MinIO (compatible S3).

### Configuration initiale

```bash
# Initialiser DVC
dvc init

# Ajouter le remote MinIO
dvc remote add -d myremote s3://mlflow/dvcstore
dvc remote modify myremote endpointurl  http://localhost:9010
dvc remote modify myremote access_key_id     root
dvc remote modify myremote secret_access_key root123456789
dvc remote modify myremote use_ssl    false
dvc remote modify myremote ssl_verify false
dvc remote modify myremote region     us-east-1
```

### Workflow DVC

```bash
# Tracker le dataset
dvc add data/dataset.csv

# Committer le pointeur dans Git
git add data/dataset.csv.dvc data/.gitignore
git commit -m "feat: add dataset versioning with DVC"

# Pousser les données vers MinIO
dvc push

# Récupérer les données (autre machine)
dvc pull
```

> 📌 Le fichier `dataset.csv.dvc` est commité dans Git — il contient le hash MD5 du fichier, pas le fichier lui-même.

---

## 🧪 Expérimentation — MLflow

### Connexion et tracking

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Connexion au serveur (dans Docker : http://mlflow:5000)
mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment("Classification_Cancer")
mlflow.sklearn.autolog()  # ← log automatique hyperparamètres + métriques + modèle

with mlflow.start_run() as run:
    clf = RandomForestClassifier(n_estimators=100, max_depth=5)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc   = accuracy_score(y_test, preds)

    # Notification Discord automatique
    notify_discord(
        message=f"Modèle sauvegardé dans MinIO.",
        run_id=run.info.run_id,
        metrics={"Accuracy": acc},
        level="success",
        task_name="Training-Complete"
    )
```

### Ce que `autolog()` capture automatiquement

| Catégorie | Détails |
|-----------|---------|
| ⚙️ Hyperparamètres | `n_estimators`, `max_depth`, `max_features`… |
| 📈 Métriques | accuracy, precision, recall, F1, AUC |
| 💾 Modèle | `.pkl` sérialisé → stocké dans MinIO |
| 📦 Dataset | Référence train/test loggée |
| 🏷️ Run ID | Hash unique pour recharger le modèle exact |

### Recharger un modèle depuis MLflow

```python
run_id = "1120cc379cea4857bf073e6a387f499e"
model  = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
predictions = model.predict(X_test)
```

---

## 📡 Notifications Discord

Le module `src/utils/discord_notify.py` envoie des embeds Discord à 3 niveaux :

```python
notify_discord(
    message   = "Entraînement terminé avec succès !",
    run_id    = run.info.run_id,
    metrics   = {"Accuracy": 0.9298, "F1": 0.9489},
    level     = "success",   # "info" | "success" | "error" | "warning"
    task_name = "Training-Complete"
)
```

| Niveau | Couleur | Déclencheur |
|--------|---------|-------------|
| ℹ️ `info` | 🔵 Bleu | Début de session / entraînement |
| ✅ `success` | 🟢 Vert | Modèle sauvegardé avec métriques |
| ❌ `error` | 🔴 Rouge | Exception avec traceback complet |
| ⚠️ `warning` | 🟡 Jaune | Avertissement non bloquant |

> 🔒 **Sécurité** : le webhook est lu depuis la variable d'environnement `DISCORD_WEBHOOK_URL`, jamais hardcodé dans le code.

---

## 📊 Résultats

### Métriques obtenues — RandomForestClassifier

| Métrique | Valeur |
|----------|--------|
| ✅ Accuracy | **93.86 %** |
| 🎯 Precision | 92.86 % |
| 🔁 Recall | 97.01 % |
| 📐 F1-Score | 94.89 % |
| 🌳 n_estimators | 100 |
| 📏 max_depth | 5 |

### Runs MLflow enregistrés

| Run Name | Durée | Statut |
|----------|-------|--------|
| vaunted-pig-402 | 8.1s | ✅ Completed |
| bold-wolf-897 | 9.5s | ✅ Completed |
| bright-asp-601 | 9.0s | ✅ Completed |
| intelligent-crab-735 | 13.4s | ✅ Completed |

> 📦 **4.7 MiB** d'artefacts stockés dans MinIO (29 objets)

---

## 🔭 Perspectives

- [ ] **CI/CD GitLab** — pipeline automatique train → test → deploy
- [ ] **Monitoring** — Prometheus + Grafana (Data Drift detection)
- [ ] **API de serving** — FastAPI / Flask avec endpoint `/predict`
- [ ] **Model Registry** — MLflow alias `@staging` / `@production`
- [ ] **Tests automatisés** — pytest + coverage
- [ ] **Lab 2** — NLP avec DistilBERT & HuggingFace Transformers

---

![Capture d'écran du Dashboard](assets/dashboard_preview.png)


---
## 📈 Évolution du projet (Stargazers over time)

Si vous aimez ce projet, n'hésitez pas à laisser une 🌟 ! L'évolution des étoiles montre l'intérêt de la communauté pour ce pipeline MLOps :

[![Stargazers over time](https://starchart.cc/lina2306i/mlflow-cicd_lab.svg?variant=adaptive)](https://starchart.cc/lina2306i/mlflow-cicd_lab)

---

---

## Licence

MIT License — voir [LICENSE](LICENSE)


---

## 👩‍💻 Auteur

**Lina Labiadh** — *Ingénieure Data & AI*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profil-0077b5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/linalabiadh/)
[![Email](https://img.shields.io/badge/Email-Contact-d14836?style=for-the-badge&logo=gmail&logoColor=white)](https://mail.google.com/mail/?view=cm&fs=1&to=lina.hkl2306@gmail.com)

*📧 Si le bouton email ne s'ouvre pas, vous pouvez me contacter directement à : **lina.hkl2306@gmail.com***


---

<div align="center">

**Stack Technologique**

`Docker Compose` • `PostgreSQL 14` • `MinIO S3` • `MLflow 3.1` • `DVC` • `scikit-learn` • `Discord Webhooks` • `Python 3.11`

---

*Système de Monitoring MLOps — Lina Labiadh • 2026*

</div>
