
# https://morsecode.world/international/translator.html
# utflag utctf uses svg to its fullest
text = "..- - ..-. .-.. .- --. / ..- - -.-. - ..-. / ..- ... . ... / ... ...- --. / - --- / .. - ... / ..-. ..- .-.. .-.. . ... - //"

def lengths(c):
    if c == ".": return (1, 1)
    elif c == "-": return (3, 1)
    elif c == " ": return (0, 3)
    elif c == "/": return (0, 1)

total_time = sum((sum(lengths(c)) for c in text))
print(total_time)

cur_time = 0
for c in text:
    (on, off) = lengths(c)
    if on != 0:
      print(f"{100.0 * cur_time / total_time:.3f}% {{ fill: #FFFF; }}");
      cur_time += on
    if off != 0:
      print(f"{100.0 * cur_time / total_time:.3f}% {{ fill: #FFF6; }}");
      cur_time += off

print("100% { fill: #FFF6; }");
