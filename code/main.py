import feature
import stitch
import cv2
import numpy as np
import os


if __name__=='__main__':
    #read data
    img_list=[]
    result_list=[]
    for filename in os.listdir(r"./" + 'data/grail'):
        img_list.append(filename)
        print(filename)

    #print(len(img_list))
    
    Decs=[]
    Pos=[]
    for i in range(0,len(img_list)):
        data_img = cv2.imread(os.path.join('data/grail',img_list[i]))#讀取圖片
        result=feature.Harris_corner_detector(data_img)  
        print(result)
        desc,pos=feature.description(data_img,result)
        print(len(desc))
        Decs.append(desc)
        Pos.append(pos)
        # for i in range(0,0):
        #     data_img=cv2.resize(data_img,None,fx=2,fy=2,interpolation=cv2.INTER_AREA)
        #     result=feature.Harris_corner_detector(data_img)  
        #     print(result)

    match=feature.matching(Decs[0],Decs[1])
    #print(Decs[0][0])
    #print(Pos[0][0])
    #print(match)
    data_img = cv2.imread(os.path.join('data/grail',img_list[0]))#讀取圖片
    data_img2 = cv2.imread(os.path.join('data/grail',img_list[1]))#讀取圖片
    tmp1=Pos[0]
    tmp2=Pos[1]
    concat=cv2.hconcat([data_img, data_img2])
    #print(Pos[0][match[0][0]])
    #print(data_img.shape[0])
    feature_matrix=[]
    for i in range(len(match)):
        print(i)
        #image = cv2.circle(data_img, (tmp1[match[i][0]][1],tmp1[match[i][0]][0]), 2, (255, 0, 0), 2) 
        #image2 = cv2.circle(data_img2, (tmp2[match[i][1]][1],tmp2[match[i][1]][0]), 2, (255, 0, 0), 2)     
        mark_result = cv2.line(concat, (tmp1[match[i][0]][1], tmp1[match[i][0]][0]), ((data_img.shape[1])+tmp2[match[i][1]][1], tmp2[match[i][1]][0]), (0, 0, 255), 1)
        feature_matrix.append([i,tmp1[match[i][0]][0],tmp1[match[i][0]][1],tmp2[match[i][1]][0],tmp2[match[i][1]][1]])
    
    print(feature_matrix)
    final_feature=np.array(feature_matrix)
    np.save('feature.npy', final_feature)


    best_shift_matrix=stitch.RANSAC(final_feature,data_img,data_img2)

    stitch.stitching(best_shift_matrix,data_img,data_img2)


    print(best_shift_matrix)
    cv2.imshow('concat', mark_result)
    cv2.imwrite('write.jpg', mark_result)
    #cv2.imshow('concat2', image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

        

    
