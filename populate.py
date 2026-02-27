# populate.py
from testpages.models import *
import random

def populate():
    for i in range(30):
        ch = ""
        
        for i in range(50):
            ch += chr(random.randint(65,91))
        
        testlist = TestList.objects.create(testListDesc=ch)
        ch = ch[::-1]
        
        TestModel.objects.create(
            testInt  = random.randint(0,100),
            testChar = ch,
            testList = testlist)