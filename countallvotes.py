#################################################################
##                                                             ##
##                      countallvotes.py                       ##
##                                                             ##
#################################################################
##                                                             ##
## Reads in 3 csv files:                                       ##
##                                                             ##
## - staffvotes.csv                                            ##
## - juniorvotes.csv                                           ##
## - seniorvotes.csv                                           ##
##                                                             ##
## And computes the total results of the student election      ##
## using a 50-50 weighting of staff and student votes.         ##
## Preferential voting is used to remove the lowest voted can- ##
## didate, and the intermediary counts are stored in a csv     ##
## file titled 'audit.csv'. This process continues until the   ##
## selection is narrowed down to the final two candidates for  ##
## each position, which are then printed to a csv file titled: ##
##                                                             ##
## - electionresults.csv                                       ##
##                                                             ##
#################################################################
##                                                             ##
## Original Code by: Dr Kurt Williams                          ##
## Date Created: Sept 4th 2024                                 ##
##                                                             ##
## Last Modified by: Dr Kurt Williams                          ##
## Date Modified: Sept 20th 2024                               ##
##                                                             ##
#################################################################

### DECLARE ALL PACKAGES ###

import numpy as np
import pandas as pd

### DECLARE THE CSV FILES TO BE USED AND THE NUMBER OF VOTES IN EACH ###

namestaff = "./staffvotes.csv"
namejnr = "./juniorvotes.csv"
namesnr = "./seniorvotes.csv"

#Junior School
jnrRoles = ["Year 8 Male","Year 8 Female","Year 9 Male","Year 9 Female","Year 10 Leader"] #position names
jnrRoleCol = [8,9,10,11,12] #column in juniorvotes.csv
jnrStaffCol = [15,16,13,14,11] #column in staffvotes.csv
num_jnrRoles = len(jnrRoles)
jnrStaffWeight = [0 for i in range(num_jnrRoles)] #weighting multiplier for staff votes

#Senior School
snrRoles = ["Head Boy/Deputy Head Boy","Head Girl/Deputy Head Girl","Sports Captain","Performing Arts Captain","Ministry Captain"] #position names
snrRoleCol = [6,7,8,9,10] #column in seniorvotes.csv
snrStaffCol = [6,7,8,9,10] #column in staffvotes.csv
num_snrRoles = len(snrRoles)
snrStaffWeight = [0 for i in range(num_snrRoles)] #weighting multiplier for staff votes

### OPEN EACH CSV AND READ IN THE DATA ###
#assuming a MS form data, which has a header of 1

stafftableraw = pd.read_table(namestaff, sep=",", header=1)
stafftable = stafftableraw.to_numpy()
len_stafftable = len(stafftable)

jnrtableraw = pd.read_table(namejnr, sep=",", header=1)
jnrtable = jnrtableraw.to_numpy()
len_jnrtable = len(jnrtable)

snrtableraw = pd.read_table(namesnr, sep=",", header=1)
snrtable = snrtableraw.to_numpy()
len_snrtable = len(snrtable)

### ARRANGE DATA INTO TABLES ###

jnrVotes = [[] for i in range(num_jnrRoles)] #table for junior votes
snrVotes = [[] for i in range(num_snrRoles)] #table for senior votes
staffjnrVotes = [[] for i in range(num_jnrRoles)] #table for junior staff votes
staffsnrVotes = [[] for i in range(num_snrRoles)] #table for senior staff votes
jnrDict = [{} for i in range(num_jnrRoles)] #dictionary for tabulating jnr votes
snrDict = [{} for i in range(num_snrRoles)] #dictionary for tabulating jnr votes

for i in range(0,num_jnrRoles):
    staffjnrVotes[i] = [[] for j in range(len_stafftable)]
    for j in range(0,len_stafftable-1):
        staffjnrVotes[i][j] = str(stafftable[j,jnrStaffCol[i]]).split(";")
    staffjnrVotes[i][:] = (x for x in staffjnrVotes[i] if x != ['nan'])

for i in range(0,num_snrRoles):
    staffsnrVotes[i] = [[] for j in range(len_stafftable)]
    for j in range(0,len_stafftable-1):
        staffsnrVotes[i][j] = str(stafftable[j,snrStaffCol[i]]).split(";")
    staffsnrVotes[i][:] = (x for x in staffsnrVotes[i] if x != ['nan'])
    
for i in range(0,num_jnrRoles):
    jnrVotes[i] = [[] for j in range(len_jnrtable)]
    for j in range(0,len_jnrtable-1):
        jnrVotes[i][j] = str(jnrtable[j,jnrRoleCol[i]]).split(";")
    jnrVotes[i][:] = (x for x in jnrVotes[i] if x != ['nan'])
        
for i in range(0,num_snrRoles):
    snrVotes[i] = [[] for j in range(len_snrtable)]
    for j in range(0,len_snrtable-1):
        snrVotes[i][j] = str(snrtable[j,snrRoleCol[i]]).split(";")
    snrVotes[i][:] = (x for x in snrVotes[i] if x != ['nan'])

### SET THE WEIGHTINGS ###
for i in range(0,num_jnrRoles):
    jnrStaffWeight[i] = int(len(jnrVotes[i]) / len(staffjnrVotes[i]))
for i in range(0,num_snrRoles):
    snrStaffWeight[i] = int(len(snrVotes[i]) / len(staffsnrVotes[i]))

##########################################
##              FUNCTIONS               ##
##########################################

