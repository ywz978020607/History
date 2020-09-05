import os
import cv2

#win y4m->png
def func0():
    y4m_temp_path = "mg_test_0888_damage.y4m"
    png_path_index3 = y4m_temp_path.split('.')[0]
    if not os.path.exists(png_path_index3):
        os.system("mkdir "+png_path_index3)
    ffmpeg_path = "E:\\software\\ffmpeg\\bin\\ffmpeg.exe"
    os.system(ffmpeg_path+" -i "+y4m_temp_path + " -vsync 0 "+ png_path_index3 +"/%4d.png -y")

def func1():
    img_path = "mg_test_0888_damage/0001.png"
    img = cv2.imread(img_path)

