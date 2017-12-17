[![CircleCI](https://circleci.com/gh/yizhang7210/Acre.svg?style=svg)](https://circleci.com/gh/yizhang7210/Acre)

# Acre
Algorithmically Constructed Rates Explorer


Overview
--------

Acre provides a service that aims to predict the profitable change in rates
of various currency pairs and instruments, using maching learning and based on
historical patterns.


Project Setup
-------------
- Clone the project: `git clone https://github.com/yizhang7210/Acre.git`
- Make sure you have virtualenv. If not, `pip/pip3 install virtualenv`
- Under main project folder, go to your virtual env:
    - `virtualenv env`
    - `source env/bin/activate`
- Install everything you need: `pip3 install -r requirements/local.txt`
- Setup your PostgresSQL database according to the Resources section below
as well as the configurations in `acre/settings/local.py`
- Remeber to give your user database creation access: `ALTER USER acreuser CREATEDB;`
- Catch up on your database schema: `./manage.py migrate`
- You should be good to go: make sure `./manage.py test` all pass


Code Commit Checklist
---------------------
- [ ] All tests pass.
- [ ] Run `pylint <app> --load-plugins pylint_django` on all apps with 10.0 score.
- [ ] Update documentation whenever appropriate.


Resources
---------
Django App:
- [Modern Django](https://medium.com/@djstein/modern-django-part-0-introduction-and-initial-setup-657df48f08f8)
- [Start Django](https://realpython.com/learn/start-django/)

REST API in Django
- [A Test Driven Approach](https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1)

PostgresSQL
- [Basic Setup](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04)
