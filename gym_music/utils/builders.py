import note_seq
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2

def idx_to_proto_token(idx):
    pass

class MidiBuilder():
  """
  Builder pattern for midi files from repeated
  appends of token indices
  """

  def __init__(self):
    self.token_sequence = []
    self.idx_to_token = idx_to_proto_token
    
  def append(self, output_idx):
    next_token = self.idx_to_token(output_idx)
    self.proto_sequence.append(next_token)
    
  def reset(self):
    self.token_sequence = []
  
  def build(self, midi_path):
    note_seq.sequence_proto_to_midi_file(self.token_sequence, midi_path)
    return midi_path



