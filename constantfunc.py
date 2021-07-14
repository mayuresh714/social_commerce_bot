import pandas as pd
import random
import pandas as pd
import en_core_web_sm
import spacy
from google_trans_new import google_translator
import re
from word2number import w2n
import changingvar as cv
from textblob import TextBlob
import createfunc as crf
import dataframe as dfi


################################################################################################################################################
def switch1(argument): 
  mydict = {"Hi":  "Hey,We have the following categories of product available now you can order them as per your need by replying in text format \n"+ crf.company_numberwise_static,
           "Hi2.0": " to add next item in your cart\n"+ crf.company_numberwise_static
           }    
  mydict.update(crf.made_one_dic)
  a = "plz give correct input option number.I am still in learning phase."
  return  (mydict.get(argument, a))
  
def switch2(pot_lis): 
  """switcher = {
          "1": "how many litres of milk do you want?", 
          "2": "how many grams or KGs of Dal you want to buy?", 
          "3": "how many Kgs of oil do you need?",
          "4": "how many soaps do you want?",
          }"""
  
  return crf.find_and_ask(pot_lis)

def switch0(arg0="Hi"):
  return switch1("Hi")

 

def switch3(arg3):
  switchof="product added to the cart \n\n'CAT'-> To view the subcategories\n'PLACE'->To place the order and confirm"
  return switchof

def switch4(arg4):
  dictl = {"1":switch1("Hi"),
           "2":"your order is taken by our side",
          }
  return dictl.get(arg4," I don't understand your response plz make it correct")

def random_response(arg):
  randomdict = { 1:"sorry I didn't hear that ",
      2:"please specify your input in correct manner which I can understand",
      3:"Ohh I didn't see that coming make it more specific in a way I can understand"
        
  }
  return randomdict[arg]

def rules(arg="not_new"):
  mp = 'WELcome to SuPeR MaRkeT ...\n enjoy the new way of whatsapp shopping with your trustworthy local businesses\n\n'
  new0 = 'shortkeys to place the orders ,checking prices,payments,cartlist etc...\n '
  new1 = '/CAT-to get the list of products\n\n'
  new2 = '/CART-to get to know about items you have added \n\n'
  new3 = '/PLACE- confirming and go towards payments\n\n'#*ADD*- specifying this will help to directly add products in your cart\n\n'#*RATE*- rate our service out of 10'#\n\n*KHATA*- know your history of last 7 days orders\n\n*INST*- write specific instruction deemands for your product delivery '
  if arg == "new":
    return mp+new0+new1+new2+new3
  else:
    return new0+new1+new2+new3

def keys():
  return rules()

def urls(args):
  print(type(args))
  dic =  cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read()
  ordi = dic['shop']['subcat']
  key = list(ordi.keys())
  print(key)
  s = ordi[key[int(args)]]
  print(s)
  return s



##3################ instaed of this take list as parameter############################################################################################
############### return find_and_ask[lis]
    
class db():
    def __init__(self,df = dfi.df):
        self.df = df

    def find(self,cat,product ):                               
        pf = self.df[self.df['category']==cat]
        mf = pf[pf['product']==product]
        return mf

    def find_prod(self,prod ):
        mf = self.df[self.df['product']==prod]
        return mf

    def find_no(self,s1,s2):
        bg = self.df[self.df["srno"]== s1]
        gb = bg[bg['subsr']==s2]
        return gb
    
    def w_to_n(self,word):
        try:
            num = w2n.word_to_num(word)
            return num
        except:
            return -1

    def get(self,lis,cust,):
        print(109)
        lisi = []
        
        new_df = self.find_no(int(lis[1]),int(lis[2]))
        print(new_df)
        for p in new_df['product']:
            stri = p
            
        lisi.append(stri)  ##########
        
        wgts = ["kilo","kgs","kilo","kg","kilogram","kilograms","litres","litre","lit"]
        swgts = ["grams","gms","gram"]
        
        try:
            for i in lis[-1].split():
                if self.w_to_n(i)!= -1:
                    pce = self.w_to_n(i)
                    quan = str(pce)
                    break
            
            for i in lis[-1].split():
                if i in swgts:
                    for j in new_df['price']:
                        price = j
                    quan +="X "+ i
                    lisi.append(quan)  #############
                    pce *= (float(price)/ 1000)
                    cv.jsonfile(cust).update('total','ad',num = pce)                    
                    lisi.append(str(pce))################
                    return  lisi
            else: 
                for j in new_df['price']:
                    price = j
                for k in new_df['weight']:
                    wd = k
                pce *= price 
                cv.jsonfile(cust).update('total','ad',num = pce)
                lisi.append(quan)  #########
                lisi.append(str(pce))#################
                
                return lisi
        except:
            return -1
          
            
def show_table(dic1,cust,sr = ""):
    sr= ""
    dic1.pop('0') 
    p = "--------------------------------------------------------\n"
    s=  p+"ITEM" + " "*15 + "QUANTITY"+" "*15+"NET"+" "*5 +"\n"
    s = s+p
    print(dic1)
 
    for i in dic1:
        a = dic1[i][0]
        b = dic1[i][1]
        c = dic1[i][-1]
        sr += a + " " * (20-len(a))
        sr += b + " " * (20-len(b))
        sr += c + "\n"
        
    return s+sr

def finalcart(my_list_get,obj,cust,my_dict):
  cv.jsonfile(cust).update('cart','ad',lis = my_list_get)
 
def sendtxt(msg,cust):
  #return gupshup().sendgupshup( msg,cust)
  return msg



def detect_and_translate(sent):
    try:
      blob = TextBlob(sent)
      print(blob.detect_language())
      return str(blob.translate(to='en'))
    except:
      return sent

def wordnum(s):
    for i in s.split():
        try:
            return (w2n.word_to_num(i)) 
        except:
            pass
    return -1

def find_no(sent,dic):
    try:
      dic.pop('quantity')
    except:
      pass
    k= re.findall(r"[-+]?\d*\.\d+|\d+", sent)
    if k != []:
      try:
        dic['quantity']+=(k)
      except:
        dic['quantity'] = k
    return dic
 
  
######################################################################################################################

class trans():

  def __init__(self):
    pass

  def detect(self,sent):
    translator = google_translator()
    lang_code = translator.detect(sent)
    #print(lang_code)
    return lang_code[0]

  def transi(self,sent,lang_code):
    translator = google_translator()
    print()
    if lang_code == "en":
        #result = translator.translate(sent, lang_src=lang_code ,lang_tgt='mr')
        return sent
    else:
        sen = translator.translate(sent,lang_tgt=lang_code)
        result = translator.translate(sen ,lang_tgt='en')
        return result
      
  def sent_trans(self,sent):
    lc= self.detect(sent)
    new  = self.transi(sent,lc)
    return new




















    




  
