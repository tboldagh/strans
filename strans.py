#!/usr/bin/env python3
"""
Shell helper program to facilitate strings manipulation
@author Tomasz Bold AGH-UST, Krakow

"""
import sys
# possible transformations

def replace(args):
    """Replaces sub-strings (requires two arguments, string to be replaces and the replacement)
        If the substring is absent in an element does nothing
    """
    f,t = args.split()[1:]
    def _f(input):
       return [ i.replace(f, t) for i in input ]
    return _f

def rem(args):
    """Removes sub-string (requires one argument)
    """
    f=args.split()[1]
    def _f(input):
       return [ i.replace(f, '') for i in input ]
    return _f


def dquote(args):
    """ Wraps elements in double quotes
    """
    def _f(input):
       return [ '"'+i+'"' for i in input ]
    return _f

def squote(args):
    """ Single quote (identical to wrap ' ')
    """
    def _f(input):
       return [ "'"+i+"'" for i in input ]
    return _f

def app(args):
    """ Appends a string to the element
        If not argument is given a space is appended
    """
    s = ' '  if args.strip() == 'app' else args.split()[1]
    def _f(input):
       return [ i+s for i in input ]
    return _f

def prep(args):
    """ Prepends a string to the element
    """
    s = args.split()[1]
    def _f(input):
       return [ s+i for i in input ]
    return _f


def join(args):
    """ Concatenate elements using delimeter passed
        If no delimeter is passed the the space character is used
    """
    s = ' '  if args.strip() == 'join' else args.replace('split', '', 1).strip()
    def _f(input):
       return s.join(input)
    return _f

def nl(args):
    """"Joins with newline character"""
    return lambda input: "\n".join(input)

def cont(args):
    """Retains elements containing substring
    """
    s = args.split()[1]
    def _f(input):
       return [ i for i in input if s in i ]
    return _f

def ncont(args):
    """Filters out elements containing substring
    """
    s = args.split()[1]
    def _f(input):
       return [ i for i in input if s not in i ]
    return _f

def strip(args):
    """Drops white characters around the element
    """
    def _f(input):
       return [ strip(i) for i in input ]
    return _f

def pick(args):
    """Pick a filed in each element that is separated by a first arg and under given index
       pick . 3 will split the element using the . into fields and pick 3rd element (counting from 0 of course)
       If the last part can be more numbers separated by coma, in such case several fields are selected
    """
    def _f(args):
        sep = args.split()[1]
        fields = [ int(i) for i in args.split()[2].split(',') ]

        def _sel(l):
            return sep.join([ l[i] for i in fields ])

        def _f(input):            
            return [ _sel(s.split(sep)) for s in input ]
    return _f


def tr(args):
    """Translate (like the tr) set of characters by another set of characters
        E.g. to replace the 'tricky' characters by the '_' tr /-\. ____  
    """
    f,t = [ i.strip() for i in args.split()[1:]]
    assert len(f) == len(t), 'tr - arguments are not of equal length'
    def _repl(s):
        return [ c if c not in f else t[f.index(c)] for c in s ]
    def _f(input):
        return [ _repl(s) for s in input ]
    return _f

def split(args):
    """Splits string into a list of elements
        If not argument is given then the white characters are used
    """
    if args.strip() == 'split':
        return lambda input: input.split()
    return lambda input: input.split(args.split()[1])

def wrap(args):
    """The prep app operations combined but works on a concatenated list"""
    prefix,suffix = args.split()[1:]
    def _f(input):
       return prefix+input+suffix
    return _f

def repr(args):
    """Make python string representation of elements list """
    def _f(input):
       return str(input)
    return _f

# to extend ... define more functions of that sort


#package all functions in a dict keyed by function name
import types
possible = {}
for name, f in dict(locals()).items():
    if isinstance(f, types.FunctionType) and f.__module__ == '__main__':
        possible[f.__name__] = f

possible_hint=' '.join(possible.keys())

# prepare transforms
todo = []


if '-h' in sys.argv:
    print('String manipulation program')
    print('example: echo a b c | strans "split | nocont a| prep *| join ,| wrap \ /"')
    print('will produce string: \*a,*b/')
    print('that is result of:')
    print('        splitting a b c into list of independent elements')
    print('        filter elements not containing a')
    print('        prepending each element by *')
    print('        concatenating with , delimeter')
    print('        and prepending with \' and appending / at the end')
    print('for every transformation there is obviously more than one possibility to implement it')
    print('\nList of all operations:')

    for name, op in possible.items():
        print(name)
        print(op.__doc__)
else:    
    tr = ' '.join(sys.argv[1:]).split('|')

    for t in tr:
        st = t.split()
        if st[0] not in possible:        
            print(f"ERROR, transformation {t} is not available, did you mean: {possible_hint}")
            break
        todo.append( possible.get(st[0])(t) )
    else:

        input = sys.stdin.read().strip()
        for op in todo:
            input = op(input)
        print(input)