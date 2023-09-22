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

def print_value(value, padding = 43):
    name = f"{value.name} {fg}{value.symbol}{sr}".ljust(padding)
    print(f"{name}{fy}{value.value}{sr}")
def print_value2(value, padding = 30):
    name = f"{value.name}:".ljust(padding)
    print(f"{name}{fy}{value.value}{fg}{value.symbol}{sr}")
def print_value3(value, padding = 43):
    name = f"{value.name} {fg}{value.symbol}{sr}".ljust(padding)
    print(f"{name}{fy}{value.value}{sr} ({fg}{value.indexs}{sr} prime)")

def print_cli(p):
    title = f"\n{Primes.str('title')} {fy}{p.request.interval}{sr}:\n"
    match p.range.count:
        case 0: result = f"{er}No primes found"
        case 1: result = f"{ok}{fy}1{sr} prime found"
        case _: result = f"{ok}{fy}{p.range.count}{sr} primes found"
    result += f" among {fy}{p.request.count}{sr} "
    result += "natural numbers." if p.request.count > 1 else "natural number."
    time = f"\n{fb}{p.time.name}: {p.time.value} {p.time.symbol}{sr}"

    print(title)
    print(result)
    if p.range.count > 0:
        if p.range.count < 20:
            print(*p.range.list, "\n")
        else:
            print(*p.range.list[:10], end="")
            print(f" {fg}...{p.range.count - 20} more...{sr} ", end="")
            print(*p.range.list[-10:], "\n")
        print_value3(p.range.first)
        print_value3(p.range.last)
        print_value2(p.pcent)
        print_value(p.sum)
        print_value(p.mean)
        print_value(p.median)
        if p.range.count > 1:
            print_value(p.pstdev)
            print_value(p.pvariance)
            print_value(p.stdev)
            print_value(p.variance)
            print_value(p.q1)
            print_value(p.q3)
            print_value(p.qi)
    print(time)
    
def print_cli_errors(p):
    print("")
    for e in p.error:
        print(f"{er} {e}")

def help():
    return '\n'.join(['',
        "Calculating primes and other mysterious numbers in specified range.\n",
        f"Usage:\t{fy}primes x{sr}\tfor range {fg}{{1..𝑥}}{sr}",
        f"or\t{fy}primes x y{sr}\tfor range {fg}{{𝑥..𝑦}}{sr}\n",
        f"where x and y"
        + f" are positive natural numbers, 𝑥 ≥ 1, "
        + f"𝑦 ≥ 𝑥 and 𝑦 < {Primes.max}.",
    ])

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
        print(help())
        sys.exit(0)

if not p.error:
    print_cli(p)
    sys.exit(0)
else:
    print_cli_errors(p)
    sys.exit(1)