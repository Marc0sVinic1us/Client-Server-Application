import socket

SERVER_HOST = ""
SERVER_PORT = 8080
DOCUMENT_ROOT = "htdocs"  # Diretório raiz onde os arquivos são armazenados

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print("Servidor em execução...")
print("Escutando por conexões na porta %s" % SERVER_PORT)


def parse_request(request):
    
    method, path, headers, body = request.split('\r\n', 3)
    filename = method.split()[1]
    headers = dict(header.split(': ', 1) for header in headers.split('\r\n')[1:])
    
    return filename, method, path, headers, body


def handle_put_request(filename, body):

    # Try e except para tratamento de erro
    try:
        # Escreve o arquivo com o corpo da requisição
        fin = open("htdocs" + filename, "wb")
        fin.write(body.encode())
        fin.close()
        
        return "HTTP/1.1 200 OK\n\n"
    
    except:
        # Caso ocorra algum erro ao criar/sobrescrever um arquivo, gera uma resposta de erro
        return "HTTP/1.1 500 INTERNAL ERROR\n\n<h1>ERROR 500!<br>INTERNAL ERROR!</h1>"


def handle_get_request(filename):
    
    # Verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
    if filename == "/":
        filename = "/index.html"

    if filename == "/ipsum":
        filename = "/ipsum.html"

    # Try e except para tratamento de erro
    try:
        # Abrir o arquivo e enviar para o cliente
        fin = open("htdocs" + filename)
        content = fin.read()
        fin.close()
        
        return "HTTP/1.1 200 OK\n\n" + content
    
    except:
        # Caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
        return "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"


while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(8192).decode('utf-8')
    
    if request:

        # Exibe a requisição feita pelo cliente
        print(request)
        
        # Faz a separação dos componentes da requisição
        filename, method, path, headers, body = parse_request(request)
        
        # Caso PUT
        if 'PUT' in method:
            response = handle_put_request(filename, body)
        
        # Caso GET
        elif 'GET' in method:
           response = handle_get_request(filename)
        
        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        
        client_connection.sendall(response.encode('utf-8'))
    
    client_connection.close()

server_socket.close()
