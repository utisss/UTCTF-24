import json

conversion = {}
with open('main.json', encoding='utf8') as f:
    conversion = json.load(f)


def build_plover(s):
    plover = ''
    if 'q' in s or 'a' in s:
        plover += 'S'
    if 'w' in s:
        plover += 'T'
    if 's' in s:
        plover += 'K'
    if 'e' in s:
        plover += 'P'
    if 'd' in s:
        plover += 'W'
    if 'r' in s:
        plover += 'H'
    if 'f' in s:
        plover += 'R'
    if 'c' in s:
        plover += 'A'
    if 'v' in s:
        plover += 'O'
    if 't' in s or 'y' in s or 'g' in s or 'h' in s:
        plover += '*'
    # this is where a '-' would go
    if 'n' in s:
        plover += 'E'
    if 'm' in s:
        plover += 'U'
    if 'u' in s:
        plover += 'F'
    if 'j' in s:
        plover += 'R'
    if 'i' in s:
        plover += 'P'
    if 'k' in s:
        plover += 'B'
    if 'o' in s:
        plover += 'L'
    if 'l' in s:
        plover += 'G'
    if 'p' in s:
        plover += 'T'
    if ';' in s:
        plover += 'S'
    if '[' in s:
        plover += 'D'
    if '\'' in s:
        plover += 'Z'
    return plover

newmap = {
    # 2: "PostFail",
    4: "a",
    5: "b",
    6: "c",
    7: "d",
    8: "e",
    9: "f",
    10: "g",
    11: "h",
    12: "i",
	13: "j",
    14: "k",
    15: "l",
    16: "m",
    17: "n",
    18: "o",
    19: "p",
    20: "q",
    21: 'r',
    22: 's',
    23: 't',
    24: 'u',
    25: 'v',
    26: 'w',
    27: 'x',
    28: 'y',
    29: 'z',
    30: '1',
    31: '2',
    32: '3',
    33: '4',
    34: '5',
    35: '6',
    36: '7',
    37: '8',
    38: '9',
    39: '0',
    40: '\r\n',
    41: 'ESC',
    42: "del",
    43: 'tab',
    44: 'space',
    45: '-',
    47: '[',
    48: ']',
    55: '*',
    56: '/',
    57: 'CapsLock',
    79: '>',
    80: '<'
}
message = ""
myKeys = open("keystrokes.txt")
i = 1
for line in myKeys:
    bytesArray = bytearray.fromhex(line.replace(':', '').strip())
    for byte in bytesArray:
        if byte != 0:
            keyVal = int(byte)
            if keyVal in newmap:
                message += newmap[keyVal]
            else:
                pass
            i += 1
    message += '\n'

m = message.split('\n')
# print(m)
s = set()
output = ""
combine = ""
in_flag = 0

for fragment in m:
    if not fragment:
        p = build_plover(s)
        if p in conversion:
            word = conversion[p]
            if word == "{^_^}":
                # I couldn't figure out an elegant way to handle words with
                # multiple chords so I print both results since I know I'm
                # in the flag, then I correct the output by hand
                if '/' in combine:
                    try:
                        output += conversion[combine]
                    except:
                        pass
                output += "_"
                combine = ""
            elif word == "{^}\\}":
                output += "}"
                in_flag = 0
            elif word == "\\{{^}":
                output += "{"
                in_flag = 1
            else:
                if in_flag:
                    if combine:
                        combine += "/" + p
                    else:
                        combine = p
                output += word
        else:
            # delete
            if p == "PWG":
                output = output[:-2]
            # I don't elegantly handle chords with '-' in them so I added this.
            # Yes, I know it's bad.
            # But maybe you should look at the dictionary first too
            elif p == "TPRBGT":
                output += "{"
                in_flag = 1
            else:
                output += p
        output += " "
        s = set()
    else:
        for char in fragment:
            s.add(char)
print(output)

