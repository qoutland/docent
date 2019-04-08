source ../venv/bin/activate
python manage.py populate_db
rm -rf static
python manage.py collectstatic
sudo systemctl restart gunicorn
