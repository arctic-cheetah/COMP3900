Dockerfile for database not required as we download official image!

docker compose -f 'docker-compose.yml' up -d --build 

export PGPASSWORD='markspass' && psql -U marksuser -h 127.0.0.1 -p 5432 -d marksdb

npm run dev