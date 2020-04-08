import os
from flask import Flask
from flask import render_template
from flask import request
from pymemcache.client.base import Client
import sys
sys.setrecursionlimit(10**6)


client = Client(('85.175.5.147', 20351))
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

GLOBAL_CACHE = {0:0, 1:1}

def fibo(n):
    if n in GLOBAL_CACHE:
        return GLOBAL_CACHE[n]

    else:
        f = fibo(n-1) + fibo (n-2)
        client.set(str(n), int(f), 60*60*24*5)
        GLOBAL_CACHE[n]=f
        return f



def get_cache(n):
    cache = {0:0, 1:1}

    if n < 2:
        client.set(str(0), '0')
        client.set(str(1), '1')
        return cache

    else:
        for i in range (2,n+1):
            if client.get(str(i))==None:
                return cache
            else:
                cache[i]=client.get(str(i)).decode("utf-8")

    return cache


@app.route('/')
def hello_world():
    return render_template('index.html', fb = None, num = 0)


@app.route('/number', methods=['GET'])
def hello_world1():
    if request.method == 'GET':
        num = request.args['number1']
        if client.get(str(num)):
            print("from cache")
            return render_template('index.html', fb = client.get(str(num)).decode("utf-8"), num=num)

        GLOBAL_CACHE = get_cache(num)
        fb = fibo(num)
        return render_template('index.html', fb = fb, num=num)


if __name__ == '__main__':

    app.run(debug=False, host='172.17.0.2', port=port)
