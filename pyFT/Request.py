import pyFT.FTError
import http.client

##################################################################
#                         FT API CONSTANTS
##################################################################

sortable = ["byline","category","imageUrl","initialPublishDateTime","lastPublishDateTime","primarySection","primaryTheme","runtimeMilliseconds","title","uri"]

curations = ["ARTICLES","BLOGS","PAGES","PODCASTS","VIDEOS"]

aspects = ["title","lifecycle","location","summary","editorial"]

##################################################################
#                         Query Atom
##################################################################

class FTAtom:
    """
    """
    def __init__(self, key, val, isNumeric=False):
        """
        """
        self.key = key
        self.val = val
        self.isNumeric = isNumeric

    def _build(self):
        _ = "\"" + self.key + "\":"
        if self.isNumeric:
            _ += str(self.val)
        else:
            _ += "\"" + self.val + "\""
        return _

class FTList:
    """
    """
    def __init__(self,key,validation):
        """
        """
        self.key = key
        self.elts = []
        self.validation = validation

    def addElts(self,li):
        if not self.validation is None:
            for elt in li:
                if not elt in self.validation:
                    msg = elt + " is not an allowed " + self.key + " element. Allowed: " + ", ".join(self.validation)
                    raise pyFT.FTError.FTException(msg)
            self.elts = li

    def _build(self):
        _ = ["\"" + e + "\"" for e in self.elts]
        _ = ",".join(_)
        return "\""+self.key+"\":"+"["+_+"]"
   
    

##################################################################
#                         queryString
##################################################################

class FTQueryString:
    """
    queryString
    """
    def __init__(self):
        """
        """
        self.basis = '\"queryString\":\"'
        self.query = ''
        self.custom = False

    def setCustomQuery(self, query):
        """
        Manually write the query
        Warning: no validity check!
        """
        self.custom = True
        self.query = query

    def setBuiltQuery(self, query):
        self.cutom = False
        self.query = query.evaluate()

    def _build(self):
        """
        Build the query
        """
        _ = self.basis
        if self.custom:
            _+=self.query
        else:
            _+=self.query
        _ += "\""
        return _

##################################################################
#                         queryContext
##################################################################

    
class FTQueryContext:
    """
    """
    def __init__(self):
        """
        """
        self.basis = "\"queryContext\":{"
        self.curations = None
        self.generics = None

    def addCuration(self,cur):
        if self.curations is None:
            self.curations = FTCuration()
        self.curations.addElts(cur)

    def addGeneric(self,key,val,isNumeric=False):
        if self.generics is None:
            self.generics = []
        self.generics.append(FTAtom(key,val,isNumeric))

    def _build(self):
        buildable = [self.curations]
        if not self.generics is None:
            buildable += self.generics
        _ = self.basis
        _ += ",".join([e._build() for e in buildable if not e is None])
        _ += "}"
        return _


class FTCuration(FTList):
    """
    """
    def __init__(self):
        FTList.__init__(self,"curations",curations)

##################################################################
#                         resultContext
##################################################################
        
class FTResultContext:
    """
    """
    def __init__(self):
        """
        """
        self.basis = '\"resultContext\":{'
        self.generics = None
        self.sortQuery = None
        self.aspects = None

    def addSortQuery(self,field,DESC=True):
        """
        Add a sorting order to the FT query
        """
        self.sortQuery = FTSortQuery(field,DESC)

    def addGeneric(self,key,val,isNumeric=False):
        if self.generics is None:
            self.generics = []
        self.generics.append(FTAtom(key,val,isNumeric))

    def addAspects(self,asp):
        if self.aspects is None:
            self.aspects = FTAspect()
        self.aspects.addElts(asp)

    def _build(self):
        buildable = [self.sortQuery,self.aspects]
        if not self.generics is None:
            buildable += self.generics
        _ = self.basis
        _ += ",".join([e._build() for e in buildable if not e is None])
        _ += "}"
        return _

class FTAspect(FTList):
    """
    """
    def __init__(self):
        FTList.__init__(self,"aspects",aspects)
        
    

    
class FTSortQuery:
    """
    """
    def __init__(self,field,DESC):
        """
        """
        if not field in sortable:
            raise FTError.FTException('The field provided is not sortable')
        self.sortField = "\""+field+"\""
        if DESC:
            self.sortOrder = "\"DESC\""
        else:
            self.sortOrder = "\"ASC\""

    def _build(self):
        """
        """
        _ = "\"sortOrder\":" + self.sortOrder
        _ += ",\"sortField\":"+self.sortField
        return _


        
##################################################################
#                         FT REQUEST
##################################################################    
        

class FTRequest:
    """
    Wrap a request to the FT API before sending it
    """

    def __init__(self,apiKey):
        """
        Constructor of the FTRequest class
        """
        self.domain = 'api.ft.com'
        self.apiKey = apiKey
        self.header = {"Content-Type": "application/json"}
        self.queryElements = [None,None,None] #queryString, queryContext, resultContext

    def customQuery(self,query):
        """
        Creates a custom query

        parameters
        ---------
        query: Manually written query

        Returns
        ------
        None
        """
        if self.queryElements[0] is None:
            self.queryElements[0] = FTQueryString()
        self.queryElements[0].setCustomQuery(query)

    def builtQuery(self,query):
        if self.queryElements[0] is None:
            self.queryElements[0] = FTQueryString()
        self.queryElements[0].setBuiltQuery(query)

    def addSortQuery(self,field,DESC=True):
        if self.queryElements[2] is None:
            self.queryElements[2] = FTResultContext()
        self.queryElements[2].addSortQuery(field,DESC)

    def addCurations(self,cur):
        if self.queryElements[1] is None:
            self.queryElements[1] = FTQueryContext()
        self.queryElements[1].addCuration(cur)

    def addGenericResultContext(self,key,val,isNumeric=False):
        if self.queryElements[2] is None:
            self.queryElements[2] = FTResultContext()
        self.queryElements[2].addGeneric(key,val,isNumeric)

    def addAspects(self,asp):
        if self.queryElements[2] is None:
            self.queryElements[2] = FTResultContext()
        self.queryElements[2].addAspects(asp)
        
    def getResults(self):
        conn = http.client.HTTPSConnection(self.domain)
        req ="/content/search/v1?apiKey="+self.apiKey
        header = {"Content-Type": "application/json"}
        body = self._build()
        conn.request(method="POST", url=req, body=body,headers=header)
        response = conn.getresponse()
        return response

    def _build(self):
        """
        """
        _ = "{"
        elt = [e._build() for e in self.queryElements if not e is None]
        _ += ",".join(elt)
        _ += "}"
        return _
