# News Portal

Note: It is developed only for Windows operating system.

To run this program you will have to follow step by step:

1. This project is required a python programming language and python version is 3.6+. So you will have to download it from https://www.python.org/downloads/source/ and install it.

2. Then You will need MySQL database (I used Xampp ) to connect this program for sending and retrieving data. Download it from https://www.apachefriends.org/index.html and install it.

3. To check python version you have to use cmd(command line interface). Go to search programs or files then enter type cmd you will see command line windows box.
Enter command line type: python --version. If python version is shown up then it is already installed. Here example picture is given below:


![cmd](https://user-images.githubusercontent.com/53641071/130817465-79e4c71d-e046-410e-8151-b56fcb7d8a0e.png)

4. You have to check pip(python package manager) version which is recommended to use python framework or third party library to run this project.

![pip](https://user-images.githubusercontent.com/53641071/130818576-0667ff88-8478-4eff-b619-f390ede8cd32.png)

5. You have to create python virtual environment. This purpose is to create an isolated environment for Python projects. Enter type 'pip install virtualenv' in cmd.

![env](https://user-images.githubusercontent.com/53641071/130819998-a2229af4-876d-48bb-8318-b68b37ab1923.png)

To make environment this project. Type 'python -m venv newsenv' in cmd. It should be like

![pip](https://user-images.githubusercontent.com/53641071/130821212-a29faa16-3580-431e-ab39-508f629d0d43.png)


Activate this python environment. I will show this picture

![pip](https://user-images.githubusercontent.com/53641071/130822133-bad6cc13-ff7c-4e3f-9fa8-302b7cfc05d6.png)

You will see from above picture from last line in cmd that is actiavted.



6. You have to download or clone from this repository. Go to link page https://github.com/safinmnabi/djangonews and download zip or clone file then extract file into newsportal directory. typing 'cd newsportal-main' means to go newsportal directory where you will see file in there. It should be like this

![pip](https://user-images.githubusercontent.com/53641071/130827505-ad1f6438-1f3c-4f57-bdf6-d54af00cc329.png)


![pip](https://user-images.githubusercontent.com/53641071/130827857-d88f933e-0635-4fcf-900e-614935aca77e.png)


7. Type 'pip install -r requirements.txt' in cmd and wait for it to download.

8. You have to create an account from SendGrid and NewsAPI to get API key.

9. Go To open .env file in project then place on NEWS_API ,SENDGRID_API,SENDGRID_FROM_EMAIL

Be sure SENDGRID_FROM_EMAIL must be register sender email in SendGrid Panel

10. Go to Xampp Control Panel, then start apache and mysql module. Go to http://localhost/phpmyadmin/index.php and enter username is root and leave blank password to sign in. Create a database name is newsportal.

11. Go to newsportal-main directory and again to go in newsportal to see settings.py file. Enter settings.py file to add python script for configuraing database settings. and modify database script will be like

![pip](https://user-images.githubusercontent.com/53641071/130833946-59657da0-9fd8-41bd-bd4d-a8a9c273a0e8.png)


12. Type 'python manage.py makemigrations' in cmd to create model data.

13. Again Type 'python manage.py migrate' in cmd to create database table.


14. Run manage.py file to runserver using cmd then you will see it is running developement server like this picture

![pip](https://user-images.githubusercontent.com/53641071/130829407-989b4690-d392-4c88-8e08-b09291607e37.png)


15. Go to localhost or http://127.0.0.1:8000 in web browser address. You will see a Login page. You will see Register page to create a account inside login page. Then enter email and password in login page then you will see news portal page.
 
16. This project is already exposed API and url address will be http://127.0.0.1:8000/api/ where do you want to use Postman and curl to fetch api. You will need email and password to get data.
