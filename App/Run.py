import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar

# "from sklearn.externals import joblib" (an alternative if error occured)
import joblib       
from sqlalchemy import create_engine

#divide strings into lists of substrings
app = Flask(__name__) 

def tokenize(text):
    # Divides strings into lists of substrings
    tokens = word_tokenize(text)        
    # Converts the substrings words to its base form
    lemmatizer = WordNetLemmatizer()    

    clean_tokens = []
    for tok in tokens:
        # Lemmatization, lowering case, removing spaces or specified characters at the start and end of a string
        clean_tok = lemmatizer.lemmatize(tok).lower().strip() 
        clean_tokens.append(clean_tok)

    return clean_tokens

# Loading data
engine = create_engine('sqlite:///../Data/disaster_messages_database.db')
df = pd.read_sql_table('disaster_messages_tbl', engine)