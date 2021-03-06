import sys
import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required
tokens = [
    'number',
    'ident'
]

literals = ['=','+','-','*','/', '(',')',';','<','>','{','}',',','[',']']

reserved = {
    'int' : 'int',
    'main': 'main',
    'return': 'return'
}

tokens = tokens+list(reserved.values())
# print(tokens)

def t_ident_token(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ident')
    return t

# A regular expression rule with some action code
def t_number(t):
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

def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(\/\/.*)'
    t.lexer.lineno += t.value.count('\n')
    pass
    # No return value. Token discarded

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_expression(p):
    '''
    expression :  int main '(' ')' '{' return number ';' '}'
    '''
    out = \
"""define dso_local i32 @main(){{
    ret i32 {} 
}}""".format(p[7])
    p[0] = out

# Error rule for syntax errors
def p_error(p):
    # print("Syntax error in input!")
    exit(-1)

if __name__ == '__main__':

    input_file_addr = sys.argv[1]
    ir_file_addr = sys.argv[2]

    input = ""
    ir = ""

    with open(input_file_addr,'r', encoding='utf-8') as fin:
        input = fin.read()


    # Build the lexer
    lexer = lex.lex()

    data = '''
    int main(){
        return 033 ;
    }
    '''

    lexer.input(input)
    # while True:
    #     tok = lexer.token()
    #     if not tok: 
    #         break      # No more input
    #     print(tok)

    parser = yacc.yacc()

    res = parser.parse(input)
    # if res == None:
    #     exit(-1)
    print(res)

    ir = res
    with open(ir_file_addr,'w',encoding='utf-8') as fout:
        fout.write(ir)