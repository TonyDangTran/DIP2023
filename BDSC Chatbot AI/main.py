from tkinter import*
import tkinter as tk
from tkinter import simpledialog
import openai

def query(prompt):
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=1,
        max_tokens=250, 
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response

def send(event=None):
    text = entry2.get()
    prompt.append({'role': 'user', 'content': text})
    response = query(prompt)
    message_content = response['choices'][0]['message']['content']
    prompt.append({'role': 'assistant', 'content': message_content})
    
    text_widget.config(state="normal")
    text_widget.insert("end",f"{display_name}: " + "\n" + text +"\n", "right")
    text_widget.insert("end", "Chatbot: " + "\n" + message_content + "\n", "left")
    text_widget.tag_configure("right",justify="right")
    text_widget.tag_configure("left", justify="left")
    text_widget.config(state="disabled")
    entry2.delete(0,"end")
 
def get_name():
    name = simpledialog.askstring("Input", "Enter the name you wish to be referred as:")
    return name.capitalize()

display_name = get_name()
prompt=[{'role': 'system', 'content': 'how may I help you?'}]

window = Tk()
window.geometry("500x750")
window.title("BDSC Chatbot AI")
window.resizable(False, False)

canvas = tk.Canvas(window, width=50, height=50,bg="#89c9ec")
canvas.pack()

entry1 = tk.Text(window,wrap="word",state="disabled",bg="#89c9ec",padx=5,pady=5)
entry1.place(x=6,y=5,width=493,height=700)


entry2 = tk.Entry(window)
entry2.place(x=5,y=720,width=420,height=20)
entry2.bind("<Return>", send)

#def write_to_csv(chat):
    #with open("emprecords.csv","a", newline = "") as csvfile:
        #writer = csv.writer(csvfile)
        #writer.writerow([[chat.entry2]])

#canvas.create_window(100,100,window=entry)


button1 = tk.Button(window, text='Send Msg', command=send)
button1.place(anchor="se", relx=0.99, rely=0.99)

text_widget = tk.Text(window, height=36, width=59,font="calibri",state="disabled")
text_widget.place(x=7, y=6)
 

scrollbar = Scrollbar(window, command=text_widget.yview)
text_widget['yscrollcommand'] = scrollbar.set
scrollbar.place(x=481, y=6, height = 688)





#canvas.create_window(5,25,window=button1)

frame = Frame(window)
frame.pack()
window.configure(background="#5f0137")
window.mainloop()

