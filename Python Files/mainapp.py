from __future__ import print_function
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import easygui
import pytesseract
from GoogleTasks import createService, displayTaskList, createTaskList, createTask
from GoogleService import convert_to_RFC_datetime

CREDENTIALS = 'credentials.json' #The credintals file goes here
API_NAME = 'tasks' #The name of the Google API being used, in this case it's tasks
API_VERSION = 'v1' #The version of said api
SCOPES = ['https://www.googleapis.com/auth/tasks'] #The scope for said API
kivy.require("2.0.0")

filename = ""

#
# The main class of the program, uses a BoxLayout component to build the GUI through Kivy.
#
class MainApp(BoxLayout):

#
# Gets the due date of the assignment given the upload text
#
    def getDate(self, givenString):
        substring = "Due"

        startIndexDate = givenString.index(substring)

        tempString = givenString[startIndexDate:len(givenString)]

        startIndexDate = tempString.index(substring)

        endIndexDate = tempString.index("at")

        dateString = tempString[startIndexDate + 4: endIndexDate]

        return dateString

#
# Gets the due time of the assignment given the upload text (not needed since Google doesn't have support for time)
#

    def getTime(self, fileText):
        startIndexTime = fileText.index("at")
        endIndexTime = fileText.index("|")

        timeString = fileText[startIndexTime + 3: endIndexTime]
        return timeString
#
# Gets the name of the assignment given the upload text
#
    def getAssignmentName(self, fileText):
        startIndexName = 0
        endIndexName = 0

        if "Available" in fileText:
            endIndexName = fileText.index("Available")
        elif "Not available" in fileText:
            endIndexName = fileText.index("Not available")
        elif "Due" in fileText:
            endIndexName = fileText.index("Due")

        nameString = fileText[startIndexName: endIndexName]
        return nameString

#
# Gets the month of when the assignment was due and turns that month into a respective integer so that Google can process it.
#
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
        return monthNumber

# Clean string: remove "Not Yet Graded" text along with 'cg' and 'sg' glitches
# (sometimes the AI glitches out and picks up 'cg' and 'sg' text while extracting text from the image)
    def removeNYG(self, inputString):
        if "Not Yet Graded" in inputString:
            inputString = inputString[16:len(inputString)]

        if "sg " or "cg " or "wg " in inputString:
            inputString = inputString[0:len(inputString)]
        return inputString

#
# This code is used to pull a file from the GUI and convert that file to a string.
#
    def fileConversion(self, value):
        filename = easygui.fileopenbox()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        fileText = pytesseract.image_to_string(filename)

#
# TODO: Slice up the fileText string into several "line strings" so that we can pull information for each individual lines.
#       Make sure to store each line in a list.

        isStringRemaning = True
        newString = ""
        stringList = []
        while isStringRemaning:
            index = fileText.index("pts")

            trimmedString = fileText[0:index]
            stringList.append(trimmedString)


            remaningString = fileText[index+4:len(fileText)]


            fileText = remaningString

            if "pts" in fileText:
                isStringRemaning = True
            else:
                isStringRemaning = False

        nameList = []
        dateList = []
        for string in stringList:
            string = self.removeNYG(string)
            assignmentName = self.getAssignmentName(string)
            nameList.append(assignmentName)

            assignmentDate = self.getDate(string)
            dateList.append(assignmentDate)

#
#   This code is used to call the methods above, and retrieve the key pieces of the selected line.
#

        taskListID = createTaskList("Software Engineering")
        print("Successfully created a class with the name Software Engineering")
        for i in range(len(nameList)):
            dateString = dateList[i]

            nameString = nameList[i]
            monthString = dateString[0:3]
            dayString = dateString[4:len(dateString)]

            monthNumber = self.monthConversion(monthString)
            dayNumber = int(dayString)

#
# This code is used to insert the variables into a the API to create a google task
#
            dt = convert_to_RFC_datetime(2021, monthNumber, dayNumber, 0, 0)

            createTask(taskListID, nameString, "", dt, "needsAction", False)
            print("Successfully created a task with the following. Class ID: ", taskListID, "Task Name: ", nameString, "Due Date: ", dt)

#
# Main function, creates the GUI and places the elements in the correct places.
#

    def classCreation(self):
        taskListID = createTaskList("Software Engineering")
        print("Successfully created a class with the name: Software Engineering")

    def __init__(self, **kwargs):
        createService(CREDENTIALS, API_NAME, API_VERSION, SCOPES)

        super().__init__(**kwargs)
        self.orientation = "vertical"

        Logo = Image(source='Logo.png')
        self.add_widget(Logo)

        Text = Label(text='[color=000000]1. Create Class List[/color]', markup = True)
        self.add_widget(Text)

        InputBox = TextInput(text='Input the name of your class here!')
        self.add_widget(InputBox)

        ClassCreationButton = Button(text="Click this button to create your class! (Do this first)")

        self.add_widget(ClassCreationButton)

        Text2 = Label(text='[color=000000]2. Upload a screenshot of your assignments using the button below! [/color]', markup = True)
        self.add_widget(Text2)

        UploadButton = Button(text="Upload File", font_size = 14)

        test = UploadButton.bind(on_press=self.fileConversion)
        self.add_widget(UploadButton)

        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (500, 650)
        App.title = "CanSync"
        Config.set('kivy', 'window_icon', 'C:/Users/User/PycharmProjects/TestProject/Python Files/CanSyncIcon.ico')
        Config.set('graphics', 'resizable', '0')
        Config.write()


class BuildApp(App):
    def build(self):
        return MainApp()

if __name__ == "__main__":
    BuildApp().run()