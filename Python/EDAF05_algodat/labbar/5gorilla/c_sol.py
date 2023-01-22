import sys
import math
import re
from timeit import default_timer as timer
from datetime import timedelta
import numpy as np


#|------------------------------ Declaration of variables ------------------------------|#


inputf = sys.argv[1]
#['data/sample/1.in', 'data/secret/0mini.in', 'data/secret/1small.in', 'data/secret/2med.in', 'data/secret/3large.in', 'data/secret/4huge.in']

# Går ej måste läsa in från std-in

#|------------------------------ Main method ------------------------------|#


def main():
    for arg in inputf:
        start = timer()
        chars, cost_mat, Q, q = read_data(arg)
        end = timer()
        #print("TIME TO READ DATA: {} \n".format(timedelta(seconds = end - start)))

        # PRINT SIM-MAT
        #print_cost_mat(chars, cost_mat)

        cost_mat = np.matrix(cost_mat)
        str1 = []
        str2 = []
        for s in q:
            str1.append(s.split()[0])
            str2.append(s.split()[1])

        indexes = str_to_indx(str1, str2, chars)
        
        for i, s in enumerate(str1): 
            str1[i] = ' ' + s
        for i, s in enumerate(str2): 
            str2[i] = ' ' + s  

        start = timer()
        f_mat = find_f_mat(str1, str2, cost_mat, indexes)
        end = timer()
        #print("TIME TO FIND F-MATRIX: {} \n".format(timedelta(seconds = end - start)))
        
        # PRINT F-MAT 
        #for i, mat in enumerate(f_mat): print_f_mat(str1[i], str2[i], mat)
        
        f = [np.matrix(mat) for mat in f_mat] #np.matrix(f_mat)

        start = timer()
        a_s1, a_s2 = Needleman_Wunsch(str1, str2, chars, cost_mat, indexes, f)
        end = timer()
        #print("TIME TO PERFORM ALGORITHM ON ALL QUERIES: {} \n".format(timedelta(seconds = end - start)))
        for a_1, a_2 in zip(a_s1, a_s2):
            a1 = ''.join(a_1)
            a2 = ''.join(a_2)
            #print(f'\nAligned string 1: {a_s1} \nAligned string 2: {a_s2}')
            print(f'{a1} {a2}')


#|------------------------------ Complementary functions ------------------------------|#


def read_data(input_file):
    #print(f'File: {input_file}')
    cost_mat = []
    q = [] # queries

    with open(input_file) as file:
        chars = file.readline().split()
        k = len(chars)
        for i in range(0,k):
            cost_mat.append(file.readline().split())
        Q = int(float(file.readline().split()[0]))
        for i in range(0, Q):
            remove_whitespace = re.compile(r'\n+')
            data = re.sub(remove_whitespace, '', file.readline())
            q.append(data)

    return chars, cost_mat, Q, q


def str_to_indx(str1, str2, chars):
    indexes1 = []
    indexes2 = []
    for i in range(len(str1)):
        s1 = str1[i]
        indexes1.append([chars.index(letter) for letter in s1])
    for i in range(len(str2)):
        s2 = str2[i]
        indexes2.append([chars.index(letter) for letter in s2])
    indexes = [indexes1, indexes2]
    return indexes 


def print_cost_mat(chars, cost_mat):
    print('\nSimularity matrix: ')
    top_row = ['  ']
    for c in chars: top_row.append(c)
    print(top_row)
    index = 0
    for i in cost_mat:
        print([chars[index], i])
        index += 1
    print()


def print_f_mat(str3, str4, f_mat):
    print('\nF matrix: ')
    top_row = ['  ']
    left_col = []
    for c in str4: top_row.append(c)
    for c in str3: left_col.append(c) 
    print(top_row)
    index = 0
    for i in f_mat.tolist():
        print([left_col[index], i])
        index += 1


#|------------------------------ Algorithm ------------------------------|#


def find_f_mat(str1, str2, cost_mat, indexes):
    # F-Matrix corresponds to our opt tree 
    d = -4
    f = []
    for x in range(len(str1)):
        # x is index for alignement nbr x
        s1 = str1[x] 
        s2 = str2[x]
        A = len(s1)
        B = len(s2)
        f_mat = np.empty((A,B))
        for i in range(0, A):
            f_mat[i,0] = d * i 
        for j in range(0, B):
            f_mat[0,j] = d * j 
        for i in range(1, A):
            for j in range(1, B):
                match = int(f_mat[i-1,j-1]) + int(cost_mat[indexes[0][x][i-1],indexes[1][x][j-1]]) 
                delete = f_mat[i-1,j] + d
                insert = f_mat[i,j-1] + d
                f_mat[i,j] = max(match, delete, insert)
        f.append(f_mat)
    return f


def Needleman_Wunsch(str1, str2, chars, cost_mat, indexes, f_mat, d=-4):
    align3 = []
    align4 = []

    for x in range(len(str1)):
        start = timer()
        align_str1 = []
        align_str2 = []
        s1 = str1[x]
        s2 = str2[x]
        i = len(str1[x]) - 1
        j = len(str2[x]) - 1 

        while (i > 0 or j > 0):
            ix1 = indexes[0][x][i-1]
            ix2 = indexes[1][x][j-1]

            if (i > 0 and j > 0 and int(f_mat[x][i, j]) == int(f_mat[x][i-1, j-1]) + int(cost_mat[ix1,ix2])):
                align_str1 = [chars[ix1]] + align_str1
                align_str2 = [chars[ix2]] + align_str2
                i = i - 1
                j = j - 1

            elif (i > 0 and int(f_mat[x][i, j]) == int(f_mat[x][i-1, j]) + d):
                align_str1 = [chars[ix1]] + align_str1
                align_str2 = ['*'] + align_str2
                i = i - 1

            else:
                align_str1 = ['*'] + align_str1
                align_str2 = [chars[ix2]] + align_str2 
                j = j - 1

        end = timer()
        #if x == 0:
        #    print("TIME TO PERFORM ALGORITHM ON FIRST QUERY: {} \n".format(timedelta(seconds = end - start)))

        align3.append(align_str1)
        align4.append(align_str2)

    return align3, align4


if __name__ == '__main__':
    main()
