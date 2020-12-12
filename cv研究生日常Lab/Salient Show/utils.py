import numpy as np
import cv2

im_path = 'ori.jpg'
img_path = 'out1.jpg' #map
save_path = "heat.jpg"


def save_heat(im_path,img_path,save_path):
    im = cv2.imread(im_path, 1)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    img = cv2.imread(img_path, 1)
    ground_hmap = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ground_hmap = ground_hmap/np.max(ground_hmap)*255
    ground_hmap = np.array(ground_hmap,np.uint8)
    ground_hmap = cv2.applyColorMap(ground_hmap,cv2.COLORMAP_JET)
    alpha = 0.4
    heat_image = cv2.addWeighted(ground_hmap,alpha,im,1-alpha,0)

    cv2.imwrite(save_path,heat_image)
    # cv2.imwrite("demo.jpg",im)



if __name__ == "__main__":
    save_heat(im_path,img_path,save_path)