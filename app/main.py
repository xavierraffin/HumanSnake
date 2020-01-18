import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

#import signal
from xbox360controller import Xbox360Controller

last_axis={"x":0,"y":0}
last_direction='up'

def on_axis_moved(axis):
#    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    global last_axis
    last_axis={"x":axis.x,"y":axis.y}

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    global last_direction
    direction = last_direction

    global last_axis
    print("{}".format(last_axis))

    if(last_axis.get("x",0)<-0.5):
       direction='left'
    elif(last_axis.get("x",0)>0.5):
       direction='right'

    if(last_axis.get("y",0)<-0.5):
       direction='up'
    elif(last_axis.get("y",0)>0.5):
       direction='down'

    last_direction=direction

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    try:
       with Xbox360Controller(0, axis_threshold=0.2) as controller:
          controller.axis_l.when_moved = on_axis_moved
          controller.axis_r.when_moved = on_axis_moved
          bottle.run(
             application,
             host=os.getenv('IP', '0.0.0.0'),
             port=os.getenv('PORT', '8080'),
             debug=os.getenv('DEBUG', True)
          )
    except KeyboardInterrupt:
       pass

