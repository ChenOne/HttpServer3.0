#coding=utf-8
'''
name: ChenOne
time:2018-10-1
email:632013028@qq.com
'''
from socket import *
import sys
import re
from threading import Thread
from setting import *   # 自己建的模块
import time

class HTTPserver(object):
    def __init__(self,addr = ('0.0.0.0',80)):  # 默认监听80端口
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind(addr)

    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)

    # HTTP服务器启动
    def server_forever(self):
        self.sockfd.listen(10)
        print("Listen the port %d..."%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from", addr)
            handle_client = Thread(target = self.handle_request,args = (connfd,))  # 每当有客户端连接创建新线程
            handle_client.setDaemon(True)  # 设置为True时主线程退出则分支线程也退出
            handle_client.start()   # 启动线程

    def handle_request(self,connfd):
        # 接收浏览器请求
        request = connfd.recv(4096)
        request_lines = request.splitlines()   # 按行切割,返回一个按行切割的列表
        # 获取请求行
        request_line = request_lines[0].decode()

        # 正则表达式提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern, request_line).groupdict()  # 获取到请求方法env["METHOD"]和请求内容env['PATH']
        except:
            response_headlers = "HTTP/1.1 500 Server Error\r\n"
            response_headlers += "\r\n"
            response_body = "Server Error"
            response = response_headlers + response_body
            connfd.send(response.encode())
            return
            
        # 将请求发给frame得到返回数据结果 
        status, response_body = self.send_request(env["METHOD"],env["PATH"])  # 返回值需要响应码和响应内容

        # 根据响应码组织响应头内容
        response_headlers = self.get_headlers(status)

        # 将结果组织为http response 发送给客户端
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()

    # 和框架frame 交互,发送request 获取response
    def send_request(self,method,path):    # 相对WebFrame,这里作为客户端接收response,WebFrame作为服务端接收request
        s = socket()
        s.connect(frame_addr)  # 作为WebFrame的客户端连接

        # 向WebFrame发送method 和 path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status = s.recv(128).decode()
        response_body = s.recv(4096*10).decode()


        return status,response_body


    def get_headlers(self, status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'

        return response_headlers



if __name__ == "__main__":
    http = HTTPserver(ADDR)   # 导入setting之后,配置文件配置会配置ADDR
    http.server_forever()   # 启动服务器




















