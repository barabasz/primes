import math, time, statistics as stat

class Param:
    def __init__(self, value, name, symbol):
        self.value = value
        self.symbol = symbol
        self.name = name
        self.info = f"{self.name}: {self.symbol} = {self.value}"

class Param2(Param):
    def __init__(self, value, name, symbol):
        super().__init__(value, name, symbol)
        self.info = f"{self.name}: {self.value}{self.symbol}"

class Prime(Param):
    def __init__(self, value, name, symbol, index):
        super().__init__(value, name, symbol)
        self.index = index
        self.sufix = self.sfx(index)
        self.indexs = f"{index}{self.sufix}"
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

class All:
    def __init__(self, list: list) -> None:
        self.list = list
        self.count = len(self.list)
        if self.count > 0:
            self.first = Prime(self.list[0], Primes.str("frstp"), "First", 1)
            self.last = Prime(self.list[-1], Primes.str("lastp"), "Last", self.count)
            self.interval = f"{{{self.first.value}..{self.last.value}}}"

class Range(All):
    def __init__(self, list: list, index_first, index_last) -> None:
        self.list = list
        self.count = len(self.list)
        if self.count > 0:
            self.first = Prime(self.list[0], Primes.str("lwstp"), "min(𝑥)", index_first)
            self.last = Prime(self.list[-1], Primes.str("highp"), "max(𝑥)", index_last)
            self.interval = f"{{{self.first.value}..{self.last.value}}}"
        match self.count:
            case 0: self.result = f"No primes found"
            case 1: self.result = f"1 prime found"
            case _: self.result = f"{self.count} primes found"
        self.half = int(self.count // 2)
            
class Request:
    def __init__(self, start, stop) -> None:
        self.first = int(start)
        self.last = int(stop)
        self.count = self.last - self.first + 1
        self.interval = f"{{{self.first}..{self.last}}}"
        self.title = f"\n{Primes.str('title')} {self.interval}:\n"

class Primes:
    """
    Calculating primes, their statistics and other related numbers in specified range.
    Usage:  primes x        for range {2..𝑥}
    or      primes x y      for range {𝑥..𝑦}
    where x and y are positive natural numbers, 𝑥 ≥ 1, 𝑦 ≥ 𝑥 and 𝑦 < 10000000.
    """
    max = 10000000
    
    def __init__(self, first, last):
        self.error = []
        if self.check(first, last):
            self.time = Timer()
            self.sieve()
            if self.range.count > 0:
                self.result()
            self.time.stop()

    def check(self, first, last):
        try:
            first = int(first)
        except ValueError:
            self.error.append(self.str('b_int'))
            return False
        try:
            last = int(last)
        except ValueError:
            self.error.append(self.str('e_int'))
            return False
        if first < 1: self.error.append(self.str('b_pos'))
        if last < 1: self.error.append(self.str('e_pos'))
        if first > last: self.error .append(self.str('e_gtb'))
        if last > self.max: self.error.append(self.str('e_max'))
        if not self.error:
            self.request = Request(first, last)
            return True
        else:
            return False
        
    def sieve(self):
        primes_all = []
        primes_range = []
        sieve_array = dict((i, True) for i in range(2, self.request.last + 1))
        for i in range(2, math.isqrt(self.request.last) + 1):
            if sieve_array[i] == False: continue
            for j in range(i * 2, self.request.last + 1, i):
                sieve_array[j] = False
        for i in sieve_array:
            if sieve_array[i] == True:
                primes_all.append(i)
                if i < self.request.first: continue
                primes_range.append(i)
        self.all = All(primes_all)
        if len(primes_range) > 0:
            first_index = primes_all.index(primes_range[0]) + 1
            self.range = Range(primes_range, first_index, self.all.count)
        else:
            self.range = Range(primes_range, 0, self.all.count)
        del sieve_array
    
    def result(self):
        self.pcent = Param2(round(self.range.count / self.request.count * 100, 2), self.str("pcent"), "%")
        self.sum = Param(sum(self.range.list), self.str("sumpr"), "Σ𝑥")
        self.median = Param(stat.median(self.range.list), self.str("mdnpr"), "𝑀𝑒")
        self.mean = Param(stat.mean(self.range.list), self.str("amean"), "x")
        self.pstdev = Param(stat.pstdev(self.range.list), self.str("pstdv"), "σ𝑥")
        self.pvariance = Param(stat.pvariance(self.range.list), self.str("pvari"), "σ²𝑥")
        if self.range.count > 1:
            self.stdev = Param(stat.stdev(self.range.list), self.str("stdev"), "s𝑥")
            self.variance = Param(stat.variance(self.range.list), self.str("svari"), "s²𝑥")
            self.q1 = Param(stat.median(self.range.list[:self.range.half]), self.str("lquar"), "Q1")
            self.q3 = Param(stat.median(self.range.list[-self.range.half:]), self.str("uquar"), "Q3")
            self.qi = Param(self.q3.value - self.q1.value, self.str("irang"), "Qi")
        
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
            case "frstp": return "First prime"
            case "lwstp": return "Lowest prime"
            case "lastp": return "Last prime"
            case "highp": return "Highest prime"
            case "sumpr": return "Sum of primes"
            case "mdnpr": return "Median (middle value)"
            case "amean": return "Arithmetic mean"
            case "pstdv": return "Pop. standard deviation"
            case "pvari": return "Pop. variance"
            case "stdev": return "Sample standard deviation"
            case "svari": return "Sample variance"
            case "lquar": return "Lower Quartile"
            case "uquar": return "Upper Quartile"
            case "irang": return "Interquartile Range"
            case "pcent": return "Percentage of primes"