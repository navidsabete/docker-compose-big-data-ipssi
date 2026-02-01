#!/bin/bash
set -e

echo "📦 Installing Python dependencies..."
docker exec -it spark-master bash -c "pip install --no-cache-dir hdfs"

echo "Waiting for NameNode UI to start..."
until docker exec spark-master curl -s http://namenode:9870/ > /dev/null; do
  echo "Waiting for HDFS NameNode UI ..."
  sleep 5
done

echo "🚀 NameNode ready. Starting Spark..."
exec "$@"