from bottle import route, run, request

@route('/currency')
def currency_static():
    if 'today' in request.query:
        return "INR - 0.49"

    return ""


if __name__ == '__main__':
    run(host='localhost', port=8000)