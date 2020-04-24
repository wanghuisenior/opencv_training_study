::请修改下面的三个参数为 训练使用的正样本数量:总数的%85  ，使用负样本的数量 大约为正样本的三倍， 宽， 高
opencv_traincascade.exe -data trained_classifiers -vec pos.vec -bg neg.txt -numPos 85 -numNeg 240 -w 40 -h 40 -numStages 15 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -mode ALL 
pause
