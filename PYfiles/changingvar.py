import json
from __init__ import *

class jsonfile():

  def __init__(self,cust,file = r'{}/mydata.json'.format(cwd)):
    self.cust = cust
    self.file = file 

  def read(self):
    f = open(self.file,'r')
    datas = json.load(f)
    f.close()
    return datas

  def write(self,content):
    with open(self.file,'w') as fp:
      json.dump(content,fp)

  def add_dict(self,dict2,update=1):
    if update == 1:
      data123 = self.read()
      data123.update(dict2)
    else:
      self.write(dict2)

  def update(self,var,action="a",msg="ok",num=0,lis=[],dict1={0:[]}):
    
    data = self.read()

    if var=='pot':
      
      if action=="r":
        return data[self.cust]['pot']
      elif action =="hi":
        data[self.cust]['pot']=['hi']
      elif action=="null":
        data[self.cust]['pot'] = []
      elif action=="ap":
        data[self.cust]['pot'].append(msg)
      elif action=="r-1":
        data[self.cust]['pot']=data[self.cust]['pot'][:-1]
      elif action=="a-1":
        return data[self.cust]['pot'][-1]
      elif action=="last":
        data[self.cust]['pot'][-1]=msg

    elif var == "pot1":
      if action=="r":
        return data[self.cust]['pot1']
      elif action == "null":
        data[self.cust]['pot1'] = []
      elif action=="a-1":
        return data[self.cust]['pot1'][-1]
      elif action == "ap":
        data[self.cust]['pot1'].append(msg)

    elif var=="mainDB":
      if action=="r":
        return data[self.cust]['mainDB']
      elif action == "null":
        data[self.cust]['mainDB'] = []
      elif action=="a-1":
        return data[self.cust]['mainDB'][-1]
      elif action == "ap":
        data[self.cust]['mainDB'].append(msg)

    elif var=="total":
      if action=="r":
        return data[self.cust]['total']
      elif action == "null":
        data[self.cust]['total']=0
      elif action == "ad":
        data[self.cust]['total'] += num

    elif var=="cart":
      if action=="r":
        return data[self.cust]['cart']
      elif action == "null":
        data[self.cust]['cart']={0:[]}
      elif action == "ad":
        dic=data[self.cust]['cart']
        last = int(list(dic.keys())[-1])+1
        dic[last] = lis   #[str(last)] + lis
        data[self.cust]['cart']=dic
      elif action == 'ad_dic':
        data[self.cust]['cart'] = dict1
        

    elif var == "contacts":
      if action == "check":
        if self.cust in data:
          return 1
    self.write(data)
     
