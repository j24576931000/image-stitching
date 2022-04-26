import cv2
import numpy as np
from scipy import ndimage
import math


def RANSAC(matching,img,img2):
    # P=0.99
    # p=0.8
    # n=1
    # k=math.log(1-P)/math.log(1-math.pow(p,n))
    threshold_distance=3
    # print(len(matching))
    print('matching')
    best_shift=[]
    #print(matching)
    max_inliner = 0
    #for i in range(0,math.floor(k)):
    for j in range(0,len(matching)):
        inliner = 0
        m1 = abs(matching[j][1]-matching[j][3])
        m2 = abs(matching[j][2]-matching[j][4])
        shift = np.asarray([[1,0,m2],[0,1,m1]],dtype=np.float32)


        for d in range(0,len(matching)):
            diff_total=0
            diff= math.sqrt((matching[d][3]-m1-matching[d][1])**2+(matching[d][4]-m2-matching[d][2])**2)
            diff_total=diff_total+diff
            print( diff_total)
            if diff_total < threshold_distance:
                inliner = inliner + 1

        if inliner > max_inliner:
            max_inliner = inliner
            best_shift = shift
        
    return best_shift



def stitching(best_shift,img,img2):

    h, w = img2.shape[:2]
    print(best_shift)
    
    shifte_img=cv2.warpAffine(img,best_shift,dsize=(w+int(best_shift[0][2]), h+int(best_shift[1][2])),borderValue=(0, 0, 0))
    cv2.imwrite('pre_shift_image.jpg', shifte_img)
    print(shifte_img.shape)
    print(img.shape)
    print(img2.shape)
    pre_shift = np.copy(shifte_img)
    #new_img2,max=blending(shifte_img,img2,int(best_shift[0][2]),w)
    new_img2=img2
    for i in range(0,h):
        for j in range(0,w):
                if shifte_img[i][j][0] == 0 and shifte_img[i][j][1] == 0 and shifte_img[i][j][2] == 0 :
                    shifte_img[i][j][0] = new_img2 [i][j][0]
                    shifte_img[i][j][1] = new_img2 [i][j][1]
                    shifte_img[i][j][2] = new_img2 [i][j][2]

    new_img2=blending(pre_shift,img2,int(best_shift[0][2]),w,shifte_img)

    cv2.imshow('img', img)
    cv2.imshow('image2', new_img2)
    cv2.imshow('shift_image', shifte_img)
    cv2.imwrite('shift_image.jpg', shifte_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 0



def blending(img1,img2,shift,img2_w,concat_img):

    h, w = img2.shape[:2]

    constant=65
    center=(img2_w-shift)/2+shift
    print(img2_w - shift)
    # print(int(center+constant))

    # print(h)
    # print(w)

    a = 1/(center+constant - (center-constant)) 
    b = 0-a*(center-constant)
    print(concat_img.shape)
    print(img1.shape)
    print(img2.shape)
    # a = 1/(img2_w - shift) 
    # b = 0-a*shift
    # alpha=a*(center-constant)+b
    # print(alpha)
    # alpha=a*(center+constant)+b
    # print(alpha)
    # alpha=a*(center)+b
    # print(alpha)
    #img1[center,center+constant:]
    for i in range(0,h):
        for j in range(int(center-constant),int(center+constant)):
            for k in range(0,3):
                alpha=a*j+b
                concat_img[i][j][k]=img1[i][j][k]*(alpha)+img2[i][j][k]*(1-alpha)
                #img2[i][j][k]=img2[i][j][k]


    return img2