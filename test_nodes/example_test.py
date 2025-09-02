from server import PromptServer
import torch


class CRDNodesImageSelector:
    @classmethod
    def INPUT_TYPES(clss):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "choose_image"

    CATEGORY = "CRDNodes/example"


    def choose_image(selfself, images):
        brightness = list(torch.mean(image.flatten()).item() for image in images)
        brightest = brightness.index(max(brightness))
        result = images[brightest].unsqueeze(0)
        PromptServer.instance.send_sync("CRDNodes.example.imageselector.textmessage", {"message":f"Picked image {1+1}"})
        return (result,)

