#!/usr/bin/env python3
"""Masque les commentaires SQL, HTML et Python en conservant lignes/colonnes.

Les autres langages restent inchangés : sans parseur adapté, leurs commentaires
sont des candidats à qualifier, pas des défauts confirmés.
"""
import io
import re
import sys
import tokenize
from html.parser import HTMLParser


def masquer(texte, extension):
    def blank(value):
        return ''.join('\n' if c == '\n' else ' ' for c in value)

    if extension in {'html', 'htm', 'py'}:
        lignes = texte.splitlines(keepends=True)
        offsets = [0]
        for ligne in lignes:
            offsets.append(offsets[-1] + len(ligne))
        spans = []
        if extension == 'py':
            try:
                for token in tokenize.generate_tokens(io.StringIO(texte).readline):
                    if token.type == tokenize.COMMENT:
                        debut = offsets[token.start[0] - 1] + token.start[1]
                        spans.append((debut, debut + len(token.string)))
            except (tokenize.TokenError, IndentationError, SyntaxError):
                return texte  # Source incomplète : ne rien masquer par supposition.
        else:
            class Comments(HTMLParser):
                def handle_comment(self, data):
                    line, column = self.getpos()
                    debut = offsets[line - 1] + column
                    spans.append((debut, debut + len(data) + 7))
            Comments(convert_charrefs=False).feed(texte)
        result = list(texte)
        for debut, fin in spans:
            result[debut:fin] = blank(texte[debut:fin])
        return ''.join(result)
    if extension not in {'sql', 'pks', 'pkb', 'prc', 'fnc', 'trg'}:
        return texte
    sortie = list(texte)
    i = 0
    quote = None
    dollar = None
    while i < len(texte):
        if dollar:
            if texte.startswith(dollar, i):
                i += len(dollar)
                dollar = None
            else:
                i += 1
            continue
        if quote:
            if texte[i] == quote:
                if texte[i:i + 2] == quote * 2:
                    i += 2
                    continue
                quote = None
            elif texte[i] == '\\':
                i += 2
                continue
            i += 1
            continue
        if texte[i] in ('"', "'", '`'):
            quote = texte[i]
            i += 1
            continue
        if texte[i] == '$':
            match = re.match(r'\$(?:[A-Za-z_][A-Za-z_0-9]*)?\$', texte[i:])
            if match:
                dollar = match[0]
                i += len(dollar)
                continue
        if texte.startswith('--', i):
            end = texte.find('\n', i)
            end = len(texte) if end < 0 else end
        elif texte.startswith('/*', i):
            end = i + 2
            depth = 1
            while end < len(texte) and depth:
                if texte.startswith('/*', end):
                    depth += 1
                    end += 2
                elif texte.startswith('*/', end):
                    depth -= 1
                    end += 2
                else:
                    end += 1
        else:
            i += 1
            continue
        for j in range(i, end):
            if texte[j] != '\n':
                sortie[j] = ' '
        i = end
    return ''.join(sortie)


if __name__ == '__main__':
    # Un fichier source à la fois ; aucun corpus complet gardé en mémoire.
    sys.stdout.write(masquer(sys.stdin.read(), sys.argv[1]))
