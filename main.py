from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter


class Watermarker(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x907')
        self.title('PyMark')

        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure(0, weight=1)

        self.my_image = Image.open('default-placeholder.png')
        self.image_ratio = self.my_image.size[0] / self.my_image.size[1]
        self.resized_image_tk = None

        self.button_frame = customtkinter.CTkFrame(self)

        self.browse_button = customtkinter.CTkButton(self.button_frame, text='Browse Files', command=self.open_files)
        self.browse_button.grid(row=0, column=0, pady=(20, 0))  # Add padding to the top
        self.path_field = customtkinter.CTkEntry(self.button_frame, width=200)
        self.path_field.grid(row=1, column=0, pady=(5, 5))  # Add less padding to the top and bottom
        self.watermark_text = customtkinter.CTkEntry(self.button_frame, width=200)
        self.watermark_text.grid(row=2, column=0, pady=(0, 10))  # Add padding to the bottom

        # Center horizontally
        self.button_frame.columnconfigure(0, weight=1)

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
        self.path_field.delete(0, END)  # Clear previous text
        self.path_field.insert(END, filename)

        self.my_image = Image.open(filename)
        self.image_ratio = self.my_image.size[0] / self.my_image.size[1]

        # Trigger the <Configure> event with the canvas dimensions
        self.canvas.event_generate('<Configure>', width=self.canvas.winfo_width(), height=self.canvas.winfo_height())


if __name__ == "__main__":
    app = Watermarker()
    app.mainloop()
