# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_create.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(520, 337)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 2)
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setText("")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 4, 0, 1, 2)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Создание пользователя"))
        self.radioButton.setText(_translate("Form", "Учитель"))
        self.pushButton.setText(_translate("Form", "Создать"))
        self.radioButton_2.setText(_translate("Form", "Ученик"))
        self.label_3.setText(_translate("Form", "Логин:"))
        self.label_4.setText(_translate("Form", "Пароль:"))

