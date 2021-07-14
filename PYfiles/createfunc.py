import pandas as pd
import changingvar as cv
import constantfunc as cf
import dataframe as dfi
import collage as cg
import json



    



        

#####    alll the func to fetch the data from  dataframe     ######

 
def update(df = dfi.df):                   #########  update the produtc and its price wala dictionary
    productinfo = {}
    for i in range(len(df)):
        productinfo[df.loc[i+1,'product']] = (df.loc[i+1,'price'])
    return productinfo
 
def category(df = dfi.df):                 ########  get list of categories
    return list(df.category.unique())
                    
def products(df = dfi.df):                 ######## get list of all products
    mk = []
    for i in df["product"]:
        mk.append(i)
    return mk

def prod_for_spec(item , df = dfi.df):      ##### return list of products of specific category
    mk = []
    pf = df[df["category"]==item]
    for i in pf['product']:
        mk.append(i)
    return mk

def company_numberwise(df = dfi.df):        ##### take note of list of categories to reply to Hi.,CAT
    inte = 1
    s = ''
    for i in subcat:
        s += str(inte)+". "+i+"\n"
        inte += 1
    return s

def made_one_line(df = dfi.df):             #### made list of products in subcat
    ss = "code       product       rate(inRs)\n"
    num = 1
    dic = {}
    for i in subcat:
        inte = 1
        for j in prod_for_spec(i,df):
            pfg = i+" "+j
            ss += str(inte)+" "*(9-len(str(inte)))+pfg +" "*(21-len(pfg))+ str(productinfo[j])+" \n"
            inte += 1
        dic[str(num)] = ss
        num += 1
        ss = "code       product       rate(inRs)\n"
    return dic

def find_and_ask(lis , df = dfi.df):         #### to ask questions about quantity
    no1 = int(lis[0])
    no2 = int(lis[1])
    item = subcat[no1 -1]
    m2 = prod_for_spec(item)
    pm =  m2[no2-1]
    
    dfdf = df[df['category']==item]
    dfdfdf = dfdf[dfdf['product']==pm]
    for i in dfdfdf['weight']:
        weight = i
    for i in dfdfdf['subweight']:
        sub = i
    if weight!="0":
        sent = "tell me how much quantity of {} do you want?(in {}/{})".format(pm,weight,sub)
    else:
        sent = "specify,how much quantity of {} {} do you want(like 2 {},3 {})".format(pm,item,item,item)
    return sent
                    
def form_product_cat(df=dfi.df):               #######  to get 'dic1' variable in certai function of cart adding
    dic1 = {}
    for i in range(len(subcat)):
        lis= prod_for_spec(subcat[i])
        for j in range(len(lis)):
            dic1[str(((i+1)*10)+j+1)] = lis[j] +" " + subcat[i]
    return dic1
    
def find_price(cat,product,df = dfi.df):       ######## to find the price of specific product and subcat
    pf = df[df['category']==cat]
    mf = pf[pf['product']==product]
    for i in mf['price']:
        price =  i
    return price

def form_price_dic(df = dfi.df):               #### basically retur the dictionary of prices with string keys like 12,13,24,etc..,
    price_dict = {}
    dic1 = {}
    for i in range(len(subcat)):
        lis= prod_for_spec(subcat[i])
        for j in range(len(lis)):
            dic1[j+1] = int(find_price(subcat[i],lis[j]))
        price_dict[str(i+1)]=dic1
        dic1 = {}
    return price_dict   

###############3   store data in variables     #################################

subcat                                      = category()      
productinfo                                 = update()
company_numberwise_static                   = company_numberwise()
made_one_dic                                = made_one_line()
dic1                                        = form_product_cat()
price_dict                                  = form_price_dic()
product                                     = products()

doc = {"subcat":subcat ,"product":product}
 
try:
    urls = cg.routine()
except:
    print("already passed")





        

