# https://pythonprogramming.net/regular-expressions-regex-tutorial-python-3/

'''
Identifiers (ex: looking for any number)

\d any number
\D anything but a number
\s space
\S anything but a space
\w any character
...

. = any character except a new line
\b the whitespace around words
\. a period

Modifiers (ex: looking for this amount of numbers) - a description
{1,3} we're expecting 1-3
+ Match 1 or more
? match 0 or 1
* match 0 or more
$ match the end of a string
^ matching the beginning of a string
| either or \d{1-3} | \w{5-6}
[] range or "variance"
more on range:
If you're looking at this range [A-Za-z] <- I don't know what he's trying to say, possibly looking for A-Z and a-z

{x} expecting "x" amount

White Space Characters: (characters that are there that you might not see)
\n new line
\s space
\t tab
\e escape
\f form feed
\r return

DON'T FORGET! ? confused
. + * ? [] $ ^

'''

import re

exampleString = '''Jessica is 15 years old, and Daniel is 27 years old.
Edward is 97, and his grandfather, Oscar, is 102.'''

# Objective: pull all names and ages form the string

ages = re.findall(r'\d{1,3}', exampleString)
#\d{1,3} is what we are looking for
#\d any number
#{1,3} we're expecting to look for 1-3 digits
#exampleString is where we are looking for it

names = re.findall(r'[A-Z][a-z]*', exampleString)
#[A-Z][a-z]*

allwords = re.findall(r'[a-z]*', exampleString)
print(allwords)
#leaving r out doesn't seem to make any difference

# Seems like they define a variable as regex https://regexone.com/references/python

# How to Write and Match Regular Expressions
# https://www.youtube.com/watch?v=K8L6KVGG-7o

text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890
Ha HaHa
MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )
coreyms.com
321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234
Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T


