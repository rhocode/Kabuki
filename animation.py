#!/usr/bin/env python

# animation.py for storing image sequences and key
class Animation:

	def __init__(self, key = '', sequence = []):
		self.key = key
		self.sequence = sequence

	def add_frame(self, frame):
		self.sequence.append(frame)

	def set_key(self, key):
		self.key = key

	def get_reversed(self):
		return Animation('rev_' + self.key, self.sequence[::-1])

	def __getitem__(self, key):
		return self.sequence[-1] if len(self.sequence) <= key else self.sequence[key]

	def __len__(self):
		return len(self.sequence)