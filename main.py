import socket
import pandas
import os

serverPort = 5000  # port number of server = 5000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket connection server.
serverSocket.bind(('', serverPort))  # binding the port number = 5000 with the server.
serverSocket.listen(1)  # let the server listen to the requests.

print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()  # store the HTTP request and both of IP and Port numbers.
    sentence = connectionSocket.recv(1024).decode()  # decode the HTTP request.
    URL = sentence.split()[1]  # store the URL from the HTTP request.

    print()
    print(addr)  # printing both of IP and Port numbers.
    print(sentence)  # printing the HTTP request.
    print()

    if URL == '/' or URL == '/index.html':
        main_html = open('main.html')

        # making the appropriate response
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/html \r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(main_html.read().encode())

        main_html.close()

    elif URL.endswith('.css'):
        style = open('style.css')

        # making the appropriate response
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/css \r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(style.read().encode())

        style.close()

    elif URL.endswith('.jpg') or URL.endswith('.jpg/') or URL.endswith('.png') or URL.endswith('.png/'):
        image_name = URL.split('/')[1]
        image_type = image_name.split('.')[1]
        if image_type == 'jpg':  # change .jpg to .jpeg as required.
            image_type = 'jpeg'

        image = open(os.path.join('images', image_name), 'rb')  # open the image with the specific path.

        # making the appropriate response
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send(('Content-Type: image/' + image_type + '\r\n').encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(image.read())

        image.close()

    elif URL == "/sortPrice" or  URL == "/sortPrice/" or URL == "/sortName" or URL == "/sortName/":
        ls = list(pandas.read_csv('data.csv').to_records(index=False)) # convert data to list of tuples.
        if URL.find("sortPrice") != -1:  # ascending sort according to price.
            ls.sort(key=lambda x: x[1])
        elif URL.find("sortName") != -1:  # ascending sort according to name.
            ls.sort(key=lambda x: x[0])

        spaces = max(len(x[0]) for x in ls) + 1  # get the length of the longest word in names.
        len_for_new_line = max(len(x[0] + str(x[1])) for x in ls) + 11  # variable for spacing to get nice output.
        output = "\n" * 2 + " " * 70 + " Names" + " " * (spaces - 5) + "|   Prices\n"
        for i in range(0, len(ls)):
            output += " " * 70
            output += "_" * len_for_new_line + "\n"
            output += "\n" + " " * 70
            output += " " + str(ls[i][0]) + " " * (spaces - len(ls[i][0])) + "|   " + str(ls[i][1]) + "$\n"

        # making the appropriate response
        connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
        connectionSocket.send('Content-Type: text/plain \r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(output.encode())

    else:
        error = open('Error.html')
        html_code = str(error.read())
        error.close()

        # find the location of IP address in HTML page to output it.
        idx = html_code.index("%")
        html_code = html_code[0:idx] + str(addr[0]) + html_code[idx + 1:]

        # find the location of Porn number in HTML page to output it.
        idx = html_code.index("%")
        html_code = html_code[0:idx] + str(addr[1]) + html_code[idx + 1:]

        # making the appropriate response
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/html \r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(html_code.encode())

    connectionSocket.close()

