web: gunicorn -w 4 -b 0.0.0.0:$PORT \
 --log-level=debug \
 --log-file /flaskr/logs/log.log \
 wsgi:app