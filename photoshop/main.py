from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from random import randint
import os
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap



app = QApplication([])
window = QWidget()
window.setWindowTitle("Фотошоп")
window.resize(700, 400)

btn_dir = QPushButton("Папка")
list_images = QListWidget()
lb_image = QLabel("Картинка")
btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_mirrow = QPushButton("Зеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

v_line1 = QVBoxLayout()
v_line2 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()

v_line1.addWidget(btn_dir)
v_line1.addWidget(list_images)
h_line1.addLayout(v_line1, stretch=20)
v_line2.addWidget(lb_image)
h_line2.addWidget(btn_left)
h_line2.addWidget(btn_right)
h_line2.addWidget(btn_mirrow)
h_line2.addWidget(btn_sharp)
h_line2.addWidget(btn_bw)

v_line2.addLayout(h_line2)
h_line1.addLayout(v_line2, stretch=80)

window.setLayout(h_line1)

class ImageProcesor():
    def __init__(self):
        self.image = None
        self.file_name = None
        self.folder = "Modified"

    def loadImage(self, file_name):
        self.file_name = file_name
        image_path = os.path.join(work_dir, file_name)
        self.image = Image.open(image_path)
    
    def showImage(self, path):
        lb_image.hide()
        pixmapimg = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimg = pixmapimg.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimg)
        lb_image.show()
    
    def saveImage(self):
        path = os.path.join(work_dir, self.folder)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.file_name)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(work_dir, self.folder, self.file_name)
        self.showImage(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(work_dir, self.folder, self.file_name)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(work_dir, self.folder, self.file_name)
        self.showImage(image_path)
    
    def do_blured(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(work_dir, self.folder, self.file_name)
        self.showImage(image_path)
    
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(work_dir, self.folder, self.file_name)
        self.showImage(image_path)

work_dir = ""
workimage = ImageProcesor()


def show_files():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()
    all_files = os.listdir(work_dir)
    extensions = [".jpg", ".png", ".jpeg", ".bmp", ".svg"]
    result = []
    for file in all_files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    list_images.clear()
    list_images.addItems(result)

def imageShow():
    if list_images.currentRow() >= 0:
        filename = list_images.currentItem().text()
        workimage.loadImage(filename)
        imagepath = os.path.join(work_dir, filename)
        workimage.showImage(imagepath)
list_images.currentRowChanged.connect(imageShow)
    

btn_dir.clicked.connect(show_files)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_blured)
btn_mirrow.clicked.connect(workimage.do_mirror)

window.show()
app.exec_()
