import util


def get(client, address, request):
    pass


def post(client, address, request):
    pass


def request_processing(client, address, method, url, request, headers, message_body):
    client.send(b'HTTP/1.1 501 WORKING ON MUSIC\r\n')
    _headers = util.headers_to_dict(headers)
    if 'Connection' in _headers:
        return _headers['Connection'] == 'keep-alive'
    return False
