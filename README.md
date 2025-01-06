# Django MongoDB Project Setup and Usage Guide

## Prerequisites

1. **Download the PEM file:** 
   - Locate and download the file `djangomongo.pem` from the repository.

2. **Open a Bash terminal:** 
   - Use a Bash terminal, such as Git Bash.

3. **Navigate to the PEM file location:** 
   - Example command:
     ```bash
     cd Desktop
     ```

4. **Establish an SSH connection to the server:** 
   - Use the downloaded PEM file to connect via SSH:
     ```bash
     ssh -i "djangomongo.pem" ubuntu@3.136.83.19
     ```

## Server Access and Project Setup

1. **Navigate to the project folder:** 
   - Change directory to the `Django_Mongo` folder:
     ```bash
     cd Django_Mongo
     ```

2. **Activate the virtual environment:** 
   - Run the following command:
     ```bash
     source venv/bin/activate
     ```

3. **(Optional) List files in the directory:** 
   - Use the `ls` command to view the files:
     ```bash
     ls
     ```

4. **Populate the database:** 
   - Locate the script `populate_books.py`. This script is used to populate the database:
     ```bash
     python populate_books.py
     ```
   - If you need to edit the script, you can use:
     ```bash
     nano populate_books.py
     ```

5. **Start the server:** 
   - Run the Gunicorn command to start the server:
     ```bash
     gunicorn --bind 127.0.0.1:8000 book_management.wsgi:application
     ```

## API Documentation and Testing

1. **Access the Swagger documentation:** 
   - Visit the following URL in your browser:
     ```
     http://3.136.83.19/api/schema/swagger/
     ```

2. **Authenticate in Swagger:** 
   - Use the following credentials to log in:
     - **Username:** `seek`
     - **Password:** `demodemo`

3. **Authorize using the token:** 
   - After logging in, use the token to authorize and test the endpoints.

4. **Postman Collection:** 
   - The Postman collection for the API is included in the repository:
     ```
     ApiDjangoMongo.postman_collection.json
     ```

## Running Tests

1. **Run automated tests:** 
   - Use the following command to execute tests for the `books` app:
     ```bash
     python manage.py test books
     ```