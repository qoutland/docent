# Docent
Find events in Reno!

## Useful Development Commands
In order to run this project completely please complete the 'docent/secrets_example.py' file and rename it to 'secrets.py'.

### Install dependencies
```
pip install -r requirements.txt
```

### Run the server
```
python manage.py runserver
```

### Populate the Activities
```
python manage.py populate_db *--test*
```

### Collect the static (CSS/JS/MEDIA)
```
python manage.py collectstatic
```

### Resync the database after a schema change
```
python manage.py makemigrations && python manage.py migrate
```
