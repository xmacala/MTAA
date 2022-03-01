import sipfullproxy as sip

sip.logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='proxy.log', level=sip.logging.INFO,datefmt='%H:%M:%S')

ipaddress = "10.54.1.106"

sip.recordroute = "Record-Route: <sip:%s:%d;lr>" % (ipaddress, sip.PORT)
sip.topvia = "Via: SIP/2.0/UDP %s:%d" % (ipaddress, sip.PORT)

server = sip.socketserver.UDPServer((sip.HOST, sip.PORT), sip.UDPHandler)
server.serve_forever()
