from flask import Flask, render_template

import dramatiq

app = Flask(__name__)

@dramatiq.actor
def prime_search():
    lower = 900
    upper = 1000

    values = []

    # print("Prime numbers between",lower,"and",upper,"are:")

    for num in range(lower,upper + 1):
       # prime numbers are greater than 1
       if num > 1:
           for i in range(2,num):
               if (num % i) == 0:
                   break
           else:
               values.append(num)

@app.route("/")
def index():
    return render_template("index.html")
