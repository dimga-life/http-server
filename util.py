import json
import os
import time
import requests
from urllib.parse import unquote


# HDRS_HTML = 'Content-Type: text/html; charset=utf-8\r\n\r\n'
# HDRS_DATA = 'Content-Type: multipart/form-data; boundary=ExampleBoundaryString\r\n\r\n'
# HDRS_CSS  = 'Content-Type: text/css; charset=utf-8\r\n\r\n'
# HDRS_JS   = 'content-type: text/javascript; charset=utf-8\r\n\r\n'
# HDRS_404  = 'Content-Type: text/html; charset=utf-8\r\n\r\n'


with open('mime_type.json') as f:
    MIME_TYPE = json.load(f)


def headers_to_dict(header: str):
    parameters = {}
    for head in header.split('\r\n'):
        index = head.index(':')
        value = head[index + 1:]
        parameters[head[:index]] = value[1:] if value.startswith(' ') else value
    return parameters


def url_to_request(url):
    text = ''
    for part in url.split('+'):
        if part:
            text += f'{unquote(part)} '
    return text[:-1]


def get_ip_info(ip, token='8869c904953fe7'):
    response = requests.get(f'https://ipinfo.io/{ip}', {'token': token})
    data = response.json()
    if 'country' in data and 'city' in data and 'region' in data:
        return data['country'], data['city'], data['region']
    return None


def get_gmt(sec: int | None = None, gmt=18_000):
    tm = time.localtime((int(time.time() - gmt) if sec is None else sec))
    weeks = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    mons = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    return f'{weeks[tm.tm_wday]}, {tm.tm_mday} {mons[tm.tm_mon]} {tm.tm_year} {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec} GMT'


def make_starting_line(version='1.1', status_code=200, reason_phrase='OK'):
    return f'HTTP/{version} {status_code} {reason_phrase}'.encode('ansi')


def make_header(last_modified: int | None = None, content_language='ru', content_type='text/html; charset=utf-8',
                connection='close', data=b'', accept_ranges='', etag=''):
    header = f'Date: {get_gmt()}\r\n'
    header += 'Server: Apache\r\n'
    header += f'Last-Modified: {get_gmt(last_modified)}\r\n'
    if etag:
        header += f'Etag: "{etag}"\r\n'
    header += f'Content-Language: {content_language}\r\n'
    header += f'Content-Type: {content_type}\r\n'
    header += f'Content-Length: {len(data)}\r\n'
    if accept_ranges:
        header += f'Accept-ranges: {accept_ranges}\r\n'
    header += f'Connection: {connection}\r\n\r\n'

    return header.encode('ansi') + data


def make_header_without_data(last_modified: int | None = None, content_language='ru',
                             content_type='text/html; charset=utf-8', connection='close', content_length=0,
                             accept_ranges='', etag='', content_range=''):
    header = f'Date: {get_gmt()}\r\n'
    header += 'Server: Apache\r\n'
    header += f'Last-Modified: {get_gmt(last_modified)}\r\n'
    if etag:
        header += f'Etag: "{etag}"\r\n'
    header += f'Content-Language: {content_language}\r\n'
    header += f'Content-Type: {content_type}\r\n'
    header += f'Content-Length: {content_length}\r\n'
    if accept_ranges:
        header += f'Accept-ranges: {accept_ranges}\r\n'
        header += f'Content-Range: {content_range}\r\n'
    header += f'Connection: {connection}\r\n\r\n'

    return header.encode('ansi')


def format_to_content_type(text: str):
    format_name = text[text.index('.'):]
    if format_name in MIME_TYPE:
        return MIME_TYPE[format_name]
    return ''


def mkdirs(path):
    p = ''
    for folder in path.split('/'):
        try:
            if folder not in os.listdir(None if p == '' else p):
                os.mkdir(f'{p}{folder}')
        except FileExistsError:
            pass
        p += f'{folder}/'


def format_path(path):
    path = path.replace('\\', '/')
    while True:
        if path and path[0] == '/':
            path = path[1:]
        else:
            break
    while True:
        if '//' in path:
            path = path.replace('//', '/')
        else:
            break
    return path


def get_meta_line(metadata: str, key: str):
    lines = metadata.split('\n')
    for line in lines:
        if line.startswith(key):
            text = line[len(key):]
            return text[1:] if text and text[0] == ' ' else text
    raise KeyError


def formating_text(t1, t2):
    return f'{t1} {"-" * (30 - len(t1))}> {t2}'


def request_to_dict(request: str):
    d = {}
    for line in request.split('\n'):
        if ':' in line:
            i = line.index(':')
            d[line[:i]] = 0
    return d


def get_name(text):
    name = ''
    for i in text[::-1]:
        if i == '/':
            break
        else:
            name += i
    return name[::-1]


def get_path(text):
    return text[:-len(get_name(text))]


def get_path_and_name(text):
    return get_path(text), get_name(text)


def get_format(text):
    if '.' in text:
        return text[len(text) - text[::-1].index('.') - 1:]
    return ''


def get_size(file):
    try:
        size = 0
        for name in os.listdir(file):
            size += get_size(f'{file}/{name}')
        return size
    except NotADirectoryError:
        return os.path.getsize(file)
