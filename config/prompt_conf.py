import json
import os
import traceback

DEFAULT_EMPTY = '————'

# 获取当前文件的相对路径，然后再获取其所在目录
config_directory = os.path.dirname(os.path.abspath(__file__))
print("CRDNodes：", config_directory)


def get_example_list():
    try:
        with open(os.path.join(config_directory, 'example_prompt_list.json'), 'r', encoding='utf-8') as f:
            read = f.read()
            data = json.loads(read)
            temp_list1 = []
            for i in data:
                temp_list1.append(i)

            return temp_list1
    except:
        traceback.print_exc()


def get_image_style():
    try:
        with open(os.path.join(config_directory, 'image_style.json'), 'r', encoding='utf-8') as f:
            f_read = f.read()
            data = json.loads(f_read)
            temp_list2 = []
            for i in data:
                temp_list2.append(i)

            return temp_list2
    except:
        traceback.print_exc()


def get_one_image_style():
    try:
        with open(os.path.join(config_directory, 'one_image_style.json'), 'r', encoding='utf-8') as f:
            # print("CRDNodes：读取one_image_style.json")
            f_read = f.read()
            data = json.loads(f_read)
            temp_list3 = []
            for i in data:
                temp_list3.append(i)

            return temp_list3
    except:
        traceback.print_exc()


def get_style_conf():
    with open(os.path.join(config_directory, 'style_conf.json'), 'r', encoding='utf-8') as f:
        # print("CRDNodes：读取example_prompt_list.json")
        read = f.read()
        data = json.loads(read)
    return data
