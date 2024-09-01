  [![Django CI](https://github.com/colarrbear/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/colarrbear/ku-polls/actions/workflows/django.yml)
  
An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).


 ## Requirements

Requires Python 3.10 or newer.  Required Python packages are listed in [requirements.txt](./requirements.txt). 

## Installation and Configuration
Check from [Installation and Configuration](https://github.com/colarrbear/ku-polls/wiki/Installation-and-Configuration)

## Running the Application

#### On MacOS or Linux:

1. Activate virtual environment
    ```terminal
    . venv/bin/activate
    ```

2. Start the Django development server
    ```terminal
    python manage.py runserver
    ```
3. Open the web browser and go to http://localhost:8000

4. To stop the server, press `Ctrl + C`

5. To deactivate virtual environment
    ```terminal
    deactivate
    ```

#### On Windows:

1. Activate virtual environment

    (If you are using PowerShell use this command)
    ```terminal
    venv\Scripts\activate
    ```
   (If you are using Command Prompt use this command)
    ```terminal
    venv\Scripts\activate.bat
    ```

2. Start the Django development server
    ```terminal
    python manage.py runserver
    ```

3. Open the web browser and go to http://localhost:8000
4. To stop the server, press `Ctrl + C`
5. To deactivate virtual environment
    ```terminal
    deactivate
    ```

## Demo Admin Account
| Username | Password |
|----------|----------|
| admin    | adminpassword     |

## Demo User Account
| Username | Password |
|----------|----------|
| tbc      | tbc  |
| tbc     | tbc |


## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan)
- [Iteration 4 Plan](../../wiki/Iteration-4-Plan)

note: Iteration 3 and 4 is in progress.

[django-tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
