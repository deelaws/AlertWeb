'''
MyWebsite module is in a different directory.
Add it to your system path to access it.
'''
import sys,site
site.addsitedir(sys.path[0]+'\\..\\MyWebsite')  
print (sys.path)  # just verify it is there  

from MyWebsite.mod_rescue.models import RescueAlert

class AlertProcessThread():
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)