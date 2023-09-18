import math
from timeit import default_timer as timer
from colored import Fore, Back, Style

class Primes:
    ok = f"{Fore.green}✔{Style.reset} "
    er = f"{Fore.red}✖{Style.reset} "
    max = 10000000

    def __init__(self, first, last):
        self.first = first
        self.last = last
        if self.check():
            self.start = timer()
            self.primes = []
            self.sieve()
            self.time = round(timer() - self.start, 4)
            self.count = len(self.primes)
            self.result()
        else:
            self.primes = None

    def check(self):
        self.error = []
        try:
            self.first = int(self.first)
        except ValueError:
            self.error.append(self.help('b_int'))
            return False
        try:
            self.last = int(self.last)
        except ValueError:
            self.error.append(self.help('e_int'))
            return False
        if self.first < 1: self.error.append(self.help('b_pos'))
        if self.last < 1: self.error.append(self.help('e_pos'))
        if self.first > self.last: self.error .append(self.help('e_gtb'))
        if self.last > self.max: self.error.append(self.help('e_max'))
        return False if self.error else True
        
    def sieve(self):
        sieve_array = dict((i, True) for i in range(2, self.last + 1))
        for i in range(2, math.isqrt(self.last) + 1):
            if sieve_array[i] == False: continue
            for j in range(i * 2, self.last + 1, i):
                sieve_array[j] = False
        for i in sieve_array:
            if i < self.first: continue
            if sieve_array[i] == True:
                self.primes.append(i)
        del sieve_array
    
    def result(self):
        self.range = f"{Fore.yellow}{{{self.first}..{self.last}}}{Style.reset}"
        self.title = f"\n{self.help('title')}{self.range}:\n"
        self.exec_time = f"\n{Fore.blue}{self.help('etime')}{self.time}{Style.reset}"
        match self.count:
            case 0: self.header_primes = f"{self.er}No primes."
            case 1: self.header_primes = f"{self.ok}{Fore.yellow}1{Style.reset} prime:"
            case _: self.header_primes = f"{self.ok}{Fore.yellow}{self.count}{Style.reset} primes:"
        self.primes_low = f"Lowest prime: {Fore.yellow}{self.primes[0]}{Style.reset}"
        self.primes_low_pos = "1st"
        self.primes_low += f" ({Fore.yellow}{self.primes_low_pos}{Style.reset} prime)"
        self.primes_high_pos = "16th"
        self.primes_high = f"Highest prime: {Fore.yellow}{self.primes[-1]}{Style.reset}"
        self.primes_high += f" ({Fore.yellow}{self.primes_high_pos}{Style.reset} prime)"

    def print_cli(self):
        print(self.title)
        print(self.header_primes)
        if self.count > 0: print(*self.primes, "\n")
        print(self.primes_low)
        print(self.primes_high)
        print(self.exec_time)

    def print_cli_errors(self):
        print("")
        for e in self.error:
            print(f"{self.er}{e}")

    @staticmethod
    def help(type):
        match type:
            case "usage": return '\n'.join(['',
                "Calculating primes and other mysterious numbers in specified range.\n",
                f"{Fore.green}Usage{Style.reset}:\t{Fore.yellow}primes x{Style.reset}\tfor range {{2..x}}",
                f"or\t{Fore.yellow}primes x y{Style.reset}\tfor range {Fore.yellow}{{x..y}}{Style.reset}\n",
                f"where {Fore.yellow}x{Style.reset} and {Fore.yellow}y{Style.reset}"
                + f" are positive natural numbers, {Fore.yellow}x ≥ 1{Style.reset}, "
                + f"{Fore.yellow}y ≥ x{Style.reset} and {Fore.yellow}y < {Primes.max}{Style.reset}.",
                ])
            case "b_int": return "Beginning of range must be an integer"
            case "b_pos": return "Beginning of range must be a positive natural number"
            case "e_int": return "End of range must be an integer"
            case "e_gt2": return "End of range must be greater than or equal to 2"
            case "e_gtb": return "End of the range must be greater than its beginning"
            case "e_pos": return "End of range must be a positive natural number"
            case "e_max": return f"End of range must be less than {Primes.max}"
            case "argsm": return "Too many arguments"
            case "etime": return "Execution time: "
            case "title": return "Calculating primes and mysterious numbers in range "