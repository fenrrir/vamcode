# coding: utf-8

import codecs

DICIONARIO = (
    ('assert', '👀'),
    ('break', '✋'),
    ('class', '🏠'),
    ('continue', '⏩'),
    ('def', '🍀'),
    ('del', '☠'),
    ('elif', '⁉️'),
    ('else', '❗️'),
    ('except', '🙏'),
    ('exec', '🛌'),
    ('finally', '🍾'),
    ('global', '☝️'),
    ('import', '⚡️'),
    ('lambda', '🦄'),
    ('pass', '♻️'),
    ('raise', '🚀'),
    ('return', '⤴️'),
    ('try', '⚽️'),
    ('while', '🔃'),
    ('yield', '⏏'),
    ('as', '🕵'), 
    ('for', '🏃'),
    ('not', '🚫'),
    ('with', '✊'),
    ('or', '💔'),
    ('if', '❓'),
    ('in', '⛵'),
    ('is', '🖇'),
    ('from', '✋'),
    ('and', '❤'),
    ('True', '👍'),
    ('False', '👎'),
    ('None', '⭕️'),
    ('=', '⬅️'),
    ('print', '👉'),
)


class StreamReader(codecs.StreamReader):
    def decode(self, entrada, erros='strict'): 
        utf_reader = codecs.getreader('utf8')
        saida = entrada
        for orig, trad in DICIONARIO:
            if trad in saida:
                saida = saida.replace(trad, orig)
        return unicode(saida), len(entrada)


def get_my_codec(name):
    if name == 'vamcode':
        return (codecs.utf_8_encode, None, StreamReader, None)

codecs.register(get_my_codec)