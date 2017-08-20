class FTBasic:
    def __init__(self,val):
        self.val = val

    def __add__(self,other):
        return FTOR(self,other)
    def __radd__(self,other):
        return FTOR(other,self)
    def __mul__(self,other):
        return FTAND(self,other)
    def __rmul__(self,other):
        return FTAND(other,self)
    def __sub__(self,other):
        return FTAND(self,FTNOT(other))
    def __rsub__(self,other):
        return FTAND(other,FTNOT(self))
    def __neg__(self):
        return FTNOT(self)
    
    def evaluate(self):
        return self.val

class FTNil(FTBasic):
    def __init__(self):
        FTBasic.__init__(self,"")

class FTOperator(FTBasic):
    def __init__(self,symb,v1,v2):
        self.v1 = v1
        self.v2 = v2
        self.symb = symb

    def evaluate(self):
        _ = "(" + self.v1.evaluate()
        _ += self.symb 
        _ += self.v2.evaluate() + ")"
        return _

class FTOR(FTOperator):
    def __init__(self,v1,v2):
        FTOperator.__init__(self," OR ",v1,v2)

class FTAND(FTOperator):
    def __init__(self,v1,v2):
        FTOperator.__init__(self," AND ",v1,v2)

class FTNOT(FTOperator):
    def __init__(self,val):
        FTOperator.__init__(self,"NOT ",FTNil(),val)
        
