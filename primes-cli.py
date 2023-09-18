import sys
from primes import Primes

p = None
args = len(sys.argv)

match args:
    case _ if args > 3:
        error = "Too many arguments"
    case 3:
        p = Primes(sys.argv[1], sys.argv[2])
    case 2:
        p = Primes(2, sys.argv[1])
    case _:
        error = "At least one argument expected"

if p!= None:
    if not p.error:
        p.print_cli()
    else:
        print(p.error)
else:
    print(error)