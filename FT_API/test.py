import Request
import Result
import FTQuerySyntax as SYN
import json

req = Request.FTRequest('x2jpnmve9tmygtbnqwwuw94f')

A = SYN.FTBasic("BNP Paribas")
B = SYN.FTBasic("Lukoil")
C = SYN.FTBasic("Natixis")
D = SYN.FTBasic("Oil")
E = SYN.FTBasic("WTI")

req.customQuery('BNP Paribas')
req.builtQuery(-A+B*C*(D-E))
req.addSortQuery('lastPublishDateTime')
req.addCurations(["ARTICLES","BLOGS"])
req.addGenericResultContext('maxResults',10,isNumeric=True)
req.addAspect(Request.aspects)
#print(req._build())

res = req.getResults()
res = Result.FTResponse(res)

for elt in res.results:
    print(elt.title)

#x = json.loads(res.read().decode())
#print(x)

