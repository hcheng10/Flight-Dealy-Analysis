import sqlite3
from flask import g, request
import datetime
import pandas as pd
import plotly
import plotly.express as px

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