import os
from config import FPS
print("Encoding video...")
if os.path.exists(r'recordings\output.mp4'):
    os.remove(r'recordings\output.mp4')
os.system('ffmpeg.exe '
   f'-framerate {FPS} '
   r'-i recordings\%06d.png '
   r'-i recordings\audio.aac '
    '-c:v h264_nvenc '
    '-preset p7 '
    '-rc vbr '
    '-cq 18 '
    '-pix_fmt yuv420p '
    '-c:a copy '
    '-shortest '
   r'recordings\output.mp4')
os.system(r"del /Q recordings\0?????.png")
print("Done.")