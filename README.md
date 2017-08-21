# pyFT
A wrapper fot the FT API headline.

# Installation

This is a WIP, so no pip install is not supported yet. You can simply fork this project, put it in your PATH/working directory and add: `import pyFT` from your code.

# Getting Started

The first step to use the wrapper is to instanciate a FTRequest object using your API developer key:

```python
import pyFT

#Comment these line and uncomment the next one to use your own API key
with open('apiKey','r') as f:
    apiKey = f.read()
#apiKey = 

#Initialize the FTRequest object using your developer key
request = pyFT.FTRequest(apiKey)
```

The most basic query consists only of a querySyntax field:

```python
#For the main part of your query, you can either set it directly:
request.customQuery("banks")
print(request._build()) #This lines print the body of the html message to stdout
#PRINT: {"queryString":"banks"}

#Or you can use the FTQuerySyntax objects:
query = (pyFT.FTBasic("banks") - pyFT.FTBasic("equity")) + pyFT.FTBasic("finance") * pyFT.FTBasic("credit")
print(query.evaluate())
#PRINT: ((banks AND (NOT equity)) OR (finance AND credit))

#You can then add it to your FTRequest:
request.builtQuery(query)
```

As it is, this query will return any match for any media. You can restrict this by using the curations field.

```python
#To look for particular media, you can use the addCurations method:
request.addCurations(["ARTICLES","BLOGS"])

#The list of allowed curations is available here:
print("Curations: " + ", ".join(pyFT.curations))
#Any other input except an empty string will result in a pyFT.FTError.FTException being raised
```

You also have to specify which fields you wish to be returned. This is done via the aspects field.

```python
#Some fields such as the uuid of the page is automatically sent by the API
#For the most interesting field, you have to specify that you want them to be returned using the 'aspects' field:
request.addAspects(['title','summary','location'])

#Authorized aspects are set here:
print("Aspects: " + ", ".join(pyFT.aspects))
```

The aspects field is actually part of a wider field named resultContext which allows to constraint your results. Some methods are readily available to set these yourself.
```python
#Some resultContext fields can be set using methods from the FTRequest class:
request.addSortQuery('lastPublishDateTime',DESC=False)
#Here is a list of sortable fields:
print("Sortable: " + ", ".join(pyFT.sortable))
```

As this wrapper is a WIP, some are not available yet. You may however use them through the addGenericResultContext method.

```python
#Not all available fields from the API have their own method.
#They will be implemented little by little, but in the meantime, you can use the addGenericResultContext method
request.addGenericResultContext('maxResults',10,isNumeric=True) #Some generic (i.e. not built-in of the wrapper) result context
```

Now, our request is almost done. You can have a look at hit with the _build method of the FTRequest instance.
```python
#Note that if you are working in the Python interpreter and you want to make sure that your request is correct before sending it, you can print it with the _build method:
print(request._build())
```

The results should look like this (note that I am using EMAC's json-pretty-pring, there is no line separation in the actual result):
```json
{
  "resultContext": {
    "maxResults": 10,
    "aspects": [
      "title",
      "summary"
    ],
    "sortField": "lastPublishDateTime",
    "sortOrder": "ASC"
  },
  "queryContext": {
    "curations": [
      "ARTICLES",
      "BLOGS"
    ]
  },
  "queryString": "((banks AND (NOT equity)) OR (finance AND credit))"
}
```

It is now time to actually send your request to the API:
```python
#Once you are happy with your request, you can call the getResults method:
result = request.getResults()
#This will send you back a HTTPResponse from the httplib library
print(result)
#<http.client.HTTPResponse object at 0xb6ebdbac>
```

At this stage, you can either wrap your own class to use the results or you can use the FTResponse class:
```python
FT_ARTICLES = pyFT.FTResponse(result)
```

Both the query and the results are stored:
```python
#If needed, this class stores your request:
print(FT_ARTICLES.query)
#Print the query as a json instance
```

The results are actually stored as a Python list of json instances:
```python
print(FT_ARTICLES.results)
"""
PRINT: (using the __repr__ method, assuming you added 'title' in the aspects)
[Title: FT interview transcript: Robert Zoellick
, Title: Lloyds reveals £201m credit hit
, Title: CDS update: Fundamentally pessimistic
, Title: 'My social life never stops'
, Title: US authorities in Iraq probe phone contracts
, Title: Jonathan Guthrie: Offshoring will hurt
, Title: John Kay: Customer inertia and the active shopper
, Title: ABB names Sulzer boss as new chief executive
, Title: Travel bears brunt of losses
, Title: Measured confidence takes over
]
```

Methods to work with this class will be added later. For now, you can return a formatted link to the article:

```python
#This is a compliant version according to the API documentation
print(FT_ARTICLES.results[0].makeHTMLhref('webapp','MyCompany',campaignParameter=True))
#PRINT: http://www.ft.com/cms/be4c9c30-dfef-11de-9d40-00144feab49a.html?FTCamp=engage/CAPI/webapp/Channel_MyCompany//B2B

#This version does not comply, but is useful when testing:
print(FT_ARTICLES.results[0].makeHTMLhref('argument not','used',campaignParameter=False))
#PRINT: http://www.ft.com/cms/s/0/be4c9c30-dfef-11de-9d40-00144feab49a.html
```
