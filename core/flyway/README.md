## flyway migrations guide
to create a migration for a **new** service (`new-service`), you must do the following:
1. in `/entask/.env` initialize the following variables:
```.env
NEW_SERVICE_USER=
NEW_SERVICE_PASSWORD=
NEW_SERVICE_DB=
```
2. in `/entask/core/postgres/initdb.sql` create a new database, aptly named:
```sql
-- ... rest of the init-script
CREATE DATABASE new_service;
-- rest of the init-script ...
```
3. in `/entask/core/flyway/entrypoint.sh` add a new `DBS` array entry:
```bash
declare -A DBS=(
  # ... rest of the array
  [new_service]=$NEW_SERVICE_DB
  # rest of the array ...
)
```
4. in `/entask/core/pgbouncer/pgbouncer.ini` add a new `[databases]` entry:
```yaml
[databases]
new_service_db = host=postgres port=5432 dbname=new_service_db
```

and also in `/entask/core/pgbouncer/userlist.txt` add a new user entry:
```
"new_service_user" "yourpassword"
```

where `yourpassword` is equal to `$NEW_SERVICE_PASSWORD`, and `new_service_user` is equal to `$NEW_SERVICE_USER`