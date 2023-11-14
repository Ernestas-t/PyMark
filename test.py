from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter


class Watermarker(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('900x680')
        self.title('PyMark')

        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure(0, weight=1)

        self.my_image = Image.open('default-placeholder.png')
        self.image_ratio = self.my_image.size[0] / self.my_image.size[1]
        self.resized_image_tk = None

        self.button_frame = customtkinter.CTkFrame(self)

        self.browse_button = customtkinter.CTkButton(self.button_frame, text='Browse Files', command=self.open_files)
        self.browse_button.pack()
        self.path_field = customtkinter.CTkEntry(self.button_frame, width=200)
        self.path_field.pack()
        self.button_frame.grid(row=0, column=0, sticky='nsew')

        self.canvas = customtkinter.CTkCanvas(self, background='black', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(row=0, column=1, columnspan=3, sticky='nsew')

        self.canvas.bind('<Configure>', self.show_full_image)

    def show_full_image(self, event):
        print(event)
        canvas_ratio = event.width / event.height

        if canvas_ratio > self.image_ratio:
            height = int(event.height)
            width = int(height * self.image_ratio)

        else:
            width = int(event.width)
            height = int(width / self.image_ratio)

        resized_image = self.my_image.resize((width, height))
        self.resized_image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(int(event.width / 2), int(event.height / 2), anchor='center',
                                 image=self.resized_image_tk)

    def open_files(self):
        filename = filedialog.askopenfilename()
        self.path_field.insert(END, filename)
        self.my_image = Image.open(filename)
        self.image_ratio = self.my_image.size[0] / self.my_image.size[1]
        self.canvas.configure()
