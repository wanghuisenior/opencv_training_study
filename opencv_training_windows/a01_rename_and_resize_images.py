# -*- coding:utf8 -*-
import os
from PIL import Image

'''
批量重命名文件夹中的图片文件，并将其尺寸缩小为40*40像素
将本文件放置于positive_images和negative_images同一目录下使用powershell运行

'''
pos_image_file_path = os.getcwd() + '\\positive_images'
neg_image_file_path = os.getcwd() + '\\negative_images'
resize_path = os.getcwd() + '\\positive_images_resized'
image_tpye = 'png'

if os.path.exists(resize_path):  # 判断resize_path是否存在，不存在则创建，存在则删除文件夹内所有文件
	for item in os.listdir(resize_path):
		os.remove(resize_path + '\\' + item)
else:
	os.mkdir(resize_path)


def rename(path):
	filelist = os.listdir(path)
	total_num = len(filelist)
	i = 0
	for item in filelist:
		if item.endswith('.' + image_tpye):
			src = os.path.join(os.path.abspath(path), item)
			dst = os.path.join(os.path.abspath(path), str(i) + '.' + image_tpye)
			try:
				os.rename(src, dst)
				# print('重命名 %s   为   %s' % (src, dst))
				i = i + 1
			except:
				continue
	print(path + ':重命名 %d 张图' % (total_num))


def resize_img(path):
	'''
	批量修改图片尺寸
	'''
	# 提取目录下所有图片,更改尺寸后保存到另一目录
	import os.path
	import glob

	def convertjpg(jpgfile, outdir, width=40, height=40):
		img = Image.open(jpgfile)
		try:
			new_img = img.resize((width, height), Image.BILINEAR)
			new_img.save(os.path.join(outdir, os.path.basename(jpgfile)))
		except Exception as e:
			print(e)

	i = 0
	for jpgfile in glob.glob(path + "\\*." + image_tpye):
		# 像素修改后存入images文件
		convertjpg(jpgfile, resize_path)
		i += 1
	print('改变尺寸%d张图' % i)


if __name__ == '__main__':
	rename(neg_image_file_path)
	rename(pos_image_file_path)
	resize_img(pos_image_file_path)