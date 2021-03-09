# %%
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
#re
import re
#sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# %%
def preProcessForRecommender(DataFrame, stem = False):
    # Drop Unnecessary Columns
    DataFrame = (
        DataFrame
        .drop(
            ["target_audience",'date_added',
            'release_year','rating','duration'],
            axis=1
        )
        .reset_index(drop=True)
    )
    return DataFrame

def preprocess(content, stem = False):
    # Step 1: Initialize stopwords, stemming.
    english_stopwords = stopwords.words('english')
    #base of english stopwords
    stemmer = SnowballStemmer('english')
    #stemming algorithm
    regex = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
    content = re.sub(regex, ' ', str(content).lower()).strip()
    tokens = []
    for token in content.split():
        if token not in english_stopwords:
            tokens.append(stemmer.stem(token))

    return " ".join(tokens)

def createCosineSimMatrix(DataFrame):
    # Step 0: Preprocess DataFrame for recommender
    DataFrame = preProcessForRecommender(DataFrame)
    DataFrame = DataFrame.fillna("Unspecified")

    # Step 1: 
    DataFrame.description = DataFrame.description.apply(lambda x: preprocess(x))
    DataFrame.listed_in = DataFrame.listed_in.apply(lambda x: preprocess(x))
    DataFrame.listed_in = DataFrame.listed_in.apply(lambda x: x.lower().split(" ")) 
    DataFrame.description = DataFrame.description.apply(lambda x: x.lower().split(" "))
    DataFrame.director = DataFrame.director.apply(lambda x: x.lower().split(","))
    DataFrame.cast = DataFrame.cast.apply(lambda x: x.lower().split(","))
    DataFrame.country = DataFrame.country.apply(lambda x: x.lower().split(","))

    # Step 2
    for index, row in DataFrame.iterrows():
        row['director'] = [item.replace(" ", "") for item in row['director']]
        row['cast'] = [item.replace(" ", "") for item in row['cast']]
        row['country'] = [item.replace(" ", "") for item in row['country']]
    
    DataFrame.set_index('title', inplace = True)

    # Step 3
    columns = DataFrame.columns
    DataFrame['bagofwords'] = ""

    for index, row in DataFrame.iterrows():
        words = ''
        for column in columns:
            words = words + ' '.join(row[column])+' '
        row['bagofwords'] = words
        
    DataFrame.drop([column for column in columns], axis=1, inplace=True)

    count = CountVectorizer()
    count_matrix = count.fit_transform(DataFrame['bagofwords'])
    return cosine_similarity(count_matrix, count_matrix)

def recommender(title, library, cosineSim):
    
    index = library[library['title']==str(title)].index[0]
    
    # creating a Series with the similarity scores in descending order
    similar_indexes = pd.Series(cosineSim[index]).sort_values(ascending=False)
    # getting the indexes of the 10 most similar movies
    top5 = list(similar_indexes.iloc[1:6].index)
    
    recommended_movies = library.iloc[pd.Index(library.index).get_indexer(top5)]

    return recommended_movies
