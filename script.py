import time
import logging
from datetime import datetime
from pytodoist import todoist
from pytodoist.api import TodoistAPI

#Setup loggging
FORMAT = '%(asctime)-15s, %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

#Setup todoists
user = todoist.login('ryqiem@gmail.com', 'YpaPiY3P4CMbdUd')
logger.info("Finished setting up todoist login")

#Setup datetime objects
today_object = datetime.today().date()

#API setup
api = TodoistAPI()
response = api.login('ryqiem@gmail.com', 'YpaPiY3P4CMbdUd')
user_info = response.json()
user_api_token = user_info['token']
logger.info("API setup succesful")

def copy_due(inp, outp):
    """
    Takes arguments

    inp: Input project
    outp: Output project

    and copies due tasks from inp to outp
    """
    #Setup projects
    due_tasks = user.get_project(inp).get_uncompleted_tasks()

    i = 1 # Iterator for log
    logger.info("Starting processing of project {project}".format(project=inp.encode('utf-8')))

    for task in due_tasks:
        output_id = user.get_project(outp).id
        if task.due_date_utc is not None:
            # print(task.due_date_utc)
            date_object = datetime.strptime(task.due_date_utc, '%a %d %b %Y %H:%M:%S %z').date()

            if today_object == date_object:
                # notes = task.get_notes()
                label_ids = task.labels

                response = api.add_item(user_api_token, task.content, project_id=output_id, priority=task.priority, labels=str(label_ids))
                logger.info("Created new task {i}".format(i=i))

                task.complete()
                logger.info("Completed old task {i}".format(i=i))
                i += 1 # Update Iterator

    duration = 30
    logger.info("Finished processing {project}, sleeping for {duration}s".format(project=inp, duration=duration))
    time.sleep(duration) # Don't breach 50 requests/min limit from todoist API

# Ticklers
copy_due("Recurrent", "Inbox")
copy_due("Tickler", "Inbox")
copy_due("Computer", "Inbox")
