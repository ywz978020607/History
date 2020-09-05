import os

tab = "0608"
start_vid = 800
end_vid = 849
"""
transfer a bunch of png into a y4m video.
very, very fast.
"""
print("\n>>>>>>>>>>>>>>>>>>>>>")
ffmpeg_path = "../ffmpeg-git-20200607-amd64-static/ffmpeg"
for ite_vid in range(start_vid, end_vid+1):
    dir_png = "/home/xql/projects/mls/dataset_png/refine/" + tab + "/mg_refine_%04d" % ite_vid 
    save_path = "/home/xql/projects/mls/dataset_png/refine/" + tab + "/mg_refine_%04d.y4m" % ite_vid
    os.system(ffmpeg_path + " -i "+ dir_png+"/%5d.png" +" -pix_fmt yuv420p -vsync 0 "+save_path+" -y")

"""
zip for transimission. can deflated ~68%
"""
print("\n>>>>>>>>>>>>>>>>>>>>>")
file_list_string = ""
for ite_vid in range(start_vid, end_vid+1):
    file_path = "/home/xql/projects/mls/dataset_png/refine/" + tab + "/mg_refine_%04d.y4m" % ite_vid
    file_list_string += file_path + " "
save_path = "/home/xql/projects/mls/dataset_png/refine/" + tab + "/results_" + tab + ".zip"
os.system("zip -r -j " + save_path + " " + file_list_string)
