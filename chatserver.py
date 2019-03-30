import socket, select

class ChatServer():
    '''
    聊天室服务器类
    用以实现服务器端的功能
    包括创建服务端socket， 连接客户端，手法客户端的数据
    '''
    def  __init__(self, host, port, numOfClients):
        self.HOST = host
        self.PORT = port
        self.server_socket = socket.socket()
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(numOfClients)
        self.socket_list = []
        self.client_names = {}

        self.socket_list.append(self.server_socket)
        print('聊天室已经打开...')

    def connect(self):
        client_conn, client_addr = self.server_socket.accept()
        try:
            welcome_msg = '欢迎来到聊天室，请输入昵称： '
            client_conn.send(welcome_msg.encode('utf-8'))
            client_name = client_conn.recv(4096).decode('utf-8')
            self.socket_list.append(client_conn)
            self.client_names[client_conn] = client_name
            msg = '现在有 ' + str(len(self.client_names)) + ' 名用户在聊天室：['+',  '.join(list(self.client_names.values()))+']'
            client_conn.send(msg.encode('utf-8'))

            for sock in self.client_names.keys():
                if (not sock == client_conn):
                    msg = self.client_name[client_conn] + ' 加入聊天室 '
                    sock.send(msg.encode('utf-8'))
                    
        except Exception as e:
            print(e)

    def disconnect(self):
        self.server_socket.close()

    def run(self):
        disconnection = False
        data = ''
        while True:
            readlist, writelist, errorlist = select.select(self.socket_list, [], [], 36000)
            if not readlist:
                print('没有用户连接， 聊天室关闭...')
                self.disconnect()
                break
            
            for client_socket in readlist:

                if client_socket is self.server_socket:

                    self.connect()

                else:

                    disconnection = False

                    try:

                        data = client_socket.recv(4096).decode('utf-8')
                        data = self.client_names[client_socket] + ' ： ' + data

                    except:

                        data = self.client_names[client_socket] + ' 离开聊天室 '
                        disconnection = True

                if (disconnection):
                    
                    self.socket_list.remove(client_socket)
                    print(data)
                    for sock in self.socket_list:
                        
                        if (not socket == self.server_socket) and (not socket == client_socket):
                            
                            try:
                                sock.send(data.encode('utf-8'))
                            except Exception as e:
                                print(e)

                    del self.client_names[client_socket]

                else:
                    print(data)
                    for sock in self.socket_list:
                        if (not sock == self.server_socket) and (not sock == client_socket):
                            try:
                                sock.send(data.encode('utf-8'))
                            except Exception as e:
                                print(e)


if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = 8888
    server = ChatServer(HOST, PORT, 10)
    server.run()

                                          
                                                               
        
        
