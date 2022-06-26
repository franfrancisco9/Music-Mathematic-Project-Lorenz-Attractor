from music21 import *
import copy 
import matplotlib.pyplot as plt
import numpy as np
from creating_lorenz import Lorenz
from analysis import analysis

bach = converter.parse('bwv860.mxl')
bach.write('midi', fp='../data/original/bach.mid')
bach.write('musicxml', fp='../data/original/bach.mxl')

bach_variation = converter.parse('bwv860.mxl')
bach.id = 'bach'
bach_variation.id = 'bach_variation'
# see score
#bach.show('musicxml')

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
xpoints_variation_rh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_rh, initial = np.array([0.95, 1.0, 1.0]))
xpoints_variation_rh_divison = []
for i in range(len(right_hand_notes)):
    current_measure = []
    for j in range(len(right_hand_notes[i])):
        current_measure.append(xpoints_variation_rh[i])
    xpoints_variation_rh_divison.append(current_measure)

right_hand_notes_var = []
for i in range(1, measures + 1):
    current_notes = []
    for j in range(len(right_hand_notes[i-1])):
        dif = xpoints_variation_rh_divison[i-1][j] / xpoints_ref_rh_divison[i-1][j]
        dif_pitch = right_hand_notes[i-1][j] * dif
        #print(dif_pitch)
        current_notes.append(dif_pitch)
        right_hand.measure(i).notes[j].pitch.frequency = dif_pitch 
    right_hand_notes_var.append(current_notes)


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
xpoints_variation_lh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_lh, initial = np.array([0.95,1.0,1.0]))
xpoints_variation_lh_divison = []
for i in range(len(left_hand_notes)):
    current_measure = []
    for j in range(len(left_hand_notes[i])):
        current_measure.append(xpoints_variation_lh[i])
    xpoints_variation_lh_divison.append(current_measure)

left_hand_notes_var = []
for i in range(1, measures + 1):
    current_notes = []
    for j in range(len(left_hand_notes[i-1])):
        dif = xpoints_variation_lh_divison[i-1][j] / xpoints_ref_lh_divison[i-1][j]
        dif_pitch = left_hand_notes[i-1][j] * dif
        #print(dif_pitch)
        current_notes.append(dif_pitch)
        left_hand.measure(i).notes[j].pitch.frequency = dif_pitch 
    left_hand_notes_var.append(current_notes)



newfig = plt.figure()
full_notes = []
full_notes_var = []
for i in range(1, measures + 1):
    for j in range(len(right_hand_notes[i-1])):
        full_notes.append(right_hand_notes[i-1][j])
        full_notes_var.append(right_hand_notes_var[i-1][j])

plt.plot(full_notes,'b', label= "Original")
plt.plot(full_notes_var, 'r', label = "Variação")
plt.title("Desvio das frequências da mão direita")
plt.ylabel("Frequência [Hz]")
plt.xlabel("Índice da nota")
plt.autoscale
plt.grid()
#plt.show()
plt.savefig("../images/desvio_variacao_rh.png")

newfig = plt.figure()
full_notes = []
full_notes_var = []
for i in range(1, measures + 1):
    for j in range(len(left_hand_notes[i-1])):
        full_notes.append(left_hand_notes[i-1][j])
        full_notes_var.append(left_hand_notes_var[i-1][j])

plt.plot(full_notes,'b', label= "Original")
plt.plot(full_notes_var, 'r', label = "Variação")
plt.title("Desvio das frequências da mão esquerda")
plt.ylabel("Frequência [Hz]")
plt.xlabel("Índice da nota")
plt.autoscale
plt.grid()
#plt.show()
plt.savefig("../images/desvio_variacao_lh.png")

right_hand.write('midi', fp='../data/var/bach_var_rh.mid')
left_hand.write('midi', fp='../data/var/bach_var_lh.mid')
right_hand.write('musicxml', fp='../data/var/bach_var_rh.mxl')
left_hand.write('musicxml', fp='../data/var/bach_var_lh.mxl')
bach.write('midi', fp='../data/var/bach_var.mid')
bach.write('musicxml', fp='../data/var/bach_var.mxl')

#right_hand.show("midi")
#left_hand.show("midi")
#bach.augmentOrDiminish(2)
#bach.show("midi")
#bach.show("musicxml")


for i in range(10):
    right_hand_notes_new = right_hand_notes_var
    right_hand_notes_var = []
    for i in range(1, measures + 1):
        current_notes = []
        for j in range(len(right_hand_notes_new[i-1])):
            dif = xpoints_variation_rh_divison[i-1][j] / xpoints_ref_rh_divison[i-1][j]
            dif_pitch = right_hand_notes_new[i-1][j] * dif
            #print(dif_pitch)
            current_notes.append(dif_pitch)
            right_hand.measure(i).notes[j].pitch.frequency = dif_pitch 
        right_hand_notes_var.append(current_notes)

newfig = plt.figure()
full_notes = []
full_notes_var = []
for i in range(1, measures + 1):
    for j in range(len(right_hand_notes[i-1])):
        full_notes.append(right_hand_notes[i-1][j])
        full_notes_var.append(right_hand_notes_var[i-1][j])

plt.plot(full_notes,'b', label= "Original")
plt.plot(full_notes_var, 'r', label = "Variação")
plt.title("Desvio das frequências da mão direita após 10 iterações")
plt.ylabel("Frequência [Hz]")
plt.xlabel("Índice da nota")
plt.autoscale
plt.grid()
#plt.show()
plt.savefig("../images/desvio_variacao_rh_10.png")




