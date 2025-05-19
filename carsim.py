# Copyright 2016 Gabriele Sales <gbrsales@gmail.com>

from functools import wraps
from subprocess import Popen, PIPE, TimeoutExpired
import atexit
import numpy as np
import random


def restart_on_broken_pipe(m):
  @wraps(m)
  def wrapper(self, *args, **kwargs):
    try:
      return m(self, *args, **kwargs)
    except BrokenPipeError:
      self._restart()
      return m(self, *args, **kwargs)

  return wrapper


class Simulator:

  NUM_T = [type(1), type(1.0), int, float, np.double]

  def __init__(self):
    self._start_worker()

  def _start_worker(self):
    self._worker = None
    self._restart()
    atexit.register(self._shutdown)

  def _restart(self):
    if self._worker is not None:
      self._shutdown()

    self.port = random.randint(1025, 0xffff)

    try:
      self._worker = Popen(['./carsim', str(self.port)], stdin=PIPE, stdout=PIPE,
                           universal_newlines=True)
    except OSError as e:
      raise SimulatorError('There was an unexpected error starting the simulator ☹') from e

  def _shutdown(self):
    assert self._worker is not None

    try:
      self._worker.communicate(timeout=10)
    except TimeoutExpired:
      self._worker.kill()

  def __repr__(self):
    return '<Running Car Simulation>'

  ## Simulation of a single car
  #
  @restart_on_broken_pipe
  def simulate(self, frame_width, upper_shape, lower_shape, left_wheel,
               right_wheel):

    self._check_num('frame_width', frame_width)
    self._check_nums('upper_shape', 5, upper_shape)
    self._check_nums('lower_shape', 5, lower_shape)
    self._check_nums('left_wheel', 2, left_wheel)
    self._check_nums('right_wheel', 2, right_wheel)

    self._send('SIM' + \
               self._car_spec(frame_width, upper_shape, lower_shape,
                              left_wheel, right_wheel))

    state_num = int(self._recv())
    return self._recv_states(state_num)

  @classmethod
  def _check_num(klass, label, value):
    assert type(value) in klass.NUM_T, label + ' should be a number'

  @classmethod
  def _check_nums(klass, label, length, value):
    assert hasattr(value, '__len__'), \
           label + ' should be a container (a list or an array)'
    assert len(value) == length, \
           '%s should have length %d' % (label, length)

    for idx, entry in enumerate(value):
      klass._check_num('%s[%d]' % (label, idx), entry)

  def _send(self, cmd):
    fd = self._worker.stdin
    fd.write(cmd)
    fd.flush()

  @staticmethod
  def _car_spec(frame_width, upper_shape, lower_shape, left_wheel, right_wheel):

    return ' %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n' % \
           (frame_width, upper_shape[0], upper_shape[1], upper_shape[2],
            upper_shape[3], upper_shape[4], lower_shape[0], lower_shape[1],
            lower_shape[2], lower_shape[3], lower_shape[4], left_wheel[0],
            left_wheel[1], right_wheel[0], right_wheel[1])

  def _recv(self):
    line = self._worker.stdout.readline().rstrip()
    if line.startswith('ERR '):
      raise SimulationError(line[4:])
    else:
      return line

  def _recv_states(self, state_num):
    out = np.zeros((state_num, 3), dtype=np.double)

    for i in range(state_num):
      tokens = self._worker.stdout.readline().rstrip().split(' ')
      out[i] = [ np.double(t) for t in tokens ]

    return out

  ## Race among cars
  #
  @restart_on_broken_pipe
  def race(self, cars):
    self._check_cars(cars)
    self._send_race(cars)
    return self._recv_scores(len(cars))

  @classmethod
  def _check_cars(klass, cars):
    assert hasattr(cars, '__len__'), 'cars should be a list'
    assert len(cars) > 0, 'cars should not be an empty list'
    assert len(cars) <= 100, \
      'you have provided too many cars (use a number less or equal to 100)'

    for idx, (frame_width, upper_shape, lower_shape, left_wheel, right_wheel) \
        in enumerate(cars):
      klass._check_num('frame_width of car %d' % idx, frame_width)
      klass._check_nums('upper_shape of car %d' % idx, 5, upper_shape)
      klass._check_nums('lower_shape of car %d' % idx, 5, lower_shape)
      klass._check_nums('left_wheel of car %d' % idx, 2, left_wheel)
      klass._check_nums('right_wheel of car %d' % idx, 2, right_wheel)

  def _send_race(self, cars):
    fd = self._worker.stdin
    fd.write('RACE %d' % len(cars))

    for frame_width, upper_shape, lower_shape, left_wheel, right_wheel \
        in cars:
      fd.write(self._car_spec(frame_width, upper_shape, lower_shape,
                              left_wheel, right_wheel))

    fd.flush()

  def _recv_scores(self, car_num):
    head = self._recv()

    out = np.zeros((car_num, 2), dtype=np.double)
    out[0] = [ np.double(t) for t in head.split(' ') ]

    fd = self._worker.stdout
    for i in range(1, car_num):
      out[i] = [ np.double(t) for t in fd.readline().rstrip().split(' ') ]

    return out

  ## Track generation
  #
  @restart_on_broken_pipe
  def new_track(self):
    self._worker.stdin.write('TRACK\n')
    self._worker.stdin.flush()

    if self._recv() != 'DONE':
      raise SimulatorError('the simulator was not able to generate a new track ☹')


class SimulatorError(Exception):
  pass

class SimulationError(Exception):
  pass


_simulator = Simulator()
print('''\
Simulator started.

Now open the webpage at this address in a separate browser window: http://localhost:%d/''' %
      _simulator.port)

def simulate(frame_width, upper_shape, lower_shape, left_wheel, right_wheel):
  ''' Simulate the race of a single car.

      Returns an N-by-3 matrix containing the (X,Y) positions and orientation
      (angle) of the car frame at successive time points.

      You can follow the simulation in the browser at the following address:
        http://localhost:8111/
  '''
  _simulator.simulate(frame_width, upper_shape, lower_shape,
                      left_wheel, right_wheel)

def race(cars):
  ''' Simulate the race of multiple cars.

      Returns an N-by-2 matrix containing the distance covered and the amount
      of time it took for each car. You can use this information to evaluate
      the performance of different cars.
  '''
  return _simulator.race(cars)

def new_track():
  ''' Generate a new racing track.

      The new track will be used for all the following simulations and races.
  '''
  return _simulator.new_track()
