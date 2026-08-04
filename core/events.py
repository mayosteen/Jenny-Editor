class EventBus:
    def __init__(self):
        self._subs = {}
    def subscribe(self, ev, cb):
        self._subs.setdefault(ev, []).append(cb)
    def emit(self, ev, data=None):
        for cb in self._subs.get(ev, [])[:]:
            cb(data)
    def unsubscribe(self, ev, cb):
        if ev in self._subs and cb in self._subs[ev]:
            self._subs[ev].remove(cb)

event_bus = EventBus()