import cv2
import dataframe as dfi
import changingvar as cv
from __init__ import *
import requests
import base64
url="https://api.imgbb.com/1/upload"  ### using imgbb

def upload_and_get_link(filename):        ### put address here of image file
    with open(filename, "rb") as file:
        payload = {
            "key": "4a05d0ef6da23523ac0b6c93eb131bb7",
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)    ##3uploading the image
        abc  = res.json()
        return abc['data']['url']        #### get hhtp url of it..

class collage():
    pathcommon = r'{}'.format(dfi.df['image'].iloc[0])
    white = cv2.imread(r'{}\files\IMAGE\white.jpeg'.format(cwd))
    
    def __init__(self):
        pass
    
    def vconcat_resize(self,img_list, interpolation
                                    = cv2.INTER_CUBIC):
            w_min = min(img.shape[1]
                                    for img in img_list)
            im_list_resize = [cv2.resize(img,
                                            (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                                                    interpolation = interpolation)
                                            for img in img_list]
            return cv2.vconcat(im_list_resize)
     
    def hconcat_resize_min(self,im_list, interpolation=cv2.INTER_CUBIC):
        h_min = min(im.shape[0] for im in im_list)
        im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                          for im in im_list]
        return cv2.hconcat(im_list_resize)

    def make(self,my_lis,path):
        lis2 = []
        ken  = len(my_lis)
        if ken%2!=0:
            last = my_lis[-1]
            my_lis = my_lis[:-1]
            for i in range(0,len(my_lis),2):
                h1 = self.hconcat_resize_min([my_lis[i] , my_lis[i+1]])
                lis2.append(h1)
            additional = self.hconcat_resize_min([self.white,last,self.white])
            lis2.append(additional)
            img_v_resize = self.vconcat_resize(lis2)            
        else:
            for i in range(0,len(my_lis),2):
                h1 = self.hconcat_resize_min([my_lis[i], my_lis[i+1]])
                lis2.append(h1)
            img_v_resize = self.vconcat_resize(lis2)
            
        new_path = r"{}\{}".format(path,'pur.jpg')
        cv2.imwrite(new_path , img_v_resize)
        print(new_path)
        return new_path
    
    def collage_for_cat(self,cat):
        df = dfi.df      
        pf = df[df['category']==cat]
        return pf

    def make_it(self,cat):
        pf = self.collage_for_cat(cat)
        #print(pf)
        index = list(pf.index)
        length = len(pf.index)
        my = []
        if cat == "oil":
            img1= cv2.imread(r'{}\oil\fortune.jpg'.format(cwd))
            img2= cv2.imread(r'{}\oil\star.jpg'.format(cwd))
            img3= cv2.imread(r'{}\oil\safola.jpg'.format(cwd))
            img4= cv2.imread(r'{}\oil\gemini.jpg'.format(cwd))

            my = [img1,img2,img3,img4]
        else:
            for i in pf['product']:
                path = cv2.imread(r"{}\files\IMAGE\{}\{}.jpg".format(cwd,cat,i))
                my.append(path)
        print(my)

        pathi = r"{}\{}".format(self.pathcommon,cat)
        #print(pathi)
        return  self.make(my,pathi)
    
    def upload_images(self,subcat,product):
        dic = cv.jsonfile("shop",r"{}\image_urls.json".format(cwd)).read()
        print(dic)
            
        for prod in product:
            df = dfi.df
            pf = df[df['product']==prod]
            image_path = r"{}\files\IMAGE\{}\{}.jpg".format(cwd,pf.loc[list(pf.index)[0],'category'], pf.loc[list(pf.index)[0],'product'])
            #link = .upload_and_get_link(image_path)
            print(image_path)
            dic['shop']['product'][prod] = image_path
            
        print(dic)
        
        for item in subcat:
            #print("ok")
            #print(item)
            dic['shop']['subcat'][item] = self.make_it(item)
            #print(item)
        print(dic,"one///////////////////////////////////////////")
            
        #dic['shop']['subcat']['soap'] = self.make_it(item)
        cv.jsonfile("shop",r"{}\image_urls.json".format(cwd)).add_dict(dic,0)
        print(cv.jsonfile("shop",r"{}\image_urls.json".format(cwd)).read(),"okok")
        return cv.jsonfile("shop",r"{}\image_urls.json".format(cwd)).read()


#obj=collage()
#obj.make_it("soap")
 
def routine():
    #def upload_images(self,subcat,product):
    dic = cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read()
    print(dic)
            
    for prod in dic['shop']['product']:
        dic['shop']['product'][prod] = upload_and_get_link(dic['shop']['product'][prod])
            
    print(dic)
        
    for item in dic['shop']['subcat']:
            #print("ok")
            #print(item)
        dic['shop']['subcat'][item] = upload_and_get_link(dic['shop']['subcat'][item])
            #print(item)
    print(dic,"one///////////////////////////////////////////")
            
        #dic['shop']['subcat']['soap'] = self.make_it(item)
    cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).add_dict(dic,0)
    print(cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read(),"okok")
    return cv.jsonfile("shop",r"{}/image_urls.json".format(cwd)).read()

    
         

 

