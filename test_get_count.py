#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import sys
sys.path.insert(0, '.')
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

# Check if there are any State objects before attempting to access them
state_objects = storage.all(State)
if state_objects:
    first_state_id = list(state_objects.values())[0].id
    print("First state: {}".format(storage.get(State, first_state_id)))
else:
    print("No State objects in storage.")
