import attr
import curses

from .events import Message, sig
from .ascii_keycodes import *

def centered(y, text):
    return y, curses.COLS//2-len(text)//2, text

@attr.s
class Renderer:
    stdscr = attr.ib()
    app_context = attr.ib()

    _current_view = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._current_view = self.index
        self.centerrow = curses.LINES //2 

    def reverse(self, key):
        """
        reverse switches to another view in response to recieved key
        """
        self._current_view(key)    

    def update(self, **context):
        """
        update delegates to the artist service to paint the corresponding view
        """
        self.stdscr.clear()
        self._current_view(None, **context)
        
        c = self.stdscr.getch()
        if c != -1:
            self.app_context.next(Message(sig.USERINPUT, to='win', body={'key':c})) 

        self.stdscr.refresh()

    def base(self, datetime_display):
        """
        base draws elements common to all views that inherit from it
        """
        offset_y = len(datetime_display)
        self.stdscr.addstr(0, curses.COLS-offset_y-1, datetime_display)
        self.stdscr.addstr(curses.LINES-1, 0, "Press X to quit")
        
    def index(self, key, **kwargs):
        """
        index draws the elements of the landing page. 
        """
        if key is None: 
            self.base(**kwargs)

            self.stdscr.addstr(*centered(self.centerrow -1, 'My Application'))
            self.stdscr.addstr(*centered(self.centerrow +1, 'Author: Tang U-Liang'))
            self.stdscr.addstr(*centered(self.centerrow +2, 'v0.0.0'))
            self.stdscr.addstr(*centered(self.centerrow +4, 'Press <ENTER> to continue'))
        
        elif key in ENTER:
            self._current_view = self.main
        
    def main(self, key, **kwargs):
        """
        main draws the elements of the application main page.
        """
        if key is None: 
            self.base(**kwargs)

            self.stdscr.addstr(*centered(self.centerrow, 'Hello World!'))
            self.stdscr.addstr(*centered(self.centerrow+2, 'Press <SPACE> to return'))

        elif key in SPACEBAR:
            self._current_view = self.index
