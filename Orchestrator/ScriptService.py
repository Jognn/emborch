import logging


class ScriptService:

    def __init__(self, filename: str = "main.lua"):
        self.filename = filename

    def _compress_text(self, text: str) -> str:
        one_line_text = text.replace('\n', ' ').replace('\r', '').split(' ')

        trimmed_text = list()
        for index, word in enumerate(one_line_text):
            one_line_text[index].strip()
            if word != '':
                trimmed_text.append(word)

        return ' '.join(trimmed_text)

    def get_binary_script(self) -> bytearray:
        with open(self.filename, 'r') as lua_script:
            text_script = lua_script.read()

        logging.info(f'Loaded script (length = {len(text_script)}): \n{text_script}')

        compressed_text = self._compress_text(text_script)
        logging.info(f'Compressed script (length = {len(compressed_text)}): \n{compressed_text}')

        binary_script = bytearray()
        binary_script.extend(map(ord, compressed_text))
        return binary_script


if __name__ == "__main__":
    script_srv = ScriptService()
    result = script_srv.get_binary_script()
    print(f'BINARY: {result}')
