import pyFT.FTError
import datetime as dt

strfRFC3339 = '%Y-%m-%dT%H:%M:%S.000Z'


def FTdateTime(val):
    return dt.datetime.strftime(val,strfRFC3339)



