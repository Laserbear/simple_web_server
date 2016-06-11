import socket
import json
def parse_packet(packet):
  packet_map = {}
  headers = {}
  packet = packet.split("\r\n")
  packet_map['method'] = packet[0].split(" ")[0]
  packet_map['path'] = packet[0].split(" ")[1]
  packet.remove(packet[0])
  for pair in packet:
    if ":" in pair:
      headers[pair.split(": ")[0]] = pair.split(": ")[1]
      packet.remove(pair)
  packet_map['headers'] = headers
  if "Content-Length" in headers.keys():
    for pair in packet:
      if packet != "":
        packet_map['body'] = pair
      else:
        packet_map['body'] = ""
  return packet_map


def serialize(packet_dict):
  res = "HTTP/1.0"
  res += " " + packet_dict['code'] + "\r\n"
  for key in packet_dict['headers'].keys():
    res += key + ": " + packet_dict['headers'][key] + "\r\n"
  res += "\r\n "
  if "body" in packet_dict:
    res += packet_dict['body']
  return res

def extract_path_and_query(request):
  path = request['path']
  pathname = path.split("?", 1)[0]
  query = path.split("?",1)[1]
  request['query'] = query
  return request

def app(request):
  response = {'headers':{'Content-Type':"text/plain"}}
  response['code'] = "200"
 
  #return serialize(parsed)
  if request['path'] == "/":
    response['body'] = "Hello World"
  elif request['path'] == "/json":
    response['body'] = request
  else:
    response['body'] = "Not Found"
  return response

def json_serialize_body(request):
  if not "Content-Type" in request:
    request['body'] = json.dumps(result['body'])
  return request


def after(app, middle):
  def inner(request):
    return app(middle(request))

def before(app, middle):
  def inner(request):
    return app(middle(request))
  return inner

sock = socket.socket()
sock.bind(('localhost', 8080))
sock.listen(1)
app = before(app, extract_path_and_query)
while True:
  ret, addr = sock.accept()
  print ret
  print "addr", addr
  mess = ret.recv(1024)
  parsed = parse_packet(mess)
  ret.send(serialize(app(parsed)))
  ret.close()





print parse_packet("GET /foo\r\nReferer: /buz\r\n")
print parse_packet("POST /foo\r\nContent-Length: 5\r\n\r\nhello world")
print serialize(parse_packet("POST /foo\r\nContent-Length: 5\r\n\r\nhello world")) == "POST /foo\r\nContent-Length: 5\r\n\r\nhello world"