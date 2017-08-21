import pyFT

#Comment these line and uncomment the next one to use your own API key
with open('apiKey','r') as f:
    apiKey = f.read()
#apiKey = 

#Initialize the FTRequest object using your developer key
request = pyFT.FTRequest(apiKey)

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

#To look for particular media, you can use the addCurations method:
request.addCurations(["ARTICLES","BLOGS"])

#The list of allowed curations is available here:
print("Curations: " + ", ".join(pyFT.curations))
#Any other input except an empty string will result in a pyFT.FTError.FTException being raised

#Some fields such as the uuid of the page is automatically sent by the API
#For the most interesting field, you have to specify that you want them to be returned using the 'aspects' field:
request.addAspects(['title','summary','location'])

#Authorized aspects are set here:
print("Aspects: " + ", ".join(pyFT.aspects))

#Some resultContext fields can be set using methods from the FTRequest class:
request.addSortQuery('lastPublishDateTime',DESC=False)
#Here is a list of sortable fields:
print("Sortable: " + ", ".join(pyFT.sortable))

#Not all available fields from the API have their own method.
#They will be implemented little by little, but in the meantime, you can use the addGenericResultContext method
request.addGenericResultContext('maxResults',10,isNumeric=True) #Some generic (i.e. not built-in of the wrapper) result context

#Note that if you are working in the Python interpreter and you want to make sure that your request is correct before sending it, you can print it with the _build method:
print(request._build())
#PRINT: {"queryString":"((banks AND (NOT equity)) OR (finance AND credit))","queryContext":{"curations":["ARTICLES","BLOGS"]},"resultContext":{"sortOrder":"ASC","sortField":"lastPublishDateTime","aspects":["title","summary"],"maxResults":10}}


#Once you are happy with your request, you can call the getResults method:
result = request.getResults()
#This will send you back a HTTPResponse from the httplib library
print(result)
#<http.client.HTTPResponse object at 0xb6ebdbac>

#At this stage, you can either wrap your own class to use the results
#Or you can use the FTResponse class:
FT_ARTICLES = pyFT.FTResponse(result)

#If needed, this class stores your request:
print(FT_ARTICLES.query)
#Print the query

#The results are stored as a list of json instance:
#NB: not a json instance with a list in it
print(FT_ARTICLES.results)
"""
PRINT: (using the __repr__ method)
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
"""

#Some method will come later. For now, you can return the html link to the article:
print(FT_ARTICLES.results[0].makeHTMLhref('webapp','MyCompany',campaignParameter=True))
#PRINT: http://www.ft.com/cms/be4c9c30-dfef-11de-9d40-00144feab49a.html?FTCamp=engage/CAPI/webapp/Channel_MyCompany//B2B

#If you do not need the campaign parameter (e.g. for test), you can always switch it off
#Warning: this only work if you had the 'location' aspect
print(FT_ARTICLES.results[0].makeHTMLhref('Not','used',campaignParameter=False))
#PRINT: http://www.ft.com/cms/s/0/be4c9c30-dfef-11de-9d40-00144feab49a.html
