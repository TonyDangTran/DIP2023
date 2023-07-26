#Version 3 of BDSC Chatbot AI
#importations
from tkinter import*
import tkinter as tk
from tkinter import simpledialog
import openai #openai module allows me to run a chatbot.
import key #API key is imported via external file for security purposes.
import csv 

#main application class, core logic 
class Chatbot: #encapsulating methods 
    def __init__(self): #attributes, Initialization 
        #This initialization is for the chatbot, main display GUI window, and seperate dialog box for name input. 
        self.prompt = [{'role': 'system', 'content': 'Hi! My name\'s BDSC Assistant, a chatbot designed to help and communicate with students, parents, teachers and more to help guide their way to find information on the Botany Downs Secondary College (BDSC) Website. How may I help you? \n\n Here are a few frequently asked questions:''\n'}] 
        message_content = self.faq()
        self.prompt.append({'role': 'assistant', 'content': message_content})
        self.display_name = self.get_name() #runs name check dialog box.
        self.create_gui(message_content) #opens GUI afterwards. 

    def faq(self):
        faq_prompt = [{'role': 'user', 'content': 'what are some frequently answered questions about Botany Downs Secondary College (BDSC)? only 5 questions only'}]
        response = self.query(faq_prompt)
        message_content = response['choices'][0]['message']['content']
        self.prompt.append(faq_prompt[0])
        self.prompt.append({'role': 'assistant', 'content': message_content})
        return message_content   

    def query(self, prompt): 
        openai.api_key = key.api_key #Openai API key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", #uses chat-gpt-3.5-turbo.
            messages=prompt, #sets the messages it receives as the prompts inputted by the end-user
            temperature=1, #Message mood. 1 is default. Lower = more emotional, Higher number = more informative.
            max_tokens=250, #limits queries to prevent spam.
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response
    def error(self): #error method. Will run when there is invalid/null input.
            error_message = "Please enter a valid message."
            self.text_widget.config(state='normal')
            self.text_widget.insert("end", "BDSC Assistant:" + "\n" + error_message + "\n", "left")
            self.text_widget.tag_configure("left", justify="left")
            self.text_widget.config(state="disabled")
            self.entry2.delete(0, "end")

    def save_to_csv(self, filename='conversation.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Role', 'Content'])  # Writing header row
            for message in self.prompt:
                writer.writerow([message['role'], message['content']])        

    def send(self, event=None): #function that runs when you click the button widget
        text = self.entry2.get().strip()

        if not text:
            Chatbot.error(self) #if not a valid text, chatbot.error(self) method defined before will run.
        elif len(text) == 1: #minimum of 2 characters otherwise invalid input.
            Chatbot.error(self) 
        else:

            self.prompt.append({'role': 'user', 'content': text}) #user's prompt 
            response = self.query(self.prompt) #user input
            message_content = response['choices'][0]['message']['content'] #reply by chatbot
            self.prompt.append({'role': 'assistant', 'content': message_content}) #appends reply via dictionary
            self.save_to_csv()
            self.text_widget.config(state="normal")
            self.text_widget.insert("end", f"{self.display_name}: " + "\n" + text + "\n" +"\n", "right") #user chat
            self.text_widget.insert("end", "BDSC Assistant: " + "\n" + message_content + "\n" + "\n", "left") #chatbot chat
            self.text_widget.tag_configure("right", justify="right") #positions user chat on the right
            self.text_widget.tag_configure("left", justify="left") #positions user chat on the left
            self.text_widget.config(state="disabled")
            self.entry2.delete(0, "end")

    def get_name(self): #popup window that asks for user input for name
        while True:
            name = simpledialog.askstring("Input", "Enter the name you wish to be referred as. Enter Blank if you would like to remain anonymous.")
            if name is not None and name.strip() != "": #catches null inputs
                return name.capitalize().strip()
            else:
                return "Anonymous"
            
    def create_gui(self,faq_response): #GUI
        self.window = Tk()
        self.window.geometry("500x350")
        self.window.title("BDSC Chatbot AI")
        self.window.resizable(False, False) #makes window unmodifiable, keeping it at "500x750" permanently. 

        canvas = tk.Canvas(self.window, width=50, height=50, bg="#89c9ec") #canvas frame to display graphics and layering.
        canvas.pack()

        self.entry1 = tk.Text(self.window, wrap="word", state="disabled", bg="#89c9ec", padx=5, pady=5) #Layer behind that contains text
        self.entry1.place(x=6, y=5, width=493, height=315)

        self.entry2 = tk.Entry(self.window) #user entry box
        self.entry2.place(x=6, y=320, width=420, height=25)
        self.entry2.bind("<Return>", self.send)
        self.entry2.insert(0,"Enter text here...")
        self.entry2.config(fg="grey") 
        self.entry2.bind("<FocusIn>",self.clear_placeholder)

        button1 = tk.Button(self.window, text='Send Msg', command=self.send) #send button, runs send method
        button1.place(anchor="se", relx=0.99, rely=0.99)

        self.text_widget = tk.Text(self.window, height=16, width=59, font="calibri", state="disabled") #text widget that keeps chatbot messages
        self.text_widget.place(x=7, y=6)
        intro_message = self.prompt[0]['content']
        self.text_widget.config(state="normal",wrap="word")
        self.text_widget.insert("end", "BDSC Assistant: " + "\n" + intro_message + "\n", "left") #Introduction message by chatbot
        self.text_widget.insert("end", f"{faq_response}\n", "left") #faq response
        self.text_widget.tag_configure("left", justify="left")
        self.text_widget.config(state="disabled")

        scrollbar = tk.Scrollbar(self.window, command=self.text_widget.yview) #scrollbar to scroll for more text, and chat history
        self.text_widget['yscrollcommand'] = scrollbar.set
        scrollbar.place(x=481, y=6, height=308)

        frame = tk.Frame(self.window)
        frame.pack()
        self.window.configure(background="#5f0137")

    def clear_placeholder(self,event):
        if self.entry2.get() == "Enter text here...":
            self.entry2.delete(0,"end")
            self.entry2.config(fg='black')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__": #runs the code
    chatbot = Chatbot()
    chatbot.run()
