import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
      Function:
      load_data: The function loads data from two csv files subsequenly merging them.

      Args:
      messages_filepath (str): the file path of "messages" csv file.
      categories_filepath (str): the file path of "categories" csv file.

      Return:
      df (DataFrame): A dataframe of merged "messages" and "categories".
      """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, how='inner', on='id')
    return df

def clean_data(df):
    """
      Function:
      clean_data: The function cleans the given Dataframe .

      Args:
      df (DataFrame): The dataframe of "messages" and "categories" require cleaning.

      Return:
      df (DataFrame): The cleaned "messages" and "categories" dataframe. 
      """

    # Expanding the dataframe to form 36 individual category columns
    categories = df['categories'].str.split(';', expand=True)

    # Taking out the first row of the categories dataframe
    row = categories.head(1)

    # Extracting a list of new column names
    category_colnames = row.applymap(lambda x: x[:-2]).iloc[0, :]
    category_colnames = category_colnames.tolist()

    # Assigning the column names for 'categories' dataframe
    categories.columns = category_colnames

    # Extracting the last character of the cells
    # Converting the cells from string to numaric
    for column in categories:
        categories[column] = categories[column].astype(str).str[-1]
        categories[column] = categories[column].astype(int)

    # Dropping the categories from the original `df`
    df = df.drop(['categories'], axis=1)

    # Concatenate the original `df` with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1, join='inner')

    # Removing the duplicates
    df.drop_duplicates(inplace=True)

    return df

def save_data(df, database_filename):
    """
       Function:
       save_data: The funtion saves the Dataframe df in a database.

       Args:
       df (DataFrame): The dataframe of merged 'messages' and 'categories'.
       database_filename (str): The database file name.

       """
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('disaster_messages_tbl', engine, index=False, if_exists='replace')

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')

if __name__ == '__main__':
    main()