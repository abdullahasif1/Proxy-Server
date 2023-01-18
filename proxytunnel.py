import socket, time
import logging
import threading
import requests
import json

s = socket.socket()
print('Socket Created')

s.bind(('localhost',9797))

s.listen(2)
print ('Listening...')

def conversion(c,client_addr):    

        ser_sock = socket.socket()
        
        client_req = c.recv(10000).decode('utf-8 ', 'replace')           #recieve request
        print("Route 2: Client's request recieved")
        
        if 'CONNECT' in client_req:
            print("https present")
        


        client_req1 = client_req.split('\n')          #converting request plus headers into list
        print(client_req1[0])
        host = client_req1[1].strip('Host: ')          # extracting host-name
        if 'www' in client_req1[1]:
            host = host.strip('www.')
        host = host.strip()

        print("---------------------")
        print(client_req)

    
        ipAddress = socket.gethostbyname(host)
       
        
        print("IP address: ", ipAddress)
        resp200 = "200 OK"
        resp502 = "502 Bad Gateway"
        try:
            print("Route 2: trying to connect to requested server")
            ser_sock.connect((ipAddress,80))

            #print("Routed 3: Connected with Server")
            print("Route 3: Response 200 sending ")
            c.sendall(bytes(resp200,"utf-8"))    

            #print("Route 4: Requesting to server")
            #ser_sock.sendall(bytes(client_req,"utf-8"))
            
        except Exception as e:
            print("------------------Error-----------------")
            print("Route 2: trying to connect to requested server fail")
            c.sendall(bytes(resp502,"utf-8"))
            print(e)
            print("Error occured. Terminating the thread")
            return
        
        

        print("Route 5: About to recieve from server")
        server_content = ""
       
        while True:
                
            server_cont =  ser_sock.recv(10000)
            c.sendall(server_cont)
            size = len(server_cont)
            print(size)
            if size== 0:
                print("Route 6: +++++++++++++closing ")
                ser_sock.close()
                c.close()
                break 
                    


        


while True:
    #print("Debug 1")

    print("Waiting for a new connection!!! ")
    c, addr = s.accept()
    print("Route 1: Connected with ", addr)
    thread = threading.Thread(target=conversion,args=(c,addr,))
    thread.start()


    
