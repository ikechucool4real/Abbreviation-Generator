#Read a file based on the name given by user and return a list of names in that file
#Generate a dictionary of abbreviations from each name in the list
#Count the number of times an abbreviation appears for each name
#Exclude abbreviations formed from more than one name i.e abbreviations that more than once
#Calculate the scores for each abbreviation
#Get the abbreviation with lowest score for each name
#Store the generated abbreviations in a file based on the user surname


#Import re library for pattern matching
import re

#Function to write abbreviation generated to an output file based on their surname
def outputfile(wordsandbestscore, filename):
    #Prompt user for their surname
    usersurname = input('Enter your surname: ')
    outputlines = []

    for word, abbrs in wordsandbestscore.items():
        cleanword = re.sub(r"[\n]", '', word)
        outputlines.append(f'{cleanword}\n')
        abbr_string = ' '.join(abbrs)
        outputlines.append(f'{abbr_string}\n\n')

    with open(f'./{usersurname}_{filename}_abbrevs.txt', 'w') as output:
            output.writelines(outputlines)


#Function to return the abbreviation with lowest score for each name
def getbestscore(wordsandscores):
    wordsandbestscore = {}

    for name, abbrs in wordsandscores.items():
        #Check if there is an acceptable abbreviation 
        if not abbrs:
            wordsandbestscore[name] = "_____"
        else:
            #Sort the abbreviations based on their scores
            sortedabbr = sorted(abbrs, key=lambda x: x[1])
            bestabbr = []

            for abbr, score in sortedabbr:
                #check if more than one abbreviation has the lowest score(which is the first of the values)
                if score == sortedabbr[0][1]:
                    bestabbr.append(abbr)
           
            wordsandbestscore[name] = bestabbr

    return wordsandbestscore


#Function to calculate scores for each abbreviation
def calculatescores(wordandabbr):
    validatedabbreviations = validateabbr(wordandabbr)
    wordsandscores = {}
    
    for name, abbrs in wordandabbr.items():
        abbrsandscores = []

        #Ignore aprostrophes, non-letter characters and convert names in the file to uppercase
        cleanname = re.sub(r"[\n+(),:']", '', name)
        cleanername = re.sub(r"-", ' ', cleanname).upper()
        words = cleanername.split()

        for abbr in abbrs:
            score = 0
            #Check if the abbreviation is valid
            if abbr not in validatedabbreviations:
                continue

            for i in range(1, len(abbr)):
                # Initialize condition_met for each letter in abbr
                condition_met = False
                
                pos = 1 if len(words) >= 2 else 0
                for j in range(pos, len(words)):
                    # Check if the letter matches the first letter of a word
                    if abbr[i] == words[j][0]:
                        score += 0
                        condition_met = True
                        break
                
                # Check if condition_met is True, meaning the letter matches the first letter of a word
                if condition_met:
                    continue
                
                for word in words:
                    # Check if the letter matches the last letter of a word
                    if abbr[i] == word[-1]:
                        if abbr[i] == 'E':
                            score += 20
                        else:
                            score += 5
                        condition_met = True
                        break
                
                # Check if condition_met is True, meaning the letter matches the last letter of a word
                if condition_met:
                    continue
                
                # If the letter doesn't match the first or last letter, calculate its score
                positionvalue = 0
                for j in range(0, len(words)):
                    if len(words[j]) > 1:
                        if abbr[i] == words[j][1]:
                            positionvalue += 1
                        elif abbr[i] == words[j][2]:
                            positionvalue += 2
                        else:
                            positionvalue += 3
                    
                        commonness = {
                            'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6, 'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,
                            'B': 8, 'C': 8, 'M': 8, 'P': 8, 'D': 9, 'G': 9, 'L': 15, 'N': 15, 'R': 15, 'S': 15,
                            'T': 15, 'O': 20, 'U': 20, 'A': 25, 'I': 25, 'E': 35
                        }
                        score += positionvalue + commonness.get(abbr[i], 0)
                        break 

            abbrandscore = (abbr, score)
            abbrsandscores.append(abbrandscore)  
        wordsandscores[name] = abbrsandscores    
    
    return wordsandscores


#Function to exclude abbreviations formed from more than one name 
def validateabbr(wordandabbr):
    countedabbreviations = countabbr(wordandabbr)
    validabbreviations = []

    for abbr,count in countedabbreviations.items():
        #Check if abbreviation only appears once
        if count == 1:
            validabbreviations.append(abbr)

    return validabbreviations


# Function to count the number of times an abbreviation appears for each name
def countabbr(nameandabbr):
    abbreviationandcount = {}
    listabbreviations = []

    for item in nameandabbr.values():
        for subitem in item:
            listabbreviations.append(subitem)
    
    for item in listabbreviations:
        abbreviationandcount[item] = listabbreviations.count(item)
    
    return abbreviationandcount


#Function to generate a dictionary of abbreviations from each name in the list
def getabbr(listofnames):
    nameandabbreviations = {}
    abbreviations = set()

    #form three letter abbreviations from the name
    for name in listofnames:
        #Ignore aprostrophes, non-letter characters and convert names in the file to uppercase
        cleanname = re.sub(r"[\n+(),:']", '', name)
        cleanername = re.sub(r"-", ' ', cleanname).upper()

        for i in range(len(cleanername)):

            #Check that abbreviation begins with the first letter of name and is more than 3 letters
            if i == 0 and len(cleanername) > 3:
                for j in range(1, len(cleanername)):

                    #Check if a character in the name is not a whitespace
                    if cleanername[j] != ' ':
                        for k in range(j+1, len(cleanername)):

                            #Check if a character in the name is not a whitespace
                            if cleanername[k] != ' ':
                                substr = cleanername[i] + cleanername[j] + cleanername[k]
                                abbreviations.add(substr)
            
            elif len(cleanername) <= 3:
                abbreviations.add(cleanername)
               
        nameandabbreviations[name] = abbreviations
        abbreviations = set()
    
    return nameandabbreviations
            

#Function to read file and produce list of names in file
def readfile():
    #Prompt user for the name of the file to read
    filename = input('Enter the name of the file: ')
    listofnames = []


    with open(f'./{filename}.txt', 'r') as content:
        for line in content:
            listofnames.append(line)

    return listofnames, filename


#Function for generating the three letter abbreviations that meets requirement
def generateabbreviations():
    
    #Read a file based on the name given by user and return a list of names in that file
    file, nameoffile = readfile()

    #Generate a dictionary of abbreviations from each name in the list
    wordstoabbr = getabbr(file)

    #Calculate the scores for each abbreviation
    abbrsandscores = calculatescores(wordstoabbr)

    #Get the abbreviation with lowest score for each name
    abbrsandbestscores = getbestscore(abbrsandscores)

    #Store the generated abbreviations in a file based on the user surname
    return outputfile(abbrsandbestscores, nameoffile)
    

if __name__ == '__main__':
    generateabbreviations()
