# Docent
Find events in Reno!

## Useful Development Commands

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

###Resync the database after a schema change
```
python manage.py makeigrations && python manage.py migrate
```
