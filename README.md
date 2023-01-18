# Proxy-Server
Transmission Control Protocol (TCP)


Built a HTTP/HTTPS proxy server which helps in creating a secured gate while connecting the web browser to the web servers. Proxy server is capable of dealing HTTP and HTTP Connect requests which are transmitted using TCP.

Features used are socket binding(for the creation of TCP as transport layer), Threading(for dealing multiple request/clients at the same time), Logging(enable/disable logging the payload and the request headers while communicating).
 
Workflow(HTTP): When a browser sends a HTTP request(requesting a web response), which is directed to the proxy server, the proxy server receives the requested header by the socket (for browser-proxy communication) and processes it. A tcp connection request is sent to the requested server by another socket(for proxy-server communication). The response from the server is collected by the proxy(by socket) and after processing it is then forwarded back to the browser(by socket). When the response by the server does not contain anything, it results in ending the connection. After the closure of connection, all the requests and payloads during the connection are then logged(using json dump) and saved as a json file.

Whereas for HTTPS: When a browser sends a HTTP CONNECT Method request a somewhat similar pathway is followed as of HTTP requests, but in a simpler manner. 
After the creation of sockets and TCP connection with the requested server, Requests and Responses are just forwarded to the Browser/Server. 
