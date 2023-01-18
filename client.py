import socket

c = socket.socket()

host = "http://www.neverssl.com"
ipAddress = socket.gethostbyname(host)

c.connect((idAddress,80))


while True:
    
    c.send(bytes(host,'utf-8'))


    recieved_text = c.recv(10000).decode()
   

    lengthofRT = len(recieved_text)

    print(recieved_text)
    print(lengthofRT)



c.close()
