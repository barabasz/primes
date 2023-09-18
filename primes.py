import math

class Primes:
    def __init__(self, start, end):
        self.first = start
        self.last = end
        if self.check():
            self.primes = []
            self.sieve()
            self.count = len(self.primes)
            self.result()
        else:
            self.primes = None

    def check(self):
        self.error = ""

        try:
            self.first = int(self.first)
        except ValueError:
            self.error += "Beginning of range must be an integer\n"
            return False
        try:
            self.last = int(self.last)
        except ValueError:
            self.error += "End of range must be an integer\n"
            return False
        
        if self.first < 1:
            self.error += "Beginning of range must be a positive natural number\n"
        if self.last < 1:
            self.error += "End of range must be a positive natural number\n"
        if self.first > self.last:
            self.error += "End of the range must be greater than its beginning\n"
        if self.last < 2:
            self.error += "End of range must be greater than or equal to 2\n"
        if self.last > 1000000:
            self.error += "End of range must be less than 1000000\n"
        
        if self.error != "":
            return False
        else:
            self.range = f"{{{self.first}..{self.last}}}"
            return True
        
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
        match self.count:
            case 0: self.title = f"No primes in range {self.range}."
            case 1: self.title = f"1 prime in range {self.range}."
            case _: self.title = f"{self.count} primes in range {self.range}:"

    def print_cli(self):
        from colored import Fore, Back, Style
        if self.count == 0:
            print(f"\n{Fore.red}✖{Style.reset} {self.title}\n")
        else:
            print(f"\n{Fore.green}✖{Style.reset} {self.title}\n")
        
        if self.count > 0:
            print(*self.primes)

