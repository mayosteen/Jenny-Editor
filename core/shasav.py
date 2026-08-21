# region Init

import re
from fractions import Fraction
from itertools import zip_longest
from math import log2

PRIMES = [2, 3, 5, 7, 11, 13, 17]

COMMAS = [
    Fraction(2, 1),
    Fraction(3, 2),
    Fraction(5, 4),
    Fraction(7, 4),
    Fraction(11, 4),
    Fraction(13, 4),
    Fraction(17, 4),
]

tokenscores = {
    # 0D
    "Ah":   Fraction(1, 1),
    # 1D
    "+":    Fraction(2, 1),
    "-":    Fraction(1, 2),
    # 2D
    "Chy":  Fraction(3, 2),
    "Scy":  Fraction(9, 4),
    "Xcy":  Fraction(27, 8),
    "Fu":   Fraction(2, 3),
    "Schu": Fraction(4, 9),
    "Ju":   Fraction(8, 27),
    # 3D
    "Ly":   Fraction(5, 4),
    "Su":   Fraction(4, 5),
    "Dry":  Fraction(25, 16),
    "Sru":  Fraction(16, 25),
    "li":   Fraction(5, 4),
    "s":    Fraction(4, 5),
    "dri":  Fraction(25, 16),
    "sr":   Fraction(16, 25),
    # 4D
    "My":   Fraction(7, 4),
    "Pu":   Fraction(4, 7),
    "Mry":  Fraction(49, 16),
    "Pru":  Fraction(16, 49),
    "mi":   Fraction(7, 4),
    "p":    Fraction(4, 7),
    "mry":  Fraction(49, 16),
    "pr":   Fraction(16, 49),
    # 5D
    "Zy":   Fraction(11, 4),
    "Tschu":Fraction(4, 11),
    "Ku":   Fraction(4, 11),
    "Zry":  Fraction(121, 16),
    "Kru":  Fraction(16, 121),
    "zi":   Fraction(11, 4),
    "k":    Fraction(4, 11),
    "zri":  Fraction(121, 16),
    "kr":   Fraction(16, 121),
}

# 按长度降序，保证最长匹配优先
SORTED_TOKENSCORES = sorted(tokenscores.keys(), key=len, reverse=True)

tokens = [
    "Ah",
    "+",    "-",
    "Chy",  "Scy",  "Xcy",  "Fu",   "Schu", "Ju",
    "Ly",   "Su",   "Dry",  "Sru",  "li",   "s",    "dri",  "sr",
    "My",   "Pu",   "Mry",  "Pru",  "mi",   "p",    "mri",  "pr",
    "Zy",   "Ku",   "Zry",  "Kru",  "zi",   "k",    "zri",  "kr",   "Tschu",
    "ta",   "cra",  "na",   "vra"
]

SORTED_TOKENS = sorted(tokens, key=len, reverse=True)

dimens = [
    {0:"Ah"},
    {-3:"Ju", -2:"Schu", -1:"Fu", +1:"Chy", +2:"Scy", +3:"Xcy",},
              {-2:"Sru", -1:"Su", +1:"Ly", +2:"Dry",},
              {-2:"Pru", -1:"Pu", +1:"My", +2:"Mry",},
              {-2:"Kru", -1:"Ku", +1:"Zy", +2:"Zry",},
]

# endregion

# region Monzo

# harmononym -> "AhChyChymik"
def h_c(harmononym: str) -> list[str]:
    return re.findall(r'[A-Z][a-z]*', harmononym)

# chordonym -> "Chymik"
def c_d(chordonym: str) -> list[str]:
    i = 0
    n = len(chordonym)
    result = []

    while i < n:
        matched = None
        for tok in SORTED_TOKENS:
            if chordonym.startswith(tok, i):
                matched = tok
                break
        if matched is not None:
            result.append(matched)
            i += len(matched)
        else:
            # 无法识别的字符：跳过或报错，视需求二选一
            raise ValueError(f"无法识别的字符 '{chordonym[i]}' at pos {i}")
    return result

# dimenonyms -> ["Chy", "mi", "k"]
def d_f(dimenonyms: list[str]) -> Fraction:
    f = Fraction(1, 1)
    for dimen in dimenonyms:
        f *= tokenscores.get(dimen, Fraction(1, 1))
    return f

# int -> 21
# int -> 22
def i_l(n):
    i = 2
    factors = {}
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 1 if i == 2 else 2
    if n > 1:
        factors[n] = 1
    return factors

# fraction -> Fraction(22, 21)
def f_l(r: Fraction):
    nf = i_l(r.numerator)
    df = i_l(r.denominator)
    return [nf.get(p,0) - df.get(p,0) for p in PRIMES]

# vector_string -> "[-1 1 0 1 -1⟩", "{-1; 1; 0; 1; -1}" or ...
def vs_l(vector_string) -> list[int]:
    return [int(x) for x in re.findall(r'-?\d+', vector_string)]

# list -> [-1, 1, 0, 1, -1]
def any_l(args) -> list[int]:
    # print(args)
    if isinstance(args, (tuple, list)) and len(args) == 1:
        return any_l(*args)
    if isinstance(args, str):
        if set("0123456789") & set(args):
            if "/" in args:
                return f_l(Fraction(args))
            else:
                return vs_l(args) # final
        return f_l(d_f(c_d(args)))
    elif isinstance(args, list) and isinstance(args[0], str):
        return f_l(d_f(args))
    elif isinstance(args, Fraction):
        return f_l(args) # final
    elif isinstance(args, (tuple, list)) and isinstance(args[0], int):
        return list(args) # final
    elif isinstance(args, Monzo):
        return args.vec
    else:
        return []


