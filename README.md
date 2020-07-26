Auto Complete Functionality 
====================================================

Features
----------------------
1) Used Trie data structure for storing locations and efficiently retrieving auto complete suggestions.
2) Implemented GET API for retrieving suggestions (Does not require authentication).
3) Implemented POST APIs for adding location, deleting location, and updating popularity for existing location (All require Authentication).
4) Wrote test cases.

Additional Features
----------------------
1) Implemented Rate Limit to avoid excessive queries.
2) Implemented Cache for search query.
3) Implemented Token based Authentication for Add, Delete, and Update APIs.
4) Implemented automated script for authentication and adding all locations provided in the data file.
5) Created dockerfile for the application.

Setup and Steps to use
-----------------------------
1) ##### Setup a conda environment or virtualenv.
2) ##### Install requirements.txt.

   Steps:-
   
   ```$ pip install virtualenv ```
   
   ```$ virtualenv myenv```

   ```$ myenv\Scripts\activate```

   ```$ pip install -r requirements.txt```
   
 3) ##### Switch to the Django project directory (auto_complete/)
 4) ##### Update Postgres config information in auto_complete/secrets.py file
 5) ##### Migrate changes to the database and create super user.
   
      Steps:-

     ```$ python manage.py makemigrations ```

     ```$ python manage.py migrate```

     ```$ python manage.py createsuperuser```
   
 6) ##### Runserver
   
    ```$ python manage.py runserver ```
   
 7) ##### Obtain Access Token using super user credentials
    
    ```$ curl --location --request POST '127.0.0.1:8000/api/login' --form 'username={username}' --form 'password={password}'```
   
 8) ##### Run script for adding all locations in the data file to database (Update username and password in the file)
   
    ```$ python script_add_locations.py --file {data file}```
   
 9) ##### Using APIs
   
    1) ##### Search API

    ```$ curl --location --request GET '127.0.0.1:8000/query?term={search string}'```

    2) ##### Add API

    ```$ curl --location --request POST '127.0.0.1:8000/add' --header 'Authorization: token {token}' --form 'location={name}' --form 'popularity={value}'```

    3) ##### Delete API

    ```$ curl --location --request POST '127.0.0.1:8000/delete' --header 'Authorization: token {token}' --form 'location={name}'```

    4) ##### Modify API

    ```$ curl --location --request POST '127.0.0.1:8000/modify' --header 'Authorization: token {token}' --form 'location={name}' --form 'popularity={value}'```
