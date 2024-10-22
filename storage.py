import util

FORMATS = {
  ".txt": "images/txt_file.png",
  ".rar": "images/archive.png",
  ".zip": "images/archive.png",
  ".7z": "images/archive.png",
  ".pptx": "images/pptx_file.png",
  ".rtf": "images/rtf_file.png",
  ".xlsx": "images/xlsx_file.png",
  ".docx": "images/docx_file.png",
  "": "images/folder.png",
  "?": "images/file.png"
}


def get(client, address, request):
    pass


def post(client, address, request):
    pass


def request_processing(client, address, method, url, request, headers, message_body):
    client.sned(b'HTTP/1.1 501 WORKING ON STORAGE\r\n')
    _headers = util.headers_to_dict(headers)
    if 'Connection' in _headers:
        return _headers['Connection'] == 'keep-alive'
    return False
