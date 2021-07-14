

import TELEGRAM as te
from __init__ import *

file1 = open("{}/token.txt".format(cwd),"r")
shop = (file1.read())

obj = te.telegram(shop)
obj.main()

 





    
