from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk, ImageFont, ImageDraw
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

        self.widget_frame = customtkinter.CTkFrame(self)
        self.widget_frame.columnconfigure(0, weight=1)  # Make button_frame resizable

        # button frame widgets:
        self.path_field_label = customtkinter.CTkLabel(self.widget_frame, text='File Path: ', font=('verdana', 12))
        self.path_field_label.grid(row=0, column=0, sticky='w', padx=15)

        self.path_field = customtkinter.CTkEntry(self.widget_frame)
        self.path_field.grid(row=1, column=0, padx=10, columnspan=2, sticky='nsew')

        self.browse_button = customtkinter.CTkButton(self.widget_frame, text='Browse Files',
                                                     command=self.load_file_name)
        self.browse_button.grid(row=2, column=0, pady=(10, 0), padx=10, sticky='w')

        self.watermark_text_label = customtkinter.CTkLabel(self.widget_frame, text='Watermark Text:',
                                                           font=('verdana', 12), anchor='w')
        self.watermark_text_label.grid(row=3, column=0, sticky='w', padx=15)

        self.watermark_text = customtkinter.CTkEntry(self.widget_frame)
        self.watermark_text.grid(row=4, column=0, padx=10, pady=(0, 10), columnspan=2, sticky='nsew')

        self.add_button = customtkinter.CTkButton(self.widget_frame, text='Add Watermark', command=self.add_watermark)
        self.add_button.grid(row=5, column=0, padx=10, sticky='w')

        self.save_button = customtkinter.CTkButton(self.widget_frame, text='Save', command=self.save_file)
        self.save_button.grid(row=5, column=1, padx=10, sticky='e')

        self.widget_frame.grid(row=0, column=0, sticky='nsew')

        self.canvas = customtkinter.CTkCanvas(self, background='#333333', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(row=0, column=1, columnspan=3, sticky='nsew')

        self.canvas.bind('<Configure>', self.show_full_image)

    def show_full_image(self, event):
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

    def load_file_name(self):
        filename = filedialog.askopenfilename()
        self.path_field.delete(0, END)  # Clear previous text
        self.path_field.insert(END, filename)

        self.open_files()

    def open_files(self):
        filename = self.path_field.get()
        self.my_image = Image.open(filename)
        self.image_ratio = self.my_image.size[0] / self.my_image.size[1]

        # Trigger the <Configure> event with the canvas dimensions
        self.canvas.event_generate('<Configure>', width=self.canvas.winfo_width(), height=self.canvas.winfo_height())

    def save_file(self):
        # Use asksaveasfile to get the file path and name
        file_path = asksaveasfile(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        # Check if the user clicked on Cancel in the dialog
        if file_path is None:
            return

        # Save the image to the specified file path
        self.my_image.save(file_path.name)

    def add_watermark(self):
        self.open_files()
        watermark_text = self.watermark_text.get()
        watermarked_image = self.my_image.copy()

        draw = ImageDraw.Draw(watermarked_image)
        font = ImageFont.truetype('verdana', 20)

        # Get the text size
        textbbox = draw.textbbox((0, 0), f'© {watermark_text}', font=font)
        # Extract width and height from the textbbox tuple
        text_width, text_height = textbbox[2] - textbbox[0], textbbox[3] - textbbox[1]

        text_position = (watermarked_image.width - text_width - 5, watermarked_image.height - text_height - 10)
        draw.text(text_position, f'© {watermark_text}', fill=(255, 255, 255, 200), font=font)

        self.my_image = watermarked_image
        self.canvas.event_generate('<Configure>', width=self.canvas.winfo_width(), height=self.canvas.winfo_height())


if __name__ == "__main__":
    app = Watermarker()
    app.mainloop()
