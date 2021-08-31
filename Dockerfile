FROM python:3.8-bullseye

#COPY api /opt/TFM/api
#COPY model.joblib /opt/TFM/model.joblib
#COPY requirements.txt /opt/TFM/requirements.txt
COPY api /api
COPY model.joblib /model.joblib
COPY TaxiFareModel /TaxiFareModel
COPY requirements.txt /requirements.txt
COPY ~/code/EmilPosmyk/gcp/elemental-icon-324116-b524483ad3f5.json

RUN pip install --upgrade pip
#RUN pip install -r /opt/TFM/requirements.txt
RUN pip install -r /requirements.txt

#CMD cd /opt/TFM/api
CMD uvicorn api.fast:app --host 0.0.0.0 --port 8050
