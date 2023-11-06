# Lab 6
# Elizabeth Healy

# Write a python progran that will open and

# open the file
# read the file
# split each line into a list of words
# strip all commas (and as much of the other punctation) from around each word) 
# put all characters in lower case
# create a Dictionary 
# load all words from the list into the dictionary, updating the count of each word - refer to page 21 of the Dictionary Slide deck or Page 405 of the text. 
# create a list of words (keys) from the dictionary
# sort the list of words (in alphabetical order) 
# print the list of words (in alphbetical order) with the number of times each word is in the original text in the following format: "The word WORD is in the text NUMBER times" 
# Submit your work to Canvas at the end of the Lab 

file = open('Obama.txt','r')
wordDict = {}
for line in file:
    data = line.replace(',', '').replace('.', '').lower().split()
    for l in data:
        #print("I have read the word "+l+"\n")
        wordDict[l] = wordDict.get(l,0) + 1
dict_list = list(wordDict.keys())
dict_list.sort()
for l in dict_list:
    n = wordDict.get(l)
    print("The word", l, "is in the text", n,"times")
file.close()
