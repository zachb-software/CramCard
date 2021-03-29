#!/usr/bin/env python
import PyPDF2
import re
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import socket
import os.path
import threading
import tkinter.messagebox
from os import path
import ipaddress
import platform
from tkinter import Entry
from pathlib import Path
# work on a PDF share mode Future

data_folder = Path("CramCards/")
#Data Entry

top=tkinter.Tk(className="CramCard")

top.configure(bg='seashell3')
var = IntVar()
global results_var
results_var=''
R1 = Radiobutton(top, text="Offset Right", variable=var, value=1)
offset=Entry(top,bd=5,width=35)
R2 = Radiobutton(top, text="Offset Left", variable=var, value=2)
pdf=Entry(top,bd=5,width=32)
pdf2=Entry(top,bd=5,width=32)
cram=Entry(top,bd=5,width=16)
page2=Entry(top,bd=5,width=32)
page21=Entry(top,bd=5,width=32)
page1=Entry(top,bd=5,width=32)
selection=Entry(top,bd=5, width=40)
selection2=Entry(top,bd=5, width=40)
input_line=Text(top,bd=5,height=20,width=35)
output_line=Text(top,bd=5,height=20,width=35)
CRAM_reader=Entry(top,bd=5,width=32)
citation=Text(top,bd=5,height=10,width=35)
page=Entry(top,bd=5,width=32)
ip_address=Entry(top,bd=5,width=32)
file_names=Entry(top,bd=5,width=16)
file_nums=Entry(top,bd=5,width=16)
global s


#Send Files to server
def filesend_loop():
   instance_counter=0
   global s
   message=""
   message="sending".encode()
   s.sendall(message)
   if ".bat" in str(file_names) or "<" in str(file_names) or ">" in str(file_names) or ".php" in str(file_names) or ".exe" in str(file_names) or ".py" in str(file_names) or "{" in str(file_names) or "}" in str(file_names) or "[" in str(file_names) or "]" in str(file_names) or "(" in str(file_names) or ")" in str(file_names):
      tkinter.messagebox.showinfo('Improper Formatting','Please do not include forbidden characters in file name.')
   else:
      print("mode 2"+file_names.get())
      file_to_open = data_folder / file_names.get()
      files=os.listdir(data_folder)
      for f in files:
         if f==file_names.get():
            f = open(file_to_open,'rb')
            message=file_names.get().encode()
            s.sendall(message)
            s.sendall(f.read(2048))
            instance_counter=instance_counter+1
         else:
            pass
      if instance_counter==0:      
         tkinter.messagebox.showinfo('File does not exist','File does not exist')
         back_b

#Receive Files from Server
def filereceive_loop():   
   global s
   message=""
   message="receiving".encode()
   s.sendall(message)
   if ".bat" in str(file_names) or "<" in str(file_names) or ">" in str(file_names) or ".php" in str(file_names) or ".exe" in str(file_names) or ".py" in str(file_names) or "{" in str(file_names) or "}" in str(file_names) or "[" in str(file_names) or "]" in str(file_names) or "(" in str(file_names) or ")" in str(file_names):
      tkinter.messagebox.showinfo('Improper Formatting','Please do not include forbidden characters in file name.')
   else:
      print("mode 1")
      fn=str(file_names.get())
      message=fn.encode()
      s.sendall(message)
      contents=s.recv(2048)
      if contents=="error":
         tkinter.messagebox.showinfo('Invalid File')
      if contents=="No Such File":
         tkinter.messagebox.showinfo('No Such File!')
      else:
         file_to_open = data_folder / file_names.get()
         f = open(file_to_open,'wb')
         f.write(contents)
         f.close()


#Get Available Files from Server
def filelist_loop():   
   global s
   message=""
   message='list'.encode()
   s.sendall(message)
   menu=s.recv(1024).decode()
   print(menu)
   for m in menu:
      input_line.insert(END,m)
   input_line.pack()
   exist_connect.pack_forget()
   close_connect.pack_forget()
   
   file_set.pack()
   
   Back_button.pack()
   

#Connect to Server
def connected():
   global s
   s=socket.socket()
   host=ip_address.get()
   port=8209
   try:
      s.connect((host,port))
      Back_button.pack_forget()
      file_search.pack()
      ip_address.pack_forget()
      connector.pack_forget()
      input_line.pack()
      Back_button.pack()
   except ConnectionError:
      tkinter.messagebox.showinfo('Connection Failed')
      
      back_b()
      back_b()
   except Exception as e:
      tkinter.messagebox.showinfo('Error'+' '+str(e))
      print(str(e))
      back_b()
      back_b()
