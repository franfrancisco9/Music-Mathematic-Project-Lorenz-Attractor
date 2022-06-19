from music21 import *
import copy 
import numpy as np
from creating_lorenz import Lorenz

bach = converter.parse('bwv860.mxl')
bach.write('midi', fp='../data/original/bach.mid')
bach.write('musicxml', fp='../data/original/bach.mxl')

bach_variation = converter.parse('bwv860.mxl')
bach.id = 'bach'
bach_variation.id = 'bach_variation'
# see score
# bach.show('musicxml')

# number of measures excluding the last chord
measures = len(bach.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure)) - 1

right_hand = bach.parts[0]
left_hand  = bach.parts[1]
right_hand.write('midi', fp='../data/original/bach_rh.mid')
left_hand.write('midi', fp='../data/original/bach_lh.mid')
right_hand.write('musicxml', fp='../data/original/bach_rh.mxl')
left_hand.write('musicxml', fp='../data/original/bach_lh.mxl')

# listen to the music
#bach.show("midi")
# listen to the right hand
#right_hand.show("midi")
# listen to the left hand
#left_hand.show("midi")

# plot pitch distribution by measure count:
#bach.plot()

# get music key
print(bach.analyze('key'))


# Right Hand Code
right_hand_notes = []
for i in range(1, measures + 1):
    current_measure = right_hand.measure(i)
    #print("Current measure:" + str(i)) # print current measure
    current_notes = []
    for j in range(len(current_measure.getElementsByClass(note.Note))):
        current_notes.append(current_measure.notes[j].pitch.frequency)
    #print("Notes for this measure:" + str(right_hand_notes))
    right_hand_notes.append(current_notes)

number_of_notes_rh = 0
for j in range(len(right_hand_notes)):
     for i in range(len(right_hand_notes[j])):
        number_of_notes_rh += 1

# get reference trajectory x values via Lorenz
xpoints_reference_rh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_rh, initial = np.array([1.0,1.0,1.0]))
xpoints_ref_rh_divison = []
for i in range(len(right_hand_notes)):
    current_measure = []
    for j in range(len(right_hand_notes[i])):
        current_measure.append(xpoints_reference_rh[i])
    xpoints_ref_rh_divison.append(current_measure)

# get variation trajectory x values via Lorenz
xpoints_variation_rh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_rh, initial = np.array([1.0,1.0,0.99]))
xpoints_variation_rh_divison = []
for i in range(len(right_hand_notes)):
    current_measure = []
    for j in range(len(right_hand_notes[i])):
        current_measure.append(xpoints_variation_rh[i])
    xpoints_variation_rh_divison.append(current_measure)
    
for i in range(1, measures + 1):
    for j in range(len(right_hand_notes[i-1])):
        dif = xpoints_variation_rh_divison[i-1][j] / xpoints_ref_rh_divison[i-1][j]
        dif_pitch = right_hand_notes[i-1][j] * dif
        #print(dif_pitch)
        right_hand.measure(i).notes[j].pitch.frequency = dif_pitch 


# Left Hand Code
left_hand_notes = []
for i in range(1, measures + 1):
    current_measure = left_hand.measure(i)
    #print("Current measure:" + str(i)) # print current measure
    current_notes = []
    for j in range(len(current_measure.getElementsByClass(note.Note))):
        current_notes.append(current_measure.notes[j].pitch.frequency)
    #print("Notes for this measure:" + str(left_hand_notes))
    left_hand_notes.append(current_notes)

number_of_notes_lh = 0
for j in range(len(left_hand_notes)):
     for i in range(len(left_hand_notes[j])):
        number_of_notes_lh += 1
# get reference trajectory x values via Lorenz
xpoints_reference_lh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_lh, initial = np.array([1.0,1.0,1.0]))
xpoints_ref_lh_divison = []
for i in range(len(left_hand_notes)):
    current_measure = []
    for j in range(len(left_hand_notes[i])):
        current_measure.append(xpoints_reference_lh[i])
    xpoints_ref_lh_divison.append(current_measure)

# get variation trajectory x values via Lorenz
xpoints_variation_lh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_lh, initial = np.array([1.0,1.0,0.99]))
xpoints_variation_lh_divison = []
for i in range(len(left_hand_notes)):
    current_measure = []
    for j in range(len(left_hand_notes[i])):
        current_measure.append(xpoints_variation_lh[i])
    xpoints_variation_lh_divison.append(current_measure)
    
for i in range(1, measures + 1):
    for j in range(len(left_hand_notes[i-1])):
        dif = xpoints_variation_lh_divison[i-1][j] / xpoints_ref_lh_divison[i-1][j]
        dif_pitch = left_hand_notes[i-1][j] * dif
        #print(dif_pitch)
        left_hand.measure(i).notes[j].pitch.frequency = dif_pitch 

right_hand.write('midi', fp='../data/var/bach_var_rh.mid')
left_hand.write('midi', fp='../data/var/bach_var_lh.mid')
right_hand.write('musicxml', fp='../data/var/bach_var_rh.mxl')
left_hand.write('musicxml', fp='../data/var/bach_var_lh.mxl')
bach.write('midi', fp='../data/var/bach_var.mid')
bach.write('musicxml', fp='../data/var/bach_var.mxl')

#right_hand.show("midi")
#left_hand.show("midi")
bach.augmentOrDiminish(2)
bach.show("midi")
#bach.show("musicxml")