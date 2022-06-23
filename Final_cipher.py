class Playfair_cipher:
    def __init__(self):
        self.matrixKey = [
            ['S', 'O', 'M', 'E', 'T'],
            ['H', 'I', 'N', 'G', 'A'],
            ['B', 'C', 'D', 'F', 'K'],
            ['L', 'P', 'Q', 'R', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        self.addSymbol = 'X'

    def regular(self, text):
        from re import findall
        template = r"[A-Z]{2}"
        return findall(template, text)

    def encryptDecrypt(self, mode, message, final=""):
        message = list(message)
        if mode == 'E':
            for symbol in message:
                if symbol not in [chr(x) for x in range(65, 91)]:
                    message.remove(symbol)
            for index in range(len(message)):
                if message[index] == 'J': message[index] = 'I'
            for index in range(1, len(message)):
                if message[index] == message[index - 1]:
                    message.insert(index, self.addSymbol)
            if len(message) % 2 != 0:
                message.append(self.addSymbol)

        binary_list = self.regular("".join(message))
        for binary in range(len(binary_list)):
            binary_list[binary] = list(binary_list[binary])
            for indexString in range(len(self.matrixKey)):
                for indexSymbol in range(len(self.matrixKey[indexString])):
                    if binary_list[binary][0] == self.matrixKey[indexString][indexSymbol]:
                        y0, x0 = indexString, indexSymbol
                    if binary_list[binary][1] == self.matrixKey[indexString][indexSymbol]:
                        y1, x1 = indexString, indexSymbol
            for indexString in range(len(self.matrixKey)):
                if self.matrixKey[y0][x0] in self.matrixKey[indexString] and self.matrixKey[y1][x1] in self.matrixKey[indexString]:

                    if mode == 'E':
                        x0 = x0 + 1 if x0 != 4 else 0
                        x1 = x1 + 1 if x1 != 4 else 0
                    else:
                        x0 = x0 - 1 if x0 != 0 else 4
                        x1 = x1 - 1 if x1 != 0 else 4

            y0, y1 = y1, y0
            binary_list[binary][0] = self.matrixKey[y0][x0]
            binary_list[binary][1] = self.matrixKey[y1][x1]
        for binary in range(len(binary_list)):
            for symbol in binary_list[binary]:
                final += symbol

        final = list(final)
        for i in range(len(final) - 1):
            if final[i] == "X":
                if final[i] != final[-1]:
                    if final[i - 1] == final[i + 1]:
                        final.remove(final[i])
                else:
                    final.remove(final[i])

        help_final = final.copy()
        final = ''
        for i in range(len(help_final)):
            final += help_final[i]

        return final
