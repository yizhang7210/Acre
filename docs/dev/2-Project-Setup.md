# Project Setup

### Dependencies
- `nix`: Download from [here](https://nixos.org/nix/download.html)
- An OANDA practice account:
    - Go [here](https://www.oanda.com/register/#/sign-up/demo) and sign up for a practice account.
    - Then log in from [here](https://trade.oanda.com/), selecting 'Practice'
    - Then go to 'My Account' -> 'Manage API Access' -> 'Generate'.
    - Record your access token in a safe place.
- node `v6.9.1`: We recommend using `nvm` for managing node versions.
    - Use install script [here](https://github.com/creationix/nvm#install-script) to install nvm.
    - Install node `v6.9.1` by doing `nvm install v6.9.1`.
    - Add the line `nvm use v6.9.1` to your `~/bash.rc` or equivalent.
- npm `5.6.0`:
    - `npm install -g npm@5.6.0`

### Database
- Right under `Acre` run `nix-shell acre.nix` to go into the nix shell for the following:
- `$ sudo -u postgres psql` to log in to the DB shell.
- `postgres=# CREATE DATABASE acre;`
- `postgres=# CREATE USER acreuser WITH PASSWORD 'acrelocaldb';`
- `postgres=# GRANT ALL PRIVILEGES ON DATABASE acre TO acreuser;`
- `postgres=# ALTER USER acreuser CREATEDB;`
- `postgres=# \q` to quit the DB shell.

### Server
- Right under `Acre` run `nix-shell acre.nix` to go into the nix shell for the following:
- Make sure you have `virtualenv`. If not, do `pip3 install virtualenv`
- Under `server` folder, go to your virtual environment by doing:
    - `virtualenv env --python=python3.4`
    - `. env/bin/activate`
- Install everything you need: `pip install -r requirements.txt`.
- Set up your local environment variable according to [here](./Environment-Variables.md#local).
- Catch up on your database schema: `./manage.py migrate`.
- To run all tests, do `./manage.py test`.
- To run all tests with coverge, do `coverage run manage.py test`, and access
the coverage report at `coverage report` or `coverage html`.
- To run the server locally, do `./manage.py runserver`, and access it by
going to `localhost:8000/v1/docs` on your browser to see the API documentation.

### Lambda
- Right under `Acre` run `nix-shell acre.nix` to go into the nix shell for the following:
- Under `lambda` folder do:
    - `virtualenv env --python=python3.4`
    - `. env/bin/activate`
    - `pip install -r requirements.txt`

### Client
- Get out of the `nix` shell by simply typing `exit` if you were in.
- The client site is a single page Elm app.
- Under `client` folder do:
    - `npm install` will install all dependencies.
    - `npm run dev` will get the local site going at `localhost:3000`.