#Close Connection
def close_conn():
   global s
   s.close()
   ip_address.delete('0', END)
   ip_address.insert(INSERT,'')
   back_b()


#File Deivery Menu
def filesend():
   file_names.pack()
   save_edit.pack_forget()
   Read.pack_forget()
   Create_mode.pack_forget()
   Edit_mode.pack_forget()
   Read_mode.pack_forget()
   Share_mode.pack_forget()
   cram.pack_forget()
   output_line.pack_forget()
   CRAM_reader.pack_forget()
   output_line.pack_forget()
   send.pack_forget()
   Edit.pack_forget()
   citation.pack_forget()
   page.pack_forget()
   page2.pack_forget()
   pdf.pack_forget()
   selection.pack_forget()
   selection2.pack_forget()
   offset.pack_forget()
   R1.pack_forget()
   R2.pack_forget()
   read_box.pack_forget()
#File Send loop initialize
def fileset():
   threading.Thread(target=filesend_loop).start() 
#File Receive loop initialize
def fileget():
   threading.Thread(target=filereceive_loop).start()
#File Check loop initialize
def filelist(): 
   file_names.pack()
   threading.Thread(target=filelist_loop).start()
   Back_button.pack_forget()
   file_search.pack_forget()
   file_set.pack()
   file_get.pack()
   Back_button.pack()
#button organizer

#Back Button
def back_b():
   exist_connect.pack_forget()
   close_connect.pack_forget()
   file_set.pack_forget()
   ip_address.pack_forget()
   file_get.pack_forget()
   pdf2.pack_forget()
   page21.pack_forget()
   citation.pack_forget()
   creator_send.pack_forget()
   page1.pack_forget()
   offset.pack_forget()
   cram.delete('0',END)
   citation.delete('1.0', END)
   page2.delete('0', END)
   page.delete('0', END)
   offset.delete('0', END)
   selection2.delete('0', END)
   selection.delete('0', END)
   connector.pack_forget()
   file_search.pack_forget()
   save_edit.pack_forget()
   Read.pack_forget()
   Create_mode.pack()
   Edit_mode.pack()
   Read_mode.pack()
   Share_mode.pack()
   input_line.delete('1.0',END)
   input_line.pack_forget()
   cram.pack_forget()
   output_line.pack_forget()
   CRAM_reader.pack_forget()
   output_line.pack_forget()
   send.pack_forget()
   Edit.pack_forget()
   citation.pack_forget()
   page.pack_forget()
   page2.pack_forget()
   pdf.pack_forget()
   selection.pack_forget()
   selection2.pack_forget()
   offset.pack_forget()
   R1.pack_forget()
   R2.pack_forget()
   read_box.pack_forget()
   Back_button.pack_forget()
   file_names.pack_forget()
   save_edit.pack_forget()
   Add_mode.pack_forget()
#Text Processing
def text_convert():
   
   global results_vars

   if path.exists('./Docs/'+str(pdf.get())+'.pdf'):
      pdfFileObj = open('./Docs/'+str(pdf.get())+'.pdf', 'rb')
      pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
      try:
         pageObj = pdfReader.getPage(int(page2.get()))
         pa=pageObj.extractText()

         if int(page2.get())-int(page.get())<=0:
            xrange=1
         else:
            xrange=int(page2.get())-int(page.get())
         for x in range(xrange):
            pages=int(x)
            pageObj = pdfReader.getPage(pages)
            pa=pageObj.extractText()
            res=re.findall(str(selection.get())+"(.*?)"+str(selection2.get()),pa,re.DOTALL)
           
            for results in res:
               results=results.replace('\n','')
     
               results_vars=results+"\n"+"\n"+"\n"+"\n"+"CITATIONS:"+citation.get('1.0',END)
        
         writeto_disk(results_vars)
         Back_button.pack()
      except (IndexError, ValueError):
         tkinter.messagebox.showinfo('Improper Formatting','There are not that many pages.')
   else:
       tkinter.messagebox.showinfo('Improper Formatting','No such file exists.')
