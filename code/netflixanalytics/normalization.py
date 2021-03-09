"""
Module with functions that normalize both Netflix and IMDB databases.
"""
#%%
def normalizeArray(array, normalizationDict = {}, denormalizationDict = {}):
    if normalizationDict.keys():
        itemNumber = 1 + max(normalizationDict.keys())
    else:
        itemNumber = 0

    for element, item in enumerate(array):
        if item in denormalizationDict.keys():
            array[element] = denormalizationDict[item]
        else:
            normalizationDict[itemNumber] = item
            denormalizationDict[item] = itemNumber
            array[element] = denormalizationDict[item]
            itemNumber += 1
    
    return array, normalizationDict, denormalizationDict

# %%
def normalizeSeries(series, normalizationDict ={}, denormalizationDict = {}):
    array, normalizationDict, denormalizationDict = normalizeArray(series.values)
    return pd.Series(array), normalizationDict, denormalizationDict

#%%
def normalizeDataFrame(dataFrame, useCols, colsNormDict = {}, colsDenormDict = {}):

# %%

# %%
