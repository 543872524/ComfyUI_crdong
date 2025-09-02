from .test_nodes.prompt_test import *
from .test_nodes.example_test import *
from .crd_nodes.image_nodes import *
from .crd_nodes.my_nodes import *
from .crd_nodes.prompt_nodes import *
from .crd_nodes.video_nodes import *
from .crd_nodes.audio_nodes import *

NODES_CONF = {
    "INTConstant": {"class": INTConstant, "name": "INT Constant"},
    "CRDNodesImageSelector": {"class": CRDNodesImageSelector, "name": "CRDNodesImageSelector"},
    "SimpleIntMathHandle": {"class": SimpleIntMathHandle, "name": "Simple Int Math Handle"},
    "SimpleJsonArrayHandle": {"class": SimpleJsonArrayHandle, "name": "Simple Json Array Handle"},
    "SimpleJsonObjectHandle": {"class": SimpleJsonObjectHandle, "name": "Simple Json Object Handle"},
    "SelectImageSize": {"class": SelectImageSize, "name": "Select Image Size"},
    "VideoTimeAndFPS": {"class": VideoTimeAndFPS, "name": "Video Time & FPS"},
    "VideoFrameSize": {"class": VideoFrameSize, "name": "Video Frame Size"},
    "Wan22StepHandle": {"class": Wan22StepHandle, "name": "Wan22 Step Handle"},
    "PromptSelectorStr": {"class": PromptSelectorStr, "name": "Prompt Selector String"},
    "PromptSelectorList": {"class": PromptSelectorList, "name": "Prompt Selector List"},
    "PromptBatchMulti": {"class": PromptBatchMulti, "name": "PromptBatchMulti"},
    "PromptExampleNode": {"class": PromptExampleNode, "name": "Prompt Example Node"},
    "PromptJoinOrList": {"class": PromptJoinOrList, "name": "Prompt Join or List"},
    "PromptList": {"class": PromptList, "name": "Prompt List"},
    "CRDAudioLengthNode": {"class": CRDAudioLengthNode, "name": "CRD Audio Length Node"},
}


def gen_mappings(node_conf: dict):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_conf.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info["name"]

    return node_class_mappings, node_display_name_mappings


NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = gen_mappings(NODES_CONF)
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]

WEB_DIRECTORY = "./web"

from aiohttp import web
from server import PromptServer
from pathlib import Path

if hasattr(PromptServer, "instance"):
    try:
        # NOTE: we add an extra static path to avoid comfy mechanism
        # that loads every script in web.
        PromptServer.instance.app.add_routes(
            [web.static("/crdweb_async", (Path(__file__).parent.absolute() / "crdweb_async").as_posix())]
        )
    except:
        pass