#Text Merge Module   
def text_convert_get():
   global results_var
 
   if path.exists('./Docs/'+str(pdf.get())+'.pdf'):
      pdfFileObj = open('./Docs/'+str(pdf.get())+'.pdf', 'rb')
      pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
      try:
         pageObj = pdfReader.getPage(int(page2.get()))
         pa=pageObj.extractText()
         if int(page2.get())-int(page.get())<=0:
            xrange=1
         else:
            xrange=int(page2.get())-int(page.get())
         for x in range(xrange):
      
            pages=int(x)
            pageObj = pdfReader.getPage(pages)
            pa=pageObj.extractText()
  
            res=re.findall(str(selection.get())+"(.*?)"+str(selection2.get()),pa,re.DOTALL)
         
            for results in res:
               results=results.replace('\n','')
            
               results_var=results+"\n"+"\n"+"\n"+"\n"+"CITATIONS:"+citation.get('1.0',END)

      except (IndexError, ValueError):
         tkinter.messagebox.showinfo('Improper Formatting','There are not that many pages.')
   else:
      tkinter.messagebox.showinfo('Improper Formatting','No such file exists.')     
#Save Module 
def writeto_disk(ress,editor=""):
   if editor=="edit":
      file_name=pdf.get()
   else:
      file_name=cram.get()
   global results_var
   results_var=ress
 
   if ".bat" in str(file_name) or "<" in str(file_name) or ">" in str(file_name) or ".php" in str(file_name) or ".exe" in str(file_name) or ".py" in str(file_name) or "{" in str(file_name) or "}" in str(file_name) or "[" in str(file_name) or "]" in str(file_name) or "(" in str(file_name) or ")" in str(file_name):
      tkinter.messagebox.showinfo('Improper Formatting','Please do not include forbidden characters in file name.')
   else:
      if(os.path.isfile('CramCards/'+str(file_name)+'.CRAM'))!=True:
         cramcard=open('CramCards/'+str(file_name)+'.CRAM','w')
         input_line.insert(END,results_var.replace("<cRaM>", "").replace("</cRaM>", ""))
         input_line.pack()
         offset_set=var
         if var=="1":
            cramcard.write("<cRaM>"+"\n"+input_line.get()[:-offset_set]+"\n"+"</cRaM>".encode())
         if var=="2":
            cramcard.write("<cRaM>"+"\n"+input_line.get()[offset_set:]+"\n"+"</cRaM>")
         else:
            cramcard.write(results_var) 
      else: 

         cramcard=open('CramCards/'+str(file_name)+'.CRAM','w')
         input_line.insert(END,cramcard.read()+"\n"+results_var.replace("<cRaM>", "").replace("</cRaM>", ""))
         input_line.pack()
         offset_set=var
         if var=="1":
            cramcard.write("<cRaM>"+"\n"+input_line.get()[:-offset_set]+"\n"+"</cRaM>")
            cramcard.close()
         if var=="2":
            cramcard.write("<cRaM>"+"\n"+inputt_line.get()[offset_set:]+"\n"+"</cRaM>")
            cramcard.close()
         else:
            cramcard.write(output_line.get('1.0',END))
         if editor=="edit":
            back_b()
         else:
            cramcard.close()
            Back_button.pack()
def textupdate_convert():
   input_line.insert(END,results)
   input_line.pack()
#Reading Module
def reader():
   global opener
   if path.exists('CramCards//'+CRAM_reader.get()+'.CRAM'):
      opener=open('CramCards/'+CRAM_reader.get()+'.CRAM','r')
      CRAM_reader.delete('0',END)
      for o in opener:
         input_line.insert(END,o.replace("<cRaM>", "").replace("</cRaM>", ""))
      input_line.pack()
      Back_button.pack()
   else:
      tkinter.messagebox.showinfo('Improper Formatting','No such file exists.')   
def write_edit():
   opener.write(END,"<cRaM>"+"\n"+input_line+"\n""</cRaM>")
#Edit save to disk
def writeedit_disk():
   if ".bat "in CRAM_reader.get() or "<" in CRAM_reader.get() or ">" in CRAM_reader.get() or ".php" in CRAM_reader.get() or ".exe" in CRAM_reader.get() or ".py" in CRAM_reader.get() or "{" in CRAM_reader.get() or "}" in CRAM_reader.get() or "[" in CRAM_reader.get() or "]" in CRAM_reader.get() or "(" in CRAM_reader.get() or ")" in CRAM_reader.get():
      tkinter.messagebox.showinfo('Improper Formatting','Please do not include forbidden characters in file name.')
   else:
      cramcard=open('CramCards/'+CRAM_reader.get()+'.CRAM','w+')
      cramcard.write("<cRaM>"+"\n"+input_line.get('1.0', END)+"\n"+"</cRaM>")
      CRAM_reader.delete('0',END)
      cramcard.close()
