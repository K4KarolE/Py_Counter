from pathlib import Path
import logging
import platform
import subprocess
from tkinter import (
    filedialog as fd,
    messagebox,
    END
    )
import os

from .class_data import (
    cv,
    settings,
    save_json
    )


'''
#############
    PRINT
#############
'''
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(filename="output.log",
                    format='%(message)s',
                    filemode='w') # w/a


def separator_generator(total):
    sep_dic={
        '10': '    -    ',
        '100': '    -   ',
        '1000': '   -   ',
        '10000': '  -   ',
        '10000000': ' - '
    }
    for value in sep_dic:
        if total < int(value):
            return sep_dic[value]


def print_title():
    title = f'\nNumbers of {os.path.basename(cv.dir_path)}:'
    logger.info(title)
    logger.info('~' * len(title)  + '\n')


def print_single_file_stat():
    cv.lines_non_blank = cv.lines_all - cv.lines_blank
    name = f'{Path(cv.file_path).name}:'
    dir = Path(cv.file_path).parent
    _sep_ = separator_generator(cv.lines_all)
    results = f'{cv.lines_all}{_sep_}{cv.lines_non_blank}{_sep_}{cv.lines_blank}{_sep_}{cv.lines_comment}\n\n'
    logger.info(name)
    logger.info('=' * len(name))
    logger.info(dir)
    logger.info('-' * len(str(dir)))
    logger.info(cv.column_titels)
    logger.info(results)


def print_total_stat():
    total = cv.result_total['sum_lines_all']
    comment = cv.result_total['sum_lines_comment']
    non_blank = total - comment
    blank = cv.result_total['sum_lines_blank']
    _sep_ = separator_generator(total)
    results = f'{total}{_sep_}{non_blank}{_sep_}{blank}{_sep_}{comment}\n'
    max_length = max(cv.sep_length, len(results))

    logger.info('\n')
    logger.info('#' * max_length)
    logger.info(' ' * int(max_length/2-3) + 'TOTAL')
    logger.info(cv.column_titels)
    logger.info("-" * max_length)
    logger.info(results)
    logger.info('#' * max_length + '\n')


def open_output_log():
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['notepad', 'output.log'])
        else:
            subprocess.Popen(["xdg-open", 'output.log'])
    except:
            messagebox.showinfo('ERROR', 'Was not able to open the output log file.')


'''
###############
    COUNTER
###############
'''
def open_file():
    with open(cv.file_path, 'r') as pf:
        cv.text_list = pf.readlines()


def lines_counter():
    cv.lines_all = len(cv.text_list)
    comment_symbols = ["'''", '"""']
    comment_symbol_pair_counter = 0
    index_counter = 1

    for index, line in enumerate(cv.text_list):

        if line == '\n':
            cv.lines_blank +=1
            
        elif line[0] == '#':
            cv.lines_comment +=1
        
        else:
            comm_sym = [k for k in comment_symbols if k in line]
            
            if comm_sym:

                # """ random comment """ / """randomcomment"""
                if 2 in [line.count(comment_symbols[0]), line.count(comment_symbols[1])]:
                    cv.lines_comment += 1
                
                # """                       """multi line comment"
                # multi line comment        """
                # """
                else:    
                    comment_symbol_pair_counter +=1
                    if comment_symbol_pair_counter % 2 == 1:
                        while (index+index_counter < cv.lines_all and 
                               comm_sym[0] not in cv.text_list[index+index_counter]):
                            index_counter +=1
                        if index + index_counter != cv.lines_all:
                            cv.lines_comment += index_counter
                        cv.lines_comment += 1
                index_counter = 1
    
    cv.result_total['sum_lines_blank'] += cv.lines_blank
    cv.result_total['sum_lines_comment'] += cv.lines_comment
    cv.result_total['sum_lines_all'] += cv.lines_all


def no_excluded_items(list_to_exclude, in_name_or_path):
    for _ in list_to_exclude:
        if _ in in_name_or_path:
            return False
    return True     


def walk_dir_create_dic():                                    
    for dir_path_b, dir_names, file_names in os.walk(cv.dir_path):
        for file in file_names:
            if (Path(file).suffix in ['.py', '.pyw'] and
                no_excluded_items(cv.exclude_file_names, file) and
                no_excluded_items(cv.exclude_dir_paths, dir_path_b)):
                    cv.file_path = Path(dir_path_b, file)
                    cv.result_dic[cv.file_path] = {}


'''
##################
    HELP FUNCS
##################
'''
def dir_path_field_validation():
    return os.path.isdir(cv.dir_path_field.get("1.0", "end-1c"))


def generate_exclude_lists():
    cv.exclude_dir_paths = [value for value in settings['exc_dir_path'].values() if value]
    cv.exclude_file_names = [value for value in settings['exc_file_name'].values() if value]


def save_all_field_values():
    settings['last_used_dir_path'] = cv.dir_path_field.get("1.0", "end-1c")
    for exc_type in cv.exclude_dic:
        for number in cv.exclude_dic[exc_type]:
            field_value = cv.exclude_dic[exc_type][number].get("1.0", "end-1c").strip()[:19]
            settings[exc_type][number] = field_value
    save_json()


'''
#####################
    BUTTON ACTION
#####################
'''
def get_dir_path():
    cv.dir_path = fd.askdirectory()
    if cv.dir_path:
        cv.dir_path_field.delete('1.0', END)
        cv.dir_path_field.insert(END, cv.dir_path)

def save_and_go():
    if dir_path_field_validation():
        save_all_field_values()
        generate_exclude_lists()
        walk_dir_create_dic()
        print_title()

        for cv.file_path in cv.result_dic.keys():
            open_file()
            lines_counter()
            print_single_file_stat()
            cv.lines_blank = 0
            cv.lines_comment = 0
        print_total_stat()
        open_output_log()

    else:
        messagebox.showinfo(
            title='ERROR',
            message='The directory path is not valid!',
            icon='error'
            )