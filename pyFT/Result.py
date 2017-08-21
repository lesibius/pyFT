import json
import pyFT.FTError as FTError

aspectsAction = {
    'title': lambda res: res['title']['title'],
    'lifecycle': lambda res: (res['lifecycle']['lastPublishDateTime'],res['lifecycle']['initialPublishDateTime']),
    'location': lambda res: res['location']['uri'],
    'summary': lambda res: res['summary']['excerpt'],
    'editorial': lambda res: res['editorial']['byline'],
}

class FTResponseAtom:
    def __init__(self,data,aspects):
        #Compulsory
        self.id = data['id']
        self.modelVersion = data['modelVersion']
        self.aspectSet = data['aspectSet']
        self.aspects = aspects
        #Facultative
        self.title = None
        self.lifecycle = None
        self.location = None
        self.summary = None
        self.editorial = None
        for asp in aspects:
            _ = aspectsAction[asp](data)
            setattr(self,asp,_)

    def __repr__(self):
        _ = ""
        if not self.title is None:
            _ += "Title: " + self.title + "\n"
        if not self.editorial is None:
            _ += "Author: " + self.editorial + "\n"
        return _

    def makeHTMLhref(self, source, orgname,campaignParameter=False):
        if campaignParameter:
            _ = "http://www.ft.com/cms/"
            _ += self.id
            _ += ".html?FTCamp=engage/CAPI/"
            _ += source
            _ += "/Channel_"
            _ += orgname
            _ += "//B2B"
        else:
            if not self.location is None:
                _ = self.location
            else:
                raise FTError.FTException("Either set campaignParameter as True when calling to makeHTMLhref or add location in aspects of the query")
        return _

    def IPythonPretty(self):
        _ = "<h2><a href=" + self.makeHTMLhref(self,"","") + ">"
        _ += self.title + "</a></h2>"
        _ += "<p>" + self.summary + "</p>"
        return _
        

class FTResponse:

    def __init__(self,response):
        jsresponse = json.loads(response.read().decode())
        self.query = jsresponse['query']
        self.aspects = self.query['resultContext']['aspects']
        self.results = [FTResponseAtom(elt,self.aspects) for elt in jsresponse['results'][0]['results']]
