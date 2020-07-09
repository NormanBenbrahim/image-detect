import datetime
from flask import Flask, render_template
from google.cloud import datastore

datastore_client = datastore.Client()

###### functions for datastore
def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times
####### end functions for datastore


app = Flask(__name__)


@app.route('/')
def root():
    # store access time in datastore
    store_time(datetime.datetime.now())

    # fetch most 10 recent access times from datastore
    times = fetch_times(10)

    return render_template('index.html', times=times)


if __name__ == '__main__':
    # This is used when running locally only
    app.run(host='127.0.0.1', port=8080, debug=True)