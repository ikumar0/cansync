from __future__ import print_function
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import Config
import easygui
import pytesseract
from GoogleTasks import createService, displayTaskList, createTaskList, createTask

CREDENTIALS = 'credentials.json' #The credintals file goes here
API_NAME = 'tasks' #The name of the Google API being used, in this case it's tasks
API_VERSION = 'v1' #The version of said api
SCOPES = ['https://www.googleapis.com/auth/tasks'] #The scope for said API
kivy.require("2.0.0")

filename = ""



class MainApp(BoxLayout):
    def getDate(self, filename):
        print(pytesseract.image_to_string(filename))

        substring = "Due"

        fileText = pytesseract.image_to_string(filename)

        if substring in pytesseract.image_to_string(filename):
            print("Found in string")
        else:
            print("Not found in string")

        startIndexDate = pytesseract.image_to_string(filename).index(substring)
        endIndexDate = pytesseract.image_to_string(filename).index("at")

        dateString = fileText[startIndexDate + 4: endIndexDate]
        return dateString

    def getTime(self, filename):
        fileText = pytesseract.image_to_string(filename)

        startIndexTime = pytesseract.image_to_string(filename).index("at")
        endIndexTime = pytesseract.image_to_string(filename).index("|")

        timeString = fileText[startIndexTime + 3: endIndexTime]
        return timeString

    def getAssignmentName(self, filename):
        fileText = pytesseract.image_to_string(filename)
        startIndexName = 0
        endIndexName = 0

        if "Available" in fileText:
            print("available has been found!")
            endIndexName = pytesseract.image_to_string(filename).index("Available")
        elif "Not available" in fileText:
            print("not available has been found!")
            endIndexName = pytesseract.image_to_string(filename).index("Not available")
        elif "Due" in fileText:
            print("due has been found!")
            endIndexName = pytesseract.image_to_string(filename).index("Due")

        nameString = fileText[startIndexName + 3: endIndexName]
        print("this line has been reached!")
        return nameString

    def monthConversion(self, month):
        monthNumber = 0
        if month == "Jan":
            monthNumber = 1
        elif month == "Feb":
            monthNumber = 2
        elif month == "Mar":
            monthNumber = 3
        elif month == "Apr":
            monthNumber = 4
        elif month == "May":
            monthNumber = 5
        elif month == "Jun":
            monthNumber = 6
        elif month == "Jul":
            monthNumber = 7
        elif month == "Aug":
            monthNumber = 8
        elif month == "Sep":
            monthNumber = 9
        elif month == "Oct":
            monthNumber = 10
        elif month == "Nov":
            monthNumber = 11
        elif month == "Dec":
            monthNumber = 12


    def fileConversion(self, value):
        print("this line was printed!")
        filename = easygui.fileopenbox()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        dateString = self.getDate(filename)
        nameString = self.getAssignmentName(filename)

        monthString = dateString[0:3]
        dayString = dateString[4:len(dateString)]

        monthNumber = self.monthConversion(monthString)
        dayNumber = int(dayString)
        print(monthNumber)
        print(dayNumber)



    def __init__(self, **kwargs):

        createService(CREDENTIALS, API_NAME, API_VERSION, SCOPES)

        super().__init__(**kwargs)
        self.orientation = "vertical"

        CSLabel = Label(text="CanSync")
        self.add_widget(CSLabel)

        UploadButton = Button(text="Upload File", font_size = 14)

        test = UploadButton.bind(on_press=self.fileConversion)
        print(test)
        self.add_widget(UploadButton)

        Window.clearcolor = (.08, .08, .08, .28)
        Window.size = (300, 650)
        Config.set('graphics', 'resizable', '0')
        Config.write()


class BuildApp(App):
    def build(self):
        return MainApp()

if __name__ == "__main__":
    BuildApp().run()