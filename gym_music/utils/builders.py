from . import midi_utils 
import numpy as np 
import random 

class Builder():
  def __init__(self):
    pass
  def append(self, next_action):
    pass

  def build(self, output_path = None):
    return output_path
  
  def close(self):
    pass

  def reset(self):
    pass



class MidiBuilder(Builder):
  """
  Builder pattern for midi files from repeated
  appends of token indices
  """

  def __init__(self,builder_idx = None):
    super().__init__()
    self.proto_sequence = []
    if builder_idx is None:
        self.builder_idx = random.randint(0,1000)
    else:
        self.builder_idx = builder_idx
    self.midi_idx = 0

    
  def append(self, next_proto):
    self.proto_sequence.append(next_proto)
    
  def reset(self):
    self.proto_sequence = []
    self.midi_idx = 0

  def close(self):
    pass
  
  def build(self, midi_path = None):
    if midi_path is None:
        midi_path = "./output/midi_{}_{}.mid".format(self.builder_idx, self.midi_idx)
    proto_sequence = np.array(self.proto_sequence, dtype = 'int64')
    midi_utils.event_indices_to_midi_file(proto_sequence, midi_path)
    self.midi_idx = self.midi_idx + 1
    
    return midi_path

    def __str__(self):
      return "proto|"+str(self.proto_sequence)




