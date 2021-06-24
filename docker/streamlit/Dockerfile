FROM python:3.7

EXPOSE 8501

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "streamlit", "run", "main.py" ]