from pathlib import Path
import os

from src import (
    cv,
    settings,
    save_json
)


def open_file():
    with open(cv.file_path, 'r') as pf:
        cv.text_list = pf.readlines()


def separator_generator(total):
    sep_dic={
        '10': '    -    ',
        '100': '    -   ',
        '1000': '   -   ',
        '10000': '  -   '
    }
    for value in sep_dic:
        if total < int(value):
            return sep_dic[value]


def print_single_file_stat():
    cv.lines_non_blank = cv.lines_all - cv.lines_blank
    name = f'{Path(cv.file_path).name}:'
    dir = Path(cv.file_path).parent
    print(name)
    print('=' * len(name))
    print(dir)
    print('-' * len(str(dir)))
    print(cv.column_titels)
    _sep_ = separator_generator(cv.lines_all)
    print(f'{cv.lines_all}{_sep_}{cv.lines_non_blank}{_sep_}{cv.lines_blank}{_sep_}{cv.lines_comment}\n\n')


def print_total_stat():
    total = cv.result_total['sum_lines_all']
    comment = cv.result_total['sum_lines_comment']
    non_blank = total - comment
    blank = cv.result_total['sum_lines_blank']
    print()
    print('#' * cv.sep_length)
    print(' ' * int(cv.sep_length/2-3) + 'TOTAL')
    print(cv.column_titels)
    print("-" * cv.sep_length)
    _sep_ = separator_generator(total)
    print(f'{total}{_sep_}{non_blank}{_sep_}{blank}{_sep_}{comment}\n')
    print('#' * cv.sep_length + '\n')
    

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


def print_title():
    print('\n')
    title = f'Numbers of {os.path.basename(cv.dir_path)}:'
    print(title)
    print('~' * len(title)  + '\n')


def get_dir_path():
    from tkinter import filedialog as fd
    cv.dir_path = fd.askdirectory()


def generate_exclude_lists():
    cv.exclude_dir_paths = [value for value in settings['exc_dir_path'].values() if value]
    cv.exclude_file_names = [value for value in settings['exc_file_name'].values() if value]


def action_terminal_version():
      
    get_dir_path()

    if cv.dir_path:
        
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




if cv.post_result_to_terminal:
    action_terminal_version()