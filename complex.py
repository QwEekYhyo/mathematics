from fraction import *
import math,random
import matrix

class Complex():
    acc = 3
    def __init__(self,real = None,im = None,mod = None,arg = None):
        if (real is None or im is None) and (mod is None or arg is None):
            raise TypeError("Needs either real and imaginary part or modulus and argument (mod, arg)")
        self.real = real if real is not None else  mod * math.cos(arg)
        self.im = im if im is not None else mod * math.sin(arg)
        self.modulus = mod if mod is not None else (self.real**2+self.im**2)**0.5
        if (self.real,self.im) != (0,0):
            self.argument = arg if arg is not None else math.atan2(self.im,self.real)
        else:
            self.argument = 0
        self.form = 0
        
    def __repr__(self):
        #a = map(lambda x : round(x,Complex.acc),[self.real,self.im,self.modulus,self.argument])
        if self.form == 0:
            if self.real and not self.im:
                return str(self.real)
            elif self.real and self.im in (1,-1):
                return f"{round(self.real,Complex.acc)}+i" if self.im > 0 else f"{round(self.real,Complex.acc)}-i"
            elif self.real:
                return f"{round(self.real,Complex.acc)}+{abs(round(self.im,Complex.acc))}i" if self.im > 0 else f"{round(self.real,Complex.acc)}-{abs(round(self.im,Complex.acc))}i"
            elif not self.real and not self.im:
                return str(self.real)
            elif not self.real and self.im in (1,-1):
                return "i" if self.im > 0 else "-i"
            else:
                return f"{abs(round(self.im,Complex.acc))}i" if self.im > 0 else f"-{abs(round(self.im,Complex.acc))}i"
            
        elif self.form == 1:
            return f"{round(self.modulus,Complex.acc)}(cos({round(self.argument,Complex.acc)}) + i sin({round(self.argument,Complex.acc)}))"

        else:
            return f"{round(self.modulus,Complex.acc)}exp({round(self.argument,Complex.acc)}i)"
            
    def __add__(self,other):
        other = cast_to_complex(other)
        return Complex(self.real+other.real,self.im+other.im)

    def __radd__(self,other):
        other = cast_to_complex(other)
        return self+other
        
    def __neg__(self):
        return Complex(-self.real,-self.im)

    def __sub__(self,other):
        return self+-cast_to_complex(other)

    def __mul__(self,other):
        if isinstance(other,matrix.Matrix):
            return other * self
        other = cast_to_complex(other)
        return Complex(self.real*other.real-self.im*other.im,self.real*other.im+self.im*other.real)

    def __rmul__(self,other):
        return self*other

    def conjugate(self):
        return Complex(self.real,-self.im)

    def __truediv__(self,other):
        other = cast_to_complex(other)
        num = self*other.conjugate()
        den = other.modulus**2
        return Complex(num.real/den,num.im/den)

    def __rtruediv__(self,other):
        other = cast_to_complex(other)
        return other/self

    def polar(self):
        self.form = 1
        return f"{self.modulus}(cos({self.argument}) + i sin({self.argument}))"

    def expo(self):
        self.form = 2
        return f"{self.modulus}exp({self.argument}i)"

    def cartesian(self):
        return self.modulus * Complex(math.cos(self.argument),math.sin(self.argument))

    def nroot(self,n):
        roots = [Complex(mod= self.modulus**(1/n),arg= (self.argument+2*k*math.pi)/n) for k in range(n)]
        return roots
    # can't compute for exemple : Complex(4,2)**2.15, maybe can improve ?
    def __pow__(self,other):
        output = 1
        if isinstance(other,int):
            for i in range(other):
                output *= self
            return output
        if isinstance(other,float):
            int_part = int(other)
            decimal = other - int_part
            output *= self**int_part
            decimal = Fraction(decimal)
            decimal.num_to_int()
            decimal.simplify()
            return [output*(n**decimal.numerator) for n in self.nroot(decimal.denominator)]

    def __eq__(self,other):
        return self.real == other.real and self.im == other.im

    def __bool__(self):
        return self.real != 0 or self.im != 0

    def __abs__(self):
        return Complex(abs(self.real),abs(self.im))

    def matrix(self):
        return matrix.Matrix([[self.real,-self.im],[self.im,self.real]])

def cast_to_complex(truc):
    if isinstance(truc,Complex):
        return truc
    elif isinstance(truc,int) or isinstance(truc,float):
        return Complex(truc,0)

def factorial(n):
    output = 1
    for i in range(2,n+1):
        output *= i
    return output

def exp(x,acc = 100):
    if isinstance(x,Complex):
        return exp(x.real,acc)*Complex(mod= 1,arg= x.im)
    else:
        return sum([(x**i)/factorial(i) for i in range(acc)])

def randcomplex(value = 25):
    return Complex(random.randrange(-value,value),random.randrange(-value,value))    
