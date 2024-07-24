from pathlib import Path

from tkinter import (
    Button,
    Canvas,
    filedialog,
    Label,
    Text,
    Tk,
    END
)

from class_data import settings, cv



FONT_STYLE, FONT_SIZE = 'Arial', 11
HEIGHT, WIDTH = 1, 19
TEXT_COLOR = '#4B4B4B'
BG_COLOR = '#F3F3F3'


class InputField(Text):
    def __init__(self, field_text = None):
        super().__init__()
        self.master = window
        self.configure(
            height=HEIGHT,
            width=WIDTH,
            font=(FONT_STYLE, FONT_SIZE), 
            fg=TEXT_COLOR
            )
        if field_text:
            self.insert(END, field_text)


class MyLabel(Label):
    def __init__(self, text, font_size):
        super().__init__()
        self.configure(
            text=text,
            font=(FONT_STYLE, font_size),
            fg=TEXT_COLOR
            )


class MyButton(Button):
    def __init__(self, text, func):
        super().__init__()
        self.configure(
                    height=1,
                    width=4,
                    text = text,
                    command = func,
                    foreground=TEXT_COLOR,
                    background=BG_COLOR,
                    activeforeground='white',
                    activebackground='grey'
                    )    


# WINDOW
window = Tk()
window.title('Code Counter')
WINDOW_WIDTH = 447
WINDOW_HEIGHT = 435
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+%d+%d' % (screen_width/2-275, screen_height/2-125))    #   position to the middle of the screen
window.resizable(0,0)   # locks the main window
window.configure(background=BG_COLOR)
# ICON
working_directory = Path().resolve()
path_icon = Path(working_directory, "docs/icon.ico") 
window.iconbitmap(path_icon)
# RECTANGLE
RECT_BASE = 7
CANVAS_FRAME_COLOR = '#D6D6D6'
canvas = Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, background = BG_COLOR)
canvas.create_rectangle(RECT_BASE-1, RECT_BASE+2, WINDOW_WIDTH-RECT_BASE, WINDOW_HEIGHT-RECT_BASE, outline=CANVAS_FRAME_COLOR, fill=BG_COLOR)
canvas.pack()


BASE_X = 20
BASE_Y = 30

dir_path_field = InputField(cv.last_used_dir_path)
dir_path_field.configure(width=int(WIDTH*2.4))
dir_path_field.place(x=BASE_X, y=BASE_Y)


'''
#######################
    EXCLUDE SECTION
#######################
'''

''' Generate exclude field widgets '''
exclude_dic = {
    "exc_dir_path": {},
    "exc_file_name": {}
    }
for exc_type in exclude_dic:
    for number in settings[exc_type]:
        field_text = settings[exc_type][number]
        exclude_dic[exc_type][number] = InputField(field_text)


''' Display exclude field widgets'''
EXC_BASE_X = BASE_X + 20
EXC_BASE_Y = BASE_Y + 150
EXC_DIFF_X = 200
EXC_DIFF_Y = 35
counter_x = 0
counter_y = 0
for exc_type in exclude_dic:
    for number in exclude_dic[exc_type]:
        pos_x = EXC_BASE_X + EXC_DIFF_X * counter_x
        pos_y = EXC_BASE_Y + EXC_DIFF_Y * counter_y
        exclude_dic[exc_type][number].place(x=pos_x, y=pos_y)
        counter_y += 1
    counter_y = 0
    counter_x += 1


''' TEXTS / RECT-FRAME '''
TITLE_POS_X_DIFF = 2
TITLE_POS_Y_DIFF = 25
exclude_title = MyLabel('Exclude from', FONT_SIZE)
exclude_title.place(x=BASE_X-TITLE_POS_X_DIFF, y=EXC_BASE_Y-65)

exclude_dir_path_title = MyLabel('Directory path', FONT_SIZE-1)
exclude_dir_path_title.place(x=EXC_BASE_X-TITLE_POS_X_DIFF, y=EXC_BASE_Y-TITLE_POS_Y_DIFF)

exclude_file_name_title = MyLabel('File name', FONT_SIZE-1)
exclude_file_name_title.place(x=pos_x-TITLE_POS_X_DIFF, y=EXC_BASE_Y-TITLE_POS_Y_DIFF)

canvas.create_rectangle(BASE_X, EXC_BASE_Y-40, WINDOW_WIDTH-BASE_X, pos_y + 50, outline=CANVAS_FRAME_COLOR, fill=BG_COLOR)


'''
#################
    BUTTONS
#################
'''
button_dir = MyButton('/', None)
button_dir.place(x=WINDOW_WIDTH-60, y=BASE_Y-4)


button_go = MyButton('Go', None)
button_go.place(x=WINDOW_WIDTH-60, y=WINDOW_HEIGHT-40)

window.mainloop()