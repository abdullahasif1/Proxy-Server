mport socket, time
import logging
import threading

s = socket.socket()
print('Socket Created')

#s.bind(('localhost',9999))

s.listen(3)
print ('Listening...')

def conversion(c,client_addr):
    
    while True:    
        
        client_text = c.recv(10000).decode()
        port = client_addr[1]
        file_name = str(port) + "_log.txt"
        logging.basicConfig(filename=file_name, level=logging.INFO)
        logging.info('Client Request: {} --> {}'.format(client_addr,client_text))
        if 'http' in client_text:
            print('http Request')
        if 'HTTP' in client_text:
            print('HTTP Request')
        if 'exit' in client_text:
            print("Closing connection with port " + str(port))
            c.close()
            break

        client_text = client_text.split()
        client_text = client_text[-1::-1]
        server_resp = ' '.join(client_text)
        c.send(bytes(server_resp, 'utf-8'))
        logging.info('Server Respone to: {} --> {}'.format(client_addr,server_resp))

while True:
    #print("Debug 1")

    print("Waiting for a new connection!!! ")
    c, addr = s.accept()
    print("Connected with ", addr)
    thread = threading.Thread(target=conversion,args=(c,addr,))
    thread.start()
    



    
