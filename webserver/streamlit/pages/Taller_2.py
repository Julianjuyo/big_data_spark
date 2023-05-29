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

collection_data_taller_2_agrupada = db['data_taller_2_agrupada']



st.title("Taller 2 -  Análisis de contenidos altamente escalables")

st.write("En esta vista se encuentran las preguntas de negocio respecto al taller 2")


# Menu para las preguntas de negocio
retos = ['Análisis descriptivo de los datos',
         'Análisis de polaridad',
         'Enriquecimiento semántico de datos'
         ]

# Seleccionar el reto
reto = st.radio(
    "Seleccione el reto que quiere ejecutar", retos)


def get_data_from_mongo(collection,limit):

    if limit == 0:
        data = collection.find()
    else:
        data = collection.find().limit(limit)

    return pd.DataFrame(data)

def readcsv(path,limit):
    if limit == 0:
        df = pd.read_csv(path)
    else:
        df = pd.read_csv(path, nrows=limit)
    return df




if reto == retos[0]:
    st.header(retos[0])

    # # Create two columns
    col1, col2 = st.columns(2)

    # # Add a date input to the first column
    start_date = str(col1.date_input("Start date", min_value=dt.date(2020, 1, 1), max_value=dt.date(2023, 12, 31)))

    # # Add a date input to the second column
    end_date =   str(col2.date_input("End date", min_value=dt.date(2020, 1, 1), max_value=dt.date(2023, 12, 31)))


    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        # Print the selected dates
        st.write("Selected date range:", start_date, "to", end_date)
    
        df_data_agrupada = get_data_from_mongo(collection_data_taller_2_agrupada,0)
        # df_data_agrupada = readcsv("agrupada.csv",0)

        
        df_data_filter = df_data_agrupada.loc[(df_data_agrupada.date>= start_date)& (df_data_agrupada.date <= end_date)]

        

        st.header("Cantidad de tweets por ubicación")

        # Filter the data to only include non-verified users
        df_verified = df_data_filter[df_data_filter['user_verified'] == False]
        grouped_data_verified = df_verified.groupby('user_location')['conteo'].sum().nlargest(10)


        # Filter the data to only include verified users
        df_no_verified = df_data_filter[df_data_filter['user_verified'] == True]
        grouped_data_no_verified = df_no_verified.groupby('user_location')['conteo'].sum().nlargest(10)


        # Plot the bar charts side by side horizontally
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))


        # Bar plot for non-verified users
        axes[0].bar(grouped_data_no_verified.index, grouped_data_no_verified.values, color='red')
        axes[0].set_title('Top 10 locaciones de los usuarios NO verificados')
        axes[0].set_xlabel('User Location')
        axes[0].set_ylabel('Numero de Tweets')
        axes[0].tick_params(axis='x', rotation=45)

        # Display labels on the bars for non-verified users
        for i, count in enumerate(grouped_data_no_verified.values):
            axes[0].text(i, count, str(count), ha='center', va='bottom')

        # Bar plot for verified users
        axes[1].bar(grouped_data_verified.index, grouped_data_verified.values, color='blue')
        axes[1].set_title('Top 10 locaciones de los usuarios verificados')
        axes[1].set_xlabel('User Location')
        axes[1].set_ylabel('Numero de Tweets')
        axes[1].tick_params(axis='x', rotation=45)

        # Display labels on the bars for verified users
        for i, count in enumerate(grouped_data_verified.values):
            axes[1].text(i, count, str(count), ha='center', va='bottom')

        # Adjust the layout
        plt.tight_layout()

        # plt.show()
        # Display the plot in Streamlit
        st.pyplot(fig)


        st.header("Cantidad de tweets verificados por día")        
        # Plot the pie chart
        fig, ax = plt.subplots(figsize=(4, 4))
        df_data_filter['user_verified'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title('User Verification')
        ax.set_ylabel('')

        # Display the plot in Streamlit
        st.pyplot(fig)




if reto == retos[1]:

    st.header(retos[1])

    # Twites en cada dia ente las fechas
    # sentimeintos y emociones
    # Grafica que relacione sentimientos y polaridad
    # data de este año

    # df = get_data_from_mongo(collection_data_taller_2,5)
    # st.write(df)



    # Correlación entre sentimientos y polaridad con el precio de bitcoin 


if reto == retos[2]:

    st.header(retos[2])


