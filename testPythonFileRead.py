import os 
import json


AppsList = []
def loadAppUrls():
    with open(os.path.abspath("TaskManager/static/Config/Applications.json")) as f:
        jsonContent = json.load(f)
        for item in jsonContent["Apps"]:
            AppsList.append("url(r'^%s/', include('%s.urls'))"%(item,item))
    return AppsList

def patterns(prefix,arg):
    return arg

urlpatterns = patterns('', loadAppUrls())
print urlpatterns
