import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'NUMBER',
    'IDENT'
]

literals = ['=','+','-','*','/', '(',')',';','<','>','{','}',',','[',']']

reserved = {
    'int' : 'INT',
    'main': 'MAIN',
    'return': 'RETURN'
}

tokens = tokens+list(reserved.values())

def t_ident_token(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

print(tokens)
# A regular expression rule with some action code
def t_NUMBER(t):
    r'(0[xX][0-9a-fA-F]+)|(0[0-7]+)|(\d+)'
    n = t.value
    if len(n)==1:
        t.value = int(n)
    elif len(n)>1:
        if n[0]=='0' and n[1] not in ['x', 'X']:
            t.value = int(n,8)
        elif n[0]=='0' and n[1] in ['x', 'X']:
            t.value = int(n,16)
        else:
            t.value = int(n)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r'

def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(\/\/.*)'
    t.lexer.lineno += t.value.count('\n')
    pass
    # No return value. Token discarded

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

data = '''
0x124+{}/<
0X43
234
033
A
int main
'''

lexer.input(data)
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)