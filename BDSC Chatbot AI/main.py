#importations
from tkinter import*
import tkinter as tk
from tkinter import simpledialog
import openai #openai module allows me to run a chatbot.
import key

#setting up functions

class Chatbot: #encapsulating
    def __init__(self):
        self.prompt = [{'role': 'system', 'content': 'Hi! My name\'s BDSC Assistant, a chatbot designed to help and communicate with students, parents, teachers and more to help guide their way to find information on the Botany Downs Secondary College (BDSC) Website. How may I help you?'}]
        self.display_name = self.get_name()
        self.create_gui()

    def query(self, prompt):
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
    
    def error(self):
        error_message = "Please enter a valid message."
        self.text_widget.config(state='normal')
        self.text_widget.insert("end","BDSC Assistant:" + "\n" + error_message + "\n", "left")
        self.text_widget.tag_configure("left",justify="left")
        self.text_widget.config(state="disabled")
        self.entry2.delete(0,"end")
        

    def send(self, event=None): #function that runs when you click the button widget
        text = self.entry2.get()

        if not text:
            Chatbot.error(self)
        elif len(text) == 1:
            Chatbot.error(self)
        else:
            self.prompt.append({'role': 'user', 'content': text}) #uses dictionary for chatbot
            response = self.query(self.prompt)
            message_content = response['choices'][0]['message']['content']
            self.prompt.append({'role': 'assistant', 'content': message_content})
            
            self.text_widget.config(state="normal")
            self.text_widget.insert("end",f"{self.display_name}: " + "\n" + text +"\n", "right") #user chat
            self.text_widget.insert("end", "BDSC Assistant: " + "\n" + message_content + "\n", "left") #chatbot chat
            self.text_widget.tag_configure("right",justify="right")
            self.text_widget.tag_configure("left", justify="left")
            self.text_widget.config(state="disabled")
            self.entry2.delete(0,"end")
    
    def get_name(self): #popup window that asks for user input for name
       while True:
            name = simpledialog.askstring("Input", "Enter the name you wish to be referred as:")
            if name is not None and name.strip() != "":
                return name.capitalize()
    


    def create_gui(self):#GUI
        self.window = Tk() 
        self.window.geometry("500x750")
        self.window.title("BDSC Chatbot AI")
        self.window.resizable(False, False)

        canvas = tk.Canvas(self.window, width=50, height=50,bg="#89c9ec") #canvas for structured graphics. More usage later on. 
        canvas.pack()

        self.entry1 = tk.Text(self.window,wrap="word",state="disabled",bg="#89c9ec",padx=5,pady=5) #Big entry box for where the text from both chatbot and user will exist.
        self.entry1.place(x=6,y=5,width=493,height=700)


        self.entry2 = tk.Entry(self.window) #Small textbox for user to input
        self.entry2.place(x=5,y=720,width=420,height=20)
        self.entry2.bind("<Return>", self.send)


        button1 = tk.Button(self.window, text='Send Msg', command=self.send) #send message button
        button1.place(anchor="se", relx=0.99, rely=0.99)

        self.text_widget = tk.Text(self.window, height=36, width=59,font="calibri",state="disabled") #text widget 
        self.text_widget.place(x=7, y=6)
        intro_message = self.prompt[0]['content']
        self.text_widget.config(state="normal",wrap="word")
        self.text_widget.insert("end", "BDSC Assistant: " + "\n" + intro_message + "\n", "left")
        self.text_widget.tag_configure("left", justify="left")
        self.text_widget.config(state="disabled")
        

        scrollbar = Scrollbar(self.window, command=self.text_widget.yview) #scrollbar
        self.text_widget['yscrollcommand'] = scrollbar.set
        scrollbar.place(x=481, y=6, height = 688)

        frame = Frame(self.window)
        frame.pack() #packing 
        self.window.configure(background="#5f0137")

    def run(self):
         self.window.mainloop()

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()

