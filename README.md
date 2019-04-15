# [Docent](https://docent.life)
Find events in Reno!

## QuickStart Guide

### Install virtualenv
```pip install virtualenv```

### Create a virtualenv
```virtualenv venv``` where **venv** is the name of the virtualenv

### Activiate the venv
Windows: ```venv\Scripts\activate.bat```

Linux/MacOS: ```source venv/bin/activate```


### Clone the repository
```git clone https://github.com/qoutland/docent```

### Install Dependencies
```pip install -r requirements.txt```

### Create secrets.py file from the template
Follow instructions in *docent/secret_example.py*

### Run the server
```python manage.py runserver```

## Useful Development Commands

### Populate the Activities
```python manage.py populate_db *--test*```

### Collect the static (CSS/JS/MEDIA)
```python manage.py collectstatic```

### Resync the database after a schema change
```python manage.py makemigrations && python manage.py migrate```
