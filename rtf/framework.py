from typing import Dict
import attr 
from queue import PriorityQueue
from rx.subject.subject import Subject
import rx 
import rx.operators as ops 
from .events import sig, Message


@attr.s
class Framework: 
    _execution_queue = attr.ib(init=False, factory=PriorityQueue)
    _object_registry = attr.ib(init=False, factory=dict) 
    _event_subject = attr.ib(init=False, factory=Subject)

    def __attrs_post_init__(self): 
        self._event_subject.subscribe(on_next=self.schedule_execution)

    def register(self, name, ao):
        """
        register updates the interval object registry with a new 
        id_ ao mapping. 
        """ 
        self._object_registry[name] = ao 

    def register_many(self, mapping:Dict): 
        """
        register_many allows bulk registration of aos
        """
        self._object_registry.update(mapping)

    def schedule_execution(self, message): 
        """
        schedule_execution handles incoming messages by locating active objects, 
        scheduling their processing in the priority queue and inserting message event
        into the active objects event queue. Note that it is the priority of 
        the object which determines the order by which it is popped from the
        queue. 
        """
        ao = self._object_registry[message.to]
        self._execution_queue.put(ao)
        ao.put(message.get_event())

    def next(self, message): 
        """
        next pushes message into the event subject. 
        """ 
        self._event_subject.on_next(message)

    def run_forever(self, tick_recipient, fps=60): 
        subscription = rx.interval(period=1/fps) \
            .pipe(ops.map(lambda _: Message(sig.TICK, to=tick_recipient))) \
            .subscribe(self._event_subject) 

        try: 
            while 1:
                if self._execution_queue.empty(): 
                    continue
                
                ao = self._execution_queue.get()
                ao.execute()
        except SystemExit:
            # exit logic 
            pass 
        finally: 
            # cleanup steps 
            subscription.dispose()
            self._event_subject.dispose()
