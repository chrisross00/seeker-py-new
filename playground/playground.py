# # want to see if a hashed html page stored as an object is different when the smallest thing changes

# import urllib.request
# fp = urllib.request.urlopen("http://www.python.org")
# tp = urllib.request.urlopen("http://www.python.org")

# mybytes = fp.read()

# mystr = mybytes.decode("utf8")
# fp.close

# print(mystr)
# # pyngrok testing
from pyngrok import ngrok

ngrok.set_auth_token("281yp8vS4XPZST04lY4MH324v54_Lj1PAyfoUvsB6o6utPXc")
http_tunnel = ngrok.connect(5000)
print(http_tunnel.public_url)

ngrok.disconnect(http_tunnel.public_url)