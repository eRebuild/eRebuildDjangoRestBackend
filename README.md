# eRebuildDjangoRestBackend

This repository contains a Django app to combine functionality currently scattered across many apps. 

To update Unity eRbuild artifacts replace files in ./static/unity/Build.

## To install on Linux VM
### For development testing
1. sudo apt install python3.10-venv
2. python3 -m venv djangoBackendEnv
3. source djangoBackendEnv/bin/activate
4. git clone https://github.com/eRebuild/eRebuildDjangoRestBackend.git
5. cd eRebuildDjangoRestBackend/
6. pip install -r requirements.txt
7. python manage.py migrate
8. python3 manage.py createsuperuser
    * Follow prompts
9. python manage.py runserver 0.0.0.0:80

### For production

#### 