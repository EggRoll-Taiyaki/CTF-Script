#!/usr/bin/env python3

from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256
import socketserver
import signal
import os
import string
import random
from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime,getStrongPrime
from Crypto.Random import get_random_bytes


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 4096
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def handle(self):
        p=getStrongPrime(512)
        q=getStrongPrime(512)
        e=65537
        n=p*q
        phi=(p-1)*(q-1)
        d=pow(e,-1,phi)
        token=os.urandom(1000//8)
        c=pow(bytes_to_long(token),e,n)
        self.send(b"n=")
        self.send(hex(n).encode())
        
        self.send(b"your token is")
        self.send(hex(c).encode())
        
        signal.alarm(60)
        for i in range(100):
            self.send(b"give me your message to decrypt")
            c=self.recv()
            try:
                c=int(c,16)
            except:
                self.send(b"wrong!")
                self.request.close()
                
            
            m=pow(c,d,n)
            brokenm=m&((2**(40)-1)*(2**492))
            self.send(hex(brokenm).encode())
        self.send(b"give me your token")
        t1=self.recv()
        print(f"{t1=}")
        if bytes.fromhex(t1.decode())==token:
            self.send(b"ezpz")
            print("G_G")
        else:
            self.send(b"wrong! try again!")    
        self.request.close()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = 'localhost', 9999
    print("HOST:POST " + HOST+":" + str(PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
