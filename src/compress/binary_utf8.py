def binary_string_to_utf8(source: str) -> str:

    utf8_string = ''
    for i in range(0, len(source), 8):
        byte = source[i:i + 8]
        utf8_string += chr(int(byte, 2))
    return utf8_string


def utf8_to_binary_string(source: str) -> str:
    binary_string = ''
    for char in source:
        binary_string += format(ord(char), '08b')
    return binary_string
