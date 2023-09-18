import sys
from primes import Primes

args = len(sys.argv)

match args:
    case _ if args > 3:
        print("\n" + Primes.er + Primes.help("argsm"))
        sys.exit(2)
    case 3:
        p = Primes(sys.argv[1], sys.argv[2])
    case 2:
        p = Primes(1, sys.argv[1])
    case _:
        print(Primes.help("usage"))
        sys.exit(0)

if not p.error:
    p.print_cli()
    sys.exit(0)
else:
    p.print_cli_errors()
    sys.exit(1)