for i in range(10):
    left_hand_notes_new = left_hand_notes_var
    left_hand_notes_var = []
    for i in range(1, measures + 1):
        current_notes = []
        for j in range(len(left_hand_notes_new[i-1])):
            dif = xpoints_variation_lh_divison[i-1][j] / xpoints_ref_lh_divison[i-1][j]
            dif_pitch = left_hand_notes_new[i-1][j] * dif
            #print(dif_pitch)
            current_notes.append(dif_pitch)
            left_hand.measure(i).notes[j].pitch.frequency = dif_pitch 
        left_hand_notes_var.append(current_notes)

newfig = plt.figure()
full_notes = []
full_notes_var = []
for i in range(1, measures + 1):
    for j in range(len(left_hand_notes[i-1])):
        full_notes.append(left_hand_notes[i-1][j])
        full_notes_var.append(left_hand_notes_var[i-1][j])

plt.plot(full_notes,'b', label= "Original")
plt.plot(full_notes_var, 'r', label = "Variação")
plt.title("Desvio das frequências da mão esquerda após 10 iterações")
plt.ylabel("Frequência [Hz]")
plt.xlabel("Índice da nota")
plt.autoscale
plt.grid()
#plt.show()
plt.savefig("../images/desvio_variacao_lh_10.png")

right_hand.write('midi', fp='../data/var/bach_var_rh_10.mid')
left_hand.write('midi', fp='../data/var/bach_var_lh_10.mid')
right_hand.write('musicxml', fp='../data/var/bach_var_rh_10.mxl')
left_hand.write('musicxml', fp='../data/var/bach_var_lh_10.mxl')
bach.write('midi', fp='../data/var/bach_var_10.mid')
bach.write('musicxml', fp='../data/var/bach_var_10.mxl')

#bach.show("musicxml")

# Check for equal notes in different initial conditions
conds = []
right_hand_notes_var_equal = []
left_hand_notes_var_equal = []
for initial_cond in [-5.005 + 0.005 * i for i in range(2002)]:
    conds.append(initial_cond)
    # Right Hand Code
    # get variation trajectory x values via Lorenz
    xpoints_variation_rh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_rh, initial = np.array([initial_cond, 1.0, 1.0]))
    xpoints_variation_rh_divison = []
    for i in range(len(right_hand_notes)):
        current_measure = []
        for j in range(len(right_hand_notes[i])):
            current_measure.append(xpoints_variation_rh[i])
        xpoints_variation_rh_divison.append(current_measure)
    
    right_hand_notes_equal = 0
    for i in range(1, measures + 1):
        current_notes = []
        for j in range(len(right_hand_notes[i-1])):
            dif = xpoints_variation_rh_divison[i-1][j] / xpoints_ref_rh_divison[i-1][j]
            dif_pitch = right_hand_notes[i-1][j] * dif
            if abs(abs(dif_pitch) - right_hand_notes[i-1][j]) < 10:
                right_hand_notes_equal += 1
    right_hand_notes_var_equal.append(right_hand_notes_equal)


    # Left Hand Code
    # get variation trajectory x values via Lorenz
    xpoints_variation_lh, _, _ = Lorenz(start = 0, end= 30, step_count = number_of_notes_lh, initial = np.array([initial_cond,1.0,1.0]))
    xpoints_variation_lh_divison = []
    for i in range(len(left_hand_notes)):
        current_measure = []
        for j in range(len(left_hand_notes[i])):
            current_measure.append(xpoints_variation_lh[i])
        xpoints_variation_lh_divison.append(current_measure)

    left_hand_notes_equal = 0
    for i in range(1, measures + 1):
        current_notes = []
        for j in range(len(left_hand_notes[i-1])):
            dif = xpoints_variation_lh_divison[i-1][j] / xpoints_ref_lh_divison[i-1][j]
            dif_pitch = left_hand_notes[i-1][j] * dif
            if abs(dif_pitch - left_hand_notes[i-1][j]) < 10:
                left_hand_notes_equal += 1
    left_hand_notes_var_equal.append(left_hand_notes_equal)
    

newfig = plt.figure()
plt.plot(conds, [i/number_of_notes_rh * 100 for i in right_hand_notes_var_equal],'b', label= "Número de notas iguais [%]")
#plt.plot(conds, right_hand_notes_var_equal, 'r', label = "Número de notas iguais na mão direita")
plt.title("Variação do número de notas iguais  - mão direita")
plt.ylabel("Número de notas iguais [%]")
plt.xlabel("Condição inicial de x")
plt.autoscale
plt.grid()
#plt.show()
plt.savefig("../images/condicao_inicial_rh.png")

newfig = plt.figure()
plt.plot(conds, [i/ number_of_notes_lh * 100 for i in left_hand_notes_var_equal],'b', label= "Número de notas iguais [%]")
#plt.plot(conds, right_hand_notes_var_equal, 'r', label = "Número de notas iguais na mão direita")
plt.title("Variação do número de notas iguais - mão esquerda")
plt.ylabel("Número de notas iguais [%]")
plt.xlabel("Condição inicial de x")
plt.autoscale
plt.grid()
#plt.show()
plt.savefig("../images/condicao_inicial_lh.png")

analysis("bwv860.mxl")
analysis("canon.mxl")
analysis("chopin.mxl")
analysis("schoenberg.mxl")
analysis("webern.mxl")