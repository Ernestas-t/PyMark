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

        self.watermark_text = None
        self.path_field = None
        self.watermark_size = 20

        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure(0, weight=1)

        self.my_image = Image.open('default-placeholder.png')
        self.image_ratio = self.my_image.size[0] / self.my_image.size[1]
        self.resized_image_tk = None

        self.draw_sidebar()

        self.canvas = customtkinter.CTkCanvas(self, background='#333333', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(row=0, column=1, columnspan=3, sticky='nsew')

        self.canvas.bind('<Configure>', self.show_full_image)

    def draw_sidebar(self):
        # make a sidebar frame to hold the widgets
        sidebar = customtkinter.CTkFrame(self)
        sidebar.columnconfigure(0, weight=1)

        # make a widget frame as a child to sidebar
        widget_frame = customtkinter.CTkFrame(sidebar, fg_color='transparent')
        widget_frame.columnconfigure(0, weight=1)

        # button frame widgets:
        path_field_label = customtkinter.CTkLabel(widget_frame, text='File Path: ', font=('verdana', 12))
        path_field_label.grid(row=0, column=0, sticky='w', padx=15)

        # file path entry field:
        self.path_field = customtkinter.CTkEntry(widget_frame)
        self.path_field.grid(row=1, column=0, padx=10, columnspan=2, sticky='nsew')

        browse_button = customtkinter.CTkButton(widget_frame, text='Browse Files',
                                                command=self.load_file_name)
        browse_button.grid(row=2, column=0, pady=(10, 0), padx=10, sticky='w')

        watermark_text_label = customtkinter.CTkLabel(widget_frame, text='Watermark Text:',
                                                      font=('verdana', 12), anchor='w')
        watermark_text_label.grid(row=3, column=0, sticky='w', padx=15)

        # watermark text entry field:
        self.watermark_text = customtkinter.CTkEntry(widget_frame)
        self.watermark_text.grid(row=4, column=0, padx=10, pady=(0, 10), columnspan=2, sticky='nsew')

        slider = customtkinter.CTkSlider(widget_frame, from_=0, to=100, command=self.set_watermark_size)
        slider.set(self.watermark_size)
        slider.grid(row=5, column=0, columnspan=2, sticky='nsew', pady=(0, 10))

        add_button = customtkinter.CTkButton(widget_frame, text='Add Watermark', command=self.add_watermark)
        add_button.grid(row=6, column=0, padx=10, sticky='w')

        save_button = customtkinter.CTkButton(widget_frame, text='Save', command=self.save_file)
        save_button.grid(row=6, column=1, padx=10, sticky='e')

        logo = customtkinter.CTkLabel(sidebar, text='PyMark', font=('Arial', 40), text_color='#2271AF')
        logo.pack(side='top', pady=30)

        # place the sidebar and widget frames, fill='x' makes the widget_frame fill the container horizontally
        sidebar.grid(row=0, column=0, sticky='nsew')
        widget_frame.pack(side='bottom', fill='x', pady=10)

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

    def set_watermark_size(self, size):
        if size > 1 and self.watermark_text.get():
            self.watermark_size = size
            self.add_watermark()

    def load_file_name(self):
        filename = filedialog.askopenfilename()
        if filename != '':
            self.path_field.delete(0, END)  # Clear previous text
            self.path_field.insert(END, filename)

            self.open_files()

    def open_files(self):
        if self.path_field.get():
            filename = self.path_field.get()
            self.my_image = Image.open(filename)
            self.image_ratio = self.my_image.size[0] / self.my_image.size[1]

            # Trigger the <Configure> event with the canvas dimensions
            self.canvas.event_generate('<Configure>', width=self.canvas.winfo_width(),
                                       height=self.canvas.winfo_height())

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
        watermark = self.watermark_text.get()
        if watermark != '':
            watermarked_image = self.my_image.copy()

            draw = ImageDraw.Draw(watermarked_image)
            font = ImageFont.truetype('verdana', self.watermark_size)

            # Get the text size
            textbbox = draw.textbbox((0, 0), f'© {watermark}', font=font)
            # Extract width and height from the textbbox tuple
            text_width, text_height = textbbox[2] - textbbox[0], textbbox[3] - textbbox[1]

            text_position = (watermarked_image.width - text_width - 35, watermarked_image.height - text_height - 35)
            draw.text(text_position, f'© {watermark}', fill=(255, 255, 255, 200), font=font)

            self.my_image = watermarked_image
            self.canvas.event_generate('<Configure>', width=self.canvas.winfo_width(), height=self.canvas.winfo_height())


if __name__ == "__main__":
    app = Watermarker()
    app.mainloop()
