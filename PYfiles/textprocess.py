import en_core_web_sm
import spacy
from google_trans_new import google_translator
import re
from word2number import w2n
import changingvar as cv
import constantfunc as cf
import createfunc as crf
import re
import random
import pandas as pd
import dataframe as dfi
import time
from nltk.stem import WordNetLemmatizer
from __init__ import *

##############################   DATAFRAME AND CONSTANT THING   ################################################
df          =  dfi.df
my          =  cv.jsonfile("ok",r'{}/intent_words.json'.format(pwd)).read()
json_dict   =  cv.jsonfile("ok",r'{}/permanentw.json'.format(pwd)).read()
               
###########################################   VARIABLE   #########################################################################


#############################################################################################################################
                    
                
                    
    
####### #############    extract and respond to queries

class text_mining():
    
    def __init__(self,cust,record_each = [{'enquiry': ['do']}], record_orders = [],state = ['e0'] ):
        self.record_orders = record_orders
        self.record_each   = record_each
        self.cust          = cust
        self.state         = state
        
    def find(self,val):
        global my
        val = WordNetLemmatizer().lemmatize(val)
        dikt = {}
        for i in my:
            if val in my[i]:
                return [i , val]
        else:
            dic = my
            cnt = my['unrecogn']['cnt']
            try:
                dic[cnt].append(val)
            except:
                dic[cnt] = [val]
            my = dic
            print(val)
            return -1

    def match(self,sent):
        global my
        sent = re.sub(r'[^\w\s]', ' ', sent)
        dikt = {}
        for i in sent.split():
            kval = self.find(i)
            if kval != -1:
                try:
                    dikt[kval[0]].append(kval[1])
                except:
                    dikt.update({kval[0]:[kval[1]]})
            #else:
                
        else:
            my['unrecogn']['cnt']  += 1
            cv.jsonfile('ok',r'{}/intent_words.json'.format(cwd)).add_dict(my,0)
            dikt = cf.find_no(sent,dikt)
            return (dikt)
            

    def response_tree(self,my):
        if 'enquiry' in my:
            if 'product' in my:
                if 'price' in my:
                    if 'weight' in my:
                        return 'e4'
                    else:
                        return 'e3'
                else:
                     return 'e2'
            else:
                return 'e1'
        else:
            if 'order' in my:
                if 'product' in my:
                    if 'quantity' in my:
                        if 'weight' in my:
                            return 'o4'
                        else:
                            return 'o3'
                    else:
                        return 'o2'
                else:
                    return 'o1'  
            else:
                if 'change' in my:
                    if 'product' in my:
                        if 'quantity' in my:
                            return 'r3'
                        else:
                            return 'r2'
                    else:
                        return "r1"
                else:
                    return "e0"

 

    def hifunc(self,arg):
        if 'hi' == arg:
            cv.jsonfile(self.cust).update('pot','hi')
            return  cf.sendtxt(cf.switch1("Hi"),self.cust)

        elif "cat" in arg:
            cv.jsonfile(self.cust).update('pot','hi')
            if cv.jsonfile(self.cust).update('contacts','check')==1:
                return cf.switch1("Hi")
            else:
                return cf.switch("Hi2.0")
            
        elif "cart" in arg:
            sp = cv.jsonfile(self.cust).update('cart','r')
            if sp== {"0":[]}:
                return "your cart is empty \njust send *Hi* and add items in your cart"
            else:
                return "your cart till now\n"+cf.show_table(sp,self.cust)+"\nTOTAL : " + str((cv.jsonfile(self.cust).update('total','r'))/2) + "\n\nuse /PLACE : to confirm the order and proceed to pay"
                
        elif "place" in arg :
            cv.jsonfile(self.cust).update('mainDB','ap',cv.jsonfile(self.cust).update('pot','r'))
            mpl = cv.jsonfile(self.cust).update('cart','r')

              
            curr_time = time.localtime()
            timei = time.strftime("%H:%M:%S", curr_time)
            mlh = {self.cust:{timei:mpl}}
            cv.jsonfile(self.cust,r'{}/complete_orders.json'.format(cwd)).add_dict( mlh )
            print('omomomomom')
            cv.jsonfile(self.cust).update('pot','null')
            cv.jsonfile(self.cust).update('pot1','null')
            net = cv.jsonfile(self.cust).update('total','r')
            cv.jsonfile(self.cust).update('total','null')
            if mpl ==  {"0":[]}:
                return cf.sendtxt("you cannot place the order as you dont have any items in your cart",self.cust )
            else:
                cv.jsonfile(self.cust).update('cart','null')
                return "thanks for shopping with us\n" + cf.show_table(mpl,self.cust) + "\nTOTAL : "+str(net/2)+"\nYour order will be delivered by half-hour,..\nvist the E- mart again...!!"
        else:
            return 0
        
    def execute(self,states):
        self.state.append(states)
        obj = self
        try:
            cur_rec  = obj.record_each[-1]
            prev_rec = obj.record_each[-2]
            if self.decide_state() == 1:
                cur_rec.update(prev_rec)
                if 'order' in cur_rec:
                    if 'enquiry' in cur_rec:
                        cur_rec.pop('enquiry')
                new_state = obj.response_tree(cur_rec)
                self.state[-1] = new_state
                return new_state
            else:
                return states
        except:
            return states
        
    def decide_state(self):
        current  = int(self.state[-1][-1])
        prev     = (self.state[-2])
        #print(current)
        if prev == 'o4' or prev == "o3" or prev[0] == "c":
            return 0
        if  current < 2:
            return 1
        else:
            cur_rec  = self.record_each[-1]
            prev_rec = self.record_each[-2]
            
            if cur_rec['product']==prev_rec['product']:
                return 1
            else:
                return 0

            

    def item_add(self):
        dic = self.record_orders[-1]
        a= dic['product'][0]
        b= dic['quantity'][0]
        c= dic['price'][0]
        net = float(b)*float(c)
        if 'weight' in dic:
            if dic['weight'][0] in ['grams','mililitres', 'gram','ml','mls','gms','gm','grm' ]:
                net = net / 1000
                b+="X"+dic['weight'][0]
                print(net)
            else:
                pass
            
        pl = [a,b,str(net)]
        print(pl,"gramsssssssssssssssssssssssssssssssssssssssssssssssssss")
        cv.jsonfile(self.cust).update('cart','ad',lis = pl)
        double = net*2
        cv.jsonfile(self.cust).update('total','ad',num=double)
      
    


