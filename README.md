# jagrmi
Test aiohttpserver

HOW UPDATE HEROKU remote server.
--------------------------------------------------------------------------------
heroku login -i

SEE INFO ABOUT DB
--------------------------------------------------------------------------------
heroku pg:info postgresql-cubed-59224 --app jagrmiaiohttpserver

SEE LOG
-------------------------------------------------------------
heroku logs -t --app jagrmiaiohttpserver

ANALYZE AND OPTIMIZE DB PERFONCE
-----------------------------------------------
heroku pg:diagnose --app jagrmiaiohttpserver

CONNECT TO DB
----------------------------
heroku pg:psql --app=jagrmiaiohttpserver