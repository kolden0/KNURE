from bottle import route, run, request, response


@route('/')
def header_check():
    content_type = request.get_header('Content-Type')

    data = {"message": "Hello", "value": 123}

    if content_type == 'application/json':
        return data

    elif content_type == 'application/xml':
        response.content_type = 'application/xml'
        return f"<root><message>{data['message']}</message><value>{data['value']}</value></root>"

    else:
        response.content_type = 'text/plain'
        return "Default text"


if __name__ == '__main__':
    run(host='localhost', port=8000)