import pandas as pd
from GoogleService import Create_Service, convert_to_RFC_datetime

CREDENTIALS = 'credentials.json' #The credintals file goes here
API_NAME = 'tasks' #The name of the Google API being used, in this case it's tasks
API_VERSION = 'v1' #The version of said api
SCOPES = ['https://www.googleapis.com/auth/tasks'] #The scope for said API

service = Create_Service(CREDENTIALS, API_NAME, API_VERSION, SCOPES)


"""
Calls GoogleService.py to create a service using the Google Tasks API
"""
def createService(CREDENTIALS, API_NAME, API_VERSION, SCOPES):
    Create_Service(CREDENTIALS, API_NAME, API_VERSION, SCOPES)

"""
Displays stuff to console [FOR DEBUGGING]
"""
def displayTaskList():
    response = service.tasklists().list().execute()
    lstItems = response.get('items')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.tasklists().list(
            maxResults=1,
            pageToken=nextPageToken
        ).execute()
        lstItems.extend(response.get('items'))
        nextPageToken = response.get('nextPageToken')

    print(pd.DataFrame(lstItems))



"""
Create A Task List using the Google Tasks API
"""
def createTaskList(name):
    TaskListAssignments = service.tasklists().insert(  # Creates an insert request
        body={'title': name}
    ).execute()
    selectedTaskListID = TaskListAssignments["id"]
    return selectedTaskListID

"""
Create A Task using the Google Tasks API
"""

def createTask(id, title, notes, due, status, deleted):
    taskBody = {
        'title': title,
        'notes': notes,
        'due': due,
        'deleted': deleted,
        'status': status
    }

    taskListAssignments = service.tasks().insert( #Creates an insert request
            tasklist=id,
            body=taskBody
    ).execute()




