class BehaviorTask(object):
    """This is the base class for behavior tasks"""

    def __init__(self):
        pass

    def loop(self):
        """ "Generator that performs one loop of behavior based on current shared state."""
        raise RuntimeError("Must be implemented by subclasses.")
