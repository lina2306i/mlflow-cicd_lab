\# 🧬 MLOps Pipeline: Breast Cancer Classification



> Architecture MLOps complète avec Docker, MLflow, MinIO, PostgreSQL, DVC et Discord Notifications  

> \*\*Cours DevOps - MLOps • iTeam University • Mai 2026\*\*  

> \*\*Auteur : Ing. LABIADH LINA\*\*



\---



\## 🏗️ Architecture



┌─────────────────────────────────────────────┐

│              mlops\_net (Docker)              │

│                                             │

│  PostgreSQL  ──►  MLflow  ◄──  MinIO        │

│     :5432          :5000       :9000        │

│                      ▲                      │

│                   Jupyter                   │

│                    :8888                    │

└─────────────────────────────────────────────┘



\## 🚀 Lancement rapide



\### Prérequis

\- Docker Desktop installé et lancé

\- Python 3.x + DVC installé



\### Démarrer l'infrastructure

```bash

docker-compose up -d --build

```



\### Accès aux interfaces

| Service | URL | Credentials |

|---------|-----|-------------|

| Jupyter Lab | http://localhost:8888 | token: `mlflow` |

| MLflow UI | http://localhost:5000 | — |

| MinIO Console | http://localhost:9001 | `root` / `root123456789` |



\---



\## 📁 Structure du projet



lab\_mlflow/

├── docker/

│   ├── Dockerfile.jupyter      # Image Jupyter + dépendances

│   └── Dockerfile.mlflow       # Image MLflow Server

├── notebooks/

│   └── 01\_experimentation.ipynb  # Notebook principal

├── src/

│   └── utils/

│       └── discord\_notify.py   # Bot notifications Discord

├── data/

│   ├── dataset.csv             # Dataset (ignoré par Git)

│   └── dataset.csv.dvc         # Pointeur DVC versionné

├── docker-compose.yml

├── requirements.txt

└── README.md



\---



\## 🔁 Versioning des données (DVC)



```bash

\# Initialiser DVC

dvc init



\# Configurer remote MinIO

dvc remote add -d myremote s3://mlflow/dvcstore

dvc remote modify myremote endpointurl http://localhost:9010

dvc remote modify myremote access\_key\_id root

dvc remote modify myremote secret\_access\_key root123456789



\# Versionner le dataset

dvc add data/dataset.csv

git add data/dataset.csv.dvc .gitignore

git commit -m "Add dataset with DVC"



\# Pousser vers MinIO

dvc push

```



\---



\## 🧪 Expérimentation MLflow



```python

import mlflow

from sklearn.ensemble import RandomForestClassifier



mlflow.set\_tracking\_uri('http://localhost:5000')

mlflow.set\_experiment("Classification\_Cancer")

mlflow.sklearn.autolog()  # Log automatique !



with mlflow.start\_run() as run:

&#x20;   clf = RandomForestClassifier(n\_estimators=100, max\_depth=5)

&#x20;   clf.fit(X\_train, y\_train)

&#x20;   # Métriques, paramètres et modèle loggés automatiquement

```



\---



\## 📊 Résultats



| Métrique | Valeur |

|----------|--------|

| Accuracy | \*\*92.98 %\*\* |

| Precision | 92.86 % |

| Recall | 97.01 % |

| F1-Score | 94.89 % |

| Runs enregistrés | 4 |

| Artefacts MinIO | 4.7 MiB |



\---



\## 📡 Notifications Discord



Le bot envoie automatiquement des notifications à 3 moments :



\- ℹ️ \*\*INFO\*\* — Début de session / entraînement

\- ✅ \*\*SUCCESS\*\* — Modèle sauvegardé avec métriques

\- ❌ \*\*ERROR\*\* — Exception avec traceback



```bash

\# Configurer le webhook (variable d'environnement)

export DISCORD\_WEBHOOK\_URL="https://discord.com/api/webhooks/..."

```



\---



\## 🚀 Perspectives



\- \[ ] CI/CD GitLab — pipeline automatique train + deploy

\- \[ ] Monitoring Prometheus + Grafana (Data Drift)

\- \[ ] Déploiement API FastAPI / Flask

\- \[ ] Model Registry MLflow (`@production`)

\- \[ ] Lab 2 : NLP avec DistilBERT \& Transformers

