import sys
import socket
import threading    
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

def head(_file):
    now = datetime.now()
    stamp = mktime(now.timetuple())
    _data = "HTTP/1.0 200 OK\r\n"
    _data += "Content-Type: text/html; charset=utf-u\r\n"
    _data += "Connection: keep-alive\r\n"
    _data += "Allow: GET, HEAD\r\n"
    _data += "Content-Type: text/html\r\n"
    _data += "data: "+format_date_time(stamp)+"\r\n"
    _data += "Content-Lenght: "+str(len(_file.read()))+"\r\n\r\n"
    return _data


def handleClient(conn,addr):
    print(f'Criando a Thread com o cliente {addr}')
    data=""
    rcv = conn.recv(2048)
    word = str(rcv,"utf-8")
    word_vec = word.split()
    print(f'{addr}:{word}')
    if len(word_vec)!= 0:
        if word_vec[0]== 'GET':
            #data += "<html><body>Hello carai</body><html>\r\n\r\n"
            if word_vec[1]=='/':
                data += head(open("index.html","r"))
                print("aqui")
                data += open("index.html","r").read()
            else:
                try:
                    data += head(open(word_vec[1][1:],"r"))
                    data += open(word_vec[1][1:],"r").read()
                except:
                    print ('deuruim')
                    data+="HTTP/1.0 404 NOT FOUND\r\n"
                    #conn.sendall(data.encode())
            conn.sendall(data.encode())
        if word_vec[0]=='HEAD':
            if word_vec[1]=='/':
                data = head(open("index","r"))
            else:
                try:
                    data = head(open(word_vec[1][1:],"r"))
                except:
                    print ('deuruim')
                    data+="ERRO 404: NOT FOUND"
                    #conn.sendall(data.encode())
            conn.sendall(data.encode())
        if word_vec[0]=='POST':
            #Prec = word_vec[1][2:]
            wFile=open('usr.txt','w')
            if word_vec[1]!='/':
                try:
                    wFile = open(word_vec[1][1:],'r')
                    wFile = open(word_vec[1][1:],'w')
                except:
                    data+="HTTP/1.0 404 NOT FOUND\r\n"


            n=word.find('\r\n\r\n')+4
            print(word[n:])
            prec = word[n:]
            prec = prec.split('&')
            print(prec)
            for x in prec:
                #x.split('=')
                print(x)
                wFile.write(f"{x}\r\n")
            conn.sendall(data.encode())

        

                    



                



       # print(f'{addr}:{word}')


server_address = ('',6789)

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(server_address)
serverSocket.listen(5)

while True:

    print('aguardando conexoes...')
    conn,addr = serverSocket.accept()

    print(f'Conectando com cliente {addr}')
    th = threading.Thread(target=handleClient,args=(conn,addr,))
    th.start()

