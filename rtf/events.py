import attr
from enum import Enum
from collections import namedtuple

# Signals --------------------------------------------------------------------------
class sig(Enum):
    HANDLED = 1
    IGNORED = 2
    TRANSITIONED = 3
    SUPER = 12

    ENTRY = 4
    EXIT = 5
    INIT = 6
    EMPTY = 7

    TICK = 8
    TERMINATE = 9
    USERINPUT = 10 
    UPDATE = 11

# Events ----------------------------------------------------------------------------
Event = namedtuple('Event', ['sig', 'body'])    

@attr.s
class Message: 
    subject:sig = attr.ib()
    to = attr.ib(default=None)
    body = attr.ib(default=None)

    def get_event(self): 
        return Event(sig=self.subject, body=self.body)

# Helper functions ------------------------------------------------------------------

def trigger(ao, signal):
    """
    trigger helps wraps signal into a simple event object and dispatch it into the ao
    """
    event = Event(signal)
    ao.dispatch(event)

def transition(ao, target_state:str):
    """
    transition puts ao into target state and returns the transition taken signal to the
    caller.
    """
    ao.state = getattr(ao, target_state, None)  
    return sig.TRANSITIONED

def ignored():
    """
    ignored returns the ignored signal to the caller indicating that the ao did not 
    process that event. 
    """
    return sig.IGNORED

def handled():
    """
    handled returns the handled signal to the caller indicating that the event 
    was processed and effects run
    """
    return sig.HANDLED

def enter(state_handler): 
    """
    enter signals the state to undertake its entry actions
    """
    state_handler(Event(sig.ENTRY)) 

def exit_(state_handler): 
    """
    exit signals the state to undertake its exit actions
    """
    state_handler(Event(sig.EXIT))

def superstate(ao, state): 
    """
    superstate puts the ao into the parent state of the current state
    (usually if the current state does not handle the event recieved), 
    it then returns the super signal to tell the dispatch method that 
    the event is to be processed by the parent state. 
    """
    ao._state = state 
    return sig.SUPER


