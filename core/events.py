class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)

    def emit(self, event_type, event=None):
        # print(f"{event_type}: {event}")
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(event)

event_bus = EventBus()