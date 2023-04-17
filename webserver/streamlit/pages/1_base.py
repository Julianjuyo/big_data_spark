from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
import os


st.title("Proyecto Base que permite calcular la tasa metabolica basal")

# Para tener variables globales
if "edad" not in st.session_state:
    st.session_state["edad"] = ""


gasto_calorico = "..."
font_color = 'gray'


# parametros de entrada
edad = st.text_input("Ingrese su edad", st.session_state["edad"])
estatura = st.slider("Indique su estatura en cm", 0, 250, value=100)
peso = st.slider("Indique su peso en kg", 0, 150, value=50)
genero = st.selectbox("Genero de nacimiento", ("Hombre", "Mujer"))

import os 


"Selecciones los días que hace ejecicio"
col1, col2, col3 = st.columns(3)
with col1:
    lunes = st.checkbox("lunes")
    martes = st.checkbox("martes")

with col2:
    Miercoles = st.checkbox("Miercoles")
    Jueves = st.checkbox("Jueves")

with col3:
    Viernes = st.checkbox("Viernes")
    Sabado = st.checkbox("Sabado")
    Domingo = st.checkbox("Domingo")


submit = st.button("Enviar")

if submit:
    st.session_state["edad"] = edad
    st.write("Su edad es : ", edad)
    st.write("Su Peso es : ", peso)
    st.write("Su Genero es : ", genero)
    st.write("Su estatura es : ", estatura)

    if genero == "Hombre":
        gasto_calorico = 10*peso + 6.25*estatura - 5*int(edad) + 5

        font_color = 'blue'
    else:
        gasto_calorico = 10*peso + 6.25*estatura - 5*int(edad) + 5
        font_color = 'pink'

    st.write()


st.markdown(
    f"<h4 style='text-align:left; color:{font_color}'> Su tasa metabolica basal es: {gasto_calorico} </h4>", unsafe_allow_html=True)
