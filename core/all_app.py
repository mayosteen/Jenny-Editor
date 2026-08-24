import importlib
all_app = [
    "terminal",
    "chords",
    "subtitle",
    "animation",
    "caftr",
    "grid",
]
for app in all_app:
    importlib.import_module(f"apps.{app}")