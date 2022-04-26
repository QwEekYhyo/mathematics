class Fraction:
    def __init__(self,num,den = 1):
        self.numerator = num
        self.denominator = den
        if self.numerator < 0 and self.denominator < 0:
            self.numerator = abs(self.numerator)
            self.denominator = abs(self.denominator)

    def __repr__(self):
        self._to_int()
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

    def simplify(self):
        x = pgdc(self.numerator,self.denominator) 
        self.numerator /= x
        self.denominator /= x

    def simplified(self):
        output = Fraction(self.numerator,self.denominator)
        if isinstance(output.numerator,float):
            output.num_to_int()
        output.simplify()
        return output

    def __mul__(self,other):
        other = cast_to_fraction(other)
        return Fraction(self.numerator*other.numerator,self.denominator*other.denominator).simplified()

    def __rmul__(self,other):
        return self*cast_to_fraction(other)

    def change_denominator(self,number):
        self.numerator *= number
        self.denominator *= number

    def changed_den(self,number):
        return Fraction(self.numerator*number,self.denominator*number)

    def __add__(self,other):
        if self.denominator == other.denominator:
            return Fraction(self.numerator+other.numerator,self.denominator).simplified()
        else:
            div = ppmc(self.denominator,other.denominator)
            return (self.changed_den(div/self.denominator)+other.changed_den(div/other.denominator)).simplified()

    def __radd__(self,other):
        return (self+cast_to_fraction(other)).simplified()

    def __neg__(self):
        return Fraction(-self.numerator,self.denominator)

    def __sub__(self,other):
        return (self+-cast_to_fraction(other)).simplified()

    def inverted(self):
        return Fraction(self.denominator,self.numerator)

    def __truediv__(self,other):
        return (self * cast_to_fraction(other).inverted()).simplified()

    def __rtruediv__(self,other):
        return (cast_to_fraction(other)*self.inverted()).simplified()

    def __pow__(self,other):
        return Fraction(self.numerator**other,self.denominator**other).simplified()

    def __eq__(self,other):
        a = self.simplified()
        b = other.simplified()
        return a.numerator == b.numerator and a.denominator == b.denominator

    def __bool__(self):
        return self.numerator != 0

    def __abs__(self):
        return Fraction(abs(self.numerator),abs(self.denominator))

    

    
def pgdc(a,b):
    if b == 0:
        return a
    else:
        return pgdc(b,a%b)

def ppmc(a,b):
    return abs(a*b)/pgdc(a,b)

def cast_to_fraction(item):
    return item if isinstance(item,Fraction) else Fraction(item,1)