'''

# a raw string: a string prefixed with an r, that tells python not to handle back slashes in any special way

sentence = 'Start a sentence and then bring it to an end'

print('\tTab')
#output: (with a tab in front) Tab

print(r'\tTab')
#output: \tTab
#the backslash is no longer handled in any special way


#Compile method
# allows us to separate out our patterns into a variable and will make it easier to reuse that variable to perform multiple searches

#search for literal text abc
#pattern = re.compile(r'abc')

# Now lets search through our text to see what matches
matches = pattern.finditer(text_to_search)

for match in matches:
    print(match)

#output: <_sre.SRE_Match object; span=(1, 4), match='abc'>
# finditer method returns an iterator that contains all of the matches
# good to find matches in an easy to read format
# each of these match ojects shows us the spand and the match itself
# span is the beginning and end index of the match
# using this we can

print(text_to_search[1:4])
#output: abc

# To match special characters use backslash (escape it)
# pattern = re.compile(r'\.')

# web address with .
# pattern = re.compile(r'coreyms\.com')
# output: <_sre.SRE_Match object; span=(139, 150), match='coreyms.com'>


# Example using metacharacters instead of literal characters
# Finding this:
'''
321-555-4321
123.555.1234
321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234'''
# digit = \d (any single digit in the text) - we want three in a row:
# pattern = re.compile(r'\d\d\d')

#Now we want - or dot
# for now, match any character "."
# pattern = re.compile(r'\d\d\d.')

#We want the next three digits, and then any character, then four more digits
#time: 15.59


# run this again:
# matches = pattern.finditer(text_to_search)
#
# for match in matches:
#     print(match)

# pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
#~18min
# with open('/Users/datateam/Desktop/Python/data.txt', 'r') as f:
#     contents = f.read()
#     matches = pattern.finditer(text_to_search)
#     for match in matches:
#         print(match)


# To only match the - or . we can use a character set: square brackets [] so [-.] = dash or dot
# don't need to escape - or . when within a character set
# this will not match two dashes or two dots, only one
# pattern = re.compile(r'\d\d\d[-.]\d\d\d[-.]\d\d\d\d')
#
# matches = pattern.finditer(text_to_search)
#
# for match in matches:
#     print(match)

#Now we only want to match 800 or 900 number ~22min
# first digit either 8 or 9, next two will be literal zeros
# pattern = re.compile(r'[89]00[-.]\d\d\d[-.]\d\d\d\d')

# matches = pattern.finditer(text_to_search)
#
# for match in matches:
#     print(match)

#output:
# <_sre.SRE_Match object; span=(190, 202), match='800-555-1234'>
# <_sre.SRE_Match object; span=(203, 215), match='900-555-1234'>

# within a character set the dash is a special character as well when it is put at the beginning or end it will just match the literal range.
# When placed between values it can specify a range.
# to match digits between one and five:
# pattern = re.compile(r'[1-5]')
#output: lists digits singling 1, 3, 5, 2, etc.
# if we did [a-z] it would list any of the letters individually
# [a-zA-Z] gives any letter lower case or upper case

# Carrot ^: ~24min
# when inside character set [^] is matches everything that is not in that character set.
# pattern = re.compile(r'[^a-zA-z]')
# output:
'''
<_sre.SRE_Match object; span=(209, 210), match='5'>
<_sre.SRE_Match object; span=(210, 211), match='-'>
<_sre.SRE_Match object; span=(259, 260), match='\n'>
<_sre.SRE_Match object; span=(262, 263), match='.'>
<_sre.SRE_Match object; span=(263, 264), match=' '>
<_sre.SRE_Match object; span=(265, 266), match='\n'>
'''

#Want to match cat, mat and pat and all other three letter words that end in "at" but we don't want to match the word bat
# everything that is not a "b" followed be a literal "at"
#pattern = re.compile(r'[^b]at')
# match any single character that isn't a "b", followed by an "a", followed by a "t"
# output:
'''
<_sre.SRE_Match object; span=(267, 270), match='cat'>
<_sre.SRE_Match object; span=(271, 274), match='mat'>
<_sre.SRE_Match object; span=(275, 278), match='pat'>
'''
# The pattern, pattern = re.compile(r'[^b]at'), matches any single character that isn't a "b", followed by an "a", followed by a "t"

# We can use quantifies to match more than one character at once
# match any character for the separator
# want three digits, a period to match any character for a separator, three more digits, any separator, four digits

# pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
# in this case we are searching for one character at a time, easy to make mistakes when a lot to type out
# quantifier will match multiple characters at a time

pattern = re.compile(r'\d{3}.\d{3}.\d{4}')

matches = pattern.finditer(text_to_search)

for match in matches:
    print(match)

'''
<_sre.SRE_Match object; span=(151, 163), match='321-555-4321'>
<_sre.SRE_Match object; span=(164, 176), match='123.555.1234'>
<_sre.SRE_Match object; span=(177, 189), match='123*555*1234'>
<_sre.SRE_Match object; span=(190, 202), match='800-555-1234'>
<_sre.SRE_Match object; span=(203, 215), match='900-555-1234'>
'''

# If we don't know the exact number we'll need to use other quantifiers
# we want to match the prefixes with the numbers, prefixes: "Mr." "Mr" "Ms" "Mrs." and the entire name that comes afterward
# start with names that start with "Mr."
# pattern = re.compile(r'Mr\.')
'''
<_sre.SRE_Match object; span=(216, 219), match='Mr.'>
<_sre.SRE_Match object; span=(260, 263), match='Mr.'>
'''

# we want to say the period after "Mr" is optional. Use quantifier "?": match 0 or 1 of those characters

# pattern = re.compile(r'Mr\.?')
'''
<_sre.SRE_Match object; span=(216, 219), match='Mr.'>
<_sre.SRE_Match object; span=(228, 230), match='Mr'>
<_sre.SRE_Match object; span=(246, 248), match='Mr'>
<_sre.SRE_Match object; span=(260, 263), match='Mr.'>
'''
# Add space and all capital letters
# pattern = re.compile(r'Mr\.?\s[A-Z]')
# matches = pattern.finditer(text_to_search)
#
# for match in matches:
#     print(match)
'''
<_sre.SRE_Match object; span=(216, 221), match='Mr. S'>
<_sre.SRE_Match object; span=(228, 232), match='Mr S'>
<_sre.SRE_Match object; span=(260, 265), match='Mr. T'>
'''

# Now match any word character after uppercase letter \w
# then what quant's we want to use for our word characters: * = 0 or more
# pattern = re.compile(r'Mr\.?\s[A-Z]\w*')

'''
<_sre.SRE_Match object; span=(216, 227), match='Mr. Schafer'>
<_sre.SRE_Match object; span=(228, 236), match='Mr Smith'>
<_sre.SRE_Match object; span=(260, 265), match='Mr. T'>
'''

# Match a group: allow us to match several different patterns, we use ()
# match a literal "r" after the M or | a literal "s" or | literal "rs"
# pattern = re.compile(r'M(r|s|rs)\.?\s[A-Z]\w*')

# this will yield the same result, it's longer but may be more clear as to what we want to do:
# pattern = re.compile(r'(Mr|Ms|Mrs)\.?\s[A-Z]\w*')

'''
<_sre.SRE_Match object; span=(216, 227), match='Mr. Schafer'>
<_sre.SRE_Match object; span=(228, 236), match='Mr Smith'>
<_sre.SRE_Match object; span=(237, 245), match='Ms Davis'>
<_sre.SRE_Match object; span=(246, 259), match='Mrs. Robinson'>
<_sre.SRE_Match object; span=(260, 265), match='Mr. T'>
'''

# Pulling it all together what we've learned so far

emails = '''
CoreyMSchafer@gmail.com
corey.schafer@university.edu
corey-321-schafer@my-work.net
'''
# Match all emails
# match everything before @ symbol. [a-zA-Z] for any lower or uppercase, and "+@" is more or more of those until we hit the at symbol, and those letters after (one or more of those: +), "\.com{
# pattern = re.compile(r'[a-zA-Z]+@[a-zA-Z]+\.com')
#
# matches = pattern.finditer(emails)
#
# for match in matches:
#     print(match)

'''
<_sre.SRE_Match object; span=(1, 24), match='CoreyMSchafer@gmail.com'>
'''

# Match all
# pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

'''
<_sre.SRE_Match object; span=(1, 24), match='CoreyMSchafer@gmail.com'>
<_sre.SRE_Match object; span=(25, 53), match='corey.schafer@university.edu'>
<_sre.SRE_Match object; span=(54, 83), match='corey-321-schafer@my-work.net'>
'''

# There are more examples of reading other RegEx here:
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-Regular-Expressions/urls.py

# Other RegEx besides .findter() ~46min https://www.youtube.com/watch?v=K8L6KVGG-7o
# .finditer() returns extra info, has more functionality
# .findall() will just return the matches as a list of strings, if it's matching groups it will only return the groups
# pattern = re.compile(r'(Mr|Ms|Mrs)\.?\s[A-Z]\w*')

# matches = pattern.findall(text_to_search)
#
# for match in matches:
#     print(match)

'''
Mr
Mr
Ms
Mrs
Mr
'''
# if there were multiple groups it would return a list of tuples and the tuples would contain all of the groups

# if there are no groups it will just return all of the matches in a list of strings

# pattern = re.compile(r'\d{3}.\d{3}.\d{4}')
# matches = pattern.findall(text_to_search)
#
# for match in matches:
#     print(match)
'''
321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234
'''

# Match method: determine if the regex matches at the beginning of the string
# search for the literal string "Start" from sentence variable
pattern = re.compile(r'Start')
# if you put re.compile(r'sentence') if would return none because it's only at the beginning of the string
matches = pattern.match(sentence)
print(matches)
#.match is not an iterable no for loop needed


# he says .match is not an iterable but it's working for me, he suggests just "print(match)"

# To search the entire string
pattern = re.compile(r'sentence')
matches = pattern.search(sentence)
print(matches)
'''
<_sre.SRE_Match object; span=(8, 16), match='sentence'>
'''


# Flags
# match a word whether it was uppercase or lowercase or mixture
# match Start but each letter could be uppercase or lowercase
pattern = re.compile(r'start', re.IGNORECASE)
# I also is IGNORECASE
#even though pattern has lowercase s it still finds 'Start'
matches = pattern.search(sentence)
print(matches)

# there are multiline flags and verbose flags (think allows you to add comments) these are commonly used

csv_ex = pd.read_csv( "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv")
lat_pattern = re.compile(r'Lat')
matches = lat_pattern.finditer(csv_ex)
for match in matches:
    print(match)

lat_pattern = re.compile(r'Lat|Lon')
matches = lat_pattern.findall(foo)
print(matches)

import pandas as pd

foo = pd.DataFrame.to_string(csv_ex)



# data = {'spike-2': [1,2,3], 'hey spke': [4,5,6], 'spiked-in': [7,8,9], 'no': [10,11,12]}
# df = pd.DataFrame(data)

lat = [col for col in df.columns if 'lat' in col]
print(list(df.columns))
print(lat)



print(csv_ex.columns)

# Now match any word character after uppercase letter \w
# then what quant's we want to use for our word characters: * = 0 or more
pattern = re.compile(r'Mr\.?\s[A-Z]\w*')

'''
<_sre.SRE_Match object; span=(216, 227), match='Mr. Schafer'>
<_sre.SRE_Match object; span=(228, 236), match='Mr Smith'>
<_sre.SRE_Match object; span=(260, 265), match='Mr. T'>
'''

#Want to match cat, mat and pat and all other three letter words that end in "at" but we don't want to match the word bat
# everything that is not a "b" followed be a literal "at"
#pattern = re.compile(r'[^b]at')
# match any single character that isn't a "b", followed by an "a", followed by a "t"
# output:



df = pd.read_csv( "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv")



data = {'spike-2': [1,2,3], 'hey spke': [4,5,6], 'spiked-in': [7,8,9], 'no': [10,11,12]}
df = pd.DataFrame(data)

spike_cols = [col for col in df.columns if 'spike' in col]
print(list(df.columns))
print(spike_cols)

df['Lat'].iteritems()