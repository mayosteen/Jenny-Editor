import re
from fractions import Fraction
from itertools import zip_longest

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

# tokenscores = {
#     # 0D
#     "Ah":   Fraction(1, 1),
#     # 1D
#     "+":    Fraction(2, 1),
#     "-":    Fraction(1, 2),
#     # 2D
#     "Chy":  Fraction(3, 2),
#     "Scy":  Fraction(9, 4),
#     "Xcy":  Fraction(27, 8),
#     "Fu":   Fraction(2, 3),
#     "Schu": Fraction(4, 9),
#     "Ju":   Fraction(8, 27),
#     # 3D
#     "Ly":   Fraction(5, 4),
#     "Su":   Fraction(4, 5),
#     "li":   Fraction(5, 4),
#     "s":    Fraction(4, 5),
#     # 4D
#     "My":   Fraction(7, 4),
#     "Pu":   Fraction(4, 7),
#     "mi":   Fraction(7, 4),
#     "p":    Fraction(4, 7),
#     # 5D
#     "Zy":   Fraction(11, 4),
#     "Tschu":Fraction(4, 11),
#     "Ku":   Fraction(4, 11),
#     "zi":   Fraction(11, 4),
#     "k":    Fraction(4, 11),
# }

# # 按长度降序，保证最长匹配优先
# SORTED_TOKENS = sorted(tokenscores.keys(), key=len, reverse=True)

tokens = [
    "Ah",
    "+",    "-",
    "Chy",  "Scy",  "Xcy",  "Fu",   "Schu", "Ju",
    "Ly",   "Su",   "li",   "s",
    "My",   "Pu",   "mi",   "p",
    "Zy",   "Ku",   "zi",   "k",
]

SORTED_TOKENS = sorted(tokens, key=len, reverse=True)



































def tokenize(text: str) -> list[str]:
    """
    最长匹配分词。
    tokens: 已按长度降序排列的 token 列表（即 SORTED_TOKENS）
    scores: token -> Fraction 映射
    返回: 切分后的 token 序列
    """
    i = 0
    n = len(text)
    result = []

    while i < n:
        matched = None
        for tok in SORTED_TOKENS:
            if text.startswith(tok, i):
                matched = tok
                break
        if matched is not None:
            result.append(matched)
            i += len(matched)
        else:
            # 无法识别的字符：跳过或报错，视需求二选一
            raise ValueError(f"无法识别的字符 '{text[i]}' at pos {i}")
    
    return result


def monzo_tuple(args) -> list[int]:
    arg_type = "none"
    result = [0]
    if args:
        if isinstance(args, str):
            if set("0123456789") & set(args):
                arg_type = "monzo str"
                result = [int(x) for x in re.findall(r'-?\d+', args)]
                if not result:
                    result.append(0)
            else:
                arg_type = "shasav_str"
        elif isinstance(args, (tuple, list)):
            print(f"monzo_tuple | list:{args}")
    print(f"{arg_type}: {args} -> {result}")
    return result





















class Monzo:
    def __init__(self, *args):
        self.vec = monzo_tuple(args)
    
    def __add__(self, another:"Monzo"):
        return Monzo([x + y for x, y in zip_longest(self.vec, another.vec, fillvalue=0)])
