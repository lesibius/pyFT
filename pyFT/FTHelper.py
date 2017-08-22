from pyFT.Request import *
import pyFT.FTError


FACETS = ["authors","authorsId","brand","brandId","category","format","genre","genreId","icb","icbId","iptc","iptcId","organisations","organisationsId","people","peopleId","primarySection","primarySectionId","primaryTheme","primaryThemeId","regions","regionsId","sections","sectionsId","specialReports","specialReportsId","subjects","subjectsId","topics","topicsId"]

class FTFacetsAtom(FTResultContext):

    def __init__(self,facets=None,maxElements=None,minThreshold=None):
        FTResultContext.__init__(self)
        self.facets =FTDict('facets',{
            'facets':None,
            'maxElements': None,
            'minThreshold' : None
            })
        self.buildable.append(self.facets)
        
    def addFacets(self,facets):
        
        if set(facets) <= set(FACETS):
            self.facets['facets'] = FTList('names',FACETS)
            self.facets['facets'].addElts(facets)
        else:
            raise pyFT.FTError.FTException("The following facets are unvalid: " + [f for f in facets if f not in FACETS].__repr__() + ". Allowed: " + ", ".join(FACETS))

    def setMaxElements(self,n):
        if n >= -1:
            self.facets['maxElements'] = FTAtom('maxElements',n,isNumeric=True)
        else:
            raise pyFT.FTError.FTException("facetMaxElement should be >= -1")

    def setMinThreshold(self,n) :
        if n > 0:
            self.facets['minThreshold'] = FTAtom('minThreshold',n,isNumeric=True)
        else:
            raise pyFT.FTError.FTException("minThreshold should be > 0")
        
        
        
class FTFacets(FTRequest):
    """
    Helper for facets
    """
    def __init__(self,apiKey):
        FTRequest.__init__(self,apiKey)

    def _addResultContext(self):
        if self.queryElements['resultContext'] is None:
            self.queryElements['resultContext'] = FTFacetsAtom()

    def addFacets(self,facets):
        self._addResultContext()
        self.queryElements['resultContext'].addFacets(facets)
        
            
    def setFacetMaxElements(self,n):
        self._addResultContext()
        self.queryElements['resultContext'].setMaxElements(n)

    def setFacetMinThreshold(self,n) :
        self._addResultContext()
        self.queryElements['resultContext'].setMinThreshold(n)


        

    


