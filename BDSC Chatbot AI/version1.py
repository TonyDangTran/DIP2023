#importations
from tkinter import*
import tkinter as tk
from tkinter import simpledialog
import openai #openai module allows me to run a chatbot.
import key

#setting up functions
def query(prompt):
    openai.api_key = key.api_key #Openai API key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=prompt,
        temperature=1, #settings for the chatbot
        max_tokens=250, 
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response

def send(event=None): #function that runs when you click the button widget
    text = entry2.get()
    prompt.append({'role': 'user', 'content': text}) #uses dictionary for chatbot
    response = query(prompt)
    message_content = response['choices'][0]['message']['content']
    prompt.append({'role': 'assistant', 'content': message_content})
    
    text_widget.config(state="normal")
    text_widget.insert("end",f"{display_name}: " + "\n" + text +"\n", "right") #user chat
    text_widget.insert("end", "Chatbot: " + "\n" + message_content + "\n", "left") #chatbot chat
    text_widget.tag_configure("right",justify="right")
    text_widget.tag_configure("left", justify="left")
    text_widget.config(state="disabled")
    entry2.delete(0,"end")
 
def get_name(): #popup window that asks for user input for name
    name = simpledialog.askstring("Input", "Enter the name you wish to be referred as:")
    return name.capitalize()

display_name = get_name() #runs get_name function before the GUI opens. 
prompt=[{'role': 'system', 'content': 'how may I help you?'}] #this will be where the chatbot asks the user for their first question. Currently not implemented. 

#GUI
window = Tk() 
window.geometry("500x750")
window.title("BDSC Chatbot AI")
window.resizable(False, False)

canvas = tk.Canvas(window, width=50, height=50,bg="#89c9ec") #canvas for structured graphics. More usage later on. 
canvas.pack()

entry1 = tk.Text(window,wrap="word",state="disabled",bg="#89c9ec",padx=5,pady=5) #Big entry box for where the text from both chatbot and user will exist.
entry1.place(x=6,y=5,width=493,height=700)


entry2 = tk.Entry(window) #Small textbox for user to input
entry2.place(x=5,y=720,width=420,height=20)
entry2.bind("<Return>", send)


button1 = tk.Button(window, text='Send Msg', command=send) #send message button
button1.place(anchor="se", relx=0.99, rely=0.99)

text_widget = tk.Text(window, height=36, width=59,font="calibri",state="disabled") #text widget 
text_widget.place(x=7, y=6)
 

scrollbar = Scrollbar(window, command=text_widget.yview) #scrollbar
text_widget['yscrollcommand'] = scrollbar.set
scrollbar.place(x=481, y=6, height = 688)

frame = Frame(window)
frame.pack() #packing 
window.configure(background="#5f0137")
window.mainloop()

