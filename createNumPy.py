from fenConversion import *
import numpy as np
import csv

eval_input = []
eval_output = []
i=0
with open('top-chess-positions.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for info in reader:

        #print(info[0])
        f = FENParser(info[0])
        vector = f.parse()
        #print(vector)
        mate_num = int(info[1])
        #print(mate_num)

        eval_input.append(vector)
        eval_output.append(mate_num)
        i += 1
        if i % 10000== 0:
            print(i/1000000)

eval_X = np.array(eval_input)
eval_Y = np.array(eval_output)

np.save('eval_X.npy', eval_X)
np.save('eval_Y.npy', eval_Y)

print("Process Complete")


i=0
mate_input_vectors= []
mate_output = []
with open('mates_part_1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for info in reader:

        #print(info[0])
        f = FENParser(info[0])
        vector = f.parse()
        #print(vector)
        mate_num = int(info[1])#only contains numbers outside of 0 at least part 1
        output_num = -1 if mate_num<0 else 1
        #print(mate_num)

        mate_input_vectors.append(vector)
        mate_output.append(output_num)
        i += 1
        if i % 10000== 0:
            print(i/1000000)


print("50 percent done")

with open('non_mates_part_2.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for info in reader:

        #print(info[0])
        f = FENParser(info[0])
        vector = f.parse()
        #print(vector)
        #print(mate_num)

        mate_input_vectors.append(vector)
        mate_output.append(0)
        i += 1
        if i % 10000 == 0:
            print(i/1000000)

mate_X = np.array(mate_input_vectors)
mate_Y = np.array(mate_output)

np.save('mate_X.npy', mate_X)
np.save('mate_Y.npy', mate_Y)
