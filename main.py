from dataclasses import dataclass
from pathlib import Path
import os



@dataclass
class Data:

    '''
    use_basic_cli_version:
    At startup automatically
    - opens file dialog for directory path
    - display stats in terminal
    No UI, no search cretaria options
    '''
    use_basic_cli_version: bool = True

    result_dic = dict()
    result_total = dict()
    text_list: str = None

    lines_blank: int = 0
    lines_non_blank: int = 0
    lines_comment: int = 0

    file_path: str = None

    column_titels = 'All / Non-blank / Blank / Comment'
    sep_length = len(column_titels)



def open_file():
    with open(cv.file_path, 'r') as pf:
        cv.text_list = pf.readlines()


def separator_generator(total):
    if total < 1000:
        _sep_ = '   -   '
    else:
        _sep_ = '  -  '
    return _sep_


def print_single_file_stat():
    cv.lines_non_blank = cv.lines_all - cv.lines_blank
    name = f'{Path(cv.file_path).stem}:'
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
                

def walk_dir_create_dic(dir_path):                                    
    for dir_path_b, dir_names, file_names in os.walk(dir_path):
        for file in file_names:
            if (Path(file).suffix in ['.py', '.pyw'] and
                'test' not in file and
                'virtual' not in dir_path_b):
                cv.file_path = Path(dir_path_b, file)
                cv.result_dic[cv.file_path] = {}
                cv.result_total = {
                    'sum_lines_blank': 0,
                    'sum_lines_comment': 0,
                    'sum_lines_all': 0
                    }

cv = Data()

if cv.use_basic_cli_version:
    from tkinter import filedialog as fd
    dir_path = fd.askdirectory()

    walk_dir_create_dic(dir_path)

    for cv.file_path in cv.result_dic.keys():
        open_file()
        lines_counter()
        print_single_file_stat()
        cv.lines_blank = 0
        cv.lines_comment = 0
    
    print_total_stat()