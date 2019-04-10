import time
import multiprocessing
from os import getpid


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's process to wait for the next frame."""
        ident = getpid()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a multiprocessing.Event() and a timestamp
            self.events[ident] = [multiprocessing.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera process when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's process after a frame was processed."""
        self.events[getpid()][0].clear()


class BaseCamera(object):
    process = None  # background process that reads frames from camera
    frame = None  # current frame is stored here by background process
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self):
        """Start the background camera process if it isn't running yet."""
        if BaseCamera.process is None:
            BaseCamera.last_access = time.time()

            # start background frame process
            BaseCamera.process = multiprocessing.Process(target=self._process)
            BaseCamera.process.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera process
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _process(cls):
        """Camera background process."""
        print('Starting camera process.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the process
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera process due to inactivity.')
                break
        BaseCamera.process = None
