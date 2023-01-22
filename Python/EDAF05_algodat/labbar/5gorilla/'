import sys
import math
import re
from timeit import default_timer as timer
from datetime import timedelta
import numpy as np


#|------------------------------ Main method ------------------------------|#


def main():
    start = timer()
    chars, sim_mat, Q, q = read_data()
    end = timer()
    #print("TIME TO READ DATA: {} \n".format(timedelta(seconds = end - start)))

    # PRINT SIM-MAT
    print_sim_mat(chars, sim_mat)

    sim_mat = np.matrix(sim_mat)
    str3 = []
    str4 = []
    for s in q:
        str3.append(s.split()[0])
        str4.append(s.split()[1])

    indexes = str_to_indx(str3, str4, chars, sim_mat)
    
    for i, s in enumerate(str3): str3[i] = ' ' + s
    for i, s in enumerate(str4): str4[i] = ' ' + s  

    start = timer()
    f_mat = find_f_mat(str3, str4, sim_mat, indexes)
    end = timer()
    #print("TIME TO FIND F-MATRICES: {} \n".format(timedelta(seconds = end - start)))
    
    # PRINT F-MAT 
    for i, mat in enumerate(f_mat): print_f_mat(str3[i], str4[i], mat), print()
    
    f = [np.matrix(mat) for mat in f_mat] 

    start = timer()
    a_s1, a_s2 = Needleman_Wunsch(str3, str4, chars, sim_mat, indexes, f)
    end = timer()
    #print("TIME TO PERFORM ALGORITHM ON ALL QUERIES: {} \n".format(timedelta(seconds = end - start)))
    for a_1, a_2 in zip(a_s1, a_s2):
        a1 = ''.join(a_1)
        a2 = ''.join(a_2)
        print(f'{a1} {a2}')


#|------------------------------ Complementary functions ------------------------------|#


def read_data(data = sys.stdin.readlines()):
    sim_mat = []
    q = [] # queries
    
    chars = data[0].split()
    k = len(chars)
    for i in range(1,k+1):
        sim_mat.append(data[i].split())
    Q = int(data[k+1])
    for i in range(1, Q+1):
        remove_enter = re.compile(r'\n+')
        strings = re.sub(remove_enter, '', data[k+i+1])
        q.append(strings)
    return chars, sim_mat, Q, q


def str_to_indx(str3, str4, chars, sim_mat):
    indexes1 = []
    indexes2 = []
    for i in range(len(str3)):
        s1 = str3[i]
        indexes1.append([chars.index(letter) for letter in s1])
    for i in range(len(str4)):
        s2 = str4[i]
        indexes2.append([chars.index(letter) for letter in s2])
    indexes = [indexes1, indexes2]
    return indexes 


def print_sim_mat(chars, sim_mat):
    print('\nSimularity matrix: ')
    top_row = ['  ']
    for c in chars: top_row.append(c)
    print(top_row)
    index = 0
    for i in sim_mat:
        print([chars[index], i])
        index += 1
    print()


def print_f_mat(str1, str2, f_mat):
    print('\nF matrix: ')
    top_row = ['  ']
    left_col = []
    for c in str2: top_row.append(c)
    for c in str1: left_col.append(c) 
    print(top_row)
    index = 0
    for i in f_mat.tolist():
        print([left_col[index], i])
        index += 1


#|------------------------------ Algorithm ------------------------------|#


def find_f_mat(str3, str4, sim_mat, indexes):
    d = -4
    f = []
    for x in range(len(str3)):
        start = timer()
        s1 = str3[x] 
        s2 = str4[x]
        A = len(s1)
        B = len(s2)
        f_mat = np.empty((A,B))
        for i in range(0, A):
            f_mat[i,0] = d * i 
        for j in range(0, B):
            f_mat[0,j] = d * j 
        for i in range(1, A):
            for j in range(1, B):
                match = int(f_mat[i-1,j-1]) + int(sim_mat[indexes[0][x][i-1],indexes[1][x][j-1]]) 
                delete = f_mat[i-1,j] + d
                insert = f_mat[i,j-1] + d
                f_mat[i,j] = max(match, delete, insert)
        end = timer()
        #if x == 0:
            #print("TIME TO FIND F-MATRIX: {} \n".format(timedelta(seconds = end - start)))
        f.append(f_mat)
    return f


def Needleman_Wunsch(str3, str4, chars, sim_mat, indexes, f_mat, d=-4):
    align3 = []
    align4 = []

    for x in range(len(str3)):
        start = timer()
        align_str3 = ''
        align_str4 = ''
        s1 = str3[x]
        s2 = str4[x]
        i = len(str3[x]) - 1
        j = len(str4[x]) - 1 

        while (i > 0 or j > 0):
            ix1 = indexes[0][x][i-1]
            ix2 = indexes[1][x][j-1]

            if (i > 0 and j > 0 and int(f_mat[x][i, j]) == int(f_mat[x][i-1, j-1]) + int(sim_mat[ix1,ix2])):
                align_str3 = chars[ix1] + align_str3
                align_str4 = chars[ix2] + align_str4
                i = i - 1
                j = j - 1

            elif (i > 0 and int(f_mat[x][i, j]) == int(f_mat[x][i-1, j]) + d):
                align_str3 = chars[ix1] + align_str3
                align_str4 = '*' + align_str4
                i = i - 1

            else:
                align_str3 = '*' + align_str3
                align_str4 = chars[ix2] + align_str4 
                j = j - 1

        end = timer()
        #if x == 0:
        #    print("TIME TO PERFORM ALGORITHM ON FIRST QUERY: {} \n".format(timedelta(seconds = end - start)))

        align3.append(align_str3)
        align4.append(align_str4)

    return align3, align4


if __name__ == '__main__':
    main()
