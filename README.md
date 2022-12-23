# ECT
electromagnetic cannon turret  
# How To Build your ECT:  
## 电路  
我建议你首先按照以下原理图搭建好你的基本电路：  
## 外壳  
3D打印所需的模型文件在这个地方。
## 代码  
Here  
### PC  
* 建议使用conda为你创建一个用于运行yolov7的环境，我使用了python3.10。
* 在codes/路径下，运行:
```bash
python elecshooterPC.py
```
## Reference：  
### Environment configuration related：  
* [查看cuda版本与torch的对应关系](https://blog.csdn.net/JohnJim0/article/details/108688964)  
* [Windows查看自己的cuda版本](https://cloud.tencent.com/developer/article/2031512)  
* [Pycharm中python导入cv2包没有代码提示问题](https://blog.csdn.net/fangzhihuaa/article/details/113903689?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1-113903689-blog-122422778.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1-113903689-blog-122422778.pc_relevant_default&utm_relevant_index=2)
### UI related：
* [kivy texture图片格式和opencv numpy图片格式互转](https://dongfangyou.blog.csdn.net/article/details/105365619)  
### Data processing related：
* [总结PID算法，位置式增量式理解以及C代码实现](https://blog.csdn.net/weixin_43193231/article/details/95194946)  
