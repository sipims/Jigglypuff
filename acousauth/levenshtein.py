#!/usr/bin/env python
# -*-coding:utf-8 -*-
#import difflib
#import sys
#import editdist
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings."""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [range(second_length) for x in range(first_length)]
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)

    return distance_matrix[first_length-1][second_length-1]



def get_min_length(sig1, sig2):
    len1 = len(sig1)
    len2 = len(sig2)
    if len1 > len2:
        return len2, sig2, len1, sig1
    else:
        return len1, sig1, len2, sig2


def match(first, second):
    first = str(first)
    second = str(second)
    min_length, min_string, max_length, max_string = get_min_length(first, second)
    print "STR1",first
    print "STR2",second
    print "LEN1",str(min_length)
    print "LEN2",str(max_length)
    for offest in range(max_length - min_length + 10):
        print "OFFSET"
        print offest
        test_string = max_string[offest:min_length+offest]
        #score = editdist.distance(min_string, test_string)
        print test_string
        score = levenshtein_distance(min_string,test_string)
        print score
        if score < 15:
            print "SCORE:::"
            print score
            print "test_string"
            print test_string
            print "min_string"
            print min_string
            return True
    return False

if __name__=="__main__":
    #from sys import argv
    first = "@$667234d8ff4d6032s99adw9<eb087b6abr3f⛿"
    second = "672c346d8ff4d6032c91ad794eb087b26ab6b3fb"
    print match(first, second)
    #print editdist.distance(first,second)
    #print levenshtein(first,second)
    #print levenshtein_distance(first,second)