class respond_to_change(text_mining):
    
    def change(self,my):
        responses = {'1':"you didnt specified the product",
                     '2':"plz specify the product in cart that you want to change"
                     }
        print(0)
        return responses[str(random.randrange(1,3))]
        

    def change_prod(self,my):
        responses = {'1':"your product {} is removed from CART",
                     '2':"ok, {} is removed from the cart successfully"
                     }
        print(0)
        cart = cv.jsonfile(self.cust).update('cart','r')
        print("cart",cart)
        for i in cart:
            if my['product'][0] in cart[i]:
                price = float(cart[i][-1])*2
                cart.pop(i)
                cv.jsonfile(self.cust).update('cart','ad_dic',dict1=cart)
                cv.jsonfile(self.cust).update('total','ad',num = -price)
                
                self.record_orders=self.record_orders[:-1]
                
                #cart = cv.jsonfile(self.cust).update('cart','r')
                #print("cart",cart)
                return responses[str(random.randrange(1,3))].format(my['product'][0])
        else:
            return "product was not added in the cart"

    def change_quan(self,my):
        responses = {'1':"okk quantity for {} is now {} as per your deemand",
                     '2':"your order to make {} of quantity {} is noted and added to the cart"
                     }
        cart = cv.jsonfile(self.cust).update('cart','r')
        
        pf=df[df['product']== my['product'][0]]
        price = float(pf.loc[list(pf.index)[0],'price'])
        
        if 'weight' in my:
            truth = 1
            if my['weight'] in ['gram','grm','ml','mililitre']:
                subwt = 1
            else:
                subwt = 0
        else:
            truth = 0

        
        for i in cart:
            if my['product'][0] in cart[i]:
                initial_pce = float(cart[i][-1])
                if truth == 1:
                    cart[i][1] = my['quantity'][0] + " " + my['weight'][0]
                    if subwt == 1:
                        price*=float(my['quantity'][0])/1000
                    else:
                        price*=float(my['quantity'][0])
                else:
                    cart[i][1] = my['quantity'][0]
                    price*=float(my['quantity'][0])
                cart[i][-1]=str(price)
                s = cart[i][1]

                netchange = (price - initial_pce)*2
                cv.jsonfile(self.cust).update('cart','ad_dic',dict1=cart)
                cv.jsonfile(self.cust).update('total','ad',num = netchange)
                
                self.record_orders=self.record_orders[:-1]
                cart = cv.jsonfile(self.cust).update('cart','r')
                print("cart",cart)
                return responses[str(random.randrange(1,3))].format(my['product'][0],s)
        else:
            return "invalid"



        
