信用卡数字识别   
方法就是用模版数字与信用卡上的数字做匹配，赋值匹配度高的    
代码每一步都注释的很详细
先导入模版图片，检测轮廓，将每个模版数字分离出来并排序，过程如下：    
1、导入模版图片
![image](https://github.com/user-attachments/assets/2383c3b5-48a4-46cd-8b6b-df98f7e2ff7c) 
2、灰度处理
![image](https://github.com/user-attachments/assets/faadf852-7865-4476-9a06-a8207969e22b) 
3、二值处理
![image](https://github.com/user-attachments/assets/f4e1a368-4b35-484f-8025-3bfb81ebf013) 
4、画外轮廓
![image](https://github.com/user-attachments/assets/e0bb2744-2380-45b2-a41a-a8ea4337b034) 
5、分离轮廓并排序存储    
这里不展示了，大家可以在代码里面debug    

导入银行卡，对银行卡处理将数字拎出来，然后对数字一一匹配     
1、导入银行卡     
![image](https://github.com/user-attachments/assets/ad8eee54-6173-4f8d-91a7-16dc6ef7b110)

2、将银行卡size调小并灰度处理    
![image](https://github.com/user-attachments/assets/5cdf9538-ba7b-413f-99e8-c851d06ce13c)


3、礼帽处理，突出图像中比背景亮的小区域     
![image](https://github.com/user-attachments/assets/34c283ac-261f-4419-a677-5cc126fd3d8c)
 

4、Sobel算子处理     
![image](https://github.com/user-attachments/assets/4ac7c26c-5c98-4914-bc08-b0be57942a6f)

5、闭运算，将数字糊一块     
![image](https://github.com/user-attachments/assets/7c0f44dd-f165-4306-9290-cd30c68ad1c3)

 
6、二值处理     
![image](https://github.com/user-attachments/assets/8b3420d7-8537-406d-a266-518199160087)


7、画出轮廓     
![image](https://github.com/user-attachments/assets/9f653d9e-7ff3-4b97-ae1e-67a38cbc9169)
  

8、提取数字轮廓并画外接矩阵，给数字框起来，然后给二值处理。对框里的数字做模版数字一样的活，让进行一一匹配    
这里不展示了，大家在代码里debug，图太小了    
9、最终效果图    
![image](https://github.com/user-attachments/assets/b2f2122b-b7bb-4109-b9b2-24f18e985af7) 

你们换别的信用卡图的时候会发现有点小bug，留给你们自己当练习了，怎么给它调好（绝对不是我懒得搞了）







