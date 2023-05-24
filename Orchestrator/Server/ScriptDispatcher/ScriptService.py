import logging


class ScriptService:

    def __init__(self):
        pass

    def _compress_text(self, text: str) -> str:
        one_line_text = text.replace('\n', ' ').replace('\r', '')
        trimmed_one_line_text = filter(lambda x: x != '', one_line_text.split(' '))
        return ' '.join(trimmed_one_line_text)

    def get_binary_script(self, script_text: str) -> bytearray:
        logging.info(f'Loaded script (length = {len(script_text)}): \n{script_text}')

        compressed_text = self._compress_text(script_text)
        logging.info(f'Compressed script (length = {len(compressed_text)}): \n{compressed_text}')

        binary_script = bytearray()
        binary_script.extend(map(ord, compressed_text))
        return binary_script


if __name__ == "__main__":
    script_srv = ScriptService()
    result = script_srv.get_binary_script()
    print(f'BINARY: {result}')