def makedicts(votes,vdict):
    for i in range(0,len(votes)-1):
        for j in range(0,len(votes[i])-1):
            if (votes[i][j] in vdict):
                break
            else:
                vdict[votes[i][j]] = 0
    return(vdict)

# THIS FUNCTION NEEDS TO BE PASSED A 2D ARRAY
# CURRENTLY IT'S GETTING A COLUMN THAT IS YET TO BE PROPERLY SPLIT

def countvotes(studvotes,vdict,staffvotes,weight):
    for i in range(0,len(studvotes)-1):
        for j in range(0,len(studvotes[0])):
            if (studvotes[i][0] == studvotes[0][j]):
                vdict[studvotes[0][j].replace('\xa0','')] += 1
    for i in range(0,len(staffvotes)-1):
        for j in range(0,len(staffvotes[0])):
            if (staffvotes[i][0] == staffvotes[0][j]):
                vdict[staffvotes[0][j].replace('\xa0','')] += weight
    return(vdict)

def removemin(studvotes,vdict,staffvotes):
    minpivot = min(vdict, key=vdict.get)
    for i in range(0,len(studvotes)-1):
        studvotes[i][:] = (x for x in studvotes[i] if x != minpivot)
    for i in range(0,len(staffvotes)-1):
        staffvotes[i][:] = (x for x in staffvotes[i] if x !=minpivot)
    return(studvotes,staffvotes)

def listpop(studvotes,name,staffvotes):
    for i in range(0,len(studvotes)):
        studvotes[i][:] = (x for x in studvotes[i] if x != name)
    for i in range(0,len(staffvotes)):
        staffvotes[i][:] = (x for x in staffvotes[i] if x != name)
    return(studvotes,staffvotes)

##########################################
##       ACTUALLY RUN THE PROGRAM       ##
##########################################

auditscore = open('audit.csv','w')

for i in range(0,num_jnrRoles):
    auditscore.write(str(jnrRoles[i]))
    auditscore.write('\n')
    jnrDict[i] = makedicts(jnrVotes[i],jnrDict[i])
    jnrDict[i] = countvotes(jnrVotes[i],
                            jnrDict[i],
                            staffjnrVotes[i],
                            jnrStaffWeight[i])
    j=0
    while (len(jnrDict[i]) > 2):
        auditscore.write('round ' + str(j) + '\n')
        auditscore.write(str(jnrDict[i]))
        auditscore.write('\n')
        jnrVotes[i],staffjnrVotes[i] = removemin(jnrVotes[i],
                                                 jnrDict[i],
                                                 staffjnrVotes[i])
        jnrDict[i].clear()
        jnrDict[i] = makedicts(jnrVotes[i],
                               jnrDict[i])
        jnrDict[i] = countvotes(jnrVotes[i],
                                jnrDict[i],
                                staffjnrVotes[i],
                                jnrStaffWeight[i])
        j+=1

collegeexec = []
for i in range(0,2):
    auditscore.write(str(snrRoles[i]))
    auditscore.write('\n')
    snrDict[i] = makedicts(snrVotes[i],snrDict[i])
    snrDict[i] = countvotes(snrVotes[i],
                            snrDict[i],
                            staffsnrVotes[i],
                            snrStaffWeight[i])
    j=0
    while (len(snrDict[i]) > 2):
        auditscore.write('round ' + str(j) + '\n')
        auditscore.write(str(snrDict[i]))
        auditscore.write('\n')
        snrVotes[i],staffsnrVotes[i] = removemin(snrVotes[i],
                                             snrDict[i],
                                             staffsnrVotes[i])
        snrDict[i].clear()
        snrDict[i] = makedicts(snrVotes[i],
                               snrDict[i])
        snrDict[i] = countvotes(snrVotes[i],
                                snrDict[i],
                                staffsnrVotes[i],
                                snrStaffWeight[i])
        j+=1
    for key in snrDict[i].keys():
        collegeexec.append(key)
        
for i in range(2,num_snrRoles):
    for j in range(0,len(collegeexec)):
        snrVotes[i],staffsnrVotes[i] = listpop(snrVotes[i],collegeexec[j],staffsnrVotes[i])
    auditscore.write(str(snrRoles[i]))
    auditscore.write('\n')
    snrDict[i] = makedicts(snrVotes[i],snrDict[i])
    snrDict[i] = countvotes(snrVotes[i],
                            snrDict[i],
                            staffsnrVotes[i],
                            snrStaffWeight[i])
    j=0
    while (len(snrDict[i]) > 2):
        auditscore.write('round ' + str(j) + '\n')
        auditscore.write(str(snrDict[i]))
        auditscore.write('\n')
        snrVotes[i],staffsnrVotes[i] = removemin(snrVotes[i],
                                             snrDict[i],
                                             staffsnrVotes[i])
        snrDict[i].clear()
        snrDict[i] = makedicts(snrVotes[i],
                               snrDict[i])
        snrDict[i] = countvotes(snrVotes[i],
                                snrDict[i],
                                staffsnrVotes[i],
                                snrStaffWeight[i])
        j+=1
        
auditscore.close()
        
##########################################
##           PRINT THE OUTPUT           ##
##########################################

finalscore = open('electionresults.csv', 'w')
for i in range(0,len(snrRoles)):
    finalscore.write(str(snrRoles[i]))
    finalscore.write('\n')
    finalscore.write(str(snrDict[i]))
    finalscore.write('\n')
for i in range(0,len(jnrRoles)):
    finalscore.write(str(jnrRoles[i]))
    finalscore.write('\n')
    finalscore.write(str(jnrDict[i]))
    finalscore.write('\n')
finalscore.close()
