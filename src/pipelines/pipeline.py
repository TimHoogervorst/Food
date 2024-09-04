from .gather import gather
from .logging import log

from uuid import uuid4


def pipeline():
    
    ## Insert functions to run pipeline here
    try:
        process_id = uuid4()
        print(f'Starting Process Gather -> "Process ID: {process_id}')
        gather()
    except Exception as e:
        log(process_id, 'Gather', 'Failed', e)
        print(f'Exceptioon Occured with Gather -> {e}')
        



