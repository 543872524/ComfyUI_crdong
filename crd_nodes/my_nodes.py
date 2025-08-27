import json
import traceback
import jsonpath


class INTConstant:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "value": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "get_value"
    CATEGORY = "CRDNodes/constants"

    def get_value(self, value):
        return (value,)


class SimpleIntMathHandle:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "first": ("INT", {"default": 10, "min": 2, "max": 100, "step": 1},),
                "second": ("INT", {"default": 2, "min": 2, "max": 100, "step": 1},),
                "operator": (["+", "-", "*", "/", "**", "//"], {"default": "+", },),
            },
        }

    CATEGORY = "CRDNodes/video"
    RETURN_TYPES = ("INT", "INT", "INT",)
    RETURN_NAMES = ("first", "second", "third")
    FUNCTION = "get_video_step"

    def get_video_step(self, first, second, operator):
        if operator is '+':
            third = first + second
        elif operator is '-':
            third = first - second
        elif operator is '*':
            third = first * second
        elif operator is '/':
            third = first / second
        elif operator is '**':
            third = first ** second
        elif operator is '//':
            third = first // second
        else:
            third = first - second
        return (first, second, third,)


class SimpleJsonArrayHandle:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "json_str": ("STRING", {"default": "", "multiline": True, },),
                "json_key": ("INT", {"default": 0, },),
            },
        }

    CATEGORY = "CRDNodes/string"
    RETURN_TYPES = ("LIST", "STRING", "STRING")
    RETURN_NAMES = ("first", "second", "third")
    OUTPUT_IS_LIST = (False, True, False)
    FUNCTION = "get_json_array"

    def get_json_array(self, json_str, json_key):
        try:
            json_data = json.loads(json_str)
            value = json_data[json_key]
            return (json_data, json_data, value,)
        except:
            traceback.print_exc()
            return ([], '', '',)


class SimpleJsonObjectHandle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_str": ("STRING", {"default": "", "multiline": True, },),
            },
            "optional": {
                "json_key": ("STRING", {"default": "", "multiline": False, },),
                "json_path": ("STRING", {"default": "", "multiline": False, },),
            }
        }

    CATEGORY = "CRDNodes/string"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("string", "key_value", "json_path_val", "json_path_array")
    OUTPUT_IS_LIST = (False, True, False, True)
    FUNCTION = "get_json_key"

    def get_json_key(self, json_str, json_key, json_path, ):
        try:
            value = ''
            json_path_val = ''
            data = json.loads(json_str)
            if json_key:
                value = data.get(json_key)
            if json_path:
                json_path_val = jsonpath.jsonpath(data, json_path)
            return (data, value, json_path_val, json_path_val,)
        except:
            traceback.print_exc()
            return ("", "", "",)

    @classmethod
    def IS_CHANGED(s, json_str):
        print(f"CRDNodes：json_str has changed，{json_str}")
        return True
