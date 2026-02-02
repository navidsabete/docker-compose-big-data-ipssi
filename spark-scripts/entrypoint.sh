#!/bin/bash
set -e

# Charger les variables
set -a
source ../.env
set +a

echo "📦 Installing Python dependencies..."
docker exec -it $SPARK_MASTER_CONTAINER_NAME bash -c "pip install --no-cache-dir hdfs"

echo "Waiting for NameNode UI to start..."
until docker exec spark-master curl -s $NAMENODE_URL > /dev/null; do
  echo "Waiting for HDFS NameNode UI ..."
  sleep 5
done

echo "🚀 NameNode ready. Starting Spark..."
exec "$@"