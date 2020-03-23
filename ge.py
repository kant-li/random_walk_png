#! -*- coding: utf-8 -*-

import sys
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QGridLayout, QMessageBox,
                             QLineEdit, QDateTimeEdit, QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QPixmap


class RandomGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.timeList = []
        self.dataList = []
        self.exlPath = '数据.xls'
        self.filePath = '折线图.png'
        self.plot = plt
        self.plot.rcParams['font.sans-serif'] = ['SimHei']
        self.plot.rcParams['axes.unicode_minus'] = False
        self.figure = self.plot.figure(figsize=(6, 3), dpi=160)
        self.ax = self.plot.axes()
        self.pic = QLabel(self)
        self.initUI()

    def initUI(self):
        # 左输入区
        title = QLabel('标题')
        start = QLabel('开始时间')
        end = QLabel('结束时间')
        inter = QLabel('记录间隔(分钟)')
        top = QLabel('值上限')
        buttom = QLabel('值下限')

        self.titleEdit = QLineEdit()
        self.startEdit = QDateTimeEdit()
        self.startEdit.setDisplayFormat('yyyy-MM-dd HH:mm')
        self.endEdit = QDateTimeEdit()
        self.endEdit.setDisplayFormat('yyyy-MM-dd HH:mm')
        self.interEdit = QLineEdit()
        self.topEdit = QLineEdit()
        self.buttomEdit = QLineEdit()

        self.interEdit.setValidator(QIntValidator())
        self.topEdit.setValidator(QDoubleValidator())
        self.buttomEdit.setValidator(QDoubleValidator())

        leftInput = QGridLayout()
        leftInput.addWidget(title, 0, 0)
        leftInput.addWidget(self.titleEdit, 0, 1)
        leftInput.addWidget(start, 1, 0)
        leftInput.addWidget(self.startEdit, 1, 1)
        leftInput.addWidget(end, 2, 0)
        leftInput.addWidget(self.endEdit, 2, 1)
        leftInput.addWidget(inter, 3, 0)
        leftInput.addWidget(self.interEdit, 3, 1)
        leftInput.addWidget(top, 4, 0)
        leftInput.addWidget(self.topEdit, 4, 1)
        leftInput.addWidget(buttom, 5, 0)
        leftInput.addWidget(self.buttomEdit, 5, 1)

        generateBtn = QPushButton('生成随机数')
        generateBtn.clicked.connect(self.generate_random_nums)

        leftInput.addWidget(generateBtn, 6, 1)

        # 下图形区
        png = QPixmap(self.filePath)
        self.pic.setPixmap(png)
        self.pic.setScaledContents(True)
        picBox = QVBoxLayout()
        picBox.addWidget(self.pic)

        # 主界面
        hBox = QHBoxLayout()
        hBox.addLayout(leftInput)

        vBox = QGridLayout()
        vBox.addLayout(hBox, 0, 0)
        vBox.addLayout(picBox, 1, 0)

        self.setLayout(vBox)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('随机数生成器')
        self.show()

    def generate_random_nums(self):
        # 验证
        if not all([self.titleEdit.text(), self.interEdit.text(), self.topEdit.text(), self.buttomEdit.text()]):
            self.warnDialog("必须输入所有参数才能生成随机数！")
            return
        # 生成数据
        title = self.titleEdit.text()
        start = self.startEdit.dateTime().toPyDateTime()
        end = self.endEdit.dateTime().toPyDateTime()
        inter = int(self.interEdit.text())
        top = float(self.topEdit.text())
        buttom = float(self.buttomEdit.text())

        self.generateTimeList(start, end, inter)
        self.generateDataList(top, buttom)

        # 生成图片
        self.generatePic(title, top, buttom)

    def warnDialog(self, text):
        QMessageBox.warning(self, '注意', text, QMessageBox.Yes, QMessageBox.Yes)

    def generateTimeList(self, start, end, inter):
        self.timeList = []
        when = start
        self.timeList.append(when.strftime("%m-%d %H:%M"))
        while when < end:
            when = when + timedelta(minutes=inter)
            self.timeList.append(when.strftime("%m-%d %H:%M"))

    def generateDataList(self, top, buttom):
        self.dataList = []
        length = len(self.timeList)
        self.dataList = [random.random() * (top - buttom) + buttom]
        for i in range(length - 1):
            pre_num = self.dataList[i]
            if pre_num < buttom:
                num = pre_num + random.random()
            elif pre_num > top:
                num = pre_num - random.random()
            else:
                num = pre_num + random.random() - 0.5
            self.dataList.append(num)

    def generatePic(self, title, top, buttom):
        self.plot.cla()

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.plot.plot(self.timeList, self.dataList, lw=0.8)
        self.plot.plot(self.timeList, [top] * len(self.timeList), lw=1)
        self.plot.ylim(bottom=buttom-1)
        self.plot.ylim(top=top+1)
        self.plot.title(title)

        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(len(self.timeList) // 10))
        self.plot.xticks(fontsize=8, rotation=40, color="gray")

        self.plot.tight_layout()
        self.plot.savefig(self.filePath)

        png = QPixmap(self.filePath)
        self.pic.setPixmap(png)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    generator = RandomGenerator()
    sys.exit(app.exec_())

