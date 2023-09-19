import sys
from colored import Fore, Back, Style
from primes import Primes

fb = Fore.blue
fy = Fore.yellow
fg = Fore.green
fr = Fore.red
sb = Style.bold
sr = Style.reset
ok = f"{fg}✔{sr} "
er = f"{fr}✖{sr} "

def print_cli(p):
    title = f"\n{Primes.str('title')} {fy}{p.range}{sr}:\n"
    match p.primes_count:
        case 0: result = f"{er}No primes."
        case 1: result = f"{ok}{fy}1{sr} prime:"
        case _: result = f"{ok}{fy}{p.primes_count}{sr} primes:"
    time = f"\n{fb}{p.time.name}: {p.time.value} {p.time.symbol}{sr}"

    print(title)
    print(result)
    if p.primes_count > 0: print(*p.primes, "\n")
    print(p.first.info)
    print(p.last.info)
    print(p.sum.info)
    print(p.mean.info)
    print(p.median.info)
    print(p.pstdev.info)
    print(p.pvariance.info)
    if p.primes_count > 1:
        print(p.stdev.info)
        print(p.variance.info)
        print(p.q1.info)
        print(p.q3.info)
        print(p.qi.info)
    print(time)
    
def print_cli_errors(p):
    print("")
    for e in p.error:
        print(e)

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
        print(Primes.help())
        sys.exit(0)

if not p.error:
    print_cli(p)
    sys.exit(0)
else:
    print_cli_errors(p)
    sys.exit(1)