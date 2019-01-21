from dramatiq import Message
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.results import Results
from flask import Flask, render_template, redirect, request

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend

import dramatiq

app = Flask(__name__)

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq_results = RedisBackend()

redis_broker.add_middleware(Results(backend=dramatiq_results))
dramatiq.set_broker(redis_broker)

log = dramatiq.logging.get_logger(__name__)

TIME_LIMIT_ACTOR = 5000

values = []
message = []

@dramatiq.actor(store_results=True, time_limit=TIME_LIMIT_ACTOR)
def prime_search(start_v, end_v):
    values = {}
    try:
        lower = start_v
        upper = end_v

        values['val'] = []

        for num in range(lower, upper + 1):
            # prime numbers are greater than 1
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        break
                else:
                    values['val'].append(num)
        return values

    except TimeLimitExceeded:
        actor = 'prime_search'
        message = f'Time limit of {TIME_LIMIT_ACTOR} ms exceeded on: {actor}'
        values['val'] = []
        values['err'] = message
        log.info(values['err'])

        return values


@app.route("/start_dramatiq")
def run():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    message.append(prime_search.send(start, end))
    return redirect("/")

def error_alert(message):
    print('Error while processing.')
    print('Message: ', message)

@app.route("/check")
def check_results():
    for el in message:
        result = el.get_result()
        if 'err' not in result:
            print(result['val'])
            values.append(el.get_result()['val'])
        else:
            error_alert(result['err'])
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html", values=values)
