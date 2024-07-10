from pathlib import Path

from tkinter import (
    Canvas,
    filedialog,
    Text,
    Tk,
    END
)

from class_data import settings


FONT_STYLE, FONT_SIZE = 'Arial', 11
HEIGHT, WIDTH = 1, 17


class ExcludeField(Text):
    def __init__(self, field_text):
        super().__init__()
        self.master = window
        self.configure(height=HEIGHT, width=WIDTH, font=(FONT_STYLE, FONT_SIZE))
        if field_text:
            self.insert(END, field_text)


# WINDOW
bg_color = '#F3F3F3'
window = Tk()
window.title('Code Counter')
window_width = 447
window_length = 290
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{window_width}x{window_length}+%d+%d' % (screen_width/2-275, screen_height/2-125))    #   position to the middle of the screen
window.resizable(0,0)   # locks the main window
window.configure(background=bg_color)
# ICON
working_directory = Path().resolve()
path_icon = Path(working_directory, "docs/icon.ico") 
window.iconbitmap(path_icon)
# RECTANGLE
rect_base = 7
canvas_frame_color = '#D6D6D6'
canvas = Canvas(window, width=window_width, height=window_length, background = bg_color)
canvas.create_rectangle(rect_base-1, rect_base+2, window_width-rect_base, window_length-rect_base, outline=canvas_frame_color, fill=bg_color)
canvas.pack()



''' Generate exclude field widgets '''
exclude_dic = {
    "exc_dir_path": {},
    "exc_file_name": {}
    }
for exc_type in exclude_dic:
    for number in settings[exc_type]:
        field_text = settings[exc_type][number]
        exclude_dic[exc_type][number] = ExcludeField(field_text)


''' Display exclude field widgets'''
BASE_X = 40
BASE_Y = 70
DIFF_X = 200
DIFF_Y = 35
counter_x = 0
counter_y = 0
for exc_type in exclude_dic:
    for number in exclude_dic[exc_type]:
        pos_x = BASE_X + DIFF_X * counter_x
        pos_y = BASE_Y + DIFF_Y * counter_y
        exclude_dic[exc_type][number].place(x=pos_x, y=pos_y)
        counter_y += 1
    counter_y = 0
    counter_x += 1




window.mainloop()