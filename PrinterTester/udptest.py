import socket

UDP_IP_ADDRESS = "192.168.40.49"
UDP_PORT_NO = 6789
Message = "Hello, Server"

level = 3

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(str(level).encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
