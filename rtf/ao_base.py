from abc import ABC, abstractmethod
from collections import deque 
import attr 
import rx.operators as ops 


@attr.s
class ActiveObject(ABC): 
    """
    ActiveObject represents a "thread" of execution on every "tick" of the application.
    Implement the init and dispatch methods in subclasses.  
    """
    name = attr.ib()
    _app_context = attr.ib() 

    priority = attr.ib(init=False, default=0, order=True, eq=True)
    _eventq = attr.ib(init=False, factory=deque) 

    def __attrs_post_init__(self):
        self._app_context.register(self.name, self)

    @abstractmethod
    def init(self, event):
        """
        init is responsible for putting the ao into its default state. You can pass 
        in an event instance to send initialization parameters to the ao.
        """
        
    @abstractmethod
    def dispatch(self, event):
        """
        dispatch takes event and executes the essential business logic of the ao in response 
        to event signals. 
        """
    
    def execute(self):
        """ 
        execute pops an event from the event queue and dispatches it to self.  
        """
        if len(self._eventq):
            event=self._eventq.pop()
            self.dispatch(event)

    def put(self, event):
        """
        put inserts an event into the objects event queue in FIFO order. 
        """ 
        self._eventq.append(event)

    def start(self, prior, start_event):
        """
        start puts this ao into it's initial state as well as as injecting required 
        services into the object.
        """
        self.priority=prior

        # end by sending initialization signal to object
        self.init(start_event) 
    
    def send(self, message):
        """
        send delegates to the .next method of the messaging service. 
        """
        if message.to is None: 
            message.to = self.name
        self._app_context.next(message)
