from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from config import STATIC
from pydub import AudioSegment
from pydub.playback import play


# Функция для увеличения громкости на 5%
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(1.0, current_volume + 0.05), None)

# Функция для уменьшения громкости на 5%
def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(max(0.0, current_volume - 0.05), None)

def play_audio(file_path):
    audio = AudioSegment.from_file(file_path, format="m4a")
    play(audio)

# Пример использования
#audio_file = "D:\\projects\\pythonProjects\\lazy_boy_bot\\static\\eto_vtoroy.m4a"

#play_audio(audio_file)