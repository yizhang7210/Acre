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
- Install everything you need: `pip3 install -r requirements.txt`
- Setup your PostgresSQL database according to the Resources section below
as well as the configurations in `acre/settings/local.py`
- Remeber to give your user database creation access: `ALTER USER acreuser CREATEDB;`
- Set up your environment variables according to `docs/dev/Envs.md#local`
- Catch up on your database schema: `./manage.py migrate`
- You should be good to go: make sure `./manage.py test` all pass
- Even better, do `coverage run manage.py test` to run test with coverage
- You can access your coverage report at `coverage report`

Code Commit Checklist
---------------------
- [ ] All tests pass.
- [ ] Run `pylint <app> --load-plugins pylint_django` on all apps with 10.0 score.
- [ ] Update documentation whenever appropriate.


Deployment
----------
- We use Circle CI for continuous integration and deployment. See `.circleci/config.yml`
for the configurations. For Circle CI, see the required environment variables in
`docs/dev/Envs.md#deploy`.
- For each environment (dev and prod), there are technically two applications
that get deployed to AWS. One in a worker tier that runs the end of day process
(at 17:00 Eastern time) for all algorithms, the other in a web server that
provides the predictions API.
- The two applications are tied to the same database in AWS RDS.
- For the worker tier, see the required environment variables in `docs/dev/Envs.md#worker`
- For the web server, see the required environment variables in `docs/dev/Envs.md#server`

Resources
---------
Django App:
- [Modern Django](https://medium.com/@djstein/modern-django-part-0-introduction-and-initial-setup-657df48f08f8)
- [Start Django](https://realpython.com/learn/start-django/)

REST API in Django:
- [A Test Driven Approach](https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1)

PostgresSQL:
- [Basic Setup](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04)

Deploy Django App to ElasticBeanstalk:
- [AWS Doc](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-apps.html)

Elm:
- [Tutorial](https://www.elm-tutorial.org/en/)
- [JSON Decode](http://elmplayground.com/decoding-json-in-elm-1)
