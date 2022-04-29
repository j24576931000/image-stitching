import cv2
import numpy as np
from scipy import ndimage
import math


def RANSAC(matching):
    # P=0.99
    # p=0.8
    # n=1
    # k=math.log(1-P)/math.log(1-math.pow(p,n))
    threshold_distance = 3
    # print(len(matching))
    print("......RANSAC......")
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
            #print( diff_total)
            if diff_total < threshold_distance:
                inliner = inliner + 1

        if inliner > max_inliner:
            max_inliner = inliner
            best_shift = shift    
            
    return best_shift



def stitching(best_shift,img,img2):

    print("......stitching......")
    h, w = img2.shape[:2]
    print(best_shift) 
    shifte_img=cv2.warpAffine(img,best_shift,dsize=(img.shape[1]+int(best_shift[0][2]), img.shape[0]+int(best_shift[1][2])),borderValue=(0, 0, 0))
    cv2.imwrite('pre_shift_image.jpg', shifte_img)
    print(shifte_img.shape)
    print(img.shape)
    print(img2.shape)
    pre_shift = np.copy(shifte_img)
    #new_img2,max=blending(shifte_img,img2,int(best_shift[0][2]),w)
    for i in range(0,h):
        for j in range(0,w):
                if shifte_img[i][j][0] == 0 and shifte_img[i][j][1] == 0 and shifte_img[i][j][2] == 0 :
                    shifte_img[i][j][0] = img2 [i][j][0]
                    shifte_img[i][j][1] = img2 [i][j][1]
                    shifte_img[i][j][2] = img2 [i][j][2]
    result = blending(pre_shift,img2,int(best_shift[0][2]),w,shifte_img)
    # cv2.imshow('img', img)
    # cv2.imshow('image2', img2)
    # cv2.imshow('shift_image', result)
    cv2.imwrite('shift_image.jpg', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result



def blending(img1,img2,shift,img2_w,concat_img):

    h, w = img2.shape[:2]

    constant=(img2_w - shift)/2
    center=(img2_w-shift)/2+shift
    print(img2_w - shift)
    a = 1/(center+constant - (center-constant)) 
    b = 0-a*(center-constant)

    # a = 1/(img2_w - shift) 
    # b = 0-a*shift
    for i in range(0,h):
        for j in range(int(center-constant),int(center+constant)):
            for k in range(0,3):
                alpha=a*j+b
                concat_img[i][j][k]=img1[i][j][k]*(alpha)+img2[i][j][k]*(1-alpha)
                #img2[i][j][k]=img2[i][j][k]

    return concat_img


def end2end_align(img,y_shifts ,y_shift_array,x_shift_array):

    avg_y_shift=np.linspace(0,-y_shifts,img.shape[1])
    # print(img.shape[1])
    # print(avg_y_shift)
    # print(x_shift_array)
    align_img = np.copy(img)
    for x in range(img.shape[1]):
        align_img[:,x] = np.roll(img[:,x], int(avg_y_shift[x]), axis=0)
    # total_x_shifts = 0
    # total_y_shifts = 0
    # for i in range(len(x_shift_array)-1,-1,-1):
    #     #for i in range(x_shift_array,img.shape[1]):
            
    #         if i == len(x_shift_array)-1:
    #             align_img[:,0:x_shift_array[i]] = np.roll(img[:,0:x_shift_array[i]], y_shifts, axis=0)
    #             total_x_shifts = total_x_shifts+x_shift_array[i]
                
    #             print(x_shift_array[i])
    #             print(total_x_shifts)
    #         else:
    #             align_img[:,total_x_shifts:total_x_shifts+x_shift_array[i]] = np.roll(img[:,total_x_shifts:total_x_shifts+x_shift_array[i]], y_shifts, axis=0)
    #             total_x_shifts = total_x_shifts+x_shift_array[i]
                
    #             print(x_shift_array[i])
    #             print(total_x_shifts)

    # align_img[:,total_x_shifts:img.shape[1]] = np.roll(img[:,total_x_shifts:img.shape[1]], y_shifts, axis=0)
    return align_img



def crop(img):
    _,thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY)
    
    top = 0
    down =0
    threshold = img.shape[1]//100
    
    for i in range(thresh.shape[0]):
        num = 0
        for j in range(thresh.shape[1]):
            if thresh[i][j] == 0 :
                num =num + 1
        if num < threshold :
            top = i
            break  
    print(top)
    for i in range(thresh.shape[0]):    
        if (len(np.where(thresh[i] == 0)[0]) )< threshold  :
            top = i
            break
    
    for i in range(thresh.shape[0]-1, -1, -1):
        num = 0
        for j in range(thresh.shape[1]):
            if thresh[i][j] == 0 :
                num =num + 1
        if num < threshold :
            down = i
            break  
    print(down)
    for i in range(thresh.shape[0]-1, -1, -1):
        if (len(np.where(thresh[i] == 0)[0])) < threshold:
            down = i
            break
    print(thresh)
    print(top)
    print(down)
    return img[top:down]


