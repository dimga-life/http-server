import socket
import json

import util
import root
import bazarik
import storage
import shop
import music
import man
import chan


last_ip_connection = ''


def request_processing(client, address):
    global last_ip_connection

    ip, port = address

    run = True
    while run:
        if ip != last_ip_connection:
            info = util.get_ip_info(ip)
            if info is None:
                print(f'connect {address[0]} (local) [')
            else:
                print(f'connect {address[0]} ( country: {info[0]} city: {info[1]} region: {info[2]} ) [')
            last_ip_connection = ip

        data = b''
        while True:
            print('recv 35')
            d = client.recv(1024)
            print(d)
            if not d:
                break
            data += d
            if b'\r\n\r\n' in data:
                break
        if data == b'':
            client.send(b'HTTP/1.1 400 BAD REQUEST\r\n')
            client.close()
            return

        print(f'{data.decode("ansi")}')
        starting_line, data = data.split(b'\r\n', 1)
        headers, message_body = data.split(b'\r\n\r\n', 1)
        method, url = starting_line.split(b' ')[:2]
        method = method.decode('ansi')
        url = url.decode('ansi')
        headers = headers.decode('ansi')
        _headers = util.headers_to_dict(headers)

        if 'Connection' in _headers:
            run = _headers['Connection'] == 'keep-alive'
        else:
            run = False

        request = None
        if '?' in url:
            url, request = url.split('?')
        http_version = '0.9'
        if b'HTTP/' in starting_line:
            http_version = starting_line[starting_line.index(b'HTTP/') + 5:].decode('ansi')

        print(f'    {method} HTTP/{http_version} "{url}"')
        if http_version != '1.1':
            client.send(b'HTTP/1.1 505 BAD VERSION HTTP\r\n')
            client.close()
            return

        if '..' in url:
            client.send(b'HTTP/1.1 400 BAD REQUEST\r\n')
            client.close()
            return

        if url.startswith('/root'):
            run = run and root.request_processing(client, address, method, url, request, headers, message_body)
        elif url == '/':
            run = run and root.request_processing(client, address, method, '/root', request, headers, message_body)
        elif url.startswith('/bazaar'):
            run = run and bazarik.request_processing(client, address, method, url, request, headers, message_body)
        elif url.startswith('/storage'):
            run = run and storage.request_processing(client, address, method, url, request, headers, message_body)
        elif url.startswith('/shop'):
            run = run and shop.request_processing(client, address, method, url, request, headers, message_body)
        elif url.startswith('/music'):
            run = run and music.request_processing(client, address, method, url, request, headers, message_body)
        elif url.startswith('/man'):
            run = run and man.request_processing(client, address, method, url, request, headers, message_body)
        elif url.startswith('/chan'):
            run = run and chan.request_processing(client, address, method, url, request, headers, message_body)
        else:
            client.send(b'HTTP/1.1 400 BAD REQUEST\r\n')
            client.close()
            return
    client.close()


def main():
    with open('config.json') as _:
        data = json.load(_)
    run = True
    ip = data['ip'] if 'ip' in data else '127.0.0.1'
    port = data['port'] if 'port' in data else 46000
    max_connect_count = data['max_connect_count'] if 'max_connect_count' in data else 10
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f'bind server on {ip}:{port}  ({max_connect_count})')
    server.bind((ip, port))
    server.listen(max_connect_count)
    print('server is run')
    while run:
        client, address = server.accept()
        try:
            request_processing(client, address)
        except ConnectionAbortedError:
            client.close()
        print('...')
        client.close()
        print(']')

    print('server is shutdown')


if __name__ == '__main__':
    main()
