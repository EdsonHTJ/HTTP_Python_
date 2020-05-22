import sys
import socket
import threading  
import os
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import gzip
from io import StringIO



def head(path,Type):
    now = datetime.now()
    stamp = mktime(now.timetuple())
    _data = "HTTP/1.0 200 OK\r\n"
    _data += "Connection: keep-alive\r\n"
    _data += "Allow: GET, HEAD\r\n"
    _data += "Content-Lenght: "+str(len(open(path,"rb").read()))+"\r\n"
    _data += "Content-Type: "+Type+"\r\n"
    _data += "Expires: "+format_date_time(stamp)+"\r\n"
    _data += "Content-Encoding: \r\n"
    _data += "Last-Modified: "+format_date_time(os.stat(path).st_mtime)+"\r\n"
    _data += "\r\n"
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
            if word_vec[1]=='/':
                data += head("index.html","text/html; charset=utf-8")
                print("aqui")
                data += open("index.html","r").read()
                data = data.encode()
            else:
                try:
                    if "css" in word_vec[1][1:]:
                        data += head(word_vec[1][1:],"text/css; charset=utf-8")
                        print("aqui2")
                        data = data.encode()
                        data += open(word_vec[1][1:],"r").read().encode()
                        print("Aqui3")
                        print("Aqui4")
                    if "jpg" in word_vec[1][1:]:
                        data += head(word_vec[1][1:],"image/jpeg")
                        data = data.encode()
                        print("aqui2")
                        data += open(word_vec[1][1:],"rb").read()
                        print("aqui3")
                    else:
                        data += head(word_vec[1][1:],"text/html; charset=utf-8")
                        data += open(word_vec[1][1:],"r").read()
                        data = data.encode()
                except:
                    print ('deuruim')
                    data =""
                    data+="HTTP/1.0 404 NOT FOUND\r\n"
                    data = data.encode()
                    #conn.sendall(data.encode())
            conn.sendall(data)
        if word_vec[0]=='HEAD':
            if word_vec[1]=='/':
                data = head("index.html","text/html; charset=utf-8")
            else:
                try:
                    if "css" in word_vec[1][1:]:
                        data += head(word_vec[1][1:],"text/css; charset=utf-8")
                    else:
                        data += head(word_vec[1][1:],"text/html; charset=utf-8")
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
                    data+="HTTP/1.0 200 OK\r\n"
                    data += "Connection: Close\r\n\r\n"
                    data+="DEUBOM\r\n"
                except:
                    data+="HTTP/1.0 404 NOT FOUND\r\n"
                    data += "Connection: Close\r\n"
            else:
                data+="HTTP/1.0 200 OK\r\n"
                data += "Connection: Close\r\n\r\n"
                data+="DEUBOM\r\n"


            n=word.find('\r\n\r\n')+4
            print("\r\n Post recebido:")
            print(word[n:])
            print("Post separado:")
            prec = word[n:]
            prec = prec.split('&')
            print(prec)
            i=1
            for x in prec:
                print(f"Chave/valor {i}:")
                #x.split('=')
                print(x)
                wFile.write(f"{x}\r\n")
                i+=1
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
    

