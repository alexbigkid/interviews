# :octocat: Ingredients for cooking :octocat: ![Tests](https://github.com/alexbigkid/ingredients_for_cooking/actions/workflows/pipeline.yml/badge.svg)
Creates a shopping list with your favorite ingredients for recipes you liked.

## APY KEY note
To be able to execute this python program an API KEY for the Spoonacular
http service is required. Since it is sensitive information and should
not be added to the plain view of source code, you would need to set up
an environment variable in you terminal with following command:<br>
```html
On *nix OS
    export SPOONACULAR_API_KEY=spoonacular_api_key_here
On Windows
    set SPOONACULAR_API_KEY=spoonacular_api_key_here
```

Or alternatively you can create file ***.env*** in root directory of this project
and add following line into the ***.env*** file:<br>
```html
   SPOONACULAR_API_KEY=spoonacular_api_key_here
```

## Prerequisites
| tool   | description                                        |
| :----- | :------------------------------------------------- |
| make   | tool to execute compile instructions from Makefile |
| pip    | python package installer                           |
| python | python interpreter (3.8.8 was used)                |

- The project should work on MacOS and Linux and any other unix like system
- I haven't tried Windows, since I don't own a windows machine
- All required packages to run the app are in requirements.txt
- All require packages to run test are in requirements_dev.txt


*** In case the system is setup that python is linked to python version 2.* ***
*** and python3 is linked to version 3.*, please use the 2nd set of rules postfixed with 3 ***
*** on the command line execute "make help" to see all Makefile rules defined ***


## Instructions for users (if make tool is installed)
| command      | description                         |
| :----------- | :---------------------------------- |
| make install | installs needed python dependencies |
| make my_dish | starts the program                  |


## Instructions for users (make tool is not available)
| command                                | description                         |
| :------------------------------------- | :---------------------------------- |
| pip install --user -r requirements.txt | installs needed python dependencies |
| python ./src/main.py                   | starts the program                  |



## Instructions for developers
| command           | description                                  |
| :---------------- | :------------------------------------------- |
| make help         | to see all make rules                        |
| make my_dish      | executes the main program                    |
| make install      | installs required packages                   |
| make install_dev  | installs required development packages       |
| make test         | runs test                                    |
| make test_verbose | runs test with verbose messaging             |
| make coverage     | runs test, produces coverage and displays it |


## Notes for i:robot: reviewers
Since I was not very familar with unittest frame work (I used pytest in the past)
I experemented with different way writing unittests: using mocks, patches and DIs.
Usually I'd write code with one style for better readability.

There are minimal code comments, I was following the Agile
[Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
guide lines from Uncle Bob. Code, function and variable naming should be descriptive.
The comments can lie, since code can be updated, but developer can forget to update comments.

#### Test ran on:
- [x] MacOS Big Sur (local machine and pipeline) / Python 3.8.8
- [x] Linux Ubuntu 20.04 (pipeline machine) / Python 3.8.5
- [x] Windows 10 (pipeline) / Python 3.7
- [x] Raspberry Pi Zero W (via ssh) / Python 3.7.3


#### program tested running on:
- [x] MacOS Big Sur (local machine) / Python 3.8.8
- [ ] Linux Ubuntu 20.04  / Python 3.8.5
- [ ] Windows 10 (pipeline) / Python 3.7
- [x] Raspberry Pi Zero W (via ssh) / Python 3.7.3


## API used
This project utilizes [Spoonacular API](https://spoonacular.com/food-api/docs) to get recipes from ingredient list. Following API are used:
- [Get recipes from ingredients API](https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients)
- [Get recipe price breakdown API](https://spoonacular.com/food-api/docs#Get-Recipe-Price-Breakdown-by-ID)


## Screenshot of functioning app
![The screenshot](docs/running_app.jpg?raw=true "running app")

:checkered_flag:
