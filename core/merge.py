import os, subprocess, sys

FPS = 60
VIDEO = r'recordings\output.mp4'

if len(sys.argv) < 2:
    print("用法: python render.py <audio_file>")
    sys.exit(1)

audio = sys.argv[1]

if not os.path.exists(audio):
    print(f"❌ 音频文件不存在: {audio}")
    sys.exit(1)

print("Encoding video...")

if os.path.exists(VIDEO):
    os.remove(VIDEO)

cmd = [
    'ffmpeg.exe',
    '-framerate', str(FPS),
    '-i', r'cache\frame_%06d.png',
    '-i', audio,
    '-c:v', 'h264_nvenc',
    '-preset', 'p7',
    '-rc', 'vbr',
    '-cq', '18',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'copy',
    '-shortest',
    '-y',
    VIDEO,
]

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f'❌ ffmpeg 失败 (code={e.returncode})，图片保留不删')
    sys.exit(1)

# 双重确认 mp4 正常
if os.path.getsize(VIDEO) == 0:
    print('❌ output.mp4 为空，图片保留不删')
    sys.exit(1)

cache_dir = "./cache"

if not os.path.exists(cache_dir):
    print(f"文件夹 '{cache_dir}' 不存在")
elif not os.path.isdir(cache_dir):
    print(f"'{cache_dir}' 不是一个文件夹")
else:
    for item in os.listdir(cache_dir):
        item_path = os.path.join(cache_dir, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
            print(f"已删除文件: {item_path}")
        # elif os.path.isdir(item_path):
        #     shutil.rmtree(item_path)
        #     print(f"已删除文件夹: {item_path}")
    print(f"\n✅ './cache' 文件夹已全部清空")

print(f"✅ Done. ({os.path.getsize(VIDEO)//1024//1024}MB)")