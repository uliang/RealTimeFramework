import sys
import attr
import time

from .ao_base import ActiveObject
from .events import sig, Message
from .ascii_keycodes import *

@attr.s
class Window(ActiveObject):
    _renderer_service = attr.ib(init=False, default=None)

    def init(self, event):
        self._renderer_service.stdscr.nodelay(True)
        self._renderer_service.stdscr.clearok(True)
        
    def dispatch(self, event):
        if event.sig is sig.TERMINATE:
            sys.exit()

        elif event.sig is sig.TICK:
            datetime_display = time.strftime("%a, %d %B %Y %H:%M:%S", time.localtime())           
            self._renderer_service.update(datetime_display=datetime_display)

        elif event.sig is sig.USERINPUT:
             keypress = event.body["key"]
             self.handle_user_input(keypress)

    def start(self, prior, start_event, *, renderer_service, **kwargs):
        self._renderer_service = renderer_service
        
        super().start(prior, start_event, **kwargs)

    def handle_user_input(self, key):
        if key in QUIT_CHARS:  
            self.send(Message(subject=sig.TERMINATE))
        else:
            self._renderer_service.reverse(key)

