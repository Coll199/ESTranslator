import string

from PyQt5 import QtCore, QtGui, QtWidgets
import json

with open('en_dictionary.json', 'r') as f1:
    en_dictionary = json.load(f1)

with open('ro_dictionary.json', 'r') as f2:
    ro_dictionary = json.load(f2)


def find_word(word, dictionary):
    for x in dictionary["words"]:
        if x["word"] == word:
            return x
    return None


def find_contraction(contraction):
    for x in en_dictionary["contractions"]:
        if x["contracted"] == contraction:
            return x
    return None


def translate_word(word):
    if word:
        return ro_dictionary["words"][int(word["id"])-1]["word"]


def expand_words(text):
    final = ""
    splitText = text.split()
    for tk in splitText:
        if "'" in tk:
            contr = find_contraction(tk)
            if contr:
                final += find_contraction(tk)["expanded"] + " "
            else:
                final += "[" + tk + "]" + " "
        else:
            final += tk + " "
    return final


# text2 = "{1} I went to the beach"
# for tk in text2.split("}"):
#     print(tk)
#
#
# text = "once upon a time I went to the beach"
# print(text.replace("upon",  "was"))
#
# text = expand_words(text)
# print(text)
#
#
# finalTranslation = ""
# for tk in text.split():
#     #if word is code
#     word = find_word(tk, en_dictionary)
#     if word:
#         finalTranslation += translate_word(word) + " "
#     else:
#         finalTranslation += "[" + tk + "]" + " "
#
# print(finalTranslation)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setReadOnly(False)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.horizontalLayout.addWidget(self.plainTextEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.onTranslateClicked)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Translate"))

    def onTranslateClicked(self):
        content = self.plainTextEdit.toPlainText()
        text = expand_words(content)
        for x in en_dictionary["expressions"]:
            text = text.replace(x["expression"], "{" + x["id"] + "}")
        print(text)
        finalTranslation = ""
        for tk in text.split():
            if tk[0] == "{":
                id = int(tk.strip(string.punctuation))
                finalTranslation += ro_dictionary["expressions"][id - 1]["expression"] + " "
            else:
                word = find_word(tk, en_dictionary)
                if word:
                    finalTranslation += translate_word(word) + " "
                else:
                    finalTranslation += "[" + tk + "]" + " "
        self.plainTextEdit_2.setPlainText(finalTranslation)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


