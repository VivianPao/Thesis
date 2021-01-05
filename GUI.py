
# https://www.geeksforgeeks.org/pyqt5-create-a-user-form-to-get-information/

# importing libraries 
from PyQt5.QtWidgets import * 
import sys 
  
# creating a class 
# that inherits the QDialog class 
class Window(QDialog): 
  
    # constructor 
    def __init__(self): 
        super(Window, self).__init__() 
  
        self.setWindowTitle("Stakeholder Network Analysis") # setting window title 
        self.setGeometry(100, 100, 300, 400) # setting geometry to the window 
        self.formGroupBox = QGroupBox("Twitter Scraping") # creating a group box 
        # self.ageSpinBar = QSpinBox() # creating spin box to select age 
        self.data2CollectComboBox = QComboBox() # creating combo box to select Data To Collect 
        self.data2CollectComboBox.addItems(["Replies", "Followers"]) # adding items to the combo box 
        self.topicLineEdit = QLineEdit() # creating a line edit 
        self.dateFromLineEdit = QLineEdit() # creating a line edit 
        self.dateToLineEdit = QLineEdit() # creating a line edit 
        self.saveAs = QLineEdit() # creating a line edit 
  
        self.createForm() # calling the method that create the form 
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) # creating a dialog button for ok and cancel 
        self.buttonBox.accepted.connect(self.getInfo) # adding action when form is accepted 
        self.buttonBox.rejected.connect(self.reject) # addding action when form is rejected 
        
        mainLayout = QVBoxLayout() # creating a vertical layout 
        mainLayout.addWidget(self.formGroupBox) # adding form group box to the layout 
        mainLayout.addWidget(self.buttonBox)  # adding button box to the layout 
        self.setLayout(mainLayout) # setting lay out 
  


    # get info method called when form is accepted 
    def getInfo(self): 
  
        # printing the form information 
        self.dateFromLineEdit
        self.dateToLineEdit
        print("Topic search: {0}".format(self.topicLineEdit.text())) 
        print("Data to collect: {0}".format(self.data2CollectComboBox.currentText())) 
        print("From date: {0}".format(self.dateFromLineEdit.text())) 
        print("To date: {0}".format(self.dateToLineEdit.text())) 
        print("Save As: {0}".format(self.saveAs.text()))
        # print("Age : {0}".format(self.ageSpinBar.text())) 
  
        # closing the window 
        self.close() 
  
    def idk(self):
        print("iddddkkkk")

    # creat form method 
    def createForm(self): 

        # creating a form layout
        layout = QFormLayout() 

        # adding rows 
        layout.addRow(QLabel("Topic search"), self.topicLineEdit) # for name and adding input text
        layout.addRow(QLabel("Data To Collect"), self.data2CollectComboBox)
        layout.addRow(QLabel("From Date (DD-MM-YYYY)"), self.dateFromLineEdit)
        layout.addRow(QLabel("To Date (DD-MM-YYYY)"), self.dateToLineEdit)
        layout.addRow(QLabel("Save As (*filename*.csv)"), self.saveAs)
        # layout.addRow(QLabel("Age"), self.ageSpinBar)

        # setting layout 
        self.formGroupBox.setLayout(layout) 

# main method 
if __name__ == '__main__': 
  
    app = QApplication(sys.argv) # create pyqt5 app 
    window = Window() # create the instance of our Window 
    window.idk()
    window.show() # showing the window

    # print("hello there")
    sys.exit(app.exec()) # start the app 


