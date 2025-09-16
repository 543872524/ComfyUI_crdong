import hashlib
from ..config.prompt_conf import DEFAULT_EMPTY, get_example_list, get_image_style, get_one_image_style


class PromptSelectorStr:

    @classmethod
    def INPUT_TYPES(s):
        ONE_IMAGE_STYLE = get_one_image_style()
        return {"required":
            {
                "prefix_select": (ONE_IMAGE_STYLE, {"default": '————', }),
                "style_input": ("STRING", {"default": '', "multiline": False},),
                "prefix_input": ("STRING", {"default": '', "multiline": True},),
                "body": ("STRING", {"default": '', "multiline": True},),
                "suffix": ("STRING", {"default": '', "multiline": True},),
            },
        }

    CATEGORY = "CRDNodes/prompt"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "get_prompt_str"

    def get_prompt_str(self, prefix_select, style_input, prefix_input, body, suffix):
        if prefix_select is DEFAULT_EMPTY or prefix_select == DEFAULT_EMPTY:
            prefix_select = ""

        if prefix_select is '自定义':
            prompt_str = style_input + prefix_input + body + suffix
        elif len(style_input) == 0 or style_input == '':
            prompt_str = prefix_select + prefix_input + body + suffix
        else:
            prompt_str = style_input + prefix_input + body + suffix
        return (prompt_str,)


class PromptSelectorStrV2:

    @classmethod
    def INPUT_TYPES(s):
        ONE_IMAGE_STYLE = get_one_image_style()
        return {"required":
            {
                "prefix_select": (ONE_IMAGE_STYLE, {"default": '————', }),
                "style_input": ("STRING", {"default": '', "multiline": False},),
                "prefix_input": ("STRING", {"default": '', "multiline": True},),
            },
        }

    CATEGORY = "CRDNodes/prompt"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "get_prompt_str"

    def get_prompt_str(self, prefix_select, style_input, prefix_input):
        if prefix_select is DEFAULT_EMPTY or prefix_select == DEFAULT_EMPTY:
            prefix_select = ""

        if prefix_select is '自定义':
            prompt_str = style_input + prefix_input
        elif len(style_input) == 0 or style_input == '':
            prompt_str = prefix_select + prefix_input
        else:
            prompt_str = style_input + prefix_input
        return (prompt_str,)


class PromptSelectorList():

    @classmethod
    def INPUT_TYPES(s):
        IMAGE_STYLE = get_image_style()
        return {
            "required": {
                "inputcount": ("INT", {"default": 5, "min": 2, "max": 1000, "step": 1}),
                "str_1": (IMAGE_STYLE, {"default": '————', }),
                "str_2": (IMAGE_STYLE, {"default": '————', }),
                "str_3": (IMAGE_STYLE, {"default": '————', }),
                "str_4": (IMAGE_STYLE, {"default": '————', }),
                "str_5": (IMAGE_STYLE, {"default": '————', }),
            },
            "optional": {
                "str_6": ("STRING", {"default": '', "forceInput": True}),
            }
        }

    CATEGORY = "CRDNodes/prompt"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "get_prompt_str"

    def get_prompt_str(self, inputcount, **kwargs):
        main_prompt = kwargs.get('str_1', '')
        for c in range(1, inputcount):
            new_prompt = kwargs[f"str_{c + 1}"]
            if new_prompt is '————':
                new_prompt = ''
            main_prompt = main_prompt + new_prompt
        return (main_prompt,)


