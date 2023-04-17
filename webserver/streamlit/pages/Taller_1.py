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

import us as us_states

import plotly.express as px



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)


# parametros para conectar a mongo
mongo = os.environ["MONGO"]
client = pymongo.MongoClient("mongodb+srv://julianestevanof:"+mongo+"@taller1.joran3x.mongodb.net/?retryWrites=true&w=majority")
db = client.Taller1


st.title("Taller 1 - Procesamiento escalable")

st.write("En esta vista se encuentran las preguntas de negocio respecto al taller 1")


# Menu para las preguntas de negocio
retos = ['Pregunta 1: Cuál es el estado con mayor tráfico de botes en un periodo dado? ',
         'Pregunta 2: ¿Cuál es el tipo de carga más común por estado, en un periodo dado?',
         'Pregunta 3: ¿Qué tanto afectó la pandemia al tráfico de embarcaciones teniendo en cuenta el número de embarcaciones por mes en cada estado en años anteriores?',
         'Pregunta 4: ¿Cómo es la distribución geográfica, en un periodo dado, de las embarcaciones?',
         'Pregunta 5: ¿Existe alguna relación entre el día de la semana y el tipo de carga en cada estado?¿La relación cambia por año?',
         'Pregunta 6: Velocidad promedio por grupo de embarcaciones',
         'Pregunta 7: Tipo de embarcación más concurrida entre un periodo dado?'
         ]

# Seleccionar el reto
reto = st.radio(
    "Seleccione el reto que quiere ejecutar", retos)


def get_data_from_mongo(collection):

    data = collection.find()
    return pd.DataFrame(data)

