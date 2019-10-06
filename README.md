# jagrmi

Test aiohttpserver

## DEPLOY HEROKU

### HOW UPDATE HEROKU remote server

heroku login -i

### SEE INFO ABOUT DB

heroku pg:info postgresql-cubed-59224 --app jagrmiaiohttpserver

### SEE LOG

heroku logs -t --app jagrmiaiohttpserver

### ANALYZE AND OPTIMIZE DB PERFONCE

heroku pg:diagnose --app jagrmiaiohttpserver

### CONNECT TO DB

heroku pg:psql --app=jagrmiaiohttpserver

### PULL

PGUSER=postgres PGPASSWORD=password]
heroku pg:pull postgresql-tapered-36826 familyT1
--app jagrmiaiohttpserver

### DB api.elephantsql.com/

psql -h rogue.db.elephantsql.com -p 5432 -U sjbyrear sjbyrear
password: eF_AMcXhN55UDzQKC8n_Bz_RMTJ0gqjE


### Autogenerate alembic
alembic revision --autogenerate -m "Added account table"

### Execute migration
alembic upgrade head

### Start application
python app.py