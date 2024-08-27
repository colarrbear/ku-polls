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
   .venv\Scripts\activate.bat
   ```

5. Install required packages
   ```terminal
   pip install -r requirements.txt
   ```

6. Create a file named `.env` in the same directory as `manage.py`:

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
   python manage.py loaddata data/polls-no-vote.json 
   python manage.py loaddata data/users.json
   ```

9. Run test
   ```terminal
   python manage.py test polls
   ```

10. Run server
   ```terminal
   python manage.py runserver
   ```
   note: if css not show try to use 
   ```terminal
   python manage.py runserver --insecure
   ```
