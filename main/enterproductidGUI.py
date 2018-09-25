import sys
from PyQt5 import QtWidgets, QtGui
from PandasModel import PandasModel
# from MatplotCanvas import PlotCanvas
import MatplotCanvas
import ApplicationLayer.ebay_finder as ef

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set up GUI Signal generators
        self.lbl1 = QtWidgets.QLabel(self)
        self.le = QtWidgets.QLineEdit('UPC:013803271829')
        self.b1 = QtWidgets.QPushButton('Search')
        self.b2 = QtWidgets.QPushButton('Plot')

        # Set up table for pandas dataframe
        self.pandasTv = QtWidgets.QTableView(self)
        self.pandasTv.setSortingEnabled(True)


        # Set up MatplotlibPlotCanvas
        # m = PlotCanvas(self, width=5, height=4)
        # m.move(0,0)

        v_box = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        v_box.addLayout(h_box)
        self.setLayout(v_box)

        # Add icons
        self.lbl1.setPixmap(QtGui.QPixmap('/Users/pAulse/Documents/productarbitrage/icons/ebayicon.png'))

        # Add buttons to layout
        v_box.addWidget(self.le)
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)
        v_box.addWidget(self.lbl1)
        v_box.addWidget(self.pandasTv)

        self.setWindowTitle('Ebay Lookup')
        self.setGeometry(200, 200, 600, 400)


        self.b1.clicked.connect(self.btn_clk)
        self.b2.clicked.connect(lambda: self.btn_plot())

        self.show()





    def btn_clk(self):
        try:
            print(self.le.text())
            df = ef.produceDataset(self.le.text())
            model = PandasModel(df)
            self.pandasTv.setModel(model)
        except Exception as e:
            print(e)

    def btn_plot(self):
        MatplotCanvas.App()
        # xaxis
        # yaxis
        # self.p_window = MatplotCanvas.App()
        # self.p_canvas = MatplotCanvas.PlotCanvas(self)
        # self.p_canvas.plot(data=[1,2,3,4,5,6])
        # self.p_window.initUI()
        # MatplotCanvas.PlotCanvas().plot(data=[1,2,3,4,5,6])
        # self.plot_ui = PlotCanvas(self, width=5, height=4)
        # self.plot_ui.s
        # self.show()


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
