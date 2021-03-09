"""
A module for exploring the netflix and imdb movies
""" 

#%%
#import relevant modules
import pandas as pd
import unidecode as udc
import plotly.express as px
import seaborn as sns
import re 
import os
import nltk
import plotly.express as px
from nltk.corpus import stopwords
import plotly.figure_factory as ff


# %%
def removeStopwords(string):
    en_stops = stopwords.words("english")
    string = re.sub("[^A-Za-z0-9\s]", "", string)
    return [item for item in string.split() if item not in en_stops]

def standarizeString(string):
    string = udc.unidecode(string)
    return re.sub('[^A-Za-z0-9\s]+', '', string).casefold()

def preprocessNetflix(filename):
    ratings_ages = {
    'TV-PG': 'Older Kids',
    'TV-MA': 'Adults',
    'TV-Y7-FV': 'Older Kids',
    'TV-Y7': 'Older Kids',
    'TV-14': 'Teens',
    'R': 'Adults',
    'TV-Y': 'Kids',
    'NR': 'Adults',
    'PG-13': 'Teens',
    'TV-G': 'Kids',
    'PG': 'Older Kids',
    'G': 'Kids',
    'UR': 'Adults',
    'NC-17': 'Adults'
    }

    return (
        pd.read_csv(filename)
        .set_index("type")
        .loc["Movie"]
        .reset_index()
        .drop(["show_id", "type"], axis= 1)
        .assign(
            title = lambda x: x['title'].apply(standarizeString),
            date_added = lambda x: x['date_added'].apply(lambda x: pd.to_datetime(x.strip(), format='%B %d, %Y')),
            duration = lambda x: x['duration'].apply(lambda y: int(y.split()[0])),
            description = lambda x: x['description'].apply(removeStopwords),
            target_audience = lambda x: x["rating"].replace(ratings_ages)
       )
    )
  
def catSeriesToString(Series, delim = ", "):
    return (
        delim
        .join(
            Series
            .dropna()
            .values
        )
        .split(delim)
    )

def getUniqueItems(Series):
    return pd.Series(
            np.unique(
            np.array(
                catSeriesToString(Series)
            )
        )
    )

def summarizeSeries(Series):
    from collections import Counter
    name = Series.name
    valCount = (
        pd.DataFrame
        .from_dict(
            Counter(Series.values),
            orient = "index"
        )
        .sort_values(0, ascending= False)
        .reset_index()
        .fillna("Not Specified")
    )
    valCount.columns = [name, "count"]
    return valCount

def splitAndSummarize(Series, Name):
    Series = pd.Series(
        catSeriesToString(Series.dropna())
    )
    Series.name = Name
    return summarizeSeries(Series)



# %%