# PromptList
class PromptList:

    @classmethod
    def INPUT_TYPES(cls):
        ONE_IMAGE_STYLE = get_image_style()
        return {"required": {
            "prefix_select": (ONE_IMAGE_STYLE, {"default": '————', }),
            "prompt_1": ("STRING", {"multiline": True, "default": ""}),
            "prompt_2": ("STRING", {"multiline": True, "default": ""}),
            "prompt_3": ("STRING", {"multiline": True, "default": ""}),
            "prompt_4": ("STRING", {"multiline": True, "default": ""}),
            "prompt_5": ("STRING", {"multiline": True, "default": ""}),
        },
            "optional": {
                "optional_prompt_list": ("LIST",)
            }
        }

    RETURN_TYPES = ("LIST", "STRING")
    RETURN_NAMES = ("prompt_list", "prompt_strings")
    OUTPUT_IS_LIST = (False, True)
    FUNCTION = "run"
    CATEGORY = "CRDNodes/prompt"

    def run(self, prefix_select, **kwargs):
        if prefix_select is DEFAULT_EMPTY or prefix_select == DEFAULT_EMPTY:
            prefix_select = ""
        prompts = []

        if "optional_prompt_list" in kwargs:
            for l in kwargs["optional_prompt_list"]:
                prompts.append(l)

        # Iterate over the received inputs in sorted order.
        for k in sorted(kwargs.keys()):
            v = kwargs[k]

            # Only process string input ports.
            if isinstance(v, str) and v != '':
                prompts.append(prefix_select + v)

        return (prompts, prompts)


class PromptJoinOrList():

    @classmethod
    def INPUT_TYPES(s):
        IMAGE_STYLE = get_image_style()
        return {
            "required": {
                "image_style": (IMAGE_STYLE, {"default": '————', }),
                "str_1": ("STRING", {"default": '', "multiline": True, }),
                "str_2": ("STRING", {"default": '', "multiline": True, }),
                "str_3": ("STRING", {"default": '', "multiline": True, }),
                "str_4": ("STRING", {"default": '', "multiline": True, }),
                "str_5": ("STRING", {"default": '', "multiline": True, }),
            }
        }

    CATEGORY = "CRDNodes/prompt"
    RETURN_TYPES = ("LIST", "STRING",)
    RETURN_NAMES = ("list", "strings",)
    OUTPUT_IS_LIST = (False, True)
    FUNCTION = "get_prompt_str"

    def get_prompt_str(self, image_style, **kwargs):
        if image_style is DEFAULT_EMPTY or image_style == DEFAULT_EMPTY:
            image_style = ""
        prompt_list = []
        prompt_str = image_style + ''
        for c in range(5):
            new_prompt = kwargs[f"str_{c + 1}"]
            if new_prompt is '————':
                new_prompt = ''
            prompt_list.append(image_style + new_prompt)
            prompt_str = prompt_str + new_prompt
        return (prompt_list, prompt_str,)


class PromptExampleNode():
    @classmethod
    def INPUT_TYPES(s):
        EXAMPLE_PROMPT = get_example_list()
        return {
            "required": {
                "prompt_select": (EXAMPLE_PROMPT, {"default": '————', "multiline": True}),
            },
        }

    CATEGORY = "CRDNodes/prompt"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "get_prompt_str"

    def get_prompt_str(self, prompt_select):
        if prompt_select == '————':
            return ("",)
        return (prompt_select,)




class CRDJoinStringMulti:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "string_1": ("STRING", {"default": '', "forceInput": True}),
                "delimiter": ("STRING", {"default": ' ', "multiline": False}),
                "return_list": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "string_2": ("STRING", {"default": '', "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "combine"
    CATEGORY = "CRDNodes/prompt"
    DESCRIPTION = """Creates single string, or a list of strings, from  
            multiple input strings.  
            You can set how many inputs the node has,  
            with the **inputcount** and clicking update.
            """

    def combine(self, inputcount, delimiter, **kwargs):
        string = kwargs["string_1"]
        return_list = kwargs["return_list"]
        strings = [string]  # Initialize a list with the first string
        for c in range(1, inputcount):
            new_string = kwargs.get(f"string_{c + 1}", "")
            if not new_string:
                continue
            if return_list:
                strings.append(new_string)  # Add new string to the list
            else:
                string = string + delimiter + new_string
        if return_list:
            return (strings,)  # Return the list of strings
        else:
            return (string,)  # Return the combined string
