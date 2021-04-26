# JBlog
A simple blog app that allows users to view posts,like  and comment.


## Installation
1.Create Virtual Environment folder

```
python -m venv env
```

2.Activate virtual environment in parent directory of your "env"

For Linux systems and MAC

```
source env/bin/avtivate
```

For Windows

```
env\Scripts\activate.bat
```

3.Install requierements
```
pip install - r requirements.txt
```

4.Create a .env file and fill in  the following input variables
"touch .env
pip install 
"
```
export SECRET_KEY='django-insecure-859e&hhj95l+0pcr0x=%k#j9z$4p18!+a4=d6byun6*@ri076v'
export DEBUG=True
export DB_NAME=,
export DB_USER=,
export DB_PASSWORD=,
export DB_HOST=''

export EMAIL_HOST='smtp.gmail.com'
export EMAIL_USE_TLS=True
export EMAIL_PORT='587'
export EMAIL_HOST_USER=''
export EMAIL_HOST_PASSWORD=''



``` 

### Input variables

5.run the application
```
python manage.py  makemigrations
python manage.py migrate
python manage.py createsuperuser 
python manage.py runserver
```
* psycopg2

