#!/bin/bash
# Script pour lancer un job Spark dans le conteneur spark-master

# Nom du script Python à exécuter
PY_SCRIPT=weather_agg.py

# Conteneur Spark Master
CONTAINER=spark-master

# Chemin dans le conteneur où se trouve le code
REMOTE_PATH=/opt/spark/work-dir/$PY_SCRIPT

echo "🚀 Lancement de $PY_SCRIPT dans le conteneur $CONTAINER..."

docker exec -it $CONTAINER /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    $REMOTE_PATH