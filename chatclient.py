#client

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():      #receive message
  while True:
    try:
      msg = client_socket.recv(BUFSIZ).decode("utf8")
      msg_list.insert(tkinter.END, msg)
    except OSError:  #client has left the chat.
      break

def send(event=None):  #send message
  msg = my_msg.get()
  my_msg.set("")  #clears input field.
  client_socket.send(bytes(msg, "utf8"))
  if msg == "{quit}":
    client_socket.close()
    top.quit()

def on_closing(event=None):     #window is closed.
  my_msg.set("{quit}")
  send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  #send message
my_msg.set("Type your name here.")
scrollbar = tkinter.Scrollbar(messages_frame)  #navigate through past messages.

#store the messages
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = "127.0.0.1"
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  
