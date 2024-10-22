import os
import util


def request_processing(client, address, method, url, request, headers, message_body):
    url = util.format_path(url)

    if url == 'root':
        html = '''<!DOCTYPE html>
<html lang="ru">
 <head>
  <link rel="stylesheet" href="/root/source/style.css">
  <title>Наш Hub</title>
  <meta http-equiv="Content-type" content="text/html;charset=utf-8">
 </head>
  <body>
   <div>
   <a href="/bazaar">Наш БаZарик</a>
   </div>
   <div>
   <a href="/storage">Наш Диск</a>
   </div>
   <div>
    <a href="/shop">Наш МагаZ</a>
   </div>
   <div>
   <a href="/music">Наш МуZыка</a>
   </div>
   <div>
   <a href="/man">Наш Слоняра</a>
   </div>
   <div>
   <a href="/chan">Наш Тян</a>
   </div>
  </body>
</html>'''.encode('utf-8')
        client.send(b'HTTP/1.1 200 OK\r\n' + util.make_header(data=html))
        return False
    path, filename = util.get_path_and_name(url)
    path = util.format_path(path)
    if '.' in filename:
        content_type = util.format_to_content_type(util.get_format(url))
        if content_type == '':
            content_type = 'multipart/mixed'
        if filename in os.listdir(path):
            client.send(b'HTTP/1.1 200 OK\r\n' + util.make_header_without_data(content_type=content_type, content_length=os.path.getsize(url)))
            with open(url, 'rb') as f:
                while True:
                    d = f.read(1024)
                    if d:
                        client.send(d)
                        if len(d) < 1024:
                            break
                    else:
                        break
        else:
            client.send(b'HTTP/1.1 404 FILE NOT FOUND\r\n')
    _headers = util.headers_to_dict(headers)
    if 'Connection' in _headers:
        return _headers['Connection'] == 'keep-alive'
    return False
