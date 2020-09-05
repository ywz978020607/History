# run_vmaf 已经是可执行的cmd命令


#用法1  single mode
# #run_vmaf format width height reference_path distorted_path [--out-fmt output_format]
run_vmaf yuv420p 416 240 \
  Videos/ori/BasketballPass_416x240_500.yuv \
  Videos/cmp/BasketballPass_416x240_500.yuv   \
  --out-fmt json


##
cd mls_code_test/vmaf/
sudo run_vmaf yuv420p 416 240  Videos/ori/BasketballPass_416x240_500.yuv  Videos/cmp/BasketballPass_416x240_500.yuv    --out-fmt json


run_vmaf yuv420p 416 240  Videos/ori/BasketballPass_416x240_500.yuv  Videos/cmp/BasketballPass_416x240_500.yuv    --out-fmt json

run_vmaf yuv420p 1920 1080  /media/x/Database/mls/fusion_ori_out/ori_yuv/val_damage_part1/mg_val_0600_damage.yuv  /media/x/Database/mls/fusion_ori_out/ori_fusion/val_damage_part1/mg_val_0600_damage.yuv    --out-fmt json




###################

from vmaf_func import *
out_json_path = "./"
# model_path = "~/mls_code_test/vmaf/model"
vmaf_json("yuv420p",1920,1080,"/media/x/Database/mls/fusion_ori_out/ori_yuv/val_damage_part1/mg_val_0600_damage.yuv","/media/x/Database/mls/fusion_ori_out/ori_fusion/val_damage_part1/mg_val_0600_damage.yuv",out_json_path)



###
#load json
import json
f = open("test.json",'w')
myjson = json.loads(f.read())
f.close()


##
#psnr ffmpeg
ffmpeg -s 1920x1080 -i out.yuv -s 1920x1080 -i out.yuv -lavfi psnr="stats_file=psnr.log" -f null -


#png直接转y4m
ffmpeg -i xx%3d.bmp  -pix_fmt yuv420p  -vsync 0 xx.y4m -y







#################

# ywz0: 脚本转换数据
# ywz2: fusion_change 转换/转yuv
# ywz3: fusion_vmaf_out 输出vmaf对比
# ywz4: fusion_psnr_out 输出psnr对比

# ywz5: 查看数据盘内容

