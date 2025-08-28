import comfy
import nodes
import torchaudio
import torch
import os
import argparse
from pathlib import Path
from comfy_extras.nodes_audio import load

try:
    import mutagen
except ImportError:
    mutagen = None


class CRDAudioLoader():
    pass

    def load_audio(self, audio_path):
        wav, simple = load(audio_path)
        return (wav, simple)


class GetAudioDuration():
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
            {
                "audio": ("AUDIO",)
            }
        }

    CATEGORY = "CRDNodes/audio"
    RETURN_TYPES = ("FLOAT", "INT",)
    RETURN_NAMES = ("duration_f", "duration_i",)
    FUNCTION = "get_audio_duration"

    def get_audio_duration(self, audio):
        duration = 0
        return (float(duration), int(duration))


def get_audio_duration_by_mutagen(file_path):
    """
    获取音频文件时长（秒）
    参数:
        file_path (str): 音频文件路径
        use_librosa (bool): 是否强制使用librosa库
    返回:
        float: 音频时长（秒）
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 优先使用mutagen（性能更好）
    if mutagen:
        try:
            audio = mutagen.File(file_path)
            if audio is not None:
                return audio.info.length
        except Exception as e:
            print(f"使用mutagen解析失败: {e}，尝试其他方法...")

    # 最后尝试使用wave模块（仅适用于WAV文件）
    if file_path.lower().endswith('.wav'):
        try:
            import wave
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                return frames / float(rate)
        except Exception as e:
            print(f"使用wave解析WAV文件失败: {e}")

    raise ValueError("无法解析音频文件，请确保文件格式正确或安装必要的库")


class CRDAudioLengthNode:
    """
    音频长度获取节点
    支持多种音频格式，返回音频长度（秒）、采样数和采样率信息
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_input": ("AUDIO",),
                "time_unit": (["seconds", "milliseconds", "samples"], {
                    "default": "seconds"
                }),
            },
            "optional": {
                "round_decimals": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 6,
                    "step": 1
                }),
            }
        }

    RETURN_TYPES = ("FLOAT", "INT", "INT", "INT", "STRING")
    RETURN_NAMES = ("length_f", "length_i", "samples", "sample_rate", "formatted_length")
    FUNCTION = "get_audio_length"
    CATEGORY = "CRDNodes/audio"

    def get_audio_length(self, audio_input, time_unit: str = "seconds",
                         round_decimals: int = 3) -> tuple:
        """
        获取音频长度信息

        Args:
            audio: 音频张量，形状为 [channels, samples] 或 [batch, channels, samples]
            time_unit: 时间单位（seconds, milliseconds, samples）
            round_decimals: 小数位数（仅对秒和毫秒有效）

        Returns:
            tuple: (长度值, 采样数, 采样率, 格式化字符串)
        """
        try:
            audio = audio_input['waveform']
            # 检查音频张量形状
            if audio.dim() not in [2, 3]:
                raise ValueError(f"音频张量维度应为2或3，当前维度: {audio.dim()}")

            # 获取采样数（最后一个维度）
            samples = audio.shape[-1]

            # 假设采样率信息存储在张量的元数据中（ComfyUI标准做法）
            sample_rate = self._get_sample_rate(audio)
            sample_rate_ = audio_input['sample_rate']
            if sample_rate_ and sample_rate != sample_rate_:
                sample_rate = sample_rate_

            # 根据时间单位计算长度
            if time_unit == "seconds":
                length = samples / sample_rate
                formatted = f"{round(length, round_decimals)}s"
            elif time_unit == "milliseconds":
                length = (samples / sample_rate) * 1000
                formatted = f"{round(length, round_decimals)}ms"
            else:  # samples
                length = float(samples)
                formatted = f"{samples} samples"

            return (float(length), int(length), samples, sample_rate, formatted)

        except Exception as e:
            raise ValueError(f"音频处理错误: {str(e)}")

    def _get_sample_rate(self, audio: torch.Tensor) -> int:
        """
        从音频张量中获取采样率

        Args:
            audio: 音频张量

        Returns:
            int: 采样率（默认44100）
        """
        # ComfyUI 通常将采样率存储在张量的元数据中
        if hasattr(audio, 'sample_rate'):
            return audio.sample_rate

        # 检查张量属性
        sample_rate_attr = getattr(audio, '_sample_rate', None)
        if sample_rate_attr is not None:
            return sample_rate_attr

        # 默认采样率（常见音频采样率）
        return 44100
