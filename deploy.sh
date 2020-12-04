git pull
pip3 install -r requirements.txt

# Update database, static files, locales
python3 manage.py syncdb  --noinput
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py makemessages -a
python3 manage.py compilemessages

# restart wsgi
# touch project_name/wsgi.py
