# WIP

i
To start the project run
```
docker-compose -f docker-compose.dev.yml up
```

If the spatial db is not initialized, run:
```
docker exec -it dp-db psql -U ckan -f /docker-entrypoint-initdb.d/30_setup_postgis.sql
docker exec -it dp-dev paster --plugin=ckanext-spatial spatial initdb -c /srv/app/production.ini
```