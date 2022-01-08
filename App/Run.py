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

# Loading model
model = joblib.load("../Models/classifier.pkl")

# Indexing webpage that displays visuals and receives user input text for model
# Flask decorator to assign URLs - dictates @app when user visits (app.com) at the given .route() execute the home() function
@app.route('/')
@app.route('/index')

def index():
    
   # Extreacting specific data for visualization 
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # Categories column names
    catg_nam = df.iloc[:, 4:].columns
    # Selecting those with none-zero values
    bol = df.iloc[:, 4:] != 0
    # Extracting the number of none-zero values
    cat_bol = bol.sum().values
    # Extracting sum of all values per column
    sum_cat = df.iloc[:, 4:].sum()
    # Extracting top-10 values
    top_cat = sum_cat.sort_values(ascending=False)[1:11]
    # Extracting those columns name
    top_cat_names = list(top_cat.index)

    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=catg_nam,
                    y=cat_bol
                )
            ],

            'layout': {
                'title': 'Message Categories distribution',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Categories"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=top_cat_names,
                    y=top_cat
                )
            ],

            'layout': {
                'title': 'Top 10 Categories',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Categories"
                }
            }
        }
    ]

    # Encoding plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Rendering web-page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)

# Indexing webpage that handles user query and displays model results
@app.route('/go')

def go():
    # This saves user input in query (A MultiDict is a dictionary subclass customized to save all values for a key)
    # "get()"" method returns the default value (second argument) if the requested data does not exist.
    query = request.args.get('query', '') 

    # Using the model to predict the query - the result is an array as many as our label columns 
    classification_labels = model.predict([query])[0]
    # Assigning each label to its corresonding column name to form an iterable: Dict
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # Rendering the go.html web-page 
    return render_template('go.html', query=query, classification_result=classification_results)

def main():
    app.run(host='0.0.0.0', port=3001, debug=True)

if __name__ == '__main__':
    main()
