from .framework import Framework
from .window import Window
from .renderer import Renderer

def main(stdscr):
    app = Framework()
    
    # create ao instances 
    win = Window('win', app)

    # initialize services
    renderer = Renderer(stdscr, app) 

    # initialize ao by setting their priority, injecting services and 
    # initial conditions via their .start method
    win.start(1, None, renderer_service=renderer)

    app.run_forever(tick_recipient='win')
