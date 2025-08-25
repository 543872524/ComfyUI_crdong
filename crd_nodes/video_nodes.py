# VideoTimeAndFPS
class VideoTimeAndFPS:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "video_time": ('INT', {'default': 5, "min": 1, "max": 4096, "step": 1, }),
                "video_fps": ('INT', {'default': 16, "min": 1, "max": 4096, "step": 1, }),
                "add_fps": ('INT', {'default': 1, "min": 0, "max": 4096, "step": 1, }),
            },
        }

    CATEGORY = "CRDNodes/video"
    RETURN_TYPES = ("INT", "FLOAT", "INT",)
    RETURN_NAMES = ("v_fps", "v_fps_float", "v_length",)
    FUNCTION = "get_video_time_and_fps"

    def get_video_time_and_fps(self, video_time, video_fps, add_fps):
        v_fps_float = round(video_fps, 6)
        v_length = video_time * video_fps + add_fps
        return (video_fps, v_fps_float, v_length)


class VideoFrameSize:
    _video_size = ["480P", "720P", "1080P"]

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "video_size": (s._video_size, {'default': "480P"}),
                "swap": ("BOOLEAN", {'default': False}),
            },
        }

    CATEGORY = "CRDNodes/video"
    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("width", "height",)
    FUNCTION = "get_video_size"

    def get_video_size(self, video_size, swap):
        if video_size == "480P":
            if swap:
                return (832, 480)
            return (480, 832)
        if video_size == "720P":
            if swap:
                return (1280, 720)
            return (720, 1280)
        if video_size == "1080P":
            if swap:
                return (1920, 1080)
            return (1080, 1920)


class Wan22StepHandle:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "count_step": ("INT", {"default": 10, "min": 2, "max": 100, "step": 1},),
                "first_step": ("INT", {"default": 2, "min": 2, "max": 100, "step": 1},),
                "operator": (["-", "half"], {"default": "-", },),
            },
        }

    CATEGORY = "CRDNodes/video"
    RETURN_TYPES = ("INT", "INT", "INT",)
    RETURN_NAMES = ("count_step", "first_step", "sec_step")
    FUNCTION = "get_video_step"

    def get_video_step(self, count_step, first_step, operator):
        if operator is '-':
            sec_step = count_step - first_step
        elif operator is 'half':
            first_step = count_step // 2
            sec_step = count_step // 2
        else:
            sec_step = count_step - first_step
        return (count_step, first_step, sec_step,)
