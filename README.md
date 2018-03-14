# After School Program Check Out App

## Overview
I am an instructor for an after school program, grades k-8. One part of the job that would benefit from being automated is student check out. We check the students out by ticking a paper list. There are 1 - 2 instructors per class, and a check out app would be useful, as both instructors could check out students at the same time, with the app updating automatically.


## Features 
* **Time recorder** - Time automatically recorded when student is checked in and checked out.  
* **Link to phone** - Quick dial to parent’s phones.  
* **Absent option** – Students marked as absent.
* **Attendance history** - See which sessions each student has attended.

## Future Enhancement
* **Photo upload** - Option to add parents’ photographs, for better security. 
* **Input form** – Parents input information and notes. 

## Technologies
* Python
* Flask
* MySQL
* JavaScript & JQuery
* Bootstrap

## User Stories
* As an instructor, I can check out my students quickly and safely.  
* As an instructor, I know which students my colleague has checked out.  
* As an instructor, if an adult has not showed up for a student, I can speed dial a parent.  
* As a parent, I can up load a photograph to show the instructor what I look like, so that my child is more secure.

## Setup Locally
### How to get this app running on your machine
1.  Install Python 3.
2.  Clone this respository.   
        ``` 
        git clone https://github.com/jjames1011/attendenceapp.git
        ```
3.  Install Flask -  http://flask.pocoo.org/docs/0.12/installation 
5.  Install miniconda - https://conda.io/miniconda.html
4.  Install MAMP - https://www.mamp.info/en/
6.  Create a virtual environment.  Refer to [miniconda](https://conda.io/miniconda.html).
7.  Move in to the respository and start your virtual environment.  
        ```
        $ source activate name_of_your_enviroment 
        ``` 
8.  Install pymysql inside your virtual environment.  
        ``` 
        $ conda install pymysql
        ```
9.  Install pytz inside your virtual environment - https://pypi.python.org/pypi/pytz
10. Start MAMP.
11. To set up the database.  
        ``` 
        $ python init.py 
        ```
12. Start your local server.  
        ```
        $ python main.py 
        ```
13. You will get a message showing the address where you will be able view the website.



    



