from music21 import *
import matplotlib.pyplot as plt
import numpy as np


def analysis(filename):
    piece = converter.parse(filename)
    right_hand = piece.parts[0]
    left_hand  = piece.parts[1]
    measures = len(piece.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure))

    # Right Hand Code
    right_hand_notes = []
    for i in range(1, measures + 1):
        current_measure = right_hand.measure(i)
        #print("Current measure:" + str(i)) # print current measure
        current_notes = []
        try:
            for j in range(len(current_measure.getElementsByClass(note.Note))):
                try:
                    current_notes.append(current_measure.notes[j].pitch.frequency)
                except:
                    current_notes.append(current_measure.notes[j].notes[0].pitch.frequency)
        except:
            pass
        #print("Notes for this measure:" + str(right_hand_notes))
        right_hand_notes.append(current_notes)

    number_of_notes_rh = 0
    for j in range(len(right_hand_notes)):
        for i in range(len(right_hand_notes[j])):
            number_of_notes_rh += 1


    # Left Hand Code
    left_hand_notes = []
    for i in range(1, measures + 1):
        current_measure = left_hand.measure(i)
        #print("Current measure:" + str(i)) # print current measure
        current_notes = []
        try:
            for j in range(len(current_measure.getElementsByClass(note.Note))):
                try:
                    current_notes.append(current_measure.notes[j].pitch.frequency)
                except:
                    current_notes.append(current_measure.notes[j].notes[0].pitch.frequency)
        except:
            pass
        #print("Notes for this measure:" + str(left_hand_notes))
        left_hand_notes.append(current_notes)

    number_of_notes_lh = 0
    for j in range(len(left_hand_notes)):
        for i in range(len(left_hand_notes[j])):
            number_of_notes_lh += 1

    newfig = plt.figure()
    full_notes_rh = []
    for i in range(1, measures + 1):
        for j in range(len(right_hand_notes[i-1])):
            full_notes_rh.append(right_hand_notes[i-1][j])
    plt.plot([full_notes_rh[i-1] for i in range(1, len(full_notes_rh))], [full_notes_rh[i] for i in range(1, len(full_notes_rh))], 'b',  marker='D',mfc='orange', label= "Trajetória mão direita")
    plt.title("Atrator da mão direita")
    plt.xlabel("Frequência da nota anterior [Hz]")
    plt.ylabel("Frequência da nota atual [Hz]")
    plt.autoscale
    plt.grid()
    #plt.show()
    plt.savefig("../images/atrator_rh_" + filename + ".png")

    newfig = plt.figure()
    full_notes_lh = []
    for i in range(1, measures + 1):
        for j in range(len(left_hand_notes[i-1])):
            full_notes_lh.append(left_hand_notes[i-1][j])
    plt.plot([full_notes_lh[i-1] for i in range(1, len(full_notes_lh))], [full_notes_lh[i] for i in range(1, len(full_notes_lh))], 'g', marker='D',mfc='red', label= "Trajetória mão esquerda")
    plt.title("Atrator da mão esquerda")
    plt.xlabel("Frequência da nota anterior [Hz]")
    plt.ylabel("Frequência da nota atual [Hz]")
    plt.autoscale
    plt.grid()
    #plt.show()
    plt.savefig("../images/atrator_lh_" + filename + ".png")

    newfig = plt.figure()
    plt.plot([full_notes_rh[i-1] for i in range(1, len(full_notes_rh))], [full_notes_rh[i] for i in range(1, len(full_notes_rh))], 'b',  marker='D',mfc='orange', label= "Trajetória mão direita")
    plt.plot([full_notes_lh[i-1] for i in range(1, len(full_notes_lh))], [full_notes_lh[i] for i in range(1, len(full_notes_lh))], 'g',  marker='D',mfc='red', label= "Trajetória mão esquerda")
    plt.title("Atrator com ambas as mãos")
    plt.xlabel("Frequência da nota anterior [Hz]")
    plt.ylabel("Frequência da nota atual [Hz]")
    plt.autoscale
    plt.grid()
    #plt.show()
    plt.savefig("../images/atrator_both_" + filename + ".png")

