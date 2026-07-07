import sys, os
from config import FPS
print("Encoding video...")
if os.path.exists(f'{sys.argv[2]}'):
    os.remove(f'{sys.argv[2]}')
os.system('ffmpeg.exe '
   f'-framerate {FPS} '
   r'-i .cache\%06d.png '
   f'-i {sys.argv[1]} '
    '-c:v h264_nvenc '
    '-preset p7 '
    '-rc vbr '
    '-cq 18 '
    '-pix_fmt yuv420p '
    '-c:a aac '
    '-shortest '
   f'{sys.argv[2]}')
os.system(r"del /Q .cache\0?????.png")
print("Done.")