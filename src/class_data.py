from dataclasses import dataclass
from pathlib import Path
from json import load, dump


def open_json():
    with open(PATH_JSON_SETTINGS) as f:
        json_dic = load(f)
    return json_dic

def save_json():
    with open(PATH_JSON_SETTINGS, 'w') as f:
        dump(settings, f, indent=2)
    return

WORKING_DIRECTORY = Path().resolve()
PATH_JSON_SETTINGS = Path(WORKING_DIRECTORY, 'settings.json')
settings = open_json()


@dataclass
class Data:

    result_dic = {}
    result_total = {
                    'sum_lines_blank': 0,
                    'sum_lines_comment': 0,
                    'sum_lines_all': 0
                    }
    
    text_list: str = None

    lines_blank: int = 0
    lines_non_blank: int = 0
    lines_comment: int = 0

    file_path: str = None
    dir_path: str = settings['last_used_dir_path']

    exclude_file_names = []
    exclude_dir_paths = []
    exclude_dic = {}

    dir_path_field: object = None

    column_titels = 'All / Non-blank / Blank / Comment'
    sep_length = len(column_titels)


cv = Data()