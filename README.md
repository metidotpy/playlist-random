# Playlist Random
## How To Run This Webapp

1. ### the first step make a venv
    + #### if you use windows
        ```bash
            python -m venv .venv
            .\.venv\Scripts\activate.bat
        ```
    + #### if you use linux
        ```bash
            sudo apt install virtualenv
            virtualenv .venv
            source .venv/bin/activate
        ```
    + #### if you use macos
        ```bash
            brew install virtualenv
            virtualenv .venv
            source .venv/bin/activate
        ```

2. ### the second step install requirements
   + #### if you use windows
        ```bash
            python -m pip install -r requirements.txt
        ```
    + #### if you use linux
        ```bash
            pip3 install -r requirements.txt
        ```
    + #### if you use macos
        ```bash
            pip install -r requirements.txt
        ```
3. ### the third step you must migrate things
    + #### run this commands
        ```bash
            python3 or python managed.py makemigrations
            python3 or python managed.py migrate
        ```
4. ### the fourth step you must compelete `.env-sample` and rename it to `.env`
   + #### add this variables to the `.env`
        ```python
            EMAIL_USE_TLS = True # if you use gmail
            EMAIL_HOST = 'smtp.gmail.com' # if you use gmail
            EMAIL_PORT = '587' # if you use gmail
            EMAIL_HOST_USER = 'youremail@gmail.com'
            EMAIL_HOST_PASSWORD = 'your password'
        ```
5. ### the fifth step you must create a superuser
   + #### run this command
        ```bash
            python manage.py createsuperuser
        ```
        and give your info
6. ### the sixth step you must run the server
   + #### run this command
        ```bash
            python manage.py runserver (your port => default is 8000)
        ```

#### I Hope You Enjoyed
#### Dont Forget Star
#### Writed By metidotpy
