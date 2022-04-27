import feature
import stitch
import projection
import cv2
import numpy as np
import os



if __name__=='__main__':
    #read data
    img_list=[]
    result_list=[]
    
    for filename in os.listdir(r"./" + 'data/data'):
        img_list.append(filename)
        print(filename)


    focallength = [667.563, 667.531, 667.425, 670.312, 668.788, 669.267, 669.961, 670.828, 671.558]
    best_shift_x = []
    best_shift_y = []
    totol_y_shifts = 0
    for i in range(0,len(img_list)):
        print(i)
        if i == 0:
            oper_img1 = img_list[i]
            oper_img2 = img_list[i+1]
        elif i == 1:
            continue
        else :
            oper_img2 = img_list[i]
        if i == 0:
            data_img = cv2.imread(os.path.join('data/data',oper_img1))#讀取圖片
            data_img=cv2.resize(data_img,(data_img.shape[1]//10,data_img.shape[0]//10), interpolation=cv2.INTER_AREA)
            cv2.imwrite('resize.jpg', data_img)
            data_img = projection.projection(data_img,focallength[i])
            #data_img = stitch.crop(data_img)
            cv2.imwrite('projection.jpg', data_img)
        else :
            data_img = oper_img1
        result=feature.Harris_corner_detector(data_img)  
        desc,pos=feature.description(data_img,result)

        data_img2 = cv2.imread(os.path.join('data/data',oper_img2))#讀取圖片
        data_img2=cv2.resize(data_img2,(data_img2.shape[1]//10,data_img2.shape[0]//10), interpolation=cv2.INTER_AREA)
        cv2.imwrite('resize.jpg', data_img2)
        if i > 1 :
            data_img2 = projection.projection(data_img2,focallength[i])
            #data_img2 = stitch.crop(data_img2)
            cv2.imwrite('projection.jpg', data_img2)
        else:
           data_img2 = projection.projection(data_img2,focallength[i+1])
           #data_img2 = stitch.crop(data_img2)
           cv2.imwrite('projection.jpg', data_img2)
        result2=feature.Harris_corner_detector(data_img2)  
        desc2,pos2=feature.description(data_img2,result2)

            # for i in range(0,0):
            #     data_img=cv2.resize(data_img,None,fx=2,fy=2,interpolation=cv2.INTER_AREA)
            #     result=feature.Harris_corner_detector(data_img)  
            #     print(result)

        match=feature.matching(desc,desc2)

        # data_img = cv2.imread(os.path.join('data/grail',img_list[0]))#讀取圖片
        # data_img2 = cv2.imread(os.path.join('data/grail',img_list[1]))#讀取圖片
        tmp1=pos
        tmp2=pos2
        #concat=cv2.hconcat([data_img, data_img2])

        feature_matrix=[]
        for i in range(len(match)):
            #image = cv2.circle(data_img, (tmp1[match[i][0]][1],tmp1[match[i][0]][0]), 2, (255, 0, 0), 2) 
            #image2 = cv2.circle(data_img2, (tmp2[match[i][1]][1],tmp2[match[i][1]][0]), 2, (255, 0, 0), 2)     
            #mark_result = cv2.line(concat, (tmp1[match[i][0]][1], tmp1[match[i][0]][0]), ((data_img.shape[1])+tmp2[match[i][1]][1], tmp2[match[i][1]][0]), (0, 0, 255), 1)
            feature_matrix.append([i,tmp1[match[i][0]][0],tmp1[match[i][0]][1],tmp2[match[i][1]][0],tmp2[match[i][1]][1]])
        
        #print(feature_matrix)
        final_feature=np.array(feature_matrix)
        #np.save('feature.npy', final_feature)

        
        best_shift_matrix=stitch.RANSAC(final_feature)
        
        totol_y_shifts=totol_y_shifts+best_shift_matrix[1][2]

        best_shift_x.append(int(best_shift_matrix[0][2]))
        best_shift_y.append(int(best_shift_matrix[1][2]))
        result = stitch.stitching(best_shift_matrix,data_img,data_img2)

        oper_img1 = result

        # cv2.imshow('concat', oper_img1)
        #cv2.imwrite('write.jpg', mark_result)
        # # #cv2.imshow('concat2', image2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    #result = cv2.imread(os.path.join('data/data2',img_list[0]))#讀取圖片

    #totol_y_shifts=58

    #align_img = stitch.end2end_align(result,totol_y_shifts,best_shift_y,best_shift_x)

    #final = stitch.crop(result)
    final = result[int(totol_y_shifts)+5:305,:]
    cv2.imwrite('result.jpg', final)

    

        

    
