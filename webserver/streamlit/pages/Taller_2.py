from collections import namedtuple

import pandas as pd
import streamlit as st

import os
import sys
from dotenv import load_dotenv

import matplotlib.pyplot as plt

import pymongo

import datetime as dt

import altair as alt

# import us as us_states
# import plotly.express as px



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)


# parametros para conectar a mongo
mongo = os.environ["MONGO"]
CONNECTION_STRING = "mongodb://172.24.99.25:27018"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['grupo_02']
collection_data_taller_2 = db['data_taller_2']




st.title("Taller 2 -  Análisis de contenidos altamente escalables")

st.write("En esta vista se encuentran las preguntas de negocio respecto al taller 2")


# Menu para las preguntas de negocio
retos = ['Análisis descriptivo de los datos',
         'Análisis de polaridad'
         ]

# Seleccionar el reto
reto = st.radio(
    "Seleccione el reto que quiere ejecutar", retos)


def get_data_from_mongo(collection,limit):

    if limit == 0:
        data = collection.find()
    else:
        data = collection.find().limit(limit)
    data = collection.find()
    return pd.DataFrame(data)




if reto == retos[0]:
    st.header(retos[0])



    # # Create two columns
    # col1, col2 = st.columns(2)

    # # Add a date input to the first column
    # start_date = str(col1.date_input("Start date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    # # Add a date input to the second column
    # end_date =   str(col2.date_input("End date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))


    df = get_data_from_mongo(collection_data_taller_2,5)

    st.write(df)

if reto == retos[1]:

    st.header(retos[1])

    # Twites en cada dia ente las fechas
    # sentimeintos y emociones
    # Grafica que relacione sentimientos y polaridad
    # data de este año



    df = get_data_from_mongo(collection_data_taller_2,5)

    st.write(df)



    # Correlación entre sentimientos y polaridad con el precio de bitcoin 



