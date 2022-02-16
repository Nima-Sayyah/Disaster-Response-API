# Disaster Response (API)
### Table of Contents

1. [Project Description](#description)
2. [Installed Libraries](#libraries)
3. [Files Descriptions](#files)
4. [Analysis Workflow](#analysis)
5. [Instructions](#instructions)
6. [License](#license)

### Project Description<a name="description"></a>

The intention of the project is to classify the disaster messages into specific categories. The project utilises disaster data from [Figure Eight](https://www.figure-eight.com/) to build a model for an API that classifies disaster messages.

Users can input messages via a web app and observe classification results in classified categories. The web app also display visualizations of the data. 

### Installed Libraries <a name="libraries"></a>

The libraries can be installed via virtual environment or in your local python directory. All libraries are available in Anaconda distribution of Python. The codes are expected to run with Python version 3 or above. The used libraries are:

- pandas 
- re
- sys
- json
- sklearn
- nltk
- sqlalchemy
- pickle
- Flask
- plotly
- sqlite3

### Files Descriptions <a name="files"></a>

The files structure is arranged as below:

    - README.md: read me file
	
    - ETL Pipeline.ipynb: contains ETL pipeline preparation code
	
    - ML Pipeline.ipynb: contains ML pipeline preparation code
	
    - \Data
		- categories.csv: categories dataset
		- messages.csv: messages dataset
		- disaster_messages_database.db: disaster response database
		- Process_Data.py: ETL process
    
    - \Models
	        - Train_Classifier.py: classification code
            - classifier.pkl: exported classifier model
    
    - \App
	        - run.py: flask file to run the app
	        - \Templates
			    - master.html: main page of the web application 
			    - go.html: result web page

### Analysis Workflow<a name = "analysis"></a>
The project encompasses three main parts:

1. **ETL Pipeline:** `Process_Data.py` file contains the script to create ETL pipline, which:

- Loads the `messages` and `categories` datasets
- Merges the two datasets
- Cleans the data
- Stores it in a SQLite database

2. **ML Pipeline:** `Train_Classifier.py` file contains the script to create ML pipline, which:

- Loads data from the SQLite database
- Splits the dataset into training and test sets
- Builds a text processing and machine learning pipeline
- Trains and tunes a model using GridSearchCV
- Outputs results on the test set
- Exports the final model as a pickle file

3. **Flask Web App:** the web app enables the user to enter a disaster message, and then view the categories of the message.


### Instructions <a name="instructions"></a>

To execute the app follow the instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python Data/Process_Data.py Data/messages.csv Data/categories.csv Data/disaster_messages_database.db`
    - To run ML pipeline that trains classifier and saves
        `python Models/Train_Classifier.py Data/disaster_messages_database.db Models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python Run.py`

3. Go to http://0.0.0.0:3001/

### Licensing, Authors, Acknowledgements, etc.<a name="license"></a>
Acknowledgement should go to Udacity for the project inspiration.