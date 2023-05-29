
FROM python:3.9.12

ENV PYTHONUNBUFFERED=1


RUN mkdir /streamlit

WORKDIR /streamlit

COPY requirements.txt /frontend-streamlit/


RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /streamlit/

ENV ON_DOCKER Yes


EXPOSE 8501


ENTRYPOINT ["streamlit", "run", "main.py"]