#Edit guts
def editor():
   Read.pack_forget()
   Edit.pack_forget()

   if path.exists('CramCards/'+CRAM_reader.get()+'.CRAM'):
      opener=open('CramCards/'+CRAM_reader.get()+'.CRAM','r')
      results=opener.read()
   
      input_line.insert(END,results.replace("<cRaM>","").replace("</cRaM>","").replace("CIT!","\n").replace("!CIT",""))
      input_line.pack()
      save_edit.pack()
      Add_mode.pack()
      Back_button.pack()
      CRAM_reader.delete('0',END)
   else:
      tkinter.messagebox.showinfo('Improper Formatting','No such file exists.')      
Edit=tkinter.Button(top,text="Edit Text", command=editor,bg="honeydew2") 
#Create File Menu
def create_mode(moded=""):
   Read.pack_forget()
   Read_mode.pack_forget()
   Create_mode.pack_forget()
   Edit_mode.pack_forget()
   Share_mode.pack_forget()
   Read.pack_forget()
   
   pdf.insert(0,'What PDF would you like to dissect?')
   pdf.pack()
   selection.insert(0,'Select START word to form 1st parameter to select passage')
   selection2.insert(0,'Select END word to form 2nd parameter to select passage')
   selection.pack()
   selection2.pack()
   offset.insert(0,'How many offset spaces do you need?')
   offset.pack()
   R1.pack(anchor = W)
   R2.pack(anchor = W)
   page.insert(0,'Which Page do you want to select to begin?')
   page2.insert(0,'Which Page do you want to select to end?')
   page.pack()
   page2.pack()
  
   cram.insert(0,"Save CramCard as")
   cram.pack()

   citation.insert(END,"Enter a citation for the work being quoted.")
   citation.pack()
   send.pack()
   Back_button.pack()
#Modify Menu
def createadd_mode():
   global page21
   global page1
   save_edit.pack_forget()
   Add_mode.pack_forget()
   Read.pack_forget()
   Read_mode.pack_forget()
   Create_mode.pack_forget()
   Edit_mode.pack_forget()
   Share_mode.pack_forget()
   Read.pack_forget()
   pdf2.insert(0,'What PDF would you like to dissect?')
   pdf2.pack()
   selection.insert(0,'Select START word to form 1st parameter to select passage')
   selection2.insert(0,'Select END word to form 2nd parameter to select passage')
   selection.pack()
   selection2.pack()
   offset.insert(0,'How many offset spaces do you need?')
   offset.pack()
   R1.pack(anchor = W)
   R2.pack(anchor = W)
   page1.insert(0,'Which Page do you want to select to begin?')
   page21.insert(0,'Which Page do you want to select to end?')
   page1.pack()
   page21.pack()
  
   cram.insert(0,"Save CramCard as")
   cram.pack()
   citation.insert(END,"Enter a citation for the work being quoted.")
   citation.pack()
   creator_send.pack()
   
   global results_var
   

#Create guts
def creator_mode():
   if "<" in str(pdf2.get()) or ">" in str(pdf2.get()) or ".php" in str(pdf2.get()) or ".exe" in str(pdf2.get()) or ".py" in str(pdf2.get()) or "{" in str(pdf2.get()) or "}" in str(pdf2.get()) or "[" in str(pdf2.get()) or "]" in str(pdf2.get()) or "(" in str(pdf2.get()) or ")" in str(pdf2.get()):
      tkinter.messagebox.showinfo('Improper Formatting','Please do not include forbidden characters in file name.')
   else:
      pdfFileObj2 = open('./Docs/'+str(pdf2.get())+'.pdf', 'rb')
      pdfReader2 = PyPDF2.PdfFileReader(pdfFileObj2)
      try:
         pageObj2 = pdfReader2.getPage(int(page21.get()))
         pa=pageObj2.extractText()
         if int(page21.get())-int(page1.get())<=0:
            xrange=1
         else:
            xrange=int(page21.get())-int(page1.get())
         for x in range(xrange):

            pages=int(x)
            pageObj2 = pdfReader2.getPage(pages)
            pa=pageObj2.extractText()
            res=re.findall(str(selection.get())+"(.*?)"+str(selection2.get()),pa,re.DOTALL)
    
            for results in res:
               results=results.replace('\n','')
         
               results_var=results
               input_line.insert(END,results_var)
               input_line.pack()#test add mode 
               details_temp="<cRaM>"+"\n"+input_line.get('1.0',END)+"CIT!"+citation.get('1.0',END)+"!CIT"+"\n"+"</cRaM>"
               writeto_disk(details_temp)
      except (IndexError, ValueError):
         tkinter.messagebox.showinfo('Improper Formatting','There are not that many pages.')
