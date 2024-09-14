## Installation and Configuration
1. Clone the repository
   ```terminal
   git clone https://github.com/colarrbear/ku-polls.git
   ```
   
2. Change directory to `ku-polls`
   ```terminal
   cd ku-polls
   ```

3. Create virtual environment
   ```terminal
   python -m venv venv
   ```

4. Activate virtual environment

   On MacOS or Linux:
   ```terminal
   . venv/bin/activate
   ```
   On Windows:
   ```terminal
   venv\Scripts\activate
   ```

5. Install required packages
   ```terminal
   pip install -r requirements.txt
   ```

6. Set Up the Secret Key (For Development) -- 
    Create a file named `.env` in the same directory as `manage.py`:

    If you don’t have a SECRET_KEY, you can set one up temporarily by
    - 6.1 Open the Python shell by running `python` in the terminal.
    - 6.2 Run the following code in the Python shell:
   
    ```terminal
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ``` 
    or you can use this key:
    ``` 
    $n3b&cwrldqee&^_t#0s68f5z_xpwn!@-*!-$1bn9t83o=9t#n
    ``` 

    - 6.3 Copy the output and paste it in the `.env` file as follows:
   
    ```terminal
    On Linux/MacOS:
    ```terminal
    cp sample.env .env
    ``` 
    On Windows:
    
    ```terminal
    copy sample.env .env
    ```

7. Run database migration
   ```terminal
   python manage.py migrate
   ```

8. Load initial data
   ```terminal
   python manage.py loaddata data/users.json
   ```

   ```terminal
   python manage.py loaddata data/polls-v4.json
   ```

9. Run test
   ```terminal
   python manage.py test polls
   ```

10. Run server
   ```terminal
   python manage.py runserver
   ```
   note: If css not show, try to use 
   ```terminal
   python manage.py runserver --insecure
   ```
