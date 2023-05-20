# This is the final project for CPSC 449 - Web Backend Engineering. 

* Here, we will be developing an online bookstore API with functionalities like view, search, and update books. 
* We will be using FastAPI for building it.
* MongoDB will be used for storing the data.

Group Members:

<li>Jeet Hirakani</li>
<li>Tejaskumar Patel</li>
<li>Ashil Shah</li>

# Required Software
 1. [MongoDB Community Edition](https://www.mongodb.com/try/download/community) 
 2. [FastAPI](https://fastapi.tiangolo.com/lo/#installation) 

# Steps to run the project

To run the project:

1. Run the command in order to create the conda environment. you can also use any other virtual environment if you like

`conda create -n restflask python=3.9`

2. Run the command to install the required commands.

`pip install -r requirements.txt`

3. Run the project with the command.

`uvicorn index:app --reload`

4. After running the project, use the SwaggerUI for viewing and testing the APIs

`http://127.0.0.1:8000/docs#/default`

  You can view and test all the APIs locally on your browser.
