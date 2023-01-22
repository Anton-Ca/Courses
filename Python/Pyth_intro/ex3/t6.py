import regex as re
import string

alphabet = list(string.ascii_lowercase)
morse = [
    ".-",
    "-...",
    "-.-.",
    "-..",
    ".",
    "..-.",
    "--.",
    "....",
    "..",
    ".---",
    "-.-",
    ".-..",
    "--",
    "-.",
    "---",
    ".--.",
    "--.-",
    ".-.",
    "...",
    "-",
    "..-",
    "...-",
    ".--",
    "-..-",
    "-.--",
    "--..",
]
code = input(
    f"\nEnter a morse code to translate.\nUse . as short char, - as long and a comma to seperate words and space to seperate letters.\n\n"
)
message = ""


def translate_to_morse(code, message):
    morse_translation = {a: m for (a, m) in zip(alphabet, morse)}
    for char in code:
        if char == " ":
            message += ","
        elif char.isalpha():
            message += " " + re.sub(char, morse_translation.get(char.lower()), char)
        else:
            message += char
    print(message)


def translate_from_morse(code, message):
    morse_translation = {m: a for (m, a) in zip(morse, alphabet)}
    pattern = r"([^\s]+)"
    morse_letters = re.findall(pattern, code.lower())

    for letter in morse_letters:
        if "," in letter:
            p = r"([.-]+)"
            l = re.findall(p, letter)[0]
            message += morse_translation.get(l) + " " + letter[len(l) + 1 :]
        elif re.search(r"([^.-]+)", letter) != None:
            p = r"([.-]+)"
            l = re.findall(p, letter)[0]
            message += morse_translation.get(l) + letter[len(l) :]
        else:
            message += morse_translation.get(letter)
    print(message)


if not code[0].isalpha():
    translate_from_morse(code, message)
else:
    translate_to_morse(code, message)
