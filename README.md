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
![image](https://github.com/user-attachments/assets/c2df7408-afe0-4ffa-b1c7-1ac81ac6dd31)
2、将银行卡size调小并灰度处理    
![image](https://github.com/user-attachments/assets/59ca63f6-697e-40f4-b57b-61661fe9cb5a)
3、礼帽处理，突出图像中比背景亮的小区域    
![image](https://github.com/user-attachments/assets/a04ecc4b-210f-4bf5-992e-8fec7d42364c)
4、Sobel算子处理    
![image](https://github.com/user-attachments/assets/c4ffe5aa-b3e4-4174-8672-670ab097c7fb)
5、闭运算，将数字糊一块    
![image](https://github.com/user-attachments/assets/e86a5a52-c56f-4322-ae1d-b6af4394d20f)
6、二值处理    
![image](https://github.com/user-attachments/assets/be1f3ff2-05ab-4c6d-8358-ac0f7256d8ef)
7、画出轮廓    
![image](https://github.com/user-attachments/assets/05c3c0cb-b152-41d2-851b-17b26ae20d38)
8、提取数字轮廓并画外接矩阵，给数字框起来，然后给二值处理。对框里的数字做模版数字一样的活，让进行一一匹配    
这里不展示了，大家在代码里debug，图太小了    
9、最终效果图    
![image](https://github.com/user-attachments/assets/c3d9ac5d-a654-4065-861f-f75d138e3be6)    





