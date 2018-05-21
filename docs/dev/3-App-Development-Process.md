# Application Development Process

### Project Management
We use Github Project to track our tasks.

Each `Project` is characterized by a `goal` that Acre would achieve as a
result of the completion of the project. And each `Issue` under the project
would be a task or a change that needs to be made to further that goal.

### Development Practices
We use a simple branching and development model where we have:
- `master` as the long running branch that represents Production.
- Developers branch directly off of `master` for feature development.
- Pull requests (PRs) are opened from the feature branch against
`master` WHILE a feature is being implemented for continuous feedback.
- PRs are continuously built, verified, and deployed to a test environment
from Circle CI.
- Every PR merge into `master` triggers a deployment to production.

### Deployment
We use Circle CI for building the Acre application, running tests and
deploying it to AWS (see [here](../../.circleci/config.yml) for more details.)
- The `server` app gets deployed to an AWS Elastic Beanstalk container.
- The `client` app gets deployed and hosted as a static site on AWS S3.
- The `lambda` app gets deployed to AWS Lambda and configures a few AWS
CloudWatch event rules to work with it.

For detailed deployment process, see the `deploy.sh` script under each app's
folder.

For required environment variables in each environment, see the
documentation [here](./Environment-Variables.md)
