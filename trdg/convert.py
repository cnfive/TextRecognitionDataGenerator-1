import os
import shutil
 
source_folder = 'output/data'  # 源文件夹路径，包含图片和对应的文本文件
destination_folder_img = 'result/images'  # 目标文件夹路径
destination_folder_txt = 'result/'
 
# 确保目标文件夹存在
if not os.path.exists(destination_folder_img):
    os.makedirs(destination_folder_img)
 
# 获取源文件夹下所有图片文件
image_files = [f for f in os.listdir(source_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff'))]
 
with open(destination_folder_txt+'\gt.txt', 'w', encoding='utf-8') as file1:
    for image_file in image_files:
    # 获取图片名称和文本名称
         name, _ = os.path.splitext(image_file)
         text_file = f"{name}.txt"  # 假设文本文件和图片同名
 
    # 检查对应的文本文件是否存在
         if os.path.exists(os.path.join(source_folder, text_file)):
        # 读取文本文件内容进行条件判断
                  with open(os.path.join(source_folder, text_file), 'r', encoding='utf-8') as file:
                            content = file.read()
                            # 根据内容决定是否移动图片
                            # if content.strip() == "condition_to_move":
                            # 移动图片到目标文件夹
                            shutil.copy(os.path.join(source_folder, image_file), destination_folder_img)
                            #把文本内容写入到gt.txt

                            file1.write('images/'+image_file+'_____'+content )
 
