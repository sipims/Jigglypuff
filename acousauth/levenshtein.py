#!/usr/bin/env python
# -*-coding:utf-8 -*-
import difflib

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
    return difflib.SequenceMatcher(a=first.lower(),b=second.lower()).ratio()>0.5


def match1(first, second):
    first = str(first)
    second = str(second)
    min_length, min_string, max_length, max_string = get_min_length(first, second)
    #print "LEN1",str(min_length)
    #print "LEN2",str(max_length)
    for offest in range(max_length - min_length):
        test_string = max_string[offest:min_length+offest]
        score = levenshtein_distance(min_string, test_string)
        if min_length - 2 > 0:
            if score < min_length - 2:
                print score
                return True
        else:
            return False
    return False

if __name__=="__main__":
    #from sys import argv
    first = "�v��k��tη�iamfine?f�ż�6�\"Ѵ"
    second = "iamfine"
    print match(first, second)
    #print levenshtein(first,second)
    #print levenshtein_distance(first,second)

