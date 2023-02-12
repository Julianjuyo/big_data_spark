
FROM python:3

ENV PYTHONUNBUFFERED=1


RUN mkdir /streamlit

WORKDIR /streamlit

COPY . /streamlit/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENV ON_DOCKER Yes


EXPOSE 8501


ENTRYPOINT ["streamlit", "run", "main.py"]

