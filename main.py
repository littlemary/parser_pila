from data_module import parse_array
from modbus_function import modbus_start_connection
from modbus_function import modbus_write_array


from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget,  QFileDialog
from PyQt5.QtCore import QSize, Qt

Form, _ = uic.loadUiType("ui.ui")


def make_message(self, msg, color):
    self.msg_label.setText(msg)

def show_records_intable(self):
    kolrows = len(self.result_arr)
    self.tableWidget.setRowCount(kolrows)
    row = 0
    for cur in self.result_arr:
        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(cur[8])))
        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(cur[0])))
        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(cur[1] + "/" + cur[2])))
        self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(cur[3])))
        self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(cur[4] + "/" + cur[5])))
        self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(cur[6])))
        self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(cur[7])))
        self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(cur[9] + "-" + cur[10])))
        self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(cur[11])))
        self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(cur[12])))
        row+=1

def import_from_file(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filenamexml, _ = QFileDialog.getOpenFileName(self, "Выберите *.prg файл", "",
                                              "PRG Files (*.prg)", options=options)

    hex_arr = []
    if filenamexml:
        try:
            make_message(self, u"Подождите... Идет импортирование данных", "green")

            with open(filenamexml, "rb") as f:
                # Read the whole file at once
                for i in f.read():
                    a = ord(chr(i))
                    a1 = "{:02x}".format(a)
                    hex_arr.append(a1)
        except:
            make_message(self, u"Не могу открыть файл", "red")
            return
    else:
        make_message(self, u"Не могу открыть файл", "red")
        return
    make_message(self, u"Данные загружены", "green")
    self.result_arr = parse_array(hex_arr)
    self.parser_complete=1
    show_records_intable(self)
    return

def startdata(self):
    if self.parser_complete==0 or len(self.result_arr)==0:
        make_message(self, u"Нет данных для отправки\nПодключите файл для разбора", "red")
        return
    connect = modbus_start_connection()
    if connect == 0:
        make_message(self, u"Ошибка соединения с ПЛК", "red")
        return
    write_modbus = modbus_write_array(self.result_arr)
    if isinstance(write_modbus, str):
            make_message(self, write_modbus, "red")
            return
    make_message(self, u"Порезка окончена", "red")
    return

def empty_table(self):
    self.parser_complete=0
    self.write_complete=0
    self.cut_complete=0
    self.result_arr=[]
    self.tableWidget.setColumnWidth(0, 100)
    self.tableWidget.horizontalHeaderItem(0).setToolTip("qty_bar")
    self.tableWidget.setColumnWidth(1, 100)
    self.tableWidget.horizontalHeaderItem(1).setToolTip("bar_length")
    self.tableWidget.setColumnWidth(2, 100)
    self.tableWidget.horizontalHeaderItem(2).setToolTip("angle_l/angle_r")
    self.tableWidget.setColumnWidth(4, 100)
    self.tableWidget.horizontalHeaderItem(4).setToolTip("Вычисляемое")
    self.tableWidget.setColumnWidth(5, 100)
    self.tableWidget.horizontalHeaderItem(5).setToolTip("real_size")
    self.tableWidget.setColumnWidth(6, 100)
    self.tableWidget.horizontalHeaderItem(6).setToolTip("article_profile")
    self.tableWidget.setColumnWidth(7, 100)
    self.tableWidget.horizontalHeaderItem(7).setToolTip("bar_code-bar_number")
    self.tableWidget.setColumnWidth(8, 100)
    self.tableWidget.horizontalHeaderItem(8).setToolTip("bar_color")


    self.tableWidget.setRowCount(0)

class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        result_arr = []
        parser_complete=0
        write_complete=0
        cut_complete=0
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.importButtonPressed)
        self.pushButton_2.clicked.connect(self.sendButtonPressed)
        self.msg_label.setText(u"Подключите *.prg файл для парсера")
        empty_table(self)
        self.tableWidget.setColumnWidth(0,100)

    def importButtonPressed(self):
        import_from_file(self)

    def sendButtonPressed(self):
        print ('hello')
        startdata(self)


if __name__=="__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())





Form, Window = uic.loadUiType("ui.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()

