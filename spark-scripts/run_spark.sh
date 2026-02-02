#!/bin/bash

set -e

# Charger les variables
set -a
source .env
set +a

# Script pour lancer un job Spark dans le conteneur spark-master

# Chemin dans le conteneur où se trouve le code
REMOTE_PATH=/opt/spark/work-dir/$SPARK_PY_SCRIPT

echo "🧹 Nettoyage du cache Ivy (sécurité)"
rm -rf ivy-cache/*

echo "📦 S'assurer que le dossier existe"

docker exec -it $SPARK_MASTER_CONTAINER_NAME mkdir -p /tmp/.ivy2

echo "⏳ Waiting for NameNode UI to start..."
until docker exec spark-master curl -s $NAMENODE_URL > /dev/null; do
  echo "Waiting for HDFS NameNode UI ..."
  sleep 5
done

echo "🚀 Lancement de $SPARK_PY_SCRIPT dans le conteneur $SPARK_MASTER_CONTAINER_NAME via spark-submit..."

docker exec -it $SPARK_MASTER_CONTAINER_NAME /opt/spark/bin/spark-submit \
    --master $SPARK_MASTER_URL \
    --conf spark.jars.ivy=/tmp/.ivy2 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.1 \
    $REMOTE_PATH