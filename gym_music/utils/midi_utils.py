#Code from github.com/djosix/Performance-RNN-PyTorch
#Provided under MIT License Copyright (c) 2018 Yuankui Lee

from  .sequence import EventSeq, ControlSeq


def event_indices_to_midi_file(event_indices, midi_file_name, velocity_scale=0.8):
    event_seq = EventSeq.from_array(event_indices)
    note_seq = event_seq.to_note_seq()
    for note in note_seq.notes:
        note.velocity = int((note.velocity - 64) * velocity_scale + 64)
    note_seq.to_midi_file(midi_file_name)

