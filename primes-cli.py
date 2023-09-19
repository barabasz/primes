import sys
from colored import Fore, Back, Style
from primes import Primes

fy = Fore.yellow
fg = Fore.green
fr = Fore.red
sr = Style.reset
ok = f"{fg}✔{sr} "
er = f"{fr}✖{sr} "


# self.range = f"{Fore.yellow}{{{self.first}..{self.last}}}{Style.reset}"
# self.title = f"\n{self.help('title')}{self.range}:\n"
# self.exec_time = f"\n{Fore.blue}{self.help('etime')}{self.time}{Style.reset}"

# match self.primes_count:
#     case 0: self.header_primes = f"{self.er}No primes."
#     case 1: self.header_primes = f"{self.ok}1 prime:"
#     case _: self.header_primes = f"{self.ok}{self.primes_count} primes:"

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
    p.print_cli()
    sys.exit(0)
else:
    p.print_cli_errors()
    sys.exit(1)
