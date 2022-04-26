import cv2
import numpy as np
from scipy import ndimage
import math
def Harris_corner_detector(img):
    cv2.imshow('Image', img)
    img_tmp=np.copy(img)
    w=img.shape[0]
    h=img.shape[1]
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_img, (3, 3), 1.0)
    Ix=cv2.Sobel(blur_image,cv2.CV_64F,1,0,3)
    Iy=cv2.Sobel(blur_image,cv2.CV_64F,0,1,3)

    Ixy=Ix*Iy
    Ixx=np.power(Ix,2)
    Iyy=np.power(Iy,2)

    Sxx=cv2.GaussianBlur(Ixx, (3, 3), 1.5)
    Syy=cv2.GaussianBlur(Iyy, (3, 3), 1.5)
    Sxy=cv2.GaussianBlur(Ixy, (3, 3), 1.5)

    array=np.zeros((2,2), dtype=np.float32)
    corner_response=np.zeros((w,h), dtype=np.float32)
    for i in range(0,w):
        for j in range(0,h):
            array[0][0]=Sxx[i][j]
            array[0][1]=Sxy[i][j]
            array[1][0]=Sxy[i][j]
            array[1][1]=Syy[i][j]
            #print(np.linalg.det(array)-0.04*np.trace(array))*np.trace(array))
            #corner_response[i][j]=np.linalg.det(array)-0.04*np.trace(array)*np.trace(array)
            #print(np.linalg.det(array))
            if np.trace(array)==0:
                 corner_response[i][j]=0
            else:
                corner_response[i][j]=np.linalg.det(array)/np.trace(array)
    print(np.max(corner_response))
    filter_corner_response=ndimage.maximum_filter(corner_response, size=(10,10) )
    result = np.where(filter_corner_response == corner_response, corner_response, 0)
    #np.save('my_array.npy', result)
    print(np.max(result))
    for i in range(0,w):
        for j in range(0,h):
            if result[i][j]<1000 or i+20>w or i-20<0 or j+20>h or j-20<0:
                result[i][j]=0

    for i in range(0,w):
        for j in range(0,h):     
            if result[i][j]!=0 :
                image = cv2.circle(img_tmp, (j,i), 2, (255, 0, 0), 2) 
                

    #cv2.imwrite('circle_image.jpg', image) 
    cv2.imshow('corner_response Image', corner_response)
    cv2.imshow('result', result)
    cv2.imshow('circle_image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result


def description(img,result):
    descriptor = []
    feature_positions = []
    img_tmp=np.copy(img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_img, (3, 3), 4.5)
    blur_gradient_x=cv2.Sobel(blur_image,cv2.CV_64F,1,0)
    blur_gradient_y=cv2.Sobel(blur_image,cv2.CV_64F,0,1)

    h, w = img.shape[:2]
    _, radian = cv2.cartToPolar(blur_gradient_x,blur_gradient_y)
    for i in range(0,h):
        for j in range(0,w):
            if result[i][j]!=0:

                desX = int( i - 10 * math.cos(radian[i,j]) )
                desY = int( j - 10 * math.sin(radian[i,j]) )
                #mark_result = cv2.line(img_tmp, (j, i), (desY, desX), (0, 0, 255), 1)
                rotate_matrix=cv2.getRotationMatrix2D((j,i),180/math.pi*(radian[i,j])*-1,1)
                image_rotation=cv2.warpAffine(src=blur_image,M=rotate_matrix,dsize=(w, h),borderValue=(255, 255, 255),flags=cv2.INTER_NEAREST)
                descriptor_matrix=matrix_cula(image_rotation,i,j)
                descriptor.append(descriptor_matrix)
                feature_positions.append([i,j])

    #cv2.imwrite('mark_result.jpg', mark_result) 
    #cv2.imshow('mark_result', mark_result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return descriptor,feature_positions


def matrix_cula(image_rotate,i,j):

    matrix4040 = image_rotate[i-20:i+20,j-20:j+20]

    matrix88 = np.zeros((8,8), dtype=np.float32)
    for i in range (1,9):
        for j in range (1,9):
            matrix88[i-1][j-1]=(np.sum(matrix4040[(i-1)*5:5*i,(j-1)*5:5*j]))/25

    matrix88=(matrix88-np.mean(matrix88))/np.std(matrix88)
    
    return matrix88

def matching(desc1,desc2):

    matching=[]
    tmp_match_j=[]
    tmp_match_i=[]
    tmp_match_var=[]
    for i in range(len(desc1)):
        now_match=3
        
        for j in range(len(desc2)):
            if math.sqrt(np.sum(np.square(desc1[i]-desc2[j]))) <3 and math.sqrt(np.sum(np.square(desc1[i]-desc2[j])))<now_match:
                now_match = math.sqrt(np.sum(np.square(desc1[i]-desc2[j])))
                match_i=i
                match_j=j
        if now_match!=3 :
            #matching.append([match_i,match_j,now_match])
            if match_j in tmp_match_j  :
                Index = tmp_match_j.index(match_j,0,len(tmp_match_j)-1)
                if now_match < tmp_match_var[Index]:
                    tmp_match_var[Index] = now_match
                    tmp_match_i[Index] = match_i
            else :
                tmp_match_j.append(match_j)
                tmp_match_i.append(match_i)
                tmp_match_var.append(now_match)


                #Min=np.argmin(np.array(tmp_match_var))
    for i in range(len(tmp_match_var)):    
        matching.append([tmp_match_i[i],tmp_match_j[i],tmp_match_var[i]])
    
    return matching


