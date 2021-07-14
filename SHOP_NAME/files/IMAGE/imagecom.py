import cv2


class collage():
    pathcommon = r'C:\Users\hp\repo\whatsnew-main\newrepo\files\IMAGE\{}\{}'
    white = cv2.imread(r'C:\Users\hp\repo\whatsnew-main\newrepo\files\IMAGE\white.jpeg')
    
    def __init__(self):
        pass
    
    def vconcat_resize(self,img_list, interpolation
                                    = cv2.INTER_CUBIC):
            # take minimum width
            w_min = min(img.shape[1]
                                    for img in img_list)
            
            # resizing images
            im_list_resize = [cv2.resize(img,
                                            (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                                                    interpolation = interpolation)
                                            for img in img_list]
            # return final image
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
            new_path = path.format('purnin.jpg')
            cv2.imwrite(new_path , img_v_resize)
            
        else:
            for i in range(0,len(my_lis),2):
                h1 = self.hconcat_resize_min([my_lis[i], my_lis[i+1]])
                lis2.append(h1)
            img_v_resize = self.vconcat_resize(lis2)
            new_path = path.format('purnin.jpg')
            cv2.imwrite(new_path , img_v_resize)
 
        self.pathcommon = r'C:\Users\hp\repo\whatsnew-main\newrepo\files\IMAGE\{}\{}'
        return new_path
    
    def collage_for_cat(self,cat):
        df = dfi.df     #pd.read_csv(r'C:\Users\hp\Downloads\tejascollage.csv')  ### me pathavaleli file
        pf = df[df['category']==cat]
        return pf

    def make_it(self,cat):
        pf = self.collage_for_cat(cat)
        print(pf)
        index = list(pf.index)
        length = len(pf.index)
        my = []
        for i in pf['product']:
            path = r"C:\Users\hp\repo\whatsnew-main\newrepo\files\IMAGE\{}\{}.jpg".format(cat,i)
            my.append(i)
        print(my)
        pathi = self.pathcommon.format(cat)
        return  self.make(my,pathi)
 
 
        
 
collage().make_it(makei)
