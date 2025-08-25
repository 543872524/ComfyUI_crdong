BASE_RESOLUTIONS = [
    (512, 512),
    (512, 768),
    (576, 1024),
    (768, 512),
    (768, 768),
    (768, 1024),
    (768, 1280),
    (768, 1344),
    (768, 1536),
    (816, 1920),
    (832, 1152),
    (832, 1216),
    (896, 1152),
    (896, 1088),
    (1024, 1024),
    (1024, 576),
    (1024, 768),
    (1080, 1920),
    (1440, 2560),
    (1088, 896),
    (1216, 832),
    (1152, 832),
    (1152, 896),
    (1280, 768),
    (1344, 768),
    (1536, 640),
    (1536, 768),
    (1920, 816),
    (1920, 1080),
    (2560, 1440),
]
pre_image_size = ["720*1280", "1280*720",
                  "2016*864(21:9)", "864*2016(9:21)", "1664*936(16:9)", "936*1664(9:16)",
                  "1584*1056(3:2)", "1056*1584(2:3)", "1472*1104(4:3)", "1104*1472(3:4)"]


# SelectImageSize
class SelectImageSize:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        base_image_size = [f'{width}*{height}' for width, height in BASE_RESOLUTIONS] + pre_image_size
        return {"required":
            {
                "image_size": (base_image_size, {"default": "936*1664(9:16)"},),
            },
        }

    CATEGORY = "CRDNodes/image"
    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("width", "height",)
    FUNCTION = "get_image_size"

    def get_image_size(self, image_size):
        image_size_strip = image_size.strip()
        if len(image_size_strip) == 0:
            return (1024, 1024)
        if "(" in image_size_strip:
            _index = image_size_strip.index("(")
            image_size_strip = image_size_strip[:_index]
        image_size_strip_split = image_size_strip.split('*')
        image_width = int(image_size_strip_split[0])
        image_height = int(image_size_strip_split[1])
        return (image_width, image_height)


aaa = []
print(aaa)