class Monzo:
    def __init__(self, *args):
        self.vec = any_l(args)
        self.update()

    # 去掉后面的 0
    def update(self):
        self.vec = self.vec[:next((i for i in range(len(self.vec)-1, -1, -1) if self.vec[i] != 0), 0)+1]
    
    def __add__(self, other:"Monzo") -> "Monzo":
        return Monzo([x + y for x, y in zip_longest(self.vec, other.vec, fillvalue=0)])

    def __sub__(self, other:"Monzo") -> "Monzo":
        return Monzo([x - y for x, y in zip_longest(self.vec, other.vec, fillvalue=0)])

    def __mul__(self, other:int):
        return Monzo([x*other for x in self.vec])

    def __str__(self) -> str:
        return "[{}⟩".format(" ".join([str(x) for x in self.vec]))
    
    def __repr__(self) -> str:
        return "Monzo({})".format(", ".join([str(x) for x in self.vec]))

    def to_fraction(self) -> Fraction:
        num = 1
        den = 1
        for p, e in zip(PRIMES, self.vec):
            if e > 0:
                num *= p ** e
            elif e < 0:
                den *= p ** (-e)
        return Fraction(num, den)

    def to_chordonym_no_octave(self) -> str:
        if len(self.vec) <= 1:
            return "Ah"
        Uppercase = 1
        chordonym = ""
        for p, e in zip(dimens[1:], self.vec[1:]):
            if e in p:
                dimen = p.get(e, "")
                if Uppercase:
                    chordonym += dimen
                    Uppercase = 0
                else:
                    chordonym += dimen.lower().replace("y", "i").replace("u", "")
        return chordonym

    def to_chordonym(self) -> str:
        chordonym = self.to_chordonym_no_octave()
        octaves = (self.vec[0] if self.vec else 0) - any_l(chordonym)[0]
        if octaves > 0:
            chordonym += "+" * abs(octaves)
        elif octaves < 0:
            chordonym += "-" * abs(octaves)
        return chordonym

# endregion

class Harmononym:
    def __init__(self, harmononym:str):
        self.monzos = [Monzo(chordonym) for chordonym in h_c(harmononym)]
        self.bass = self.monzos[0]

    def __str__(self):
        return "".join([monzo.to_chordonym() for monzo in self.monzos])

    def na(self):
        m = self.monzos.copy()
        self.monzos = [
            m[0],  # Ah
            m[1],  # Chy
            m[1] - m[2] +m[0],  # Chy - Ly (+Ah) = Chys
        ]

    def cra(self):
        m = self.monzos.copy()
        self.monzos = [
            m[2] - m[1] +m[0],  # Ly - Chy (+Ah) = Fuly
            m[2],  # Ly
            m[0],  # Ah
        ]

    def vra(self):
        m = self.monzos.copy()
        self.monzos = [
            m[2],  # Ly
            m[1] + m[2] -m[0],  # Chy + Ly (-Ah) = Chyli
            m[1],  # Chy
        ]

# region Functograph

def Functograph(f, df_c="AhChyLy"):
    df_h = Harmononym(df_c)
    f = c_d(f)
    if "cra" in f: df_h.cra()
    if  "na" in f: df_h. na()
    if "vra" in f: df_h.vra()
    print(f)
    print(df_h)

# Functograph("Ahcranavra")
# Functograph("Ahcrana")
# Functograph("Ahcravra")
# Functograph("Ahnavra")
# Functograph("Ahcra")
# Functograph("Ahna")
# Functograph("Ahvra")
# Functograph("Ahta")
# endregion

# region Val

class Val:
    def __init__(self, edo):
        self._edo = edo
        self.update()

    def update(self):
        self.vec = [round(self._edo*log2(p)) for p in PRIMES]

    def __matmul__(self, other:Monzo):
        return sum(v*e for v,e in zip(self.vec, other.vec))
    
    def __str__(self):
        return "⟨{}]".format(" ".join(map(str,self.vec)))
    
    @property
    def edo(self):
        return self._edo

    @edo.setter
    def edo(self, value):
        self._edo = value
        self.update()

# endregion

# region Val

class Tuning:
    def __init__(self, edo):
        self._edo = edo
        self.update()

    def update(self):
        self.vec = [round(self._edo*log2(c)) for c in COMMAS]

    def __matmul__(self, other:Monzo):
        return sum(v*e for v,e in zip(self.vec, other.vec))
    
    def __str__(self):
        return "[{}]".format("-".join(map(str,self.vec)))
    
    @property
    def edo(self):
        return self._edo

    @edo.setter
    def edo(self, value):
        self._edo = value
        self.update()

# endregion

# region Unittest
"""
if __name__ == "__main__":
    e_72 = Val(72)
    for a in [
        "Chymik",
        ["Chy", "mi", "k"],
        "[-1 1 0 1 -1⟩", 
        "{-1; 1; 0; 1; -1}",
        "-1, 1, 0, 1, -1",
        "21/22",
        Fraction(21, 22),
        [-1, 1, 0, 1, -1],

        "Chymik+",
        ["Chy", "mi", "k", "+"],
        "[0 1 0 1 -1⟩", 
        "{0; 1; 0; 1; -1}",
        "0, 1, 0, 1, -1",
        "21/11",
        Fraction(21, 11),
        [0, 1, 0, 1, -1],

        "42/11",
        "84/11",
        "168/11",
        "420/11",
    ]:
        m = Monzo(a)
        print(a, m, m.to_fraction(), m.to_chordonym(), m * e_72)
"""
# endregion