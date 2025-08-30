import time

from server import PromptServer
from ..config.prompt_conf import DEFAULT_EMPTY, get_prompt_conf


class PromptBatchMulti():
    @classmethod
    def INPUT_TYPES(s):
        ONE_IMAGE_STYLE = get_prompt_conf().get('ONE_IMAGE_STYLE', [])
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "prefix_select": (ONE_IMAGE_STYLE,),
                "prompt_1": ("STRING", {"default": '', "multiline": True},),
                "prompt_2": ("STRING", {"default": '', "multiline": True},),
            },
            "optional": {},
            "hidden": {
                "prompt": "PROMPT",
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    @classmethod
    def IS_CHANGED(s, inputcount):
        print("CRDNodes==========================================", inputcount)
        return float(time.time())

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "combine"
    CATEGORY = "CRDNodes/prompt"
    DESCRIPTION = """
    通过inputcount控制有多少个输入框
"""

    def combine(self, inputcount, prefix_select,unique_id=None, **kwargs):
        node_id = str(unique_id[0]) if isinstance(unique_id, list) else str(unique_id)

        main_prompt = prefix_select + kwargs["prompt_1"]
        for c in range(1, inputcount):
            new_prompt = kwargs[f"prompt_{c + 1}"]
            main_prompt = main_prompt + new_prompt

        try:
            PromptServer.instance.send_sync("crd_multi_input_update", {
                "id": node_id,
            })
        except Exception as e:
            pass

        return (main_prompt,)
