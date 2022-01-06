import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle

nltk.download(['wordnet', 'punkt', 'stopwords'])

def load_data(database_filepath):
    """
       Function:
       load_data: This function loads data from database

       Args:
       database_filepath: the path of the database

       Return:
       X (DataFrame) : Message features dataframe
       Y (DataFrame) : target dataframe
       category (list of str) : target labels list
       """
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('disaster_messages_tbl', engine)
    X = df['message']  # Message Column
    Y = df.iloc[:, 4:]  # Classification label
    return X, Y

def tokenize(text):
    """
    Function: 
    tokenize: This function splits text into words and return the root form of the words
    
    Args:
      text(str): the message
    
    Return:
      lemm(list of str): a list of the root form of the message words
    """

    # Normalize text
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

    # Tokenize text
    words = word_tokenize(text)

    # Remove stop words
    stop = stopwords.words("english")
    words = [t for t in words if t not in stop]

    # Lemmatization
    lemm = [WordNetLemmatizer().lemmatize(w) for w in words]

    return lemm

def build_model():
    """
     Function: 
     build_model: This function builds a model for classifing the disaster messages

     Return:
       cv(list of str): classification model
     """

    # Create a pipeline
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
    ])
    # Create Grid search parameters
    parameters = {
        'tfidf__use_idf': (True, False),
        'clf__estimator__n_estimators': [50, 60, 70]
    }

    cv = GridSearchCV(pipeline, param_grid=parameters)

    return cv

