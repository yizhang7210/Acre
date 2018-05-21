# Environment Variables
We use environment variables for credentials and settings. Here is the list of
what needs to be where. To make sure an environment variable exists, add the
following line to your `~/bash.rc` or equivalent: `export ENV_VAR=<ENV_VAR_VALUE>`.

### Local
Locally everything runs under the `local` settings. You need the following
environment variables for connecting to OANDA, the rates provider.
```
TOKEN_GAME=<your-oanda-game-environment-token>
```

### Deploy
On CircleCI we use the `deploy` settings. The following are required:
```
ACRE_ENV=DEPLOY
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
TOKEN_GAME=<your-oanda-game-environment-token>
```

### Server
On Acre's application server, the following are required:
```
ACRE_ENV=DEV or PROD
DJANGO_SETTINGS_MODULE=acre.settings
RDS_DB_NAME=<db-name>
RDS_HOSTNAME=<db-hostname>
RDS_PASSWORD=<db-password>
RDS_PORT=<db-port>
RDS_USERNAME=<db-username>
TOKEN_GAME=<your-oanda-game-environment-token>
```
