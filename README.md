# Stackover-challenge3-
# Stackover-challenge3 APP
Stackover-challenge3 is a community encyclopedia application that provides where users can post questions and receive answers from other users knowledgeable in that areas.

**Application Features**

* Post Questions
* Post Answers
* Accept an answer
* Update an Answer
* Search a question by an ID
* Retieve All Questions
* New user can sign up
* User Can Login

# A user can do the following :

- Can view all questions
- Can Search a question by an ID
- Can sign up
- Can Login
- Can Update an Answer
- Can Login

**Application demo**
* To interact with the application via postman
     * https://rugandaride.herokuapp.com/api/v2/rides/

    then use the following endpoints to perform the specified tasks
    
    EndPoint                                           | Functionality
    ------------------------                           | ----------------------
    POST /auth/signup                               | Create a user account
    POST /auth/login                                   | Log in a user
    GET /questions                                | Fetch all questions
    GET /questions/<questionId>                                      | Fetch a specific
question
    POST /questions                               | Post a question
    Delete /questions/<questionId>                  | Delete a question
    GET  /questions/<questionId>    | Retrieve passengers who requested to join the ride
    


**Getting started with the app**

**Prerequisites**

* [Python 3.6](https://docs.python.org/3/)

* [Flask](http://flask.pocoo.org/)

* [PostgreSQL](https://www.postgresql.org/)

* [JWT](auth0.com/docs/jwt)

# Installation

Create a new directory and initialize git in it. Clone this repository by running
```sh
$ git clone https://github.com/fahadmak/Stackover-challenge3-.git
```
Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using
```sh
$ virtualenv venv
```
Activate the virtual environment
```sh
$ cd venv/scripts/activate.bat
```
Install the dependencies in the requirements.txt file using pip
```sh
$ pip install -r requirements.txt
```

Start the application by running
```sh
$ python run.py
```
