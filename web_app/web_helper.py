import sqlite3
from flask import g, request
import datetime
import pandas as pd
import plotly
import plotly.express as px
from sklearn.preprocessing import OneHotEncoder

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("comments.sqlite")
        cmd = """
            CREATE TABLE IF NOT EXISTS comment_table (
            score TEXT,
            comment TEXT,
            date TEXT
            )
            """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
    return g.message_db


# this function could inserting a user message into the database of messages.
def insert_message(request):
    score = request.form["score"]
    message = request.form["comment"]
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # open a connection to messages.db
    connection_obj = get_message_db()
    cursor_obj = connection_obj.cursor()

    insert_cmd = """
        INSERT INTO comment_table
        (score, comment, date)
        VALUES
        (?, ?, ?)
        """
    data = (score, message, today)
    cursor_obj.execute(insert_cmd, data)

    connection_obj.commit() # save changes
    connection_obj.close() # close connection


# this function will return a collection of n random messages from the message_db
# n argument is request.form["number"] which is a html script in string form
def view_messages():
    # open a connection to messages.db
    connection_obj = get_message_db()
    cursor_obj = connection_obj.cursor()

    length_cmd = "SELECT COUNT(*) FROM comment_table"
    cursor_obj.execute(length_cmd)
    num_len = cursor_obj.fetchone()[0]

    out = ""

    if (num_len == 0):
        out = ("No feedback!<br><br>")
        return out

    cmd = "SELECT * FROM comment_table ORDER BY date"

    for row in cursor_obj.execute(cmd): # row is a tuple
        out = out + "date: " + row[2] + " score: " + row[0] + " message: " + row[1] + "<br>"

    connection_obj.close() # close connection
    return out # a html script in string form


def plotly_flights(year):
    LAX_flight = pd.read_csv(r"data\LAX_flight.csv")

    fig = px.line(data_frame = LAX_flight[LAX_flight['FL_DATE'].str.contains(pat = str(year))], # data that needs to be plotted
                 x = "FL_DATE", # column name for x-axis
                 y = "Total_flight_per_day",
                 markers=True,
                 color = "week", # column name for color coding
                 width = 800,
                 height = 500)

    # reduce whitespace
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # show the plot
    return fig

def plotly_flights2(year):
    LAX_flight = pd.read_csv(r"data\LAX_flight.csv")
    fig = px.line(data_frame = LAX_flight[LAX_flight['FL_DATE'].str.contains(pat = str(year))], # data that needs to be plotted
                 x = "FL_DATE", # column name for x-axis
                 y = "punctuality rate",
                 markers=True,
                 color = "week", # column name for color coding
                 width = 800,
                 height = 500)

    # reduce whitespace
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # show the plot
    return fig


def LAX_table():
    LAX_flight = pd.read_csv(r"data\LAX_flight.csv")
    LAX_flight = LAX_flight.iloc[: , 1:]
    return LAX_flight

def weather_data():
    weather = pd.read_csv(r"data\weather2012_2018.csv")
    return weather

def weather_data_each_year(Weather):
    conn=sqlite3.connect("project.db") # create data base called project

    Weather.fillna(0,inplace=True)
    Weather['local_time LA (airport)'] = pd.to_datetime(Weather['local_time LA (airport)'])#normalize time
    Weather["Day_time"]=Weather["local_time LA (airport)"].apply(lambda x:str(x)[0:10])#only need day don't care about hours and min
    cols=["Day_time",'local_time LA (airport)',"Ff","N","RRR","VV"]
    Weather=Weather[cols]
    Weather.columns = ["Day_time",'Observation_time', 'wind_speed',"cloud", 'precipitation', 'visibility']#rename
    Weather["precipitation"]=Weather["precipitation"].replace("Signs of precipitation", 0)
    Weather["cloud"]=Weather["cloud"].replace({'100%.':1,#Convert percentages to corresponding decimals for subsequent calculations
                          '70 -80%.':0.75,
                          '50%.':0.5,
                          0:0,
                         'The sky is not visible due to fog and/or other meteorological phenomena.':0,
                         '20-0%.':0.1,
                          'Cloudless':0
                                   })
    Weather.to_sql("Weather", conn, if_exists = "replace", index = False)#put Weather.csv to the data base"\
    #cmd will calculate average wind speed, average visibility, total precipitation per day
    cmd = """
   
       SELECT Day_time,AVG(wind_speed) AS wind_speed_perday,AVG(visibility) AS visibility_perday, AVG(cloud) AS cloud_perday ,SUM(precipitation) AS precipitation_perday
       FROM Weather
       GROUP BY Day_time
       
         """
    LAX_weather= pd.read_sql_query(cmd, conn)
    #Convert real cloud cover according to real weather
    for i in range(len(LAX_weather["cloud_perday"])):
        if(LAX_weather["cloud_perday"][i]==0):
            LAX_weather["cloud_perday"][i]='cloudless'
        elif(LAX_weather["cloud_perday"][i]<0.3):
            LAX_weather["cloud_perday"][i]='less cloudy'
        elif(LAX_weather["cloud_perday"][i]<0.7):
            LAX_weather["cloud_perday"][i]='cloudy'
        else:
            LAX_weather["cloud_perday"][i]="overcast"  
    #Convert precipitation to heavy, medium and light rain
    for i in range(len(LAX_weather["precipitation_perday"])):
        if(LAX_weather["precipitation_perday"][i]==0):
            LAX_weather["precipitation_perday"][i]="no_rain"
        elif(LAX_weather["precipitation_perday"][i]<10):
            LAX_weather["precipitation_perday"][i]="light_rain"
        elif(LAX_weather["precipitation_perday"][i]<25):
            LAX_weather["precipitation_perday"][i]="moderate_rain"
        else:
            LAX_weather["precipitation_perday"][i]="heavy_rain"   
    #creating instance of one-hot-encoder
    encoder = OneHotEncoder(handle_unknown='ignore')

    #perform one-hot encoding on ['cloud_perday','precipitation_perday'] column 
    encoder_df = pd.DataFrame(encoder.fit_transform(LAX_weather[['cloud_perday','precipitation_perday']]).toarray())

    #merge one-hot encoded columns back with original DataFrame
    LAX_weather = LAX_weather.join(encoder_df)

    #view final df
    LAX_weather.drop(labels=['cloud_perday','precipitation_perday'], axis=1, inplace=True)
    colNameDict = {0:'cloudless',
                   1:'cloudy',
                   2:'fog',
                   3:'less cloudy',
                   4:'overcast',
                   5:'heavy_rain',
                   6:'light_rain',
                   7:'moderate_rain',
                   8:'no_rain'
                  }                  
    LAX_weather.rename(columns = colNameDict,inplace=True)
    conn.close()

    return LAX_weather

def merge_data(LAX_weather, LAX_flight):
    conn=sqlite3.connect("project.db") # create data base called project

    LAX_weather.to_sql("LAX_weather", conn, if_exists = "replace", index = False)#put temps.csv to the data base"
    LAX_flight.to_sql("LAX_flight", conn, if_exists = "replace", index = False)#put temps.csv to the data base"

    cmd = """
    SELECT *
    FROM LAX_flight
    LEFT JOIN LAX_weather ON LAX_weather.Day_time = LAX_flight.FL_DATE
        
        """
        
    data = pd.read_sql_query(cmd, conn)

    #use min max normalization
    for column in data[["wind_speed_perday","visibility_perday","Total_flight_per_day"]]:
        data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())

    sorted_df = data.sort_values(by='FL_DATE')
    sorted_df=sorted_df.drop(labels=["Day_time","week"],axis=1)
    return sorted_df