# Real_Estate_Evaluation
Real Estate Data Dashboard
Welcome to the Real Estate Data Dashboard project! This guide will walk you through setting up and running a complete data project on your computer.
This project uses Python, PySpark, and PostgreSQL to process real estate data and then displays a beautiful, interactive dashboard in your web browser.
Follow these steps exactly, and you'll have the project running in no time.
Project Files
Your project is organized in a very professional way, which is great! You have correctly separated your code from your data and used a standard src (source) folder.
Your project folder should look like this:
BIGDATACOURSEWORK/
├── .venv/
├── data/
│   ├── raw/
│   │   └── Real estate.csv
│   ├── output/
│   ├── input/
├── src/
│   └── etl/
│       ├── dashboard.py
│       ├── extract.py
│       ├── load.py
│       └── transform.py
├── requirements.txt
└── README.md

You should have your Real estate.csv file in the data/raw folder for the extract.py script to find it.

Step 1: Install the Prerequisites
You need a few programs installed on your computer to get started.
•	Python 3.10+: The main programming language.
o	Download Python
o	Important: During installation, check the box that says "Add Python to PATH."
•	PostgreSQL: This is the database we'll use to store the processed data.
o	Download PostgreSQL
o	During installation, remember the password you set for the postgres user. You will need it later.
•	Git: A tool for downloading the project files.
o	Download Git

Step 2: Set Up the Project
a. Download the Code
1.	Open your command line or terminal.
2.	Choose a location on your computer to save the project (e.g., your Desktop).
3.	Run this command to download the project folder:
4.	git clone https://github.com/your-username/your-repo-name.git

(Replace your-username/your-repo-name with your actual GitHub repository information.)
5.	Navigate into the project folder:
6.	cd your-repo-name

b. Set Up the Python Environment
This step creates a clean, isolated space for your project's dependencies.
1.	Create a virtual environment:
2.	python -m venv venv

3.	Activate the virtual environment.
o	On Windows:
o	venv\Scripts\activate

o	On macOS/Linux:
o	source venv/bin/activate

4.	Install the required Python libraries from the requirements.txt file.
5.	pip install -r requirements.txt

c. Set Up the Database
1.	Open pgAdmin, the tool that comes with PostgreSQL.
2.	Log in with the postgres username and the password you created during installation.
3.	Right-click on "Databases" and select "Create" -> "Database...".
4.	Name the new database real_estate_db.
5.	Click "Save."
6.	
Step 3: Run the Project
a. Update Your Database Password
Open src/etl/load.py and src/etl/dashboard.py in a code editor. Find the line DB_PASSWORD = "your_password"and replace "your_password" with the actual password you created for the postgres user. Do this for both files.
b. Run the Pipeline
Now, run each of the three ETL scripts one by one. Each script has a clear output to tell you that it worked. Make sure you are in the root directory of your project folder (BIGDATACOURSEWORK).
1.	Run the Extract script: This will read the raw CSV and create a Parquet file.
2.	python src/etl/extract.py

3.	Run the Transform script: This will read the Parquet file, process it, and create a new one.
4.	python src/etl/transform.py

5.	Run the Load script: This will read the final Parquet file and load the data into your PostgreSQL database.
6.	python src/etl/load.py

c. Run the Web App
This script will start a web server on your computer that hosts your dashboard.
1.	Make sure your virtual environment is still active.
2.	Run the app script:
3.	python src/etl/dashboard.py

4.	You should see a message in the terminal like Dash is running on http://127.0.0.1:8050/.
d. View the Result
1.	Open your web browser (Chrome, Firefox, etc.).
2.	Go to the following address:
3.	http://127.0.0.1:8050

4.	You should now see the beautiful, interactive dashboard!
Congratulations, you have successfully run a complete data project!

