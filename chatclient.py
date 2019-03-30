import socket, select, threading, sys

class ChatClient():
    """
    聊天室客户端类
    用以实现客户端的功能
    包括创建客户端socket， 连接服务器， 收发服务器端和其他客户端的数据
    """
    def  __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.client_socket = socket.socket()
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_readlist = [self.client_socket]

    def receivemessage(self):
        while True:
            readline, writelist, errorlist = select.select(self.client_readline, [], [])
            if self.client_socket in readlist:
                try:
                    print(self.client_socket.recv(4096).decode('utf-8'))
                except socket.error as err:
                    print('连接错误...')
                    exit()

    def run(self):
        thread_recievemsg = threading.Thread(target = self.receivemessage)
        thread_recievemsg.start()

        thread_sendmsg = threading.Thread(target=self.sendmessage)
        thread_sendmsg.start()

if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = 8888
    client = ChatClient(HOST, PORT)
    client.run()
    
