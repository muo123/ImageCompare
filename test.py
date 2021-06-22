from tkinter import *
import tkinter.filedialog

import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot

from PIL import Image
from PIL import ImageTk    

####核心代码部分####

def calculate1(image1, image2):
    # 单通道直方图算法
    # 计算单通道的直方图的相似值并进行归一化
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])  
    cv2.normalize(hist1, hist1,0,255*0.9,cv2.NORM_MINMAX)
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    cv2.normalize(hist2, hist2,0,255*0.9,cv2.NORM_MINMAX)

    # 计算直方图的重合度，利用巴氏距离法
    degree = 0
    degree = 1- cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    return degree
 
def calculate2(image1, image2):
    # 计算RGB每个通道的直方图相似度
    # 将图像分离为RGB三个通道，再计算每个通道的相似值
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate1(im1, im2)
    sub_data = sub_data / 3
    return sub_data

####图形界面部分####

# 全局变量
global img_display1
global img_display2
global img_display3
global filename1
global filename2
global filename3

vec_x1 = 0.05 # 第一张图片x坐标
vec_x2 = 0.25 # 第二张图片x坐标
vec_x3 = 0.5 # 第三张图片x坐标
vec_y1 = 0.1 # 按钮y坐标
vec_y2 = 0.2 # 图片y坐标

# 设置界面的性质
root = Tk()
root.geometry('900x600') #界面大小
root.resizable(0,0)   # 禁止界面大小调整
root.title('图像相似度计算') # 界面标题
root.configure(bg = 'gray') #界面背景颜色


filename1 = ''
filename2 = ''
filename3 = ''

# 函数用于打开文件并显示图像
def display1():
    global img_display1
    global filename1
    
    filename1=tkinter.filedialog.askopenfilename() # 打开文件管理器
    if filename1 != '':
        lb.config(text='您选择的文件是'+filename1)
        
        img1 = Image.open(filename1) # 打开图片
        resized1 = img1.resize((150, 150)).convert('RGB') #调整图片大小
        img_display1 = ImageTk.PhotoImage(resized1)   
        label_img1 = tkinter.Label(root, image = img_display1)
        label_img1.place(relx=vec_x1, rely=vec_y2)
    else:
        lb.config(text='您未选择任何文件')    
    
def display2():
    global img_display2
    global filename2
    
    filename2=tkinter.filedialog.askopenfilename()
    if filename2 != '':
        lb.config(text='您选择的文件是'+filename2)
        img2 = Image.open(filename2)
        resized2 = img2.resize((150, 150)).convert('RGB')
        img_display2 = ImageTk.PhotoImage(resized2)
        label_img2 = tkinter.Label(root, image = img_display2)
        label_img2.place(relx=vec_x2, rely=vec_y2)
    else:
        lb.config(text='您未选择任何文件')  

# 函数用于比较图像相似度
def compare():
    global filename1
    global filename2
    global filename3
    global img_display3
    
    if(filename1 != '' and filename2 != ''):
        img1_path = filename1
        img2_path = filename2
            
        # 使用opencv方法计算图像相似度
        imgobj1 = cv2.imread(img1_path)
        imgobj2 = cv2.imread(img2_path)

        # 将图片大小进行统一
        img1 = cv2.resize(imgobj1, (256, 256))
        img2 = cv2.resize(imgobj2, (256, 256))
    
        res1 = calculate1(img1, img2) #单通道直方图计算
        res2 = calculate2(img1, img2) #三通道直方图计算
        string2 = "单通道直方图相似度：%s" % res1 + "\n" + "三直方图算法相似度：%s" % res2
        lb_cmp.config(text=string2)
    
    
        lb.config(text='')
        if res1 < 0.6:
            lb_res.config(text="哎呀，这两张图片看起来不太像呢≈( •̀ ω •́ )✧")
        else:
            lb_res.config(text="哇塞，这两张图片看起来真像≈o(*^＠^*)o")
            
        # 画出单通道直方图图像相似度比较的折线图
        hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])
        cv2.normalize(hist1, hist1,0,255*0.9,cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2,0,255*0.9,cv2.NORM_MINMAX)
        pyplot.plot(range(256), hist1, 'r')
        pyplot.plot(range(256), hist2, 'b')
        pyplot.title('单通道图像对比度')
        pyplot.rcParams['font.sans-serif']=['SimHei']
        pyplot.rcParams['axes.unicode_minus'] = False
        filename3 = r'C:\test\test.png'
        pyplot.savefig(filename3)   # 将图片保存

        # 在图形界面显示折线图           
        img3 = Image.open(filename3)
        resized3 = img3.resize((430, 280)).convert('RGB')
        img_display3 = ImageTk.PhotoImage(resized3)
        label_img3 = tkinter.Label(root, image = img_display3)
        label_img3.place(relx=vec_x3, rely=vec_y2)
        
        pyplot.clf() #清空数据图
    else:
        lb_res.config(text='--这是一个利用图像直方图特征计算图像相似度的程序--', bg='gray')
        
    
# 提示标签
lb = Label(root, text='请选择两张图像，进行图像相似度计算', bg='gray')
lb.place(relx=0.1, rely=vec_y1, relwidth=0.8, relheight=0.1)
lb.pack()
lb_file = Label(root,text='')
lb_file.pack()

# 输出结果的标签
lb_res = Label(root, text='--这是一个利用图像直方图特征计算图像相似度的程序--', bg='gray')
lb_res.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

# 按钮一选择第一张图片
btn1 = Button(root, text='选择图像一', command=display1)
btn1.place(relx=vec_x1, rely=vec_y1, relwidth=0.17, relheight=0.05)

# 按钮二选择第二张图片
btn2 = Button(root, text='选择图像二', command=display2)
btn2.place(relx=vec_x2, rely=vec_y1, relwidth=0.17, relheight=0.05)

# 按钮三进行图片相似度对比
btn3 = Button(root, text='对比', command=compare)
btn3.place(relx=vec_x3, rely=vec_y1, relwidth=0.17, relheight=0.05)

# 设置提示1
txt1 = Text(root)
txt1.place(relx=vec_x1, rely=vec_y2, relwidth=0.17, relheight=0.25)
txt1.insert(END, "   请选择第一张图像")
txt1.config(state=DISABLED)

# 设置提示2
txt2 = Text(root)
txt2.place(relx=vec_x2, rely=vec_y2, relwidth=0.17, relheight=0.25)
txt2.insert(END, "   请选择第二张图像")
txt2.config(state=DISABLED)

# 设置结果对比的区域
txt3 = Text(root)
txt3.place(relx=vec_x1, rely=0.5, relwidth=0.37, relheight=0.15)
txt3.insert(END, "")
txt3.config(state=DISABLED)

lb_cmp = Label(root, text='')
lb_cmp.place(relx=vec_x1, rely=0.5, relwidth=0.37, relheight=0.15)

# 设置直方图展示的区域
txt3 = Text(root)
txt3.place(relx=0.5, rely=0.2, width=430, height=280)
txt3.insert(END, "    直方图展示区")
txt3.config(state=DISABLED)

root.mainloop()