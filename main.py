from data_module import parse_array

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,  QFileDialog
Form, _ = uic.loadUiType("ui.ui")


def make_message(msg, color):
    print (msg)


def import_from_file(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filenamexml, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;PRG Files (*.prg)", options=options)

    hex_arr = []
    if filenamexml:
        try:
            make_message(u"Подождите... Идет импортирование данных", "green")

            with open(filenamexml, "rb") as f:
                # Read the whole file at once
                for i in f.read():
                    a = ord(chr(i))
                    a1 = "{:02x}".format(a)
                    hex_arr.append(a1)
        except:
            make_message(u"Не могу открыть файл", "red")
            return
    else:
        make_message(u"Не могу открыть файл", "red")
        return
    make_message(u"Данные загружены", "green")
    result_arr = parse_array(hex_arr)

    return


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.printButtonPressed)

    def printButtonPressed(self):
        import_from_file(self)


if __name__=="__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())



result_arr = []

Form, Window = uic.loadUiType("ui.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()

