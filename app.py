from flask import Flask, render_template, redirect

from dramatiq.brokers.redis import RedisBroker

import dramatiq

app = Flask(__name__)

values = []

redis_broker = RedisBroker(host="redis", port=6379)
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def prime_search():
    lower = 900
    upper = 1000

    # print("Prime numbers between",lower,"and",upper,"are:")

    for num in range(lower,upper + 1):
       # prime numbers are greater than 1
       if num > 1:
           for i in range(2,num):
               if (num % i) == 0:
                   break
           else:
               values.append(num)

@app.route("/start_dramatiq")
def run():
    prime_search.send()
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html", values=values)
