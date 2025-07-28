# Serverless - GL Python Template
This project created to easily create new services using [Serverless framework](https://www.serverless.com/).
For detailed instructions, please refer to the [documentation](https://www.serverless.com/framework/docs/providers/aws/).

## Installation/deployment instructions
To create new service, please execute shell script in the service directory: `./createNewService.sh py name-of-your-new-service`

> **Requirements**: Python `(v 3.11.x)` and [uv](https://github.com/astral-sh/uv) for dependency management.
> 
> **Quick Setup with UV (Recommended)**:
> 1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
> 2. Sync dependencies: `make sync`
> 3. Run tests: `make test`
>
> **Alternative with pyenv** (if you prefer traditional virtual environments):
> - Install pyenv: `brew install pyenv` (macOS) or `apt-get install pyenv` (Linux)
> - Install Python: `pyenv install 3.11.5`
> - Create virtual environment: `pyenv virtualenv 3.11.5 cloud`
> - Activate for directory: `pyenv local cloud`
> - Then use: `make install_test` and `make test`


### Using make rules
| dependency installations | description                                                               |
| :----------------------- | :------------------------------------------------------------------------ |
| `make install`           | install project dependencies                                              |
| `make install_test`      | install project dependencies and dependencies required for unit tests     |
| `make install_all`       | install project dependencies, unit tests and all development dependencies |

| domain commands      | description                                                           |
| :------------------- | :-------------------------------------------------------------------- |
| `make create_domain` | creates custom domain for the service in currently active environment |
| `make delete_domain` | deletes custom domain for the service in currently active environment |

| deployment commands | description                                            |
| :------------------ | :----------------------------------------------------- |
| `make deploy`       | deploys service to currently active environment        |
| `make deploy_env`   | deploys service to environment, which is set in .envrc |
| `make deploy_dev`   | deploys service to dev environment                     |
| `make deploy_qa`    | deploys service to qa environment                      |
| `make deploy_prod`  | deploys service to prod environment                    |

| remove commands    | description                                              |
| :----------------- | :------------------------------------------------------- |
| `make remove`      | removes service from currently active environment        |
| `make remove_env`  | removes service from environment, which is set in .envrc |
| `make remove_dev`  | removes service from dev environment                     |
| `make remove_qa`   | removes service from qa environment                      |
| `make remove_prod` | removes service from prod environment                    |

| unit tests commands | description                                                     |
| :------------------ | :-------------------------------------------------------------- |
| `make test`         | runs unit tests                                                 |
| `make test_v`       | runs unit tests verbosely                                       |
| `make test_ff`      | runs unit tests fast fail, 1st test failing will stop the tests |
| `make test_vff`     | runs unit tests verbosely and with fast fail option             |
| `make coverage`     | runs unit tests with test coverage                              |

| other commands  | description                                                   |
| :-------------- | :------------------------------------------------------------ |
| `make clean`    | cleans project from all python and serverless build artifacts |
| `make settings` | displays some settings                                        |
| `make help`     | displays help page with make rules options                    |


### Remotely
Copy and replace your `url` - found in Serverless `deploy` command output - and `name` parameter in the following `curl` command in your terminal, Postman or vscode extention: `Thunder Client` to test your newly deployed application. Don't forget to use authentication token.

### Project structure

```
.
├── Makefile                             # Makefile, which creates project rules
├── README.md                           # This file
├── package-lock.json
├── package.json                        # some serverless plugin dependencies
├── publish.sh                          # shell script to deploy service
├── requirements.txt                    # project python dependencies
├── requirements_all.txt                # all python dependencies for development
├── requirements_test.txt               # project dependencies and dependencies for unit tests
├── serverless.yml                      # serverless config
├── src                                 # directory with production code sources
│   ├── gl_hello.py         # example lambda IO (Lambda Request and Response definitions)
│   └── gl_hello_io.py          # example lambda code
└── tests                               # unit tests directory
    ├── context.py                      # helper python file to link to production code
    └── test_gl_hello.py    # unit tests for example lambda

```
