from . import midi_utils 
import numpy as np 
import random 

class MidiBuilder():
  """
  Builder pattern for midi files from repeated
  appends of token indices
  """

  def __init__(self,builder_idx = None):
    self.proto_sequence = []
    if builder_idx is None:
        self.builder_idx = random.randint(0,1000)
    else:
        self.builder_idx = builder_idx
    self.midi_idx = 0

    
  def append(self, next_proto):
    self.proto_sequence.append(next_proto)
    
  def reset(self):
    self.token_sequence = []
    self.midi_idx = 0

  def close(self):
    pass
  
  def build(self, midi_path = None):
    if midi_path is None:
        midi_path = "./output/midi_{}_{}.mid".format(self.builder_idx, self.midi_idx)
    cat_sequence = np.concatenate(self.proto_sequence,axis = 0)
    midi_utils.event_indices_to_midi_file(cat_sequence, midi_path)
    self.midi_idx = self.midi_idx + 1
    
    return midi_path




