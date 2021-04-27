# Commands

    command                description                                example

    int <name> <value>     declare integer type variable              int height 5
    chr <name> <value>     declare character type variable            chr esclamation !
    put <var/chr>          put on screen the value specified          put height OR put 'A'
    get <var>              get ascii value on var                     get letter
    loop <condition>       like a while                               loop run OR loop i<10; # NO SPACES ALLOWED IN CONDITION
    pool                   end of looped code block                   pool
    tape <name> <len>      declare int list                           tape prime_numbers 10
    set <name> <value>     update an existing variable                set height 4  OR  set prime_numbers[3] 5 
    pp <name>              increases by 1 value                       pp i
    mm <name>              decreases by 1 value                       mm countdown


# Consts

Since spaces are used to separate arguments, and this language is so good that is not parsed in any way, to print a space, you have a builtin constant
named "_s" to use like this

    put _s

you also have these constants builtin:

    "True" and "False" that corresponds to 1 and 0
    "__version" is the compiler version


you can declare constants like this:
    const <name>: <value>
they are evaluated before transpilation.
They can be declared at any point of the code, the position doesn't matter

# Functions

you can declare a line-function like this
       
       func name: <code>

line functions don't take arguments
example

PROGRAM:

        func foo: put 'f'; put 'o'; put 'o'
        foo

OUTPUT:
    foo

I'm currently working on more complete functions with arguments


# Comments

everything after a ; or a newline that doesn't start with a command key, is considered a comment.
you can use # to use keys in comments

example

    put 'A'  # this will put the letter "A" to the screen</br>

OUTPTUT: A

# file extensions
this is just a convention

name.cmm   -   source file</br>
name.lh    -   library/header</br>
name.ccm   -   custom commands chart </br> 


