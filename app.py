from dramatiq import Message
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

values = []
message = []

@dramatiq.actor(store_results=True)
def prime_search(start_v, end_v):
    lower = start_v
    upper = end_v
    values = []

    for num in range(lower,upper + 1):
       # prime numbers are greater than 1
       if num > 1:
           for i in range(2,num):
               if (num % i) == 0:
                   break
           else:
               values.append(num)
    # print(values)
    return values

@app.route("/start_dramatiq")
def run():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    message.append(prime_search.send(start, end))
    # print(dir(message))
    # print(message.get_result())
    return redirect("/")

@app.route("/check")
def check_results():
    for el in message:
        print(el.get_result())
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html", values=values)
