#!/bin/bash

# Script pour lancer un job Spark dans le conteneur spark-master



# Nom du script Python à exécuter
PY_SCRIPT=weather_agg.py

# Conteneur Spark Master
CONTAINER=spark-master

# Chemin dans le conteneur où se trouve le code
REMOTE_PATH=/opt/spark/work-dir/$PY_SCRIPT

echo "🧹 Nettoyage du cache Ivy (sécurité)"
rm -rf ivy-cache/*


echo "📦 S'assurer que le dossier existe"

docker exec -it $CONTAINER mkdir -p /tmp/.ivy2

echo "🚀 Lancement de $PY_SCRIPT dans le conteneur $CONTAINER via spark-submit..."

docker exec -it $CONTAINER /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --conf spark.jars.ivy=/tmp/.ivy2 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.1 \
    $REMOTE_PATH
    #--jars /opt/spark/jars/$KAFKA_JAR \