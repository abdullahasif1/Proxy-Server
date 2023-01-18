import socket

c = socket.socket()


c.connect(('neverssl.com',80))


#response = requests.get('http://neverssl.com')
#print(response)


while True:
    print("connected")
    c.send(bytes('neverssl.com', 'utf-8'))
    #text = 'http://neverssl.com'
    print('-------------')

    print('+++++++')
    recieved_text = c.recv(10000).decode()
    lengthofRT = len(recieved_text)

    print(recieved_text)
    print(lengthofRT)

c.close()
                                                                                             
                
