import random
import changingvar as cv
import constantfunc as cf
import createfunc as crf
import textprocess as tp
import time
import re
 
import datetime
from __init__ import *
 
class sub1():
  def __init__(self,cust):
      self.cust=cust
      
  def add_and_show(self,arg,obj="u",dictionary={}): 
    try:
        print(arg,len(arg))
        cv.jsonfile(self.cust).update('pot','ap',arg)
        pot = cv.jsonfile(self.cust).update('pot','r')
        print(pot)
        
        if len(pot) == 2:
            if pot[-1] in "1234":
                p = cf.urls(pot[-1])
                print(p,"url")
                return [cf.urls(pot[-1]),cf.switch1(pot[-1])]
            else:
                cv.jsonfile(self.cust).update('pot','r-1')
                return cf.sendtxt("plz give the correct input so I can understand.",self.cust) 
        elif len(pot) == 3:
            if pot[-1] in '12345':
                return cf.sendtxt(cf.switch2(pot[1:]),self.cust)
            else:
                cv.jsonfile(self.cust).update('pot','r-1')
                return cf.sendtxt("plz give the correct input so I can understand.",self.cust)
        elif len(pot)==4:
            get = cf.db().get(pot,self.cust)
            if get != -1:
              cv.jsonfile(self.cust).update('pot','last',str(wtm))
              cv.jsonfile(self.cust).update('pot1','ap',cv.jsonfile(self.cust).update('pot','r'))
              cv.jsonfile(self.cust).update('pot','hi')
              cf.finalcart(get,self.cust,obj,dictionary)
              return cf.sendtxt(cf.switch3(pot[-1]),self.cust)
            else:
                cv.jsonfile(self.cust).update('pot','r-1')
                return cf.sendtxt("plz give the correct input so I can understand.\nTo order new item just send *Hi* here",self.cust) 
        else:
            cv.jsonfile(self.cust).update('pot','r-1')
            return cf.sendtxt("plz give the correct input so I can understand.\nTo order new item just send *Hi* here",self.cust) 
    except:  
        pot = cv.jsonfile(self.cust).update('pot','r')
        if len(pot)==4:
            wtm = cf.db().get(pot,self.cust)
            if wtm != -1:
              cv.jsonfile(self.cust).update('pot','last',str(wtm))
              cv.jsonfile(self.cust).update('pot1','ap',cv.jsonfile(self.cust).update('pot','r'))
              cv.jsonfile(self.cust).update('pot','hi')
              cf.finalcart( wtm,obj,self.cust,dictionary)
              return cf.sendtxt(cf.switch3(pot[-1]),self.cust)
            else:
                cv.jsonfile(self.cust).update('pot','r-1')
                return cf.sendtxt("plz give the correct input so I can understand.\nTo order new item just send *Hi* here",self.cust) 
            return cf.sendtxt(cf.switch3(pot[-1]),self.cust)
        else:
            cv.jsonfile(self.cust).update('pot','r-1')
            return cf.sendtxt(cf.random_response(random.randint(1,3)),self.cust)
            
##############################################################################################################3###################3



###/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 

def next(a,msg,cust):
  obj = tp.combine(cust)
  pm = obj.ans_que(msg)
  print(pm )
  if str(pm) != "0":
    return (pm)
  else:
    return (a.add_and_show(msg))


def add_each_msg(msg,user):
  dic = cv.jsonfile("ok",r'{}/userdata/msgs.json'.format(cwd)).read()
  current_time = str(datetime.datetime.now())
  print(90)
  current_time = current_time.split(" ")
  d1     = current_time[0]
  timeit = current_time[-1]
  try:
    dic[d1][timeit] = {"user":user,"message":msg}
  except:
    dic[d1] = ({timeit:{"user":user,"message":msg}})
  cv.jsonfile("ok",r'{}/userdata/msgs.json'.format(cwd)).add_dict(dic,0)
  print(dic)
  print("added to chain")

def sms_reply(msg,remote_number = "+917666779269"):
  am = msg.lower()
  add_each_msg(am,remote_number)
  #am = cf.detect_and_translate(am)
  if 'start' in am:
      pf = {remote_number: {"pot": [], "pot1": [], "mainDB": [], "total": 0, "cart": {0:[]}}}
      cv.jsonfile(remote_number).add_dict(pf)
      return "welcome start your order \n use the code /key to understand the processes"
    
  elif 'key' in am:
      pf = {remote_number: {"pot": [], "pot1": [], "mainDB": [], "total": 0, "cart": {0:[]}}}
      cv.jsonfile(remote_number).add_dict(pf)
      return cf.keys()
    
  elif cv.jsonfile(remote_number).update('contacts','check')==1:
      mk = next(sub1(remote_number),am,remote_number)
      
  else:
      pf = {remote_number: {"pot": [], "pot1": [], "mainDB": [], "total": 0, "cart": {0:[]}}}
      cv.jsonfile(remote_number).add_dict(pf)
      mk = ("welcome start your order \n use the code /key to understand the processes")
 
  return (mk)