#Edit Menu
def edit_mode():
   Read_mode.pack_forget()
   Read.pack_forget()
   Create_mode.pack_forget()
   Edit_mode.pack_forget()
   Share_mode.pack_forget()
   Read.pack_forget()
   CRAM_reader.pack()
   Edit.pack()
   Back_button.pack()
#read menu
def read_mode():
   Read_mode.pack_forget()
   Create_mode.pack_forget()
   Edit_mode.pack_forget()
   Share_mode.pack_forget()
   Read_mode.pack_forget()
   Read.pack_forget()
   CRAM_reader.insert(0,'Enter an existing CramCard to read it')
   CRAM_reader.pack()
   read_box.pack()
   Back_button.pack()
Read=tkinter.Button(top,text="Read existing CramCard", command=reader,bg="honeydew2") 
#Share guts
def share_mode():
   if not ip_address.get():
      ip_address.pack()
      connector.pack()
      close_connect.pack_forget()
   else:
      connector.pack_forget()
      ip_address.pack_forget()
      exist_connect.pack()
      close_connect.pack()
   file_set.pack_forget()
   Back_button.pack()
   save_edit.pack_forget()
   Read.pack_forget()
   Create_mode.pack_forget()
   Edit_mode.pack_forget()
   Read_mode.pack_forget()
   Share_mode.pack_forget()
   cram.pack_forget()
   output_line.pack_forget()
   CRAM_reader.pack_forget()
   output_line.pack_forget()
   send.pack_forget()
   Edit.pack_forget()
   citation.pack_forget()
   page.pack_forget()
   page2.pack_forget()
   pdf.pack_forget()
   selection.pack_forget()
   selection2.pack_forget()
   offset.pack_forget()
   R1.pack_forget()
   R2.pack_forget()
   read_box.pack_forget()
#Button Complex
Create_mode=tkinter.Button(top,text="CREATE Text", command=create_mode,bg="honeydew2") 
Edit_mode=tkinter.Button(top,text="EDIT Text", command=edit_mode,bg="honeydew2") 
Read_mode=tkinter.Button(top,text="READ Text", command=read_mode,bg="honeydew2")
Share_mode=tkinter.Button(top,text="SHARE Text",command=share_mode,bg="honeydew2")
send=tkinter.Button(top,text="Save Text",command=text_convert,bg="honeydew2")
save_edit=tkinter.Button(top,text="Save Text",command=writeedit_disk,bg="honeydew2")
Back_button=tkinter.Button(top,text="BACK",command=back_b,bg="honeydew2")
read_box=tkinter.Button(top,text="Read",command=reader,bg="honeydew2")
edit_box=tkinter.Button(top,text="Read",command=write_edit,bg="honeydew2")
connector=tkinter.Button(top,text="Connect",command=connected,bg="honeydew2")
exist_connect=tkinter.Button(top,text="Current Server",command=connected,bg="honeydew2")
close_connect=tkinter.Button(top,text="Close Connection to Existing Server",command=close_conn,bg="honeydew2")
file_set=tkinter.Button(top,text="Send File",command=fileset,bg="honeydew2")
file_search=tkinter.Button(top,text="Search",command=filelist,bg="honeydew2")
file_get=tkinter.Button(top,text="Get File",command=fileget,bg="honeydew2")
Add_mode=tkinter.Button(top,text="ADD Text", command=createadd_mode,bg="honeydew2") 
update_send=tkinter.Button(top,text="update Text",command=textupdate_convert,bg="honeydew2")
creator_send=tkinter.Button(top,text="Merge to New File",command=creator_mode,bg="honeydew2")
Create_mode.pack()
Edit_mode.pack()
Read_mode.pack()
Share_mode.pack()
top.mainloop()