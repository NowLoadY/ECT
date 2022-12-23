# ECT
electromagnetic cannon turret  
电磁炮台（简单模型）
# How To Build your ECT:  
## Circuit  
我建议你首先按照以下原理图搭建好你的基本电路：  
## 3D print  
3D打印所需的模型文件在这个地方。
## Code  
Here  
### For PC  
#### Install
* 建议使用conda为你创建一个用于运行yolov7的环境。
* 环境配置要求具体见yolov7官方仓库。  
#### Run
* 在codes/路径下，运行:
```bash
python elecshooterPC.py
```
确保你的电脑已经支持串口通信，并已经连接好了摄像头
### For RasPi Pico  
#### Install
* 在官网下载.uf2文件，按照官方教程安装好micropython。
* 在Thonny中连接Pico
* 将 codes/elecshooterPico.py 和 partsPico.py 烧录到Pico里面。
* 如果你希望它通电自动运行，你需要更改elecshooterPico.py名字为main.py。
#### Run  
* 通常选择通电自动运行，否则会变得很麻烦。  
* 确保你已经把Pico和舵机云台和串口通信模块连接起来。如果你手里准备了蜂鸣器，也别忘了它。  
## Reference：  
### Environment configuration related：  
* [查看cuda版本与torch的对应关系](https://blog.csdn.net/JohnJim0/article/details/108688964)  
* [Windows查看自己的cuda版本](https://cloud.tencent.com/developer/article/2031512)  
* [Pycharm中python导入cv2包没有代码提示问题](https://blog.csdn.net/fangzhihuaa/article/details/113903689?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1-113903689-blog-122422778.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1-113903689-blog-122422778.pc_relevant_default&utm_relevant_index=2)
### UI related：
* [kivy texture图片格式和opencv numpy图片格式互转](https://dongfangyou.blog.csdn.net/article/details/105365619)  
### Data processing related：
* [总结PID算法，位置式增量式理解以及C代码实现](https://blog.csdn.net/weixin_43193231/article/details/95194946)  
