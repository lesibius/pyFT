import pyFT

searchable = ["apiUrl","authors","authorsId","brand","brandId","byline","category","contributorRights","format","genre","genreId","icb","icbId","id","initialPublishDateTime","iptc","iptcId","lastPublishDateTime","masterEntityId","masterSource","organisations","organisationsId","originatingParty","people","peopleId","primarySection","primarySectionId","primaryTheme","primaryThemeId","regions","regionsId","runtimeMilliseconds","sections","sectionsId","specialReports","specialReportsId","subheading","subjects","subjectsId","title","topics","topicsId","uri"]

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

class FTSearch(FTBasic):
    """
    """
    def __init__(self,field,search,equals=False):
        """
        Parameters
        ----------
        field: Field searched (must be searchable)
        search: Term searched
        equals: (Optional) If True, the field must match, else it should contain the search term
        """
        FTBasic.__init__(self,'')
        self.update(field,search,equals)
        

    def _makeString(self):
        _ = self.field + ":"
        if self.equals:
            _ += "="
        _ += "\"" + self.search + "\""
        return _

    def update(self,field,search,equals):
        if not field in searchable:
            raise pyFT.FTError.FTException("Field \"" + field + "\" not searchable")
        self.field = field
        self.search = search
        self.equals = equals
        _ = self._makeString()
        self.val = _
        
                

                    
    
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
        
