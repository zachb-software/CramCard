#!/usr/bin/env python
import socket
import os
import signal
import sys
import tkinter
import threading
import tkinter.messagebox
from tkinter import *
import platform
from pathlib import Path
direct='SHARE'
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host=socket.gethostname()
print(socket.gethostbyname(socket.getfqdn()))
port=8209
s.bind((host,port))
s.listen(5)
data_folder = Path("SHARE/")

#end connection safely
def closed():
   os.system("fuser -k 8209/tcp")
   quit()
#selection menu
def select_menu():
   
   
   try:
      mode=""
      if mode=="":
         mode=c.recv(1024)
     #list mode
      if mode.decode()=="list":
         file_list=""
         files=os.listdir(direct)

         for f in files:
            file_list=file_list+"\n"+f
         print(file_list)
         c.sendall(file_list.encode())
         print(mode.decode())
         if mode.decode()=="list":
            select_menu() 
      #send to server
      if mode.decode()=="sending":
         name=c.recv(2048)
         print(name.decode())
         name2=name.decode()
         if "<" in name2 or ">" in name2 or ".bat" in name2 or ".php" in name2 or ".exe" in name2 or ".py" in name2 or "{" in name2 or "}" in name2 or "[" in name2 or "]" in name2 or "(" in name2 or ")" in name2:
            print("Please don't send corrupted docs") 
         else:
            try:
               file_to_open = data_folder / name2
               l=open(file_to_open,"wb")
               content=c.recv(2048)
               l.write(content)
    
               print(content)
               l.close()
            except:
               pass
         print(mode.decode())
         if mode.decode()=="sending":
            select_menu()
      #send to client
      if mode.decode()=="receiving":
         name=c.recv(2048)
         print(name)
         n=name.decode()
         if ".CRAM" not in n:
            print("Please send a valid file name")
         else:
            try:
               file_to_open = data_folder / n
               l=open(file_to_open,"rb")
               c.send(l.read(2048))
               print("sending")
            except FileNotFoundError:
               c.send("No Such File").encode()
            except:
               c.send("error").encode()
         print(mode.decode())
         if mode.decode()=="receiving":
            select_menu()


      
   except KeyboardInterrupt:
        c.close()
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        
        sys.exit()
#button matrix
def button_():
   top = tkinter.Tk()
   B = tkinter.Button(top, text ="Close",command=closed)
   B.pack()
   top.mainloop() 
threading.Thread(target=button_).start()
while True:
  
   c,addr=s.accept()
   threading.Thread(target=select_menu).start()

   
   
      
     



   