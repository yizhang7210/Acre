[![CircleCI](https://circleci.com/gh/yizhang7210/Acre.svg?style=svg)](https://circleci.com/gh/yizhang7210/Acre)

# Acre
Algorithmically Constructed Rates Explorer


## Overview

Acre provides a service that aims to predict the profitable change in rates
of various currency pairs and instruments, using machine learning and based on
historical patterns.


## Project Setup
- Clone the project: `git clone https://github.com/yizhang7210/Acre.git`

### Server
- Make sure you have virtualenv. If not, `pip/pip3 install virtualenv`
- Under `server`, go to your virtual env by doing:
    - `virtualenv env --python=python3.4`
    - `. env/bin/activate`
- Install everything you need: `pip install -r requirements.txt`
- Setup your PostgresSQL database according to the Resources section below
as well as the configurations in `acre/settings/local.py`
- Remeber to give your user database creation access: `ALTER USER acreuser CREATEDB;`
- Set up your environment variables according to `docs/dev/Envs.md#local`
- Catch up on your database schema: `./manage.py migrate`
- You should be good to go: make sure `./manage.py test` all pass
- Even better, do `coverage run manage.py test` to run test with coverage
- You can access your coverage report at `coverage report` or `coverage html`

### Lambda
- Go through the same virtualenv setup as the server, but with python 3.6:
- Under `lambda` folder do:
    - `virtualenv env --python=python3.6`
    - `. env/bin/activate`
    - `pip install -r requirements.txt`

### Client
- The client single page app is written in Elm.
- Under `client` folder do:
    - `npm install`
    - `npm run dev` will get the local site going at `localhost:3000`


## Code Commit Checklist
- [ ] All tests pass.
- [ ] Run `pylint <app> --load-plugins pylint_django` on all sever apps with 10.0 score.
- [ ] Update documentation whenever appropriate.


## Deployment
- We use Circle CI for continuous integration and deployment. See `.circleci/config.yml`
for the configurations. For Circle CI, see the required environment variables in
`docs/dev/Envs.md#deploy`.
- For the web server, see the required environment variables in `docs/dev/Envs.md#server`

## Resources
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
