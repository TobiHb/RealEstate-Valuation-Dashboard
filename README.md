# 1118 Applications of Data Science: Robotic Process Automation with Machine Learning
# Project Assignment
## Tobias Hundsberger
## h12042646
<img width="1414" alt="image" src="https://github.com/user-attachments/assets/2e9557aa-e5f8-4bec-925d-3fc00b20b180" />


# Real Estate Valuation Model
In this project a Flask Server with a connected SQLite database is created. Beside servign as collector of property properties, it integrates an DecisionTree-Regressor ML-Model which calculates a property price based on the properties of the specific property, which is typed into the formula within the web application.
This internally calculated model price can be compared with the price when it was typed in within the formular on the Webpage by the script (optional to type in this extra price).
The purpose is to compare this price which is demanded by the property seller with the calculated model price to check if the demanded price is reasonable.

# Dataset Model was trained on:
https://www.kaggle.com/datasets/nelgiriyewithana/new-york-housing-market



# Data Cleaning
In data-Folder:
-Data.ipynb = Used for data cleaning and preprocessing the raw dataset NY_House_Dataset.csv into the Clean_NY.csv

# DecisionTree-GRID_Search.ipynb
The Decision-Tree algorithm then is trained on the Clean_NY.csv dataset.
Then the model is pickled into dt_model.pkl.

# Flask_Main.py is the Application-Server which implements the HTML templates and CSS stylesheets from the folders 'static' and 'templates'
It also implements the Model.py file which contains the ML-Model application. It imports the dt_model.pkl and adds a kind of wrapper for the Flask-Application

# property.db is the SQL-Database for the Flask-Applikations
It can be deleted if it causes errors. Flask Applikations will create new property.db File automatically.




# Application Instruction:

Run:
Start Flask Server with:

**python Flask_Main.py**

Now open the Server with a webbrowser.

**Variant 1:**
Run the Robot Skript with manually scrapped and saved data from https://www.redfin.com/city/30749/NY/New-York.

Run:
robot Robot_Manual_Skript.txt

**Variant 2:**
Run the Robot Skript with automatically scrapped data from https://www.redfin.com/city/30749/NY/New-York.
Links probably need to be refreshed manually on the website since older links will get invalid in short periods of time. 

Run (after exchanging Links):
robot Robot_Automatic_Skript.txt

**Variant 3:**
Manually add data into the formular on 'Add Property'.

Skript now automatically adds property values in the NewProperty page within the Flask Server.
After submitting one Property Object, the Machine Learning model calculates a new price based on the properties of the property.

You are also welcome to put data in the website formular manually and check.
