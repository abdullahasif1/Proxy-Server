import socket, time
import logging
import threading
#import requests
import json
import sys

s = socket.socket()
print('Socket Created')

s.bind(('localhost',9999))

s.listen(20)
print ('Listening...')

def conversion(c,client_addr):    
    client_req = c.recv(10000).decode('utf-8 ', 'replace')           #recieve request
    if(len(client_req)==0):
        return
    if 'CONNECT' in client_req:
        print('Its a CONNECT request')
        connecT(c,client_addr,client_req)
        return

    request_response_header = {}
    request_response_header["Incoming header: "] = client_req
    if "Connection: keep-alive" in client_req:
        client_req = client_req.replace("Connection: keep-alive", "Connection: close")
    if "Proxy-connection: keep-alive" in client_req:
        client_req = client_req.replace("Proxy-connection: keep-alive", "Proxy-connection: close")

    ser_sock = socket.socket()

    
    request_response_header["Modified header: "] = client_req
    #json = json.dumps(request_response_header)



    #port = client_addr[1]                      #creating port name respective log file
    #file_name = str(port) + "_log.txt"
    #logging.basicConfig(filename=file_name, level=logging.INFO)
    #logging.info('Client Request: {} --> {}'.format(client_addr,client_req))



    #print("Route 2: Client's request recieved")
    client_req1 = client_req.split('\n')          #converting request plus headers into list
 #   print(client_req1[0])
  #  host = client_req1[1].strip('Host: ')          # extracting host-name

    status_line = client_req1[0]
    print("client's request: ", client_req1[0])
    #    host = client_req1[4].strip('Host: ')          # extracting host-name
  #  host = status_line.split(" ")[1]
    #odb.outbrain.com:443
  #  host = host.split(':')[0]
    

    for header in client_req1:
        if "Host" in header:
            host = header.split()[1]



    host = host.strip()

    #print("---------------------")
    #print(client_req)


    try:
        ipAddress = socket.gethostbyname(host)
    except:
        pass
    #print("IP address: ", ipAddress)
    try:
        #print("Route 3")
        ser_sock.connect((ipAddress,80))
        #print("Routed 3: Connected with Server")

        #print("Route 4: Requesting to server")
        ser_sock.sendall(bytes(client_req,"utf-8"))
        #print("Route 4: Request sent")
    except Exception as e:
        #print("------------------Error-----------------")
        #print(e)
        #print("Error occured. Terminating the thread")
        return

    #print("Route 5: About to recieve from server")
    server_cont_decoded = ""
       
    while True:
            #1.send(bytes(client_req,"utf-8"))
            #print("Debug: 1")
            server_cont =  ser_sock.recv(10000)
            #print(server_cont)
            size = len(server_cont)
            if size == 0:
                with open(host +'.json', 'w') as f:
                    request_response_header["Server's Response: "] = server_cont_decoded

                    print("name of host -----------------------------------------------------------------------\n",host,"\n\n")
                    print(server_cont_decoded)
                    json.dump(request_response_header, f, indent=2)
                    print('-------------------Json Dump ----------------')
                #print("Route 6: +++++++++++++closing ")
                ser_sock.close()
                c.close()
                break
            c.sendall(server_cont)

            server_cont_decoded = server_cont_decoded + server_cont.decode('ISO-8859-1')
            
            #json.dumps(request_response_header)
            #print('-------------------Json Dump ----------------')
            #print(size)
             
                    


        

        #port = client_addr[1]                      #creating port name respective log file
        #file_name = str(port) + "_log.txt"

        #logging.basicConfig(filename=file_name, level=logging.INFO)
        #logging.info('Client Request: {} --> {}'.format(client_addr,client_req))
        
        #logging.info('Server Respone to: {} --> {}'.format(client_addr,server_resp))


def connecT(c,client_addr, client_req):

       #print("Debug:  1")
        server_sock = socket.socket()
        
        #print("Just entered connect function: Client's request following")
        
        #print("Debug:  2")
        #print(client_req)
        
        client_req1 = client_req.split('\n')          #converting request plus headers into list
        #print("Debug:  3")
        status_line = client_req1[0]
        
        request_response_header = {}
        
        #print("client's request: ", client_req1[0])
        
        request_response_header["Client's Request: "] = client_req1[0]
        

    #   host = client_req1[4].strip('Host: ')          # extracting host-name
        host = status_line.split(" ")[1]
        #odb.outbrain.com:443

        host = host.split(':')[0]
        
      #  host[0] = host[0].strip()
        
        #print("host is : ",host[0])
        
        
        #print("Debug:  4")

        #port = client_addr[1]                      #creating port name respective log file
        #file_name = str(port) + "_log.txt"
        
        #logging.basicConfig(filename=file_name, level=logging.INFO)
        #logging.info(format(json))


        try:
            ipAddress = socket.gethostbyname(host)
        except Exception as e:
            return


        #print("IP address: ", ipAddress)
        #resp200 = "<Response [200]>"
        resp200 = "HTTP/1.1 200 OK\r\n\r\n"
        #resp502 = "<Response [502]>"
        resp502 = "HTTP/1.1 502 Bad Gateway\r\n\r\n"
        try:
            #print("Route 2: trying to connect to requested server")
            server_sock.connect((ipAddress,443))
            #print("Routed 3: Connected with Server, tunnel ready")
            #print("Route 3: Response 200 sending ")
            
            #logging.info('Server Respone to: {} --> {}'.format(client_addr,resp200))       
        
        except Exception as e:        
            #print("------------------Error-----------------")
            #print("Route 2: trying to connect to requested server fail")
            c.sendall(bytes(resp502,"utf-8"))
           
            #request_response_header["Server's Response: "] = resp502
            #json = json.dumps(request_response_header)

        

            #logging.info('Server Respone to: {} --> {}'.format(client_addr,resp502))
            #logging.info(format(json))
            
            return



        
        c.sendall(bytes(resp200,"utf-8"))
        #request_response_header["Server's Response: "] = resp200
       

        #json = json.dumps(request_response_header)
        
        
        print("===================================")
        #print(client_header)
        print("-----------------------------------")


        thread_1 = threading.Thread(target=client_server,args=(c,server_sock,json,))
        thread_1.start()
        

        thread_2 = threading.Thread(target=server_client,args=(c,server_sock,json,))
        thread_2.start()
                       
        #print("Both threads has been created")

     
def client_server(client_socket,server_socket,json):
    
    #print("Inside the thread: client to server")
    while 1:
        data = client_socket.recv(10000)
    
        size = len(data)
        #print("Size = ",size)
        if size == 0:
            server_socket.close()
            #print("Communication ended")
            return
    
        server_socket.sendall(data)
        #logging.info(format(json))
    
    

def server_client(client_socket,server_socket,json):
    while 1:
        #print("Inside the thread: server to client")
        data = server_socket.recv(10000)
    
        size = len(data)
        #print("Size = ",size)
        if size == 0:
            client_socket.close()
            #print("Communication ended")
            return
        client_socket.sendall(data)
        #logging.info(format(json))





while True:
    #print("Debug 1")

    c, addr = s.accept()
    #print("Route 1: Connected with ", addr)
    thread = threading.Thread(target=conversion,args=(c,addr,))
    thread.start()


    
