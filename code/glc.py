from sys import argv
import os

if len(argv) < 2:
    print("arguments:\nfile [flags]")
    print("flags:\n\t-c or --compile\t\tautomatically compyle using gcc\n\t--clean\t\t\tremove out.c\n\t-o <name>\t\tname of output file")
    
    exit(1)
    


try:
    with open(argv[1], 'r') as f:
        program = f.read()
except:
    print("no such file"); exit(1)

WDIR = os.path.dirname(os.path.abspath(argv[1]))+'/'

flags = []
for i in argv[1:]:
    if i[0] in ['-', '--']:
        flags.append(i.replace('-', ''))


def debug(txt, typ='info'):
    print(f'[{typ}] {txt}')
    0


debug('building references')

repls = {
    'int':   'int $0 = $1',
    'chr':   "char $0 = '$1'",
    'tape':  'int $0[$1] = {0}',
    'put':   'putchar($0)',
    'get':   '$0 = getchar()',
    'loop':  'while($0){',
    'pool':  '}',
    'set':   '$0 = $1',
    'pp': '$0++',
    'mm': '$0--'
}

# dict1.update(dict2)

RegNames = {
    '__version': '01',
    'True': '1',
    'False': '0',
    '_s': " "
}

funcs = {}

debug('gettin\' custom commands')

while 'custom' in program:
    for line in program.split('\n'):
        line = line.split('#')[0]
        comm = line.strip(' ')
        if comm.split(' ')[0] == 'custom':
            program = program.replace(line, '')
            try:
                mname = comm.replace(f'{comm.split(" ")[0]} ', '')
                with open(WDIR+mname, 'r') as f:
                    exec(f.read())
                repls.update(commands)
            except Exception as error:
                debug(f'unable to load custom commands from {mname}, aborting transpilation', 'fatal error')
                if 'v' in flags: debug(f'transpiler error:\n\t{error}', 'error info')
                else: debug('use -v option to check the transpiler error')
                exit(1)

debug('attaching headers')

while 'include' in program:
    libs = ''
    for line in program.split('\n'):
        line = line.split('#')[0]
        comm = line.strip(' ')
        if comm.split(' ')[0] == 'include':
            program = program.replace(line, '')
            file = comm.replace(f'{comm.split(" ")[0]} ', '')
            try:
                with open(WDIR+file, 'r') as f:
                    libs += '\n'+f.read()
            except:
                debug(f"{file}: file not found")

    program = libs + program


debug('reading constants')

NewProgrBuff = []
for line in program.split('\n'):
    line = line.split('#')[0]
    comm = line.strip(' ')

    #print(comm)
    if comm.split(' ')[0] == 'const':
        try:
            RegNames[comm.split(' ')[1].strip(':')] = comm.split(':')[1].strip(' ')
        except: debug(f'{comm}:  const statement not completed', 'error')
    else:
        NewProgrBuff.append(comm)

program = NewProgrBuff
#print(RegNames)

debug('reading functions')

NewProgrBuff = []
for line in program:
    comm = line.strip(' ')

    #print(comm)
    if comm.split(' ')[0] == 'func':
        try:
            funcs[comm.split(' ')[1].strip(':')] = comm.split(':')[1].strip(' ')
        except: debug(f'{comm}:  func statement not completed', 'error')
    else:
        NewProgrBuff.append(comm)

program = NewProgrBuff
#print(funcs)


nbuff = []
for line in program:
    a = line
    for name in funcs:
         a = a.replace(name, funcs[name])
    #print(f'{line}  ---> {a}')
    nbuff.append(a)
program=nbuff

nbuff=[]
for line in program:
    for i in line.split(';'): nbuff.append(i.strip(' '))
program=nbuff

#print('\n'.join(program));exit(0)

OUTPUT = '/*transpiled with CCCp*/\nint main(){\n'


debug('transpiling')

#print(program)
POG = 0
while POG < len(program):

    cian = program[POG]
    POG += 1
        
    key = cian.split(' ')[0]
    args = cian.replace(key, '').strip(' ').split(' ')
    if args == ['']: args = []

    #print(f'{cian}   {key} {args}')

    if not(key in repls):
        continue
    
    if len(args) != repls[key].count('$'):
        debug(f'line {POG}: {key} takes {repls[key].count("$")} arguments, but {len(args)} were given.', 'error')
    
    buildbuff = repls[key]+';'
    
    for i in range(repls[key].count('$')):
        if args != []: buildbuff = buildbuff.replace(f'${i}', args[i])

    
    OUTPUT+=buildbuff
    #print(buildbuff)
    
    if key in ['loop', 'loop']: OUTPUT = OUTPUT[:-1]
    
    OUTPUT += '\n'
    

OUTPUT += 'return 0;}'

#print(RegNames)
ficsout = ''
for i in OUTPUT.split('\n'):
    a = i
    for name in RegNames:
         a = a.replace(name, RegNames[name])
    #print(f'{i}  ---> {a}')
    ficsout += a+'\n'
        
OUTPUT = ficsout



debug('writing to out.c')

with open(WDIR+'out.c', 'w') as f:
    f.write(OUTPUT)

if 'c' in flags or 'compile' in flags:
    out = 'out'
    if 'o' in flags:
        out = argv[argv.index('-o')+1]
    
    debug(f'compiling to {out}')
    import os
    
    if 'v' in flags: os.system(f'gcc {WDIR}out.c -o {WDIR+out}')
    else:
        os.system(f'gcc {WDIR}out.c -o {WDIR+out} >.garbage 2>&1')
        os.system('rm .garbage')
    
    if 'clean' in flags:
        os.system(f'rm {WDIR}out.c')
    else:
        debug('to automatically remove out.c use --clean', 'note')
else:
    debug('to automatically compile use -c or --compile', 'note')

debug('done!')
