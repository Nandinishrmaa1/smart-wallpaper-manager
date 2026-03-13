import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox

import requests 
import os
from datetime import datetime
import ctypes

FOLDER_NAME = "Wallpapers"
HISTORY_FILE = "history.txt"

os.makedirs(FOLDER_NAME, exist_ok=True)
#print("Folders ready!")

KEY = api_key

def search_wallpaper(topic):
    URL = f'https://api.unsplash.com/search/photos/?query={topic}&client_id={KEY}'
    res = requests.get(URL)

    if res.status_code == 200:
        data = res.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['urls']['full'],data['results'][0]['user']['name']
        else:
            return None,None
    else:
        print(f'Error : {res.status_code}')
        return None,None

def download_wallpaper(img_url, topic):
    res = requests.get(img_url) 
    if res.status_code == 200:
        topic = topic.replace(' ','_')
        file_path = os.path.join(FOLDER_NAME, f'{topic}.jpg')

        
        with open(file_path,'wb') as f:
            f.write(res.content)
        print('Wallpaper saved!')
        print(f'File saved at: {file_path}')
        return file_path
    else:
        print('Failed to download image')

def save_history(topic, photographer, file_path):
    history = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Topic: {topic} | Photographer: {photographer} | Saved at: {file_path}'
    with open(HISTORY_FILE,'a') as f:
        f.write(history +'\n')



def set_wallpaper(file_path):
    abs_path = os.path.abspath(file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)

    print('Desktop wallpaper changed!')


#GUI Fn
def download_action():
    
    topic = text_entry.get()
    if topic != '':
        status_label.config(text='Downloading... please wait')
        img_url, photographer = search_wallpaper(topic)
        if img_url:
            
            print(f'Image URL: {img_url}')
            print(f'Photographer: {photographer}')
            file_path = download_wallpaper(img_url,topic)
            save_history(topic,photographer,file_path)
            set_wallpaper(file_path)
            
            status_label.config(text='Wallpaper saved!')
           
        else:
            status_label.config(text='Invalid topic')
    else:
        status_label.config(text='Please enter a topic!')
    text_entry.delete(0,tk.END)
def view_history():
    if not os.path.exists(HISTORY_FILE):
        messagebox.showinfo('Download History', 'No history yet!')
        return
    with open(HISTORY_FILE,'r') as f:
        content = f.read()
    messagebox.showinfo('Download History', content)

#GUI 
root = tk.Tk()

root.title("Smart Wallpaper Manager")

root.geometry('500x400')
msg = tk.Label(root, text="Smart Wallpaper Manager")
msg.pack(pady=10)

topic_label = ttk.Label(root, text='Enter topic')
topic_label.pack(pady=10)
topic_label.focus()

text_entry = ttk.Entry(root,width=30)
text_entry.pack()

btn_dw = tk.Button(root, text='Download Wallpaper', command=download_action)
btn_vh = tk.Button(root, text='View History', command=view_history)
btn_dw.pack(pady=10)
btn_vh.pack(pady=10)
status_label = tk.Label(root,text="")
status_label.pack()

root.resizable(False,False)
root.mainloop()
