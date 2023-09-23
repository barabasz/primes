import math, time, statistics as stat

class Param:
    def __init__(self, value, name, symbol):
        self.value = value
        self.symbol = symbol
        self.name = name
        self.info = f"{self.name}: {self.symbol} = {self.value}"

class ParamGaps(Param):
    def __init__(self, value, list, name, symbol):
        super().__init__(value, name, symbol)
        self.list = list
        self.count = len(list)
        self.count_text = "1 time" if self.count == 1 else f"{self.count} times"
        self.first = f"{{{list[0][0]}, {list[0][1]}}}"
        self.last = f"{{{list[-1][0]}, {list[-1][1]}}}"
        self.more = self.count - 2 if self.count > 3 else False

class Prime(Param):
    def __init__(self, value, name, symbol, index):
        super().__init__(value, name, symbol)
        self.index = index
        self.sufix = self.sfx(index)
        self.indexs = f"{index}{self.sufix}"
        self.info = f"{self.name}: {self.symbol} = {self.value} ({self.indexs} prime)"
    def sfx(self, n: int):
        return "%s"%({1:"ˢᵗ",2:"ⁿᵈ",3:"ʳᵈ"}.get(n%100 if (n%100)<20 else n%10,"ᵗʰ"))

class Timer(Param):
    def __init__(self):
        super().__init__(0, Primes.str("etime"), "ms")
        self.start = time.time()
    def sieve(self):
        self.sieve_name = Primes.str("stime")
        self.sieve = time.time()
        self.sieve = round((self.sieve - self.start) * 10**3, 4)
        self.info = f"{Primes.str('stime')}: {self.sieve} {self.symbol}"
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
            case 0: self.result = Primes.str("r_npf")
            case 1: self.result = Primes.str("r_1pf")
            case _: self.result = f"{self.count} {Primes.str('r_psf')}"
        self.half = int(self.count // 2)

class Request:
    def __init__(self, start, stop) -> None:
        self.first = int(start)
        self.last = int(stop)
        self.count = self.last - self.first + 1
        self.interval = f"{{{self.first}..{self.last}}}"
        self.title = f"\n{Primes.str('title')} {self.interval}:\n"

class Gaps:
    def __init__(self, list: list) -> None:
        gaps, gaps_list = {}, []
        for i in range(len(list) - 1):
            gap = list[i+1] - list[i]
            try:
                gaps[gap] += 1
            except KeyError:
                gaps[gap] = 1
            gaps_list.append((list[i], list[i+1], gap))
        gaps_list.append((list[-1], None, None))
        max_value = max(gaps)
        max_list = tuple((i[0], i[1]) for i in gaps_list if i[2] == max_value)
        min_value = min(gaps)
        min_list = tuple((i[0], i[1]) for i in gaps_list if i[2] == min_value)
        com_count = max(gaps.values())
        com_value = next((i for i in gaps if gaps[i] == com_count))
        com_list = tuple((i[0], i[1]) for i in gaps_list if i[2] == com_value)
        self.list = gaps
        self.max = ParamGaps(max_value, max_list, Primes.str("g_max"), "∆ₘₐₓ")
        self.min = ParamGaps(min_value, min_list, Primes.str("g_min"), "∆ₘᵢₙ")
        self.com = ParamGaps(com_value, com_list, Primes.str("g_com"), "∆ᶠ")

class Primes:
    """
    Calculating primes, their statistics and other related numbers in specified range.
    Usage:  primes x        for range {1..𝑥}
    or      primes x y      for range {𝑥..𝑦}
    where x and y are positive natural numbers, 𝑥 ≥ 1, 𝑦 ≥ 𝑥 and 𝑦 < 10000000.
    """
    max = 10000000
    
    def __init__(self, first, last):
        self.error = []
        if self.check(first, last):
            self.time = Timer()
            self.sieve()
            self.time.sieve()
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
        n = self.request.last
        sieve_array = [True for i in range(2, n + 1)]
                           
        for i in range(2, math.isqrt(n) + 1):
            if sieve_array[i] == True:
                for j in range(i * 2, n - 1, i):
                    sieve_array[j] = False
        primes_all = tuple(k for k, v in enumerate(sieve_array) if v == True and k >= 2)
        primes_range = tuple(i for i in primes_all if i >= self.request.first)
        del sieve_array
        
        self.all = All(primes_all)
        if len(primes_all) > 0:
            first_index = primes_all.index(primes_range[0]) + 1
            self.range = Range(primes_range, first_index, self.all.count)
        else:
            self.range = Range(primes_range, 0, self.all.count)

    def result(self):
        self.pcent = Param(round(self.range.count / self.request.count * 100, 2), self.str("pcent"), "%")
        self.sum = Param(sum(self.range.list), self.str("sumpr"), "Σ𝑥")
        self.median = Param(stat.median(self.range.list), self.str("mdnpr"), "𝑀𝑒")
        self.mean = Param(stat.mean(self.range.list), self.str("amean"), "μ")
        self.gaps = Gaps(self.range.list)
        self.pstdev = Param(stat.pstdev(self.range.list), self.str("pstdv"), "σ𝑥")
        self.pvariance = Param(stat.pvariance(self.range.list), self.str("pvari"), "σ²𝑥")
        if self.range.count > 1:
            self.stdev = Param(stat.stdev(self.range.list), self.str("stdev"), "s𝑥")
            self.variance = Param(stat.variance(self.range.list), self.str("svari"), "s²𝑥")
            self.q1 = Param(stat.median(self.range.list[:self.range.half]), self.str("lquar"), "Q₁")
            self.q3 = Param(stat.median(self.range.list[-self.range.half:]), self.str("uquar"), "Q₃")
            self.qi = Param(self.q3.value - self.q1.value, self.str("irang"), "Qᵢ")

    @staticmethod
    def str(code):
        match code:
            case "amean": return "Arithmetic mean"
            case "argsm": return "Too many arguments"
            case "b_int": return "Beginning of range must be an integer"
            case "b_pos": return "Beginning of range must be a positive natural number"
            case "e_gt2": return "End of range must be greater than or equal to 2"
            case "e_gtb": return "End of the range must be greater than its beginning"
            case "e_int": return "End of range must be an integer"
            case "e_max": return f"End of range must be less than {Primes.max}"
            case "e_pos": return "End of range must be a positive natural number"
            case "etime": return "Total time"
            case "frstp": return "First prime"
            case "g_com": return "Most common gap"
            case "g_max": return "Longest gap"
            case "g_min": return "Shortest gap"
            case "g_oth": return "Other gaps"
            case "highp": return "Highest prime"
            case "irang": return "Interquartile Range"
            case "lastp": return "Last prime"
            case "lquar": return "Lower Quartile"
            case "lwstp": return "Lowest prime"
            case "mdnpr": return "Median (middle value)"
            case "notap": return "Not applicable"
            case "pcent": return "Percentage of primes"
            case "pstdv": return "Pop. standard deviation"
            case "pvari": return "Pop. variance"
            case "r_1pf": return "1 prime found"
            case "r_npf": return "No primes found"
            case "r_psf": return "primes found"
            case "stdev": return "Sample standard deviation"
            case "stdev": return "Sample standard deviation"
            case "stime": return "Sieve time"
            case "sumpr": return "Sum of primes"
            case "svari": return "Sample variance"
            case "title": return "Primes, their statistics and other related numbers in range"
            case "uquar": return "Upper Quartile"