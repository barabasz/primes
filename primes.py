import math, time, statistics as stat

class Param:
    def __init__(self, value, name, symbol):
        self.value = value
        self.symbol = symbol
        self.name = name
        self.info = f"{self.name}: {self.symbol} = {self.value}"

class Prime(Param):
    def __init__(self, value, name, symbol, index):
        super().__init__(value, name, symbol)
        self.index = int(index)
        self.sufix = self.sfx(self.index)
        self.indexs = f"{self.index}{self.sufix}"
        self.info = f"{self.name}: {self.symbol} = {self.value} ({self.indexs} prime)"
    def sfx(self, n: int):
        return "%s"%({1:"st",2:"nd",3:"rd"}.get(n%100 if (n%100)<20 else n%10,"th"))

class Timer(Param):
    def __init__(self):
        super().__init__(0, Primes.str("etime"), "ms")
        self.start = time.time()
    def stop(self):
        self.stop = time.time()
        self.value = round((self.stop - self.start) * 10**3, 4)
        self.info = f"{self.name}: {self.value} {self.symbol}"

class Primes:
    """
    Calculating primes, their statistics and other related numbers in specified range.
    Usage:  primes x        for range {2..𝑥}
    or      primes x y      for range {𝑥..𝑦}
    where x and y are positive natural numbers, 𝑥 ≥ 1, 𝑦 ≥ 𝑥 and 𝑦 < 10000000.
    """
    max = 10000000
    primes = []
    primes_all = []

    def __init__(self, first, last):
        self.first = first
        self.last = last
        if self.check():
            self.time = Timer()
            self.sieve()
            self.result()
        else:
            self.primes = None

    def check(self):
        self.error = []
        try:
            self.first = int(self.first)
        except ValueError:
            self.error.append(self.str('b_int'))
            return False
        try:
            self.last = int(self.last)
        except ValueError:
            self.error.append(self.str('e_int'))
            return False
        if self.first < 1: self.error.append(self.str('b_pos'))
        if self.last < 1: self.error.append(self.str('e_pos'))
        if self.first > self.last: self.error .append(self.str('e_gtb'))
        if self.last > self.max: self.error.append(self.str('e_max'))
        return False if self.error else True
        
    def sieve(self):
        sieve_array = dict((i, True) for i in range(2, self.last + 1))
        for i in range(2, math.isqrt(self.last) + 1):
            if sieve_array[i] == False: continue
            for j in range(i * 2, self.last + 1, i):
                sieve_array[j] = False
        for i in sieve_array:
            if sieve_array[i] == True:
                self.primes_all.append(i)
                if i < self.first: continue
                self.primes.append(i)
        del sieve_array
    
    def pindex(self, p: int):
        return self.primes_all.index(p) + 1
    
    def result(self):
        first = self.primes[0]
        last  = self.primes[-1]
        self.primes_count = len(self.primes)
        match self.primes_count:
            case 0: self.primes_result = f"No primes"
            case 1: self.primes_result = f"1 prime"
            case _: self.primes_result = f"{self.primes_count} primes"
        half = int(self.primes_count // 2)
        self.range = f"{{{first}..{last}}}"
        self.title = f"\n{self.str('title')} {self.range}:\n"
        self.first = Prime(first, self.str("frstp"), "min(𝑥)", self.pindex(first))
        self.last = Prime(last, self.str("lastp"), "max(𝑥)", self.pindex(last))
        self.sum = Param(sum(self.primes), self.str("sumpr"), "Σ𝑥")
        self.median = Param(stat.median(self.primes), self.str("mdnpr"), "𝑀𝑒")
        self.mean = Param(stat.mean(self.primes), self.str("amean"), "x̄")
        self.pstdev = Param(stat.pstdev(self.primes), self.str("pstdv"), "σ𝑥")
        self.pvariance = Param(stat.pvariance(self.primes), self.str("pvari"), "σ²𝑥")
        if self.primes_count > 1:
            self.stdev = Param(stat.stdev(self.primes), self.str("stdev"), "s𝑥")
            self.variance = Param(stat.variance(self.primes), self.str("svari"), "s²𝑥")
            self.q1 = Param(stat.median(self.primes[:half]), self.str("lquar"), "Q1")
            self.q3 = Param(stat.median(self.primes[-half:]), self.str("uquar"), "Q3")
            self.qi = Param(self.q3.value - self.q1.value, self.str("irang"), "Qi")
        self.time.stop()

    @staticmethod
    def str(code):
        match code:
            case "title": return "Primes, their statistics and other related numbers in range"
            case "b_int": return "Beginning of range must be an integer"
            case "b_pos": return "Beginning of range must be a positive natural number"
            case "e_int": return "End of range must be an integer"
            case "e_gt2": return "End of range must be greater than or equal to 2"
            case "e_gtb": return "End of the range must be greater than its beginning"
            case "e_pos": return "End of range must be a positive natural number"
            case "e_max": return f"End of range must be less than {Primes.max}"
            case "argsm": return "Too many arguments"
            case "etime": return "Execution time"
            case "stdev": return "Sample standard deviation"
            case "notap": return "Not applicable"
            case "frstp": return "Lowest prime"
            case "lastp": return "Highest prime"
            case "sumpr": return "Sum of primes"
            case "mdnpr": return "Median (middle value)"
            case "amean": return "Arithmetic mean"
            case "pstdv": return "Population standard deviation"
            case "pvari": return "Population variance"
            case "stdev": return "Sample standard deviation"
            case "svari": return "Sample variance"
            case "lquar": return "Lower Quartile"
            case "uquar": return "Upper Quartile"
            case "irang": return "Interquartile Range"

    @staticmethod
    def help():
        return '\n'.join(['',
            "Calculating primes and other mysterious numbers in specified range.\n",
            f"Usage:\tprimes x\tfor range {{2..𝑥}}",
            f"or\tprimes x y\tfor range {{𝑥..𝑦}}\n",
            f"where x and y"
            + f" are positive natural numbers, 𝑥 ≥ 1, "
            + f"𝑦 ≥ 𝑥 and 𝑦 < {Primes.max}.",
        ])