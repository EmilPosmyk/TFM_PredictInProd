from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
import pytz

import pandas as pd
import joblib

app = FastAPI()

# If we do not use the add_middleware method, then our API will only work when called from Back-End code (or similar),
# but not when called from the JavaScript code of a web page. Open this link in order to learn more about CORS…
# So, all these are different origins:
#
#     http://localhost
#     https://localhost
#     http://localhost:8080
#
# Even if they are all in localhost, they use different protocols or ports, so, they are different "origins".
# To achieve this, the backend must have a list of "allowed origins".
#
# https://fastapi.tiangolo.com/tutorial/cors/
#
app.add_middleware(
    CORSMiddleware,
    # allow_origin_regex='https://.*\.example\.org'
    allow_origins=["*"],  # this can be list of origins: origins = ["http://localhost","http://localhost:8080", ...]
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, ...
    allow_headers=["*"]  # Accept, Accept-Language, Content-Language, Content-Type - always allowed
)


@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict(pickup_datetime,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count):

    # create datetime object from user provided date
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user provided datetime with the NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    # convert the user datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)

    # format the datetime as expected by the pipeline
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

    # fixing a value for the key, unused by the model
    # in the future the key might be removed from the pipeline input
    # even though it is used as a parameter for the Kaggle submission
    key = "2013-07-06 17:18:00.000000119"

    # build X beware to the order of the parameters
    X = pd.DataFrame(dict(
        key=[key],
        pickup_datetime=[formatted_pickup_datetime],
        pickup_longitude=[float(pickup_longitude)],
        pickup_latitude=[float(pickup_latitude)],
        dropoff_longitude=[float(dropoff_longitude)],
        dropoff_latitude=[float(dropoff_latitude)],
        passenger_count=[int(passenger_count)]))

    # ⚠️ TODO: get model from GCP
    # pipeline = get_model_from_gcp()

    pipeline = joblib.load('model.joblib')

    # make prediction
    results = pipeline.predict(X)

    # convert response from numpy to python type
    pred = float(results[0])

    return dict(prediction=pred)

