#!/usr/bin env python
import os

##########################################################

pos_image_dir = os.getcwd() + '\\positive_images_resized'  # 正样本样本图片所在目录                       #
neg_image_dir = os.getcwd() + '\\negative_images'  # 负样本样本图片所在目录                       #
img_type = ['jpg', 'png', 'bmp']  # 允许的图片文件类型


##########################################################

def create_pos_info(rootdir):
	files = os.listdir(rootdir)
	name = os.path.split(files[0])
	file_name = 'pos.txt'
	with open(os.getcwd() + '\\' + file_name, 'w+') as f:
		for file in files:
			# name = os.path.split(file)
			if file.endswith(tuple(img_type)):
				print(file)
				f.write(rootdir + '\\' + file + ' ' + '1 0 0 40 40\n')
			else:
				pass


def create_neg_info(rootdir):
	files = os.listdir(rootdir)
	file_name = 'neg.txt'
	with open(os.getcwd() + '\\' + file_name, 'w+') as f:
		for file in files:
			# name = os.path.split(file)
			if file.endswith(tuple(img_type)):
				print(file)
				f.write(rootdir + '\\' + file + '\n')
			else:
				pass


if __name__ == '__main__':
	create_pos_info(pos_image_dir)
	create_neg_info(neg_image_dir)

