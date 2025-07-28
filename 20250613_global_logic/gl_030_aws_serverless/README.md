# GlobalLogic AWS serverless ![Tests](https://github.com/alexbigkid/gl_030_aws_serverless/actions/workflows/pipeline.yml/badge.svg)
GlobalLogic job


## Deployement strategy
deploy.sh is very flexible it will run all scripts which begin with 3 digits in order,
to make sure the needed infrastructure is available before deploying services

| Script name            | description                                              |
| :--------------------- | :------------------------------------------------------- |
| Deploy.sh              | the main script, which is the entry point of deployement |
| CommonLib.sh           | common functionality                                     |
| InstallTools.sh        | Installs any other needed tools                          |
| 001_DeployTerraform.sh | deployes terraform infrastructure                        |
| 002_DeployLambdas.sh   | deploys all services                                      |


## Directory structure
| Directory name    | description                    |
| :---------------- | :----------------------------- |
| docs              | documents for the project      |
| integration-tests | location for integration tests |
| services           | project services directory      |
| terraform         | terraform modules              |


### Terraform directory structure
The templates directory has all modules definitions. The dev, stage and prod would directories would actually create Cloud infrastructure for those environments using module templates.
- terraformStateBootstrap: This is an initial module, which creates S3 bucket and dynamoDB table.
   - S3 resource: the terraform state files will be stored centrally on S3 bucket.
   - dynamoDB resource: table will lock the S3 bucket content for a resource during the deployment and unlock after deployment finishes. This prevents simultanious deployment from team members.
- postgreDB in templates directory: is module for deployment of postgreeDB
- 001_postgreDB in dev/stage/prod directories to deploy RDS DB resource in those environments using the module from templates
  - includes also the locking mechanism for CI/CD deployement.
