import librosa
import numpy as np
from scipy.io.wavfile import write

# 1. 读取音频
audio_path = "input.mp3"
y, sr = librosa.load(audio_path, sr=None, mono=True)

# 2. 归一化到 [-1, 1]
y = y / (np.max(np.abs(y)) + 1e-11)

# 3. 二值化（1-bit）
y_binary = np.where(y >= 0, 1.0, -1.0)

# 4. 映射到 uint8 [0, 255]
y_uint8 = ((y_binary + 1) / 2 * 255).astype(np.uint8)

# 5. 保存为 WAV
output_path = "output_1bit.wav"
write(output_path, sr, y_uint8)

print("1-bit 二值化 WAV 已保存:", output_path)