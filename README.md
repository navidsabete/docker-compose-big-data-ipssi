# Docker Compose Big Data Exam - IPSSI
## **🌦️ Big Data Weather Streaming Pipeline**


### 🎯 Objectif

Implémenter une architecture Big Data permettant de collecter, traiter et stocker des données météorologiques en temps réel à l'aide de Kafka, Spark, HDFS et Airflow, le tout orchestré via Docker Compose.

#### ⚙️ Variables d'environnement

Les variables sont définis dans un fichier .env Vous trouverez le modèle on env_template.txt que vous aurez besoin de copier dans votre propre fichier .env sur votre machine. Affectez ensuite la valeur que vous souhaitez sur chaque variable.

#### 📁 Structure du projet

root *(docker-compose-big-data-ipssi)*/

├── docker-compose.yml        *# Mise en place de l'architecture*

├── weather_flow/        *# Producer (Kafka)*

├── spark-scripts/       *# Job Spark*

├── airflow/dags/        *# DAG Airflow*

├── notebooks/           *# Jupyter notebook du producer* 
       

### 🚀 Étapes du projet

##### Étape 1 – Jupyter Lab

Mise en place d'un environnement Jupyter pour l'affichage du streaming.

##### Étape 2 – Kafka

Récupération des données météo via une API, transformation, puis streaming vers un topic Kafka.

##### Étape 3 – Spark

Lecture du stream Kafka avec Spark, agrégation par fenêtre d'une minute calculant la température moyenne et le nombre d'alertes vent fort.

##### Étape 4 – HDFS

Sauvegarde des résultats Spark dans HDFS via InsecureClient, avec création automatique des répertoires et des fichiers CSV.

##### Étape finale – Airflow

Création d'un DAG Airflow permettant de lire Kafka et d'écrire les alertes dans HDFS et sauvegarde dans un fichier JSON. Le DAG est déclenché manuellement. 

### ▶️ Lancement du projet

Le lancement est piloté via un Makefile. Commandes disponibles sur le fichier Makefile de l'exercice.

Interfaces principales :
- Jupyter Lab : http://localhost:8888/
    - pour y accéder, consulter les logs pour récupérer le lien avec token : "*To access the server, open this file in a browser [...] Or copy and paste one of these URLs*
        http://127.0.0.1:8888/lab?token=<token>⁠ 
    "
- Spark UI :
    - Master : http://localhost:8080/
    - Worker : http://localhost:8081/
- HDFS - NameNode UI : http://localhost:9870/
- Airflow UI : http://localhost:8082/

---
Des scripts Bash sont utilisés pour faciliter le lancement des traitements. Le script *run_spark.sh* permet de soumettre le job Spark au cluster (Spark Master + Workers) via spark-submit, garantissant une exécution du traitement de streaming. Un script *entrypoint.sh* est également utilisé après lancement des conteneurs pour initialiser l'environnement (dépendances) et lancer certains services.

---
### 🔮 Améliorations possibles

Automatisation du DAG Airflow