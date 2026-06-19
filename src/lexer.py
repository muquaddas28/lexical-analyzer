import re


class LexicalAnalyzer:
    TYPE_KEYWORDS = frozenset({
        'int', 'float', 'char', 'double', 'void', 'bool',
        'string', 'long', 'short', 'unsigned', 'signed', 'struct', 'const'
    })

    def __init__(self):
        kw = (r'int|float|char|double|if|else|while|for|return|void|break|'
              r'continue|switch|case|default|do|struct|bool|string|const|'
              r'long|short|unsigned|signed|NULL|true|false')
        self.token_rules = [
            ('COMMENT_ML',    r'/\*[\s\S]*?\*/'),
            ('COMMENT_SL',    r'//[^\n]*'),
            ('PREPROCESSOR',  r'#[^\n]*'),
            ('STRING',        r'"[^"\n]*"'),
            ('STRING_ERR',    r'"[^"\n]*'),
            ('CHAR_LITERAL',  r"'(?:\\.|[^'\\])'"),
            ('KEYWORD',       rf'\b(?:{kw})\b'),
            ('NUMBER',        r'\b0[xX][0-9a-fA-F]+\b|\b\d+(?:\.\d+)?\b'),
            ('IDENTIFIER',    r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('RELATIONAL_OP', r'==|!=|<=|>=|<|>'),
            ('LOGICAL_OP',    r'&&|\|\||!'),
            ('BITWISE_OP',    r'<<|>>|[&|^~]'),
            ('ASSIGN_OP',     r'='),
            ('ARITH_OP',      r'[+\-*/%]'),
            ('PUNCTUATION',   r'[;,(){}[\].:?]'),
            ('NEWLINE',       r'\n'),
            ('SKIP',          r'[ \t\r]+'),
            ('MISMATCH',      r'.'),
        ]
        self.master_regex = '|'.join(
            f'(?P<{name}>{pattern})' for name, pattern in self.token_rules
        ) #KEYWORD | NUMBER | IDENTIFIER | 

    def tokenize(self, source_code):
        tokens      = []
        errors      = []
        symbol_table = {} #Variables ki information store karne ke liye.
        line_num    = 1
        line_start  = 0 #calculte column no
        current_type = 'unknown' #Kyuki abhi tak koi datatype nahi mila.
        scope_depth  = 0

        for match in re.finditer(self.master_regex, source_code): #Returns matches one by one
            kind  = match.lastgroup #Token kis category ka hai.
            value = match.group(kind)
            col   = match.start() - line_start + 1 #Column number nikalne ke liye.

            if kind == 'NEWLINE':
                line_num  += 1
                line_start = match.end()

            elif kind in ('SKIP', 'COMMENT_SL', 'PREPROCESSOR'):
                pass

            elif kind == 'COMMENT_ML':
                nl = value.count('\n')
                if nl:
                    line_num  += nl
                    line_start = match.start() + value.rfind('\n') + 1

            elif kind == 'STRING_ERR':
                errors.append(
                    f"Line {line_num}, Col {col}: Lexical Error — "
                    f"unterminated string literal '{value}'"
                )

            elif kind == 'MISMATCH':
                errors.append(
                    f"Line {line_num}, Col {col}: Lexical Error — "
                    f"unknown token '{value}'"
                )

            else:
                tokens.append((kind, value, line_num, col))

                if value == '{':
                    scope_depth += 1
                elif value == '}':  #block ends 
                    scope_depth = max(0, scope_depth - 1)
                    current_type = 'unknown'

                if kind == 'KEYWORD' and value in self.TYPE_KEYWORDS:
                    current_type = value

                if kind == 'IDENTIFIER' and value not in symbol_table:
                    scope = 'Global' if scope_depth == 0 else f'Local (L{scope_depth})'
                    symbol_table[value] = {
                        'type':  current_type,
                        'scope': scope,
                        'line':  line_num,
                        'col':   col,
                    }

                if value == ';':
                    current_type = 'unknown'

        return tokens, symbol_table, errors
