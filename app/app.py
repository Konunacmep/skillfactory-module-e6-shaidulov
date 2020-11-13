import os
from flask import Flask
from pymemcache.client import base

app = Flask(__name__)
port = int(os.environ.get("PORT"))
mem_host = os.environ.get("MEMCACHED_HOST")
mem_port = os.environ.get("MEMCACHED_PORT")
client = base.Client((mem_host, mem_port))


# считать рекурсивно сказано не было, поэтому и не будем
# значения первых двух членов последовательности возмем 1 и 1
def fibo_calc(num):
    n1 = 1
    n2 = 1
    if num == 1:
        return n2
    else:
        for i in range(2, num):
            n1, n2 = n2, n1 + n2
        return n2


@app.route('/', methods=['GET'])
def greeting():
    return 'Используйте GET с параметром'


@app.route('/<int:fibo_number>', methods=['GET'])
def search_or_calc(fibo_number):
    if fibo_number <= 0:
        return 'Нет такого числа'
    result = client.get(f'{fibo_number}')
    if not result:
        result = fibo_calc(fibo_number)
        client.set(f'{fibo_number}', result)
        return f'Вычислен {fibo_number} элемент: {result}'
    return f'Взят из кэша {fibo_number} элемент: {result.decode("utf-8")}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
