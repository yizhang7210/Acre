# Project Structure
Acre consists of 3 parts, the event trigger, the application server,
and a web client.

### The Event Trigger
The event trigger (at `lambda/`) is the overall entry point of Acre.

Everyday at 5pm New York time, an event rule set up on AWS CloudWatch
triggers the `Acre-Daily` function deployed on AWS Lambda, which in turn
sends an End-of-Day request to the Acre server to update its predictions
for the next day.

### The Application Server
The server (at `server/`) is a Django project that hosts the logic of
Acre's prediction capabilities. It includes the following Django apps:

#### api
This is Acre's product interface, the predictions web API. It's full
endpoints documentation is hosted on `/v1/docs`.

#### algos
The `api` passes prediction update and retrieval requests to the
individual `algos` to process. Each algorithm (named after mathematicians, e.g.
Euler) is characterized by the set of `datasource` it utilizes, and as a result,
each algorithm is responsible for its own data transformation process.

#### datasource
This is the app that integrates with all Acre's data source providers
and persist all required raw data for `algos`.

#### core
This is Acre's shared utility app with convenience functions covering
areas such as date, time and mathematical calculations.

#### scripts
These are utility scripts that seed some necessary data for Acre.

### The Web Client
The web client (at `client`) written in Elm serves as a presentational
example of how Acre's predictions can be queried and visualized.
