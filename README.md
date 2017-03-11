# Dyeus
Dyeus is a web application for gathering and displaying sensory data, and making recommendations based on preset rules.

#Usage
### Requirements
* Git
* Python 3
* Node.js
* Bower
* Ember-cli


### Setup
* Clone this repository
* Optionally create a virtualenv
* `cd Dyeus`
* `pip install -r requirements.txt`
* `cd dyeus`
* `cp local_settings.py settings.py`
* `cd ..`
* `./manage.py migrate`

### Running in development mode
* Backend: `./manage.py runserver`
* Frontend: `cd frontend; ember serve`

### Running tests
* Backend: `./manage.py test`
* Frontend: `cd frontend; ember test`
