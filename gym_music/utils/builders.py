from .midi_utils import event_indices_to_midi_file 

class MidiBuilder():
  """
  Builder pattern for midi files from repeated
  appends of token indices
  """

  def __init__(self, builder_idx = 0):
    self.proto_sequence = []
    self.builder_idx = builder_idx
    self.midi_idx = 0

    
  def append(self, next_proto):
    self.proto_sequence.append(next_proto)
    
  def reset(self):
    self.token_sequence = []
    #self.midi_idx = 0
  
  def build(self, midi_path = None):
    if midi_path is None:
        midi_path = "./output/tmp/midi_{}_{}.mid".format(self.builder_idx, self.midi_idx)
    midi_utils.event_indices_to_midi_file(self.proto_sequence, midi_path)
    self.midi_idx = self.midi_idx + 1
    
    return midi_path




