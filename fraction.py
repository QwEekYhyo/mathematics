class Fraction:
    def __init__(self,num,den = 1):
        self.numerator = num
        self.denominator = den
        if self.numerator < 0 and self.denominator < 0:
            self.numerator = abs(self.numerator)
            self.denominator = abs(self.denominator)

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"

    def _to_int(self):
        if isinstance(self.numerator,float) and self.numerator.is_integer():
            self.numerator = int(self.numerator)
        if isinstance(self.denominator,float) and self.denominator.is_integer():
            self.denominator = int(self.denominator)
                    
    def num_to_int(self):
        while not self.numerator.is_integer():
            self.numerator *= 10
            self.denominator *= 10
        self._to_int()

    def simplify(self):
        x = pgdc(self.numerator,self.denominator) 
        self.numerator /= x
        self.denominator /= x
        self._to_int()        

    def simplified(self):
        output = Fraction(self.numerator,self.denominator)
        if isinstance(output.numerator,float):
            output.num_to_int()
        output.simplify()
        return output

def pgdc(a,b):
    if b == 0:
        return a
    else:
        return pgdc(b,a%b)