"""
This is the code for the PC to control ECT remotely.
The codes run correctly only when your uart and camera are available.
If your uart module is not ready, you may want to modify the codes.
The code combines "Yolov7" and "Night Image Enhancement",details about which are included in the readme file.
If you have any problems, feel free to raise issues!
author:NowLoadY
email:2225649558@qq.com
version:1.0
2022/12/23
"""
import math
import cv2
import numpy as np
import serial
import os
import torch
import torch.utils
from torch.autograd import Variable
from SCI_model import Finetunemodel
import detect_with_API


class MemoryFriendlyLoader(torch.utils.data.Dataset):
    def __init__(self, img_dir):
        self.low_img_dir = img_dir
        self.train_low_data_names = []
        self.ori_img = None

        for root, dirs, names in os.walk(self.low_img_dir):
            for name in names:
                self.train_low_data_names.append(os.path.join(root, name))

        self.train_low_data_names.sort()
        self.count = len(self.train_low_data_names)

    def transform(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.transpose((2, 0, 1))
        image = image.astype(np.float32) / 255.0
        image = torch.from_numpy(image)
        return image

    def load_images_transform(self, file):
        _, im_cv = cam.read()
        self.ori_img = im_cv.copy()
        cv2.imshow("ori", im_cv)
        im = self.transform(im_cv)
        return im

    def __getitem__(self, index):
        low_file = self.train_low_data_names[index]
        low = self.load_images_transform(low_file)
        return low, low_file

    def __len__(self):
        return self.count


########################################################
def PID_updater(PID, Bias, NowVal, TargetVal):
    Bias[0] = NowVal - TargetVal
    Change = (PID[0] * (Bias[0] - Bias[1]) + PID[1] *
              Bias[0] + PID[2] * (Bias[0] - 2 * Bias[1] + Bias[2]))
    Bias[2] = Bias[1]
    Bias[1] = Bias[0]
    return Change


class PC_Commander:
    def __init__(self, UartPort=None):
        if UartPort is not None:
            self.PC_UART = serial.Serial(UartPort, 115200)
        self.Yolov7_detector = detect_with_API.detectapi(weights=trained_model_name)
        self.velocity = 8
        self.Angles = [0.0, 0.0]
        self.focal_length = 120
        self.AaPID_X = [0.01, 0.01, 0.0]
        self.AaBias_X = [0.0, 0.0, 0.0]
        self.AaPID_Y = [0.01, 0.01, 0.0]
        self.AaBias_Y = [0.0, 0.0, 0.0]
        self.FirstAimTarget = False
        self.UartStrs = ['']

    def detectTargets(self, Img):
        result, names = self.Yolov7_detector.detect([Img])
        objects = []
        for cls, (x1, y1, x2, y2), conf in result[0][1]:
            objects.append([names[cls], x1, y1, x2, y2, conf])
        return objects

    def PlotImg(self, Img, Objects):
        for name, x1, y1, x2, y2, conf in Objects:
            cv2.rectangle(Img, (x1, y1), (x2, y2), (50, 200, 50))
            cv2.putText(Img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (200, 0, 0), 2)
        return Img

    def AimCalcPoint(self, Objects, Distance, Angle, ImgShape, ClassName='person'):
        PointShooterShould = None
        PointBulletShould = None
        PointShooterNowNeedX = None
        W, H = ImgShape[1], ImgShape[0]
        for name, X1, Y1, X2, Y2, conf in Objects:
            if name == ClassName:
                PointShooterShould = [(X1 + X2) // 2, int(min(Y1, Y2) + (Y1 + Y2) / 6)]
                PointShooterNowNeedX = [(X1 + X2) // 2, H // 2]
                Time = Distance / self.velocity
                if Angle >= 0:
                    ChangedH = self.velocity * math.sin(Angle) * Time - (0.5 * 9.81 * (Time ** 2))
                else:
                    ChangedH = self.velocity * math.sin(Angle) * Time + (0.5 * 9.81 * (Time ** 2))
                temp = ChangedH / Distance
                if temp < -1:
                    temp = -1
                elif temp > 1:
                    temp = 1
                if Angle >= 0:
                    ChangeH = Distance * math.sin(
                        Angle - math.asin(temp)) / Distance * self.focal_length
                else:
                    ChangeH = -Distance * math.sin(
                        Angle - math.asin(temp)) / Distance * self.focal_length
                PointBulletShould = [PointShooterNowNeedX[0], PointShooterNowNeedX[1] + int(ChangeH)]
                return PointShooterShould, PointBulletShould, PointShooterNowNeedX
        self.FirstAimTarget = False
        return PointShooterShould, PointBulletShould, PointShooterNowNeedX

    def SendCommands(self, commands):
        self.PC_UART.write(commands)


# ----start initialize---- #
cam = cv2.VideoCapture(0)
modelPath = './SCI_weights/difficult.pt'
trained_model_name = 'yolov7-e6e.pt'
MyCommander = PC_Commander(UartPort='COM12')

TestDataset = MemoryFriendlyLoader(img_dir='./SCI_data/medium')
test_queue = torch.utils.data.DataLoader(
    TestDataset, batch_size=1,
    pin_memory=True, num_workers=0)
model = Finetunemodel(modelPath)
model = model.cuda()
model.eval()

# ----start loop---- #
while True:
    with torch.no_grad():
        for _, (input, image_name) in enumerate(test_queue):
            try:
                if MyCommander.PC_UART.inWaiting():
                    strlines = MyCommander.PC_UART.read(MyCommander.PC_UART.inWaiting()).decode().split('\n')
                    MyCommander.UartStrs = strlines[len(strlines) - 2].split('|')
                if MyCommander.UartStrs[0] == 'rc':
                    MyCommander.Angles[0] = math.radians(float(MyCommander.UartStrs[1]))
                    MyCommander.Angles[1] = math.radians(float(MyCommander.UartStrs[2]))
            except:
                pass
            MyCommander.UartStrs = ['']

            #########################
            # ----Image Enhance---- #
            #########################
            input = Variable(input, volatile=True).cuda()
            i, r = model(input)
            image_numpy = r[0].cpu().float().numpy()
            image_numpy = (np.transpose(image_numpy, (1, 2, 0)))
            image_numpy = np.clip(image_numpy * 255, 0, 255)
            image_cv = cv2.cvtColor(image_numpy, cv2.COLOR_RGB2BGR).astype(np.uint8)
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            mean_val = cv2.mean(gray)[0]
            if mean_val > 130:
                image_cv = TestDataset.ori_img
            else:
                image_cv = cv2.medianBlur(image_cv, 5)
            #####################
            # ----inference---- #
            #####################
            objects = MyCommander.detectTargets(image_cv)
            image_cv = MyCommander.PlotImg(image_cv, objects)

            #########################################
            # ----Monocular distance estimation---- #
            #########################################
            distance = 15  # m
            pass

            ###################
            # ----analyse---- #
            ###################
            point_shooter_should, point_bullet_should, point_shooter_now_needX = MyCommander.AimCalcPoint(objects,
                                                                                                          ImgShape=image_cv.shape,
                                                                                                          Angle=
                                                                                                          MyCommander.Angles[
                                                                                                              1],
                                                                                                          Distance=distance,
                                                                                                          ClassName='bottle')
            if (point_shooter_should is not None) and (point_bullet_should is not None):

                w, h = image_cv.shape[1], image_cv.shape[0]
                x1, y1 = point_shooter_should
                x2, y2 = point_bullet_should
                x3, y3 = point_shooter_now_needX
                image_cv = cv2.line(image_cv, [image_cv.shape[1] * 8 // 20, h // 2],
                                    [image_cv.shape[1] * 12 // 20, h // 2],
                                    (255, 255, 255), 2)
                if abs(point_shooter_should[1] - point_bullet_should[1]) < 4:
                    image_cv = cv2.circle(image_cv, point_shooter_should, 9, (0, 255, 0), 2)
                    image_cv = cv2.circle(image_cv, point_bullet_should, 6, (0, 255, 0), -1)
                else:
                    image_cv = cv2.circle(image_cv, point_shooter_should, 9, (0, 0, 255), 2)
                    image_cv = cv2.circle(image_cv, point_bullet_should, 6, (0, 0, 255), -1)
                image_cv = cv2.circle(image_cv, point_shooter_now_needX, 4, (150, 150, 150), -1)
                cv2.putText(image_cv, "Distance:{} m".format(distance), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 0, 255), 3)
                cv2.putText(image_cv, "Velocity:{} m/s".format(MyCommander.velocity), (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255), 3)
                cv2.putText(image_cv, "Angle: {} , {}".format(round(MyCommander.Angles[0] * 180 / math.pi, 1),
                                                              round(MyCommander.Angles[1] * 180 / math.pi, 1)),
                            (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 0, 255), 3)

                if not MyCommander.FirstAimTarget:
                    MyCommander.PC_UART.write("AC|{}|{}|{}\n".format(x1, y1, MyCommander.JiaoJu).encode())
                    MyCommander.FirstAimTarget = True
                    MyCommander.AaBias_X = [0.0, 0.0, 0.0]
                    MyCommander.AaBias_Y = [0.0, 0.0, 0.0]
                else:
                    changeValX = PID_updater(MyCommander.AaPID_X, MyCommander.AaBias_X, x1, w / 2)
                    changeValX = round(changeValX, 1)
                    changeValY = PID_updater(MyCommander.AaPID_Y, MyCommander.AaBias_Y, y1, y2)
                    changeValY = round(changeValY, 1)
                    MyCommander.PC_UART.write("AA|{}|{}\n".format(-changeValX, -changeValY).encode())
            cv2.imshow("result", image_cv)
            cv2.waitKey(1)
