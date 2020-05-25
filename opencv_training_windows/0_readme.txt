注意：
请确保已安装了opencv-3.4.10-vc14_vc15.exe，并配置好环境变量
1 所有的文件及文件夹路径不要动
2 请使用windows powershell窗口运行.py文件，或者直接运行批处理文件
2 运行批处理文件前请确认已经更改好参数
3 训练完成后分类器文件存放在trained_classifiers文件夹下cascade.xml

步骤：
0 将正样本图片文件放在positive_images文件夹下，将所有负样本图片negative_images文件夹下
1 执行 1_批量重命名、尺寸缩小.bat， 可以看到positive_images_resized文件夹下已经有改变了尺寸的图片
2 执行 2_生成正样本和负样本描述文件.bat ，运行完成后会生成pos.txt文件和neg.txt文件
3 执行 3_创建vec文件、请编辑好参数后运行.bat ，运行完成后会生成pos.vec文件
4 执行 4_开始训练、请编辑好参数后运行.bat ，开始训练
注： 如果已经有正样本图片及标注好的描述文件，无需执行前面两部操作，可以直接执行第三步创建vec文件，执行前确认各文件路径
出现的异常：
