#!/usr/bin/env python
# animation.py for storing image sequences and key


class Animation:
    def __init__(self, key="", sequence=[], attrs={}):
        self.key = key
        self.sequence = sequence
        self.attrs = attrs

    def add_frame(self, frame):
        self.sequence.append(frame)

    def set_key(self, key):
        self.key = key

    def get_reversed(self):
        frame = self.attrs.get("hold_frame", -1)
        new_attrs = self.attrs.copy()
        return Animation("rev_" + self.key, self.sequence[::-1], new_attrs)

    def __getitem__(self, key):
        return self.sequence[-1] if len(self.sequence) <= key else self.sequence[key]

    def __len__(self):
        return len(self.sequence)

    def is_latch(self):
        return self.attrs.get("latch", True)

    def get_latched(self):
        frame = self.attrs.get("hold_frame", -1)
        newAttrs = self.attrs.copy()
        return Animation("hold_" + self.key, [self.sequence[frame]])
