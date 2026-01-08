import requests # request module is used to fetch api request data
from tkinter import*
from urllib.request import urlopen
import io
import webbrowser
from PIL import Image, ImageTk
class NewsApp:
    def __init__(self):
# fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=e94cb1d17dc24932a96e44053f0ec6ff').json()

        #inital GUI load
        self.load_gui()
        self.load_news_items(2)
    def load_gui(self):
        self.root = Tk() # tkinter ka object
        self.root.geometry('400x600')
        self.root.resizable(0,0)
        self.root.configure(background="black")
        self.root.title("News Application")
    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_items(self,index):
        self.clear()
        img_url = self.data['articles'][index]['urlToImage']
        raw_data = urlopen(img_url).read()
        im = Image.open(io.BytesIO(raw_data)).resize((350,250))
        photo = ImageTk.PhotoImage(im)
        label = Label(self.root,image = photo)
        label.pack(pady=20)

        #Heading

        heading = Label(self.root,text=self.data['articles'][index]['title'],bg="black",fg="white",wraplength=350,justify='center')
        heading.pack(pady=(10,20))
        heading.config(font=("Times New Roman",20))

        #details
        details = Label(self.root, text=self.data['articles'][index]['description'], bg="black", fg="white", wraplength=350,
                        justify='center')
        details.pack(pady=(10, 20))
        details.config(font=("Times New Roman", 15))
        frame = Frame(self.root,bg="black")
        frame.pack(expand=True,fill="both")

        #previous
        prev = Button(frame,text="Previous",width=16,height=3,command=lambda: self.load_news_items(index-1))
        prev.pack(side='left')

        #read more
        read = Button(frame, text="Read More", width=16, height=3, command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.pack(side='left')

        #next
        next = Button(frame, text="Next", width=16, height=3,command=lambda: self.load_news_items(index+1))
        next.pack(side='left')
        next.pack(side='left')

        self.root.mainloop()


    def open_link(self,url):
        webbrowser.open(url)



obj = NewsApp()