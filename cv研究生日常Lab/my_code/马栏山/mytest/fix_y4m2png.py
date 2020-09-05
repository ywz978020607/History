import os

y4m_temp_path = "/media/x/Database/mls/dataset/train_damage_part1/mg_train_0040_damage.y4m"
png_path_index3 = "/media/x/Database/mls/dataset_png/train_damage_part1/mg_train_0040_damage/blur"

os.system("ffmpeg -i "+y4m_temp_path + " -vsync 0 "+ png_path_index3 +"/%4d.png -y")

