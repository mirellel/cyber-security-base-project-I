# Cyber Security Base project I
Course project for Cyber Security Base 2023 (https://cybersecuritybase.mooc.fi/)

For this project, I used a web application that I had made for another course as a base. The application is a simple chat forum. The original project did not have the vulnerabilities listed below. 

This project is implemented with Python and Flask. For the application to work, you must have PostgreSQL installed on your computer. If you do not have it installed, see https://www.postgresql.org/download/

## Installation
- Clone this repository or download the ZIP file and extract it to a folder of your choosing
- Install needed dependencies with command ```pip install -r requirements.txt```
- Create a .env file in the root folder that has the information
  - ```DATABASE_URL='postgresql:///yourusername'```
    - If this does not work you might have to use ```postgresql+psycopq2:///yourusername``` or ```postgresql:///yourusername:yourpassword@host5432/projectname``` for DATABASE_URL
  - ```SECRET_KEY=yoursecretkey```
  - For example, you can generate a secret_key in Python with the secrets library:
    - ```>>> import secrets```
    - ```>>> secrets.token_hex(16)```
   
- In another terminal, open Postgresql database with ```start-pg.sh```
- ```flask run``` will start the application in localhost port 5000
   - Remember to have the database running in another terminal!
