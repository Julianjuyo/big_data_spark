from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
import subprocess
from subprocess import check_output
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime as dt
import re
import numpy


st.title("Tarea de arranque")


filelist = []

data_folder= "reuters21578"


for root, dirs, files in os.walk(data_folder):
    for file in files:
        filename = os.path.join(root, file)
        filelist.append(file)


# RETO 1
def contar_palabras(array_filenames):

    filenames = " ".join(array_filenames)
    result = subprocess.run(
        f"cat {filenames} | wc -w", shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout


# Reto 2
def palabras_frecuentes(array_filenames):

    filenames = " ".join(array_filenames)
    result = subprocess.run(
        f"cat {filenames} | tr -c '[:alnum:]' '[\n*]'|tr '[:upper:]' '[:lower:]'  | sort | uniq -c | sort -nr", shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout

# RETO 3


def n_palabras_frecuentes(array_filenames, n):

    filenames = " ".join(array_filenames)
    result = subprocess.run(
        f"cat {filenames} | tr '[:upper:]' '[:lower:]' | tr -cs '[:alpha:]' '[\n*]' | sort | uniq -c | sort -nr | head -n {n}", shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout


# Creacion de nube de palabras
def nube_palabras(palabras):

    stopwords = []

    wordcloud = WordCloud(stopwords=stopwords,
                          background_color="white").generate(palabras)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    st.write("Nube de palabras")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


# Menu para los retos
retos = ['Reto 1: Contar palabras',
         'Reto 2: frecuencia de las palabras',
         'Reto 3: N palabras más frecuentes',
         'Reto 4: ¿En cuál archivo aparece más veces cierta palabra y cuál archivo tiene más palabras?',
         'Reto 5: N palabras más frecuentes consecitivamente',
         'Reto 6: Procesos lanzados a una hora'
         ]

# Seleccionar el reto
reto = st.radio(
    "Seleccione el reto que quiere ejecutar", retos)


# Metodo para buscar los archivos por el nombre
def files_by_name():

    st.header("Buscar archivos por nombre")
    st.write(filelist)
    answers = st.text_input(
        "Ingres el nombre del archivo en caso de que sea más de un archivo ingrese los nombres separados por comas:")

    return answers.split(',')

# Metodo para seleccionar los archivos existentes


def select_files():

    st.header("Seleccionar archivos")
    return st.multiselect(
        "seleccione el/los archivos", filelist)


if reto == retos[0]:

    st.header(retos[0])

    selected_files = [data_folder+"/" + string for string in files_by_name()]

    submit_file_name = st.button("Resultado input")
    if submit_file_name:
        st.write("Nombre archivo: ", selected_files)
        resp = contar_palabras(selected_files)
        st.success("El número de palabras en el archivo es: " + resp)

    selected_files = ["reuters21578/" + string for string in select_files()]

    submit_selected_file = st.button("Resultado Selección")
    if submit_selected_file:
        st.write("Nombre archivo: ", selected_files)
        resp = contar_palabras(selected_files)
        st.success("El número de palabras en el archivo es:" + resp)

if reto == retos[1]:

    st.header(retos[1])

    selected_files = [data_folder+"/" + string for string in files_by_name()]

    submit_file_name = st.button("Resultado input")
    if submit_file_name:
        st.write("Nombre archivo: ", selected_files)
        resp = palabras_frecuentes(selected_files)
        st.success("El número de palabras en el archivo es: " + resp)

        result_without_numbers = re.sub(r'\d+', '', resp)
        nube_palabras(result_without_numbers)

    selected_files = ["reuters21578/" + string for string in select_files()]

    submit_selected_file = st.button("Resultado Selección")
    if submit_selected_file:
        st.write("Nombre archivo: ", selected_files)
        resp = palabras_frecuentes(selected_files)
        print(type(resp))
        st.success("Se muestran <ocurrencia palabra> <palabra> : " + resp)

        result_without_numbers = re.sub(r'\d+', '', resp)
        nube_palabras(result_without_numbers)

if reto == retos[2]:

    st.header(retos[2])

    number = st.number_input(
        "Inserte el número N de palabras frecuentes que quiere obtener", min_value=1, value=1)

    selected_files = [data_folder+"/" + string for string in files_by_name()]

    submit_file_name = st.button("Resultado input")
    if submit_file_name:
        st.write("Nombre archivo: ", selected_files)
        resp = n_palabras_frecuentes(selected_files, number)
        st.success("El número de palabras en el archivo es: " + resp)

        result_without_numbers = re.sub(r'\d+', '', resp)
        nube_palabras(result_without_numbers)

    selected_files = [data_folder+"/" + string for string in select_files()]

    submit_selected_file = st.button("Resultado Selección")
    if submit_selected_file:
        st.write("Nombre archivo: ", selected_files)
        resp = n_palabras_frecuentes(selected_files, number)
        st.success("Se muestran <ocurrencia palabra> <palabra> : " + resp)

        result_without_numbers = re.sub(r'\d+', '', resp)
        nube_palabras(result_without_numbers)

if reto == retos[3]:

    st.header(retos[3])


    def retoGFuncion():

        if (st.session_state.fileselected_G != None) and (st.session_state.word_selected != None):

            filenameMostWord = ""
            filenameMostWords = ""
            countWords = []
            countWord = []

            for filename in st.session_state.fileselected_G:

                path = data_folder+"/"+filename

                countWords.append(int(check_output(["wc","-w",path]).split()[0]))
                grepanswer = check_output(["grep","-o",st.session_state.word_selected, path])
                countWord.append(int(check_output(["wc","-l"], input=grepanswer).split()[0]))
            filenameMostWord = st.session_state.fileselected_G[numpy.argmax(countWord)]
            filenameMostWords = st.session_state.fileselected_G[numpy.argmax(countWords)]
            response = 'The file with most words is '+ filenameMostWords + ' with a word count of '+ str(max(countWords)) +'.\nThe file with most occurences of the word '+ st.session_state.word_selected +' is '+ filenameMostWord + ' with a word count of '+ str(max(countWord)) + '.\n' 
            st.session_state.retoG = response        
        else:
            st.session_state.retoG = 'Please fill out the data'
            st.error("Please select files and a word to look for")
    

    multichoice = st.multiselect('Seleccione los archivos a revisar', filelist, key='fileselected_G')

    wordSelected = st.text_input('Ingrese la palabra a buscar en los archivos', key='word_selected')


    button = st.button('Consultar', on_click=retoGFuncion)
    answerTxt = st.text_area('Respuesta Reto G', key = 'retoG', disabled = True)



if reto == retos[4]:

    st.header(retos[4])


if reto == retos[5]:

    st.header(retos[5])
