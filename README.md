SYSTEM REQUIREMENTS:

Software Requirements:
Platform		-Windows 7/10
Front End		-HTML, Bulma CSS
Development Tool	-Jupyter Notebook
Back End		-Flask, SQLite3
Programming Language    -Python

Hardware Requirements:
Name of the Processor –Intel core i3 
Hard Disk Capacity	 -1 TB
RAM Capacity	 -8.00GB


Download:
•	Download and install Anaconda from  Anaconda.com/downloads
•	Go to Anaconda Prompt and install the following packages
	numpy==1.16.2
	pandas==0.24.2
	pickle
	matplotlib==3.2.1
	sklearn
	flask
	requests
	flask_login 
	geocoder
	sqlite3
	flask_sqlalchemy 
	flask_login 

Datasets used File Names: dengue_features_train.csv, dengue_labels_train.csv
(SOURCE: https://www.kaggle.com/hafizwaqas101/dengueai)

How to Use:
After Installing all the software set up the project as follows
•	Open the command prompt at the folder name-auth as shown below
	> C:\Users\Akhila\Desktop\mini-project\auth\>
•	Then, enter on the command prompt the following
	>set FLASK_APP=project
	>flask run
•	Open the URL shown in the propmt 
	http://127.0.0.1:5000/

This will open the project on the browser, to access it signup and then login.

  • The user can check for no of dengue cases [Home Page/Tab]
  • The user can check statistics, check for symptoms [Check Page/Tab]
  • The user can also check for their past history of symptoms [History Page/Tab] 


