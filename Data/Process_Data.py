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

    # Split `categories` into separate category columns.
    categories = df['categories'].str.split(';', expand=True)

    # Cut the last character of each category
    # select the first row of the categories dataframe
    row = categories.head(1)
    category_colnames = row.applymap(lambda x: x[:-2]).iloc[0, :]
    category_colnames = category_colnames.tolist()

    # Rename the columns of `categories`
    categories.columns = category_colnames

    # Convert category values to just numbers 0 or 1.
    for column in categories:
        categories[column] = categories[column].astype(str).str[-1]
        categories[column] = categories[column].astype(int)

    # drop the original categories column from `df`
    df = df.drop(['categories'], axis=1)

    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1, join='inner')

    # Drop the duplicates.
    df.drop_duplicates(inplace=True)

    return df