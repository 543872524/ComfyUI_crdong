import time

from comfy_api.latest import ComfyExtension, io

from server import PromptServer
from ..config.prompt_conf import DEFAULT_EMPTY, get_prompt_conf
from ..crd_nodes.my_nodes import CrdContainsAnyDict


class TestExtendComfyNode(io.ComfyNode):
    pass

class PromptBatchMulti():
    @classmethod
    def INPUT_TYPES(s):
        ONE_IMAGE_STYLE = get_prompt_conf().get('ONE_IMAGE_STYLE', [])
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 10, "step": 1}),
                "prefix_select": (ONE_IMAGE_STYLE,),
                "prompt_1": ("STRING", {"default": '', "multiline": True},),
                "prompt_2": ("STRING", {"default": '', "multiline": True},),
            },
            "optional": CrdContainsAnyDict(),
            "hidden": {
                "unique_id": "UNIQUE_ID",
            }
        }

    @classmethod
    def IS_CHANGED(s, **kwargs):
        print("CRDNodes==========================================")
        return float(time.time())

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "combine"
    CATEGORY = "CRDNodes/prompt"
    DESCRIPTION = """
    通过inputcount控制有多少个输入框
"""

    def combine(self, inputcount, prefix_select, unique_id=None, **kwargs):
        node_id = str(unique_id[0]) if isinstance(unique_id, list) else str(unique_id)

        main_prompt = prefix_select + kwargs["prompt_1"]
        for c in range(1, inputcount):
            new_prompt = kwargs[f"prompt_{c + 1}"]
            main_prompt = main_prompt + new_prompt

        if unique_id and PromptServer is not None:
            try:
                PromptServer.instance.send_progress_text(
                    f"<tr><td>Output: </td><td><b></b></td></tr>",
                    unique_id
                )
            except:
                pass

        return (main_prompt,)
