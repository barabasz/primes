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
        return "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n%100 if (n%100)<20 else n%10,"th"))

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
            self.time_start = time.time()
            self.sieve()
            self.time_stop = time.time()
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
        self.range = f"{{{self.first}..{self.last}}}"
        self.title = f"\n{self.str('title')} {self.range}:\n"
       
        self.time_symbol = "ms"
        self.time_value = round((self.time_stop - self.time_start) * 10**3, 4)
        self.time_name = self.str("etime")
        self.time_info = f"{self.time_name}: {self.time_value} {self.time_symbol}"
        
        self.first = Prime(first, self.str("frstp"), "min(𝑥)", self.pindex(first))
        self.last = Prime(last, self.str("lastp"), "max(𝑥)", self.pindex(last))
        self.sum = Param(sum(self.primes), self.str("sumpr"), "Σ𝑥")
        self.median = Param(stat.median(self.primes), self.str("mdnpr"), "𝑀𝑒")
        self.mean = Param(stat.mean(self.primes), self.str("amean"), "x̄")
        

        self.primes_pstdev = stat.pstdev(self.primes)
        self.primes_pvariance = stat.pvariance(self.primes)
        if self.primes_count > 1:
            self.primes_stdev = stat.stdev(self.primes)
            self.primes_variance = stat.variance(self.primes)
            self.primes_half_list = int(self.primes_count // 2)
            self.primes_q1 = stat.median(self.primes[:self.primes_half_list]) 
            self.primes_q3_name = "Upper Quartile"
            self.primes_q3 = stat.median(self.primes[-self.primes_half_list:])
            self.qi_symbol = "Qi"
            self.qi_value = self.primes_q3 - self.primes_q1
            self.qi_name = "Interquartile Range"
        
    def print_cli(self):
        match self.primes_count:
            case 0: self.header_primes = f"No primes."
            case 1: self.header_primes = f"1 prime:"
            case _: self.header_primes = f"{self.primes_count} primes:"
        self.primes_pstdev_info = f"Popul. std deviation:\tσ𝑥 = {self.primes_pstdev}"
        self.primes_pvariance_info = f"Popul. variance:\tσ²𝑥 = {self.primes_pvariance}"
        if self.primes_count > 1:
            self.primes_stdev_info = f"Sample std deviation:\ts𝑥 = {self.primes_stdev}"
            self.primes_variance_info = f"Sample variance:\ts²𝑥 = {self.primes_variance}"
            self.primes_q1_info = f"Lower Quartile:\tQ1 = {self.primes_q1}"
            self.primes_q3_info = f"Upper Quartile:\tQ3 = {self.primes_q3}"
            primes_qi_info = f"{self.qi_name}:\t{self.qi_symbol} = {self.qi_value}"
        
        print(self.title)
        print(self.header_primes)
        if self.primes_count > 0: print(*self.primes, "\n")
        print(self.first.info)
        print(self.last.info)
        print(self.sum.info)
        print(self.mean.info)
        print(self.median.info)
        print(self.primes_pstdev_info)
        print(self.primes_pvariance_info)
        if self.primes_count > 1:
            print(self.primes_stdev_info)
            print(self.primes_variance_info)
            print("q1", self.primes_q1)
            print("q3", self.primes_q3)
            print(primes_qi_info)
        print(self.time_info)
        
    def print_cli_errors(self):
        print("")
        for e in self.error:
            print(e)

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