class respond_to_order(text_mining):
    
    def order(self,my):
        responses = json_dict['o1']
        return responses[str(random.randrange(1,5))]
    
    def quan(self,miy):
        responses = json_dict['o2']
        return responses[str(random.randrange(1,5))].format(miy['product'][0])
    
    def weight(self,my):
        print(my,"hddashkhdadh")
        pf = df[df['product']==my['product'][0]]
        weight =  str(pf.loc[list(pf.index)[0],'weight'])
        if weight == '0':
            my.update({'weight':[0]})
            return self.get('o4',my)
        else:
            responses = json_dict['o3']
            return responses[str(random.randrange(1,2))]
        
    def cart(self,my):
        print(my)
        pf = df[df['product']==my['product'][0]]
        print(pf)
        stock =  str(pf.loc[list(pf.index)[0],'stock'])
        price =  str(pf.loc[list(pf.index)[0],'price'])
        my.update({'price':[price]})
        if stock != "0":
            self.record_orders.append(my)
            self.record_each = []
            print("empty")
            responses = json_dict['o4']
            self.item_add()
            dic = cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read()
            path = dic['shop']['product'][my['product'][0]]
            updated = responses[str(random.randrange(1,5))] + "\n\n use /CART : to view ordered items. "
            return [ path, updated ]
        else:
            responses = json_dict['e2_else']
            return responses[str(random.randrange(1,5))].format(my['product'][0])

         

class respond_to_enquiry(text_mining):

    def enquiry(self,my):
        if 'subcat' in my:
            pf = df[df['category']==my['subcat'][0]]
            index= pf.loc[list(pf.index)[0],'srno']
            dic = cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read()
            path = dic['shop']['subcat'][my['subcat'][0]]
            return [path , "yes here are the products in the {} category".format(my['subcat'][0])+"\n"+ cf.switch1(str(index))]
        else:
            responses = json_dict['e1']
            return responses[str(random.randrange(1,5))]
    
    def equan(self,my):
        pf = df[df['product']==my['product'][0]]
        stock =  str(pf.loc[list(pf.index)[0],'stock'])
        prod = str(pf.loc[list(pf.index)[0],'product'])
        if stock != "0":
            responses = json_dict['e2_if']
            dic = cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read()
            path = dic['shop']['product'][prod]
            return [path,responses[str(random.randrange(1,5))].format(my['product'][0])]
        else:
            responses = json_dict['e2_else']
            return responses[str(random.randrange(1,5))].format(my['product'][0])
        
    def eprice(self,my):
        pf     =  df[df['product']==my['product'][0]]
        price  =  str(pf.loc[list(pf.index)[0],'price'])
        weight =  str(pf.loc[list(pf.index)[0],'weight'])
        
        if 'quantity' in my:
            if weight != "0":
                responses = json_dict['e3_if_1']
                net = float(price) * float(my['quantity'][0])
                return responses[str(random.randrange(1,5))].format(my['quantity'][0],weight,my['product'][0], str(net) )
            else:
                responses = json_dict['e3_else_1']
                net = float(price) * float(my['quantity'][0])
                return responses[str(random.randrange(1,5))].format(my['quantity'][0],my['product'][0], str(net) )
        else:
            if weight != "0":
                responses = json_dict['e3_if_2']
                net = float(price) * 1.0
                return responses[str(random.randrange(1,5))].format("1",weight,my['product'][0], str(net) )
            
            else:
                responses = json_dict['e3_else_2']
                net = float(price) * 1.0
                return responses[str(random.randrange(1,5))].format( "1" ,my['product'][0], str(net))
        
    def ecart(self,my):
        return "yes ecart is happening"

    def check_if_mixing(self,my):
        #s=  self.hinfunc(
        #if re.group(s,msg)
        return 0
    
 
 
            
class combine(respond_to_order,respond_to_enquiry,respond_to_change):
    
    def get(self,arg,my_dict):
        res_json = {
                    'o1':self.order,
                    'o2':self.quan,
                    'o3':self.weight,
                    'o4':self.cart,
                    'e1':self.enquiry,
                    'e2':self.equan,
                    'e3':self.eprice,
                    'e4':self.ecart,
                    'r1':self.change,
                    'r2':self.change_prod,
                    'r3':self.change_quan,
                    "e0":self.check_if_mixing,
                }
        if arg=='e0':
            return self.check_if_mixing(my_dict)
        else:
            return res_json[arg](my_dict) 
        
    def ans_que(self, pitch):
        s = self.hifunc(pitch)
        if s!=0:
            return s
        else:
            mai  = self.match(pitch)
            self.record_each.append(mai)
            mac  = self.response_tree(mai)
            print(mac)
            #mac =  self.execute(mac)
            #print(mac)
            mac  = self.get(mac,mai)
            print(self.state)
            return mac
 
     

######################################################   below part is for practice purpose   #############
                                             
def find():
    obj = combine("MayureshKhanaj")
    while 1:
        que = input("ask: ")                                
        print(obj.ans_que(que))
         
#find()

######################################################################   upto this ####################
 


 