if reto == retos[0]:
    st.header(retos[0])

    # Create two columns
    col1, col2 = st.columns(2)

    # Add a date input to the first column
    start_date = str(col1.date_input("Start date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    # Add a date input to the second column
    end_date =   str(col2.date_input("End date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        # Print the selected dates
        st.write("Selected date range:", start_date, "to", end_date)
        
        df_data = get_data_from_mongo(db.Agrupacion1_3_4)

        df_data.rename(columns={'DATE': 'fecha'}, inplace=True)

        df_data['fecha'] = pd.to_datetime(df_data['fecha'].str.replace(' ', '-'))

        df_data_filter = df_data.loc[(df_data.fecha>= start_date)& (df_data.fecha <= end_date)]

        if df_data_filter.empty:
            st.error("No hay datos en el periodo seleccionado")

        else:
            df_data_group_by = df_data_filter.groupby("State").agg(Cant=('Cant', 'sum'))

            max_row = df_data_group_by.loc[df_data_group_by['Cant'].idxmax()]

            st.success("El estado con mayor tráfico en el periodo es: " + str(max_row.name) +" con un numero de: " + str(max_row["Cant"])+" embarcaciones")

        
if reto == retos[1]:

    st.header(retos[1])

    # Create two columns
    col1, col2 = st.columns(2)

    # Add a date input to the first column
    start_date = str(col1.date_input("Start date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    # Add a date input to the second column
    end_date =   str(col2.date_input("End date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    if start_date > end_date:
        st.error("Error: La fecha final debe ser mayor a la fecha inicial.")
        
    else:
        # Print the selected dates
        st.write("Rango seleccionado", start_date, "to", end_date)
        
        df_data = get_data_from_mongo(db.Agrupacion2_5)


        df_data.rename(columns={'DATE': 'fecha'}, inplace=True)
        df_data['fecha'] = pd.to_datetime(df_data['fecha'].str.replace(' ', '-'))

        df_data['Cargo'] = df_data['Cargo'].astype(int)

        df_data_filter = df_data.loc[(df_data.fecha>= start_date)& (df_data.fecha <= end_date)]


        if df_data_filter.empty:
            st.error("No hay datos en el periodo seleccionado")

        else:
            df_data_group_by = df_data_filter.groupby(["State", "Cargo"]).agg(Cant=('Cant', 'sum'))

            st.write(df_data_group_by)

            max_row = df_data_group_by.loc[df_data_group_by['Cant'].idxmax()]

            st.success("El estado con mayor tráfico en el periodo es: " + str(max_row.name) +" con un numero de: " + str(max_row["Cant"])+" embarcaciones")

    

if reto == retos[2]:
    st.header(retos[2])

    df_data = get_data_from_mongo(db.Agrupacion1_3_4)

    state = st.selectbox("Seleccione un estado", df_data["State"].unique())


    df_data_show = df_data[df_data["State"] == state]

    df_data_show.drop(['_id','State'], axis=1, inplace=True)

    # Set the index of the DataFrame to the datetime column
    df_data_show = df_data_show.set_index('DATE')

    st.header("Numero de embarcaciones por dia en el estado: " + state)

    # Create a line chart with dates on the x-axis
    st.line_chart(df_data_show)


if reto == retos[3]:
    st.header(retos[3])


        # Create two columns
    col1, col2 = st.columns(2)

    # Add a date input to the first column
    start_date = str(col1.date_input("Start date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    # Add a date input to the second column
    end_date =   str(col2.date_input("End date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        # Print the selected dates
        st.write("Selected date range:", start_date, "to", end_date)
        
        df_data = get_data_from_mongo(db.Agrupacion1_3_4)

        df_data.rename(columns={'DATE': 'fecha'}, inplace=True)

        df_data['fecha'] = pd.to_datetime(df_data['fecha'].str.replace(' ', '-'))

        df_data_filter = df_data.loc[(df_data.fecha>= start_date)& (df_data.fecha <= end_date)]

        if df_data_filter.empty:
            st.error("No hay datos en el periodo seleccionado")

        else:

            # use the us library to convert state names to state codes
            df_data_filter['state_code'] = df_data_filter['State'].apply(lambda x: us_states.states.lookup(x).abbr)
            

            df_data_group_by = df_data_filter.groupby("state_code").agg(num_embarcaciones=('Cant', 'sum'))

            df_data_group_by = df_data_group_by.reset_index()


            # create the choropleth map
            fig = px.choropleth(df_data_group_by,
                                locations='state_code', 
                                locationmode="USA-states", 
                                scope="usa",
                                color='num_embarcaciones',
                                color_continuous_scale="Viridis_r", 
                                )

            st.plotly_chart(fig)


if reto == retos[4]:
    st.header(retos[4])

    df_data = get_data_from_mongo(db.Agrupacion2_5)

    df_data['Year'] = df_data['DATE'].apply(lambda x: dt.datetime.strptime(x, '%Y %m %d').date().year)

    Year = st.selectbox("Seleccione un año", df_data["Year"].unique())

    df_data_show = df_data[df_data["Year"] == Year]

    df_pivot = pd.pivot_table(
        df_data_show,
        values="Cant",
        index="WEEKDAY",
        columns="Cargo",
        aggfunc='count')

    # Plot a bar chart using the DF
    ax = df_pivot.plot(kind="bar")
    # Get a Matplotlib figure from the axes object for formatting purposes
    fig = ax.get_figure()
    # Change the plot dimensions (width, height)
    fig.set_size_inches(7, 6)
    # Change the axes labels
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Amount")

    st.pyplot(fig)



if reto == retos[5]:
    st.header(retos[5])

    df_data = get_data_from_mongo(db.Agrupacion6)
    df_data.drop(['_id'], axis=1, inplace=True)


    # df_data_group_by = df_data.groupby("Group").agg(Avg_Velocity=('Avg Velocity', 'avg'))

    df_data_group_by = df_data.groupby('Group')['Avg Velocity'].mean()


    df_data_group_by = df_data_group_by.reset_index()


    df_data_group_by.sort_values(by=['Avg Velocity'], inplace=True, ascending=False)

    st.write(df_data_group_by)

    # Create a bar chart using pyplot
    fig, ax = plt.subplots()
    ax.bar(df_data_group_by['Group'],df_data_group_by['Avg Velocity'])

    # Set chart title and axis labels
    ax.set_title('Grupo vs Velocidad Promedio historico')
    ax.set_xlabel('Group')
    ax.set_ylabel('Velocidad Promedio (Nudos)')

    st.pyplot(fig)

if reto == retos[6]:
    st.header(retos[6]) 

    # Create two columns
    col1, col2 = st.columns(2)

    # Add a date input to the first column
    start_date = str(col1.date_input("Start date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    # Add a date input to the second column
    end_date =   str(col2.date_input("End date", min_value=dt.date(2017, 1, 1), max_value=dt.date(2023, 12, 31)))

    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        # Print the selected dates
        st.write("Selected date range:", start_date, "to", end_date)
        
        df_data = get_data_from_mongo(db.Agrupacion7)


        df_data.rename(columns={'DATE': 'fecha'}, inplace=True)

        df_data_filter = df_data.loc[(df_data.fecha>= start_date)& (df_data.fecha <= end_date)]


        if df_data_filter.empty:
            st.error("No hay datos en el periodo seleccionado")

        else:

            df_data_group_by = df_data_filter.groupby("Classification").agg(numero_embarcaciones=('Cant', 'sum'))
            
            df_data_group_by.sort_values(by=['numero_embarcaciones'], inplace=True, ascending=False)
            
            st.write(df_data_group_by)

            max_row = df_data_group_by.loc[df_data_group_by['numero_embarcaciones'].idxmax()]

            st.success("El tipo embarcación con mayor tráfico en el periodo es: " + str(max_row.name) +" con un numero de: " + str(max_row["numero_embarcaciones"])+" embarcaciones")

        




