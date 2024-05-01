from prepare import *

Gramática=[
    ('S', ['·','expression']), 
    ('expression', ['expression', 'PLUS', 'term']), 
    ('expression', ['term']), 
    ('term', ['term', 'TIMES', 'factor']), 
    ('term', ['factor']), 
    ('factor', ['LPAREN', 'expression', 'RPAREN']), 
    ('factor', ['ID']), 
    ('factor', ['#'])
    ]

##prueba de cerradura 

I = [('S', ['·','expression'])]

I1 = [('S', ['·', 'expression']), 
('expression', ['·', 'expression', 'PLUS', 'term']), 
('expression', ['·', 'term']), 
('term', ['·', 'term', 'TIMES', 'factor']), 
('term', ['·', 'factor']), 
('factor', ['·', 'LPAREN', 'expression', 'RPAREN']), 
('factor', ['·', 'ID']), 
('factor', ['·', '#'])]

J = cerradura(I, Gramática)

print(J)

##prueba de mover

X = 'expression'

J1 = mover(I1, X, Gramática)

print(J1)

J2 = mover(I1, 'term', Gramática)

print(J2)

