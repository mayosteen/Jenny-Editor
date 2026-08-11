import librosa
import soundfile as sf
import re
import math
from fractions import Fraction

tokens = [
    "Tschu", "Schu", "Scy", "Xcy", "Chy",
    "Ah", "Fu", "Ju", "Ly", "Su", "My", "Pu", "Zy", "Ku",
    "li", "mi", "zi", "si", "pi",
    "s", "p", "k", "+", "-"
]
# 所有 token 及其对应的分数
tokenscores = {
    "Ah":   Fraction(1, 1),
    "+":    Fraction(2, 1),
    "-":    Fraction(1, 2),
    "Chy":  Fraction(3, 2),
    "Scy":  Fraction(9, 4),
    "Xcy":  Fraction(27, 8),
    "Fu":   Fraction(2, 3),
    "Schu": Fraction(4, 9),
    "Ju":   Fraction(8, 27),
    "Ly":   Fraction(5, 4),
    "Su":   Fraction(4, 5),
    "My":   Fraction(7, 4),
    "Pu":   Fraction(4, 7),
    "Zy":   Fraction(11, 4),
    "Tschu":Fraction(4, 11),
    "Ku":   Fraction(4, 11),
    "li":   Fraction(5, 4),
    "s":    Fraction(4, 5),
    "mi":   Fraction(7, 4),
    "p":    Fraction(4, 7),
    "zi":   Fraction(11, 4),
    "k":    Fraction(4, 11),
}




# 按长度降序，保证最长匹配优先
tokens.sort(key=len, reverse=True)

def tokenize(s):
    tklist = []
    result = Fraction(1, 1)
    i = 0
    while i < len(s):
        match = None
        for t in tokens:
            if s[i:i+len(t)] == t:
                match = t
                break
        if match:
            tklist.append(match)
            result *= tokenscores[match]
            i += len(match)
        else:
            tklist.append(s[i])  # 无法匹配的字符单独输出
            i += 1
    return tklist, result



def output(s):
    for t in re.findall(r'[A-Z][a-z]*', s):  # 仅匹配大写字母开头的 token
        fraction = tokenize(t)[1]
        steps = 12 * (math.log2(float(fraction)))
        osteps = round(steps)
        y, sr = librosa.load(f"tunings/12/German Concert D {(60+osteps):03d} 083.wav", sr=None)
        y_new = librosa.effects.pitch_shift(y, sr=sr, n_steps=steps-osteps)
        sf.write(f"tunings/JI/{t}.wav", y_new, int(sr))
        print(f"Generated {t}.wav with {steps:.2f} steps ({fraction})")

# for i in ["Chy", "Scy", "Xcy", "Fu", "Schu", "Ju"]:
#     for j in ["", "li", "s", "mi", "p", "zi", "k"]:
#         output(i + j)
# output("Ah")
# for i in ["Ly", "Su", "My", "Pu", "Zy", "Ku"]:
#     output(i)
output("Ah")