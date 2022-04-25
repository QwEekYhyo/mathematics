# Logan LUCAS

import random,copy
import complex as c

class Matrix:
    def __init__(self,values = None, Isize = 3):
        if not values:
            ide = [[1 if i == j else 0 for i in range(Isize)] for j in range(Isize)]

        self.values = values or ide
        self.width = len(self.values)
        self.length = len(self.values[0]) if len(self.values) >= 1 else 0

    def __repr__(self):
        output = ""
        val = []
        ldict = {}

        for j in range(self.width):
            for i in range(self.length):
                if i not in ldict or len(str(self.values[j][i])) > ldict[i]:
                    ldict[i] = len(str(self.values[j][i])) 
                    
        for i in range(self.length):
            temp = []
            for j in range(self.width):
                dif = ldict[i]-len(str(self.values[j][i]))
                if dif > 0:
                    temp.append(" "*dif + str(self.values[j][i])) 
                else:
                    temp.append(str(self.values[j][i]))
            val.append(temp)
        
        for i in range(self.width):
            output+= "( "
            for j in range(self.length):
                output+= val[j][i]+" "
            output+=")\n"
                
        return output

    def __add__(self,other):
        if isinstance(other,Matrix):
            if self.width == other.width and self.length == other.length:
                output = []
                for i in range(self.width):
                    temp = []
                    for j in range(self.length):
                        temp.append(self.values[i][j]+other.values[i][j])
                    output.append(temp)
                return Matrix(output)
            raise ValueError("Matrices don't have the same dimensions")
        raise TypeError("You can only add matrices together")

    def __radd__(self,other):
        return self+other

    def __neg__(self):
        output = []
        for i in self.values:
            temp = []
            for j in i:
                temp.append(-j)
            output.append(temp)
        return Matrix(output)

    def __sub__(self,other):
        if isinstance(other,Matrix):
            return -other + self

    def __mul__(self,other):
        if isinstance(other,int) or isinstance(other,float) or isinstance(other,c.Complex):
            output = []
            for i in self.values:
                temp = []
                for j in i:
                    temp.append(j*other)
                output.append(temp)
            return Matrix(output)

        elif isinstance(other,Matrix):
            if self.length == other.width:
                output = []
                for i in range(self.width):
                    temp = []
                    for j in range(other.length):
                        res = 0
                        for k in range(self.length):
                            res += self.values[i][k] * other.values[k][j]
                        temp.append(res)
                    output.append(temp)
                return Matrix(output)

            raise ValueError("Cannot multiply these matrices (nb of columns of the first one != nb of lines of the second one)")
            
    def __rmul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            output = []
            for i in self.values:
                temp = []
                for j in i:
                    temp.append(j*other)
                output.append(temp)
            return Matrix(output)

    def __pow__(self,other):
        if isinstance(other,int):
            if self.length == self.width:
                output = Matrix(None,self.length)
                for i in range(other):
                    output *= self
                return output
            raise ValueError("Only square matrices can be raised to a power")
        
    def __eq__(self,other):
        if isinstance(other,Matrix) and self.width == other.width and self.length == other.length:
            for i in range(self.width):
                for j in range(self.length):
                    if self.values[i][j] != other.values[i][j]:
                        return False
            return True
        return False

    def __bool__(self):
        for i in self.values:
            for j in i:
                if j != 0:
                    return True
        return False
    __nonzero__ = __bool__

    def __abs__(self):
        output = []
        for i in self.values:
            temp = []
            for j in i:
                temp.append(abs(j))
            output.append(temp)
        return Matrix(output)

    def __getitem__(self,item):
        if isinstance(item,int) or isinstance(item,slice):
            output = []
            for i in self.values:
                if isinstance(item,int):
                    output.append([i[item]])
                else:
                    output.append(i[item])
            return Matrix(output)

    def __setitem__(self,key,value):
        if key[0] <= self.width and key[1] <= self.length:
            self.values[key[0]][key[1]] = value
        else:
            raise IndexError('Index out of range')

    def __delitem__(self,item):
        if isinstance(item,str):
            try:
                todel = int(item[1:])
                if item[0] == 'l':
                    del(self.values[todel])
                    self.width -= 1
                elif item[0] == 'c':
                    for i in self.values:
                        del(i[todel])
                    self.length -= 1
                    
            except ValueError:
                print("Wrong input")
            
    def transpose(self):
        output = []
        for i in range(self.length):
            temp = []
            for j in range(self.width):
                temp.append(self.values[j][i])
            output.append(temp)
        return Matrix(output)

    def extend(self,other):
        if isinstance(other,Matrix):
            if self.width == other.width:
                output = []
                for i in range(self.width):
                    temp = []
                    temp.extend(self.values[i])
                    temp.extend(other.values[i])
                    output.append(temp)
                return Matrix(output)
            
            raise ValueError("Can only extend matrices with the same nb of lines")
        raise TypeError("Can only extend another matrix")

    def determinant(self):
        if self.width == self.length:
            if self.width == 2:
                return self.values[0][0]*self.values[1][1] - self.values[0][1]*self.values[1][0]
            elif self.width >= 3:
                output = 0
                cp = copy.deepcopy(self)
                del cp['l0']
                for i in range(self.width):
                    if i%2 == 0:
                        signe = 1
                    else:
                        signe = -1
                    coef = self.values[0][i]
                    deter = cp[0:i].extend(cp[i+1:self.width]).determinant()
                    output += signe*coef*deter
                return output 

    def cofactor(self):
        if self.width == self.length:
            output = []
            for i in range(self.width):
                temp = []
                cp = copy.deepcopy(self)
                del cp['l{}'.format(i)]
                for j in range(self.length):
                    signe = (-1)**(i+j)
                    sub = cp[0:j].extend(cp[j+1:self.width])
                    temp.append(sub.determinant() * signe)
                output.append(temp)
            return Matrix(output)
    
    def invert(self):
        deter = self.determinant()
        if deter:
            co = self.cofactor()
            return (1/deter)*co.transpose()
        raise ValueError("Matrix isn't invertible")

    def tofract(self):
        output = []
        for i in range(self.width):
            temp = []
            for j in range(self.length):
                val = self.values[i][j]
                temp.append(fract(val))
            output.append(temp)
        return Matrix(output)

def fract(fl):
    output = fl.as_integer_ratio()
    return "{}/{}".format(output[0],output[1])

def newMatrix(value = 1000,width = 3,length = 0):
    if not length:
        length = width
    output = []
    for i in range(width):
        temp = []
        for j in range(length):
            temp.append(random.randrange(-value,value))
        output.append(temp)
    return Matrix(output)

def newComplexMatrix(value = 30, width = 3, length = 0):
    if not length:
        length = width
    return Matrix([[c.randcomplex(value) for i in range(length)] for j in range(width)])
    
    
print("Matrix(values,Identity size) : identity size only utilized if value is empty")
print("newMatrix : value , width , length (all optional)")
print("newComplexMatrix : value , width , length (all optional)")