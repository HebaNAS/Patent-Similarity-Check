# -*- coding: utf-8 -*-

import logging
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

# Create an event handler to start watchinf for
# folder changes
class AddEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    # We're only watching for added files
    def on_created(self, event):
        if not event.is_directory:
            print('file created')

            # Stop the observer if a file is added
            self.observer.stop()

def main(context, dag_run_obj):
    """
    This script watches a folder (and subfolders) for any added files
    """

    # Assign the folder to be watched
    path = '/usr/local/airflow/PDFs'

    # Create an observer
    observer = Observer()

    # Inject the observer into the event handler created previously
    event_handler = AddEventHandler(observer)

    # Start the observer
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    observer.join()

    # Return result to airflow DAG
    dag_run_obj.payload = {'message': True}
    return dag_run_obj

if __name__ == "__main__":
    main(context, dag_run_obj)