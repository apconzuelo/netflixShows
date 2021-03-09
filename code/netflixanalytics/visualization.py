import pandas as pd
import plotly.express as px

def frequencyAnalysis(
    DataFrame, 
    MaxEntries = 10, 
     logX = False, logY =False
    ):
    MaxEntries = min(len(DataFrame), MaxEntries)
    return (
        px.bar(
            DataFrame.loc[range(MaxEntries, -1, -1)],
            y = DataFrame.columns[0],
            x = DataFrame.columns[1],
            log_x = logX, log_y = logY
        )
    )
    
def dateAddedAnalysis(DataFrame):
    
    months = {
        1 + key: value
        for key, value 
        in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    }
    ByDate = (
        DataFrame
        .assign(
            year = lambda x: x['date_added'].dt.year,
          #  month = lambda x: x["date_added"].dt.month
        )
        .groupby(["year", "target_audience"])["title"]
        .count()
        .reset_index()
        .assign(
          #  month = lambda x: x["month"].apply(lambda y: months[y])
        )
        
    ) 
    ByDate = ByDate[ByDate["year"] < 2021]

    return px.line(
            ByDate,
            color = "target_audience",
            x = "year", 
            y = "title"
        )

def targetAudienceCounts(DataFrame):
    
    ByRating = (
        DataFrame
        .groupby(["rating", "target_audience"])["title"]
        .count()
        .reset_index()
    ) 
    ByRating.columns = ["rating", "target_audience", "title_count"]
    return (
        px.bar(
            ByRating,
            y = "rating",
            x = "title_count",
            color = "target_audience"
        )
    )

def durationDistplot(DataFrame):
    DataFrame = (
        DataFrame
        .groupby(
            [
                "target_audience", 
                "duration"
            ]
        )
        ["title"]
        .count()
        .reset_index()
    )
    DataFrame.columns = ["target_audience", "duration", "title"]
    return (
        px.histogram(
            DataFrame.dropna(),
            x="duration", 
            y="title", 
            # color="target_audience",
            marginal="box", # or violin, rug
            hover_data= DataFrame.columns,
            nbins = 50, 
        )
    )

