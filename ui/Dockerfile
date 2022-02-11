FROM continuumio/miniconda3

ENV APP_HOME_NEW /app_new
WORKDIR $APP_HOME_NEW
COPY . $APP_HOME_NEW

EXPOSE 8005

RUN pip install -r requirements.txt

CMD ["python", "web_app.py"]