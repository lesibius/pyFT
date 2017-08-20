# pyFT
A wrapper fot the FT API headline

A simple example:

```python
#Import the pyFT module
import pyFt as FT

apiKey = "YOUR API KEY"

#Build a query string.
# + corresponds to OR 
# * corresponds to AND
# - corresponds to NOT or AND NOT depending on whether it replaces __neg__ or __sub__
# A lot of work is incoming on this part of the wrapper
querystr = FT.FTBasic('WTI')+FT.FTBasic('Oil')*FT.FTBasic('US')+FT.FTBasic('Shale oil')

#Wrap your request
req =FT.FTRequest(apiKey)                       #Your API key belongs here
req.builtQuery(querystr)                        #Add you quey
req.addSortQuery('lastPublishDateTime')         #You have some sorting options available
req.addCurations(['ARTICLES'])                  #ARTICLES, BLOGS, VIDEOS...
req.addGenericResultContext('maxResults',10,isNumeric=True) #Some generic (i.e. not built-in of the wrapper) result context
req.addAspect(FT.aspects)     #This add all "aspects": location, summary, title, ...
res = req.getResults()        #Get the results
FT_ARTICLES = FT.FTResponse(res)    #Store the results in a new class dedicated to work on it

#Let)s print the titles:
for article in FT_ARTICLE.results:
  print(article.title)

```
