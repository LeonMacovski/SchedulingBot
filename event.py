class Event:
    def __init__(self, scheduler, time, title):
        self.scheduler = scheduler
        self.time = time
        self.title = title
        self.subscribers = []

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            return 1
        return 0
