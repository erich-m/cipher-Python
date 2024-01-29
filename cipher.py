import sys#use this to get command line arguments
from dataclasses import dataclass#use this to create the datatype for the flag inputs

#*create a datatype to store all the flag information that is parsed from the command line
@dataclass
class flags:
    valid: str
    function: str
    encodeShift: int
    inputType: str
    inputPath: str
    outputType: str
    outputPath: str

#frequency of letters in the english language
ef = [0.08167,0.01462,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07707,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.02360,0.00150,0.01974,0.00074];
#alphabet constant
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];

# *letterCount: counts the number of letters in a provided string of text
def letterCount(text):
    count = 0;
    for c in text:#loop through the text
        if c.isalpha():#if the character is a letter in the alphabet, add to the total
            count = count+1;
    return count;

#*textFreq: counts the number of each individual letter in a provided string of text
def textFreq(text):
    f=[0]*26;#create an array of 26 integers to store the total number for each letter (A is index 0, B is index 1 and so on)

    for c in text:#for all the characters in the text
        if c.isalpha():#if it is a letter
            index = offset(c);#calculate the index by taking the decimal value of the letter (A->65, B->66, etc) and subtracting 65...(A->0, B->1,etc)
            f[index] = f[index]+1;#add to the count at the index
    return f;#return the list of indexes

#*offset: calculates and returns the index by taking the decimal value of the letter (A->65, B->66, etc) and subtracting 65...(A->0, B->1,etc)
def offset(letter):
    return ord(letter.upper()) - 65;

#*encode: takes a letter and applies a given shift. returns a new character
def encode(letter,shift):
    val = offset(letter);#get the index value for the letter (A->0, B->1,etc)
    val=(val+shift)%26;#perform the shift on the value and then mod 26 to convert back to a scale of 0 to 25

    if letter.isupper():#if the given letter is uppercase, return a shifted letter in upper case
        return chr(val + 65);
    else:#if the given letter is lowercase, return a shifted letter in lower case
        return chr(val + 97);

#*chiSquare: takes a string of text and a shift and calculates the chi square value for the given shift (used in statistics)
#?Chi-square is a statistical test used to examine the differences between categorical variables from a random sample in order to judge goodness of fit between expected and observed results.
def chiSquare(text,shift):
    chi = 0;

    n = letterCount(text);
    f = textFreq(text);

    for l in range(0,26):#loop through all the letters in the alphabet
        char = alphabet[l];

        numerator = (n*ef[l])-(f[offset(encode(char,shift))]);#numerator for chi square function
        denominator = n*n*ef[l];#denominator for chi square function

        chi = chi+(numerator * numerator) / denominator;#calculate the chi value for the shift
    return chi;

#*predictChi loops determines a prediction for the shift for a given text string
def predictChi(text):
    chiVals = [];
    for s in range(0,26):#loop through the shifts from 0 to 26
        chiVals.append(chiSquare(text,s));#calculate the shift and append it to the list
    return chiVals.index(min(chiVals));#return the index of the minimum chi value. the minimum is the best fit value and the index is the shift

#*popLeft reverses the list order, pops the last (which is actually the first) element, and then reverses order again
#use as popLeft(array)
def popLeft(array):
    array.reverse();
    array.pop();
    array.reverse();

#*encodeString: encodes a string
def encodeString(text,shift):
    newText = "";
    for c in text:
        if c.isalpha():
            newText = newText+encode(c,shift);
        else:
            newText = newText+c;
    return newText;

#*reverts the new text to the origin text with newline characters from the original source
def matchNewlines(origin,new):
    matched = "";
    originList = list(origin);
    newList = list(new);

    n = 0;
    for c in range(0,len(origin)):
        if originList[c] == "\n":
            matched = matched+"\n";
        else:
            matched = matched+newList[n];
            n=n+1;
    return matched;

#*function to parse the command line
def parseFlags():
    i = flags("invalid","not set",0,"not set","not set","not set","not set");
    try:
        argv = sys.argv;
        popLeft(argv)#pop the python file name off the list

        #check for the -f flag, encode/decode and -s, shift value if encode
        if len(argv) >= 2:
            if argv[0].lower() == "-f":
                popLeft(argv);
                if argv[0].lower() == "encode":
                    i.function = "encode";
                    popLeft(argv);

                    if len(argv) >= 2:
                        if argv[0].lower() == "-s":
                            popLeft(argv);
                            if argv[0].lstrip("-").isdigit():
                                i.encodeShift = argv[0];
                                popLeft(argv);
                            else:
                                raise Exception("Oops, invalid shift value provided");
                        else:
                            raise Exception("Oops, invalid flag detected");
                    else:
                        raise Exception("Oops, not enough arguments provided");
                elif argv[0].lower() == "decode":
                    i.function = "decode";
                    popLeft(argv);
                else:
                    raise Exception("Oops, invalid function selected");
            else:
                raise Exception("Oops, invalid flag detected");
        else:
            raise Exception("Oops, not enough arguements provided");

        #check the input parameters
        if len(argv) >= 2:
            if argv[0].lower() == "-i":
                popLeft(argv);
                if argv[0].lower() == "file":
                    i.inputType = "file";
                    popLeft(argv);

                    if len(argv) >= 2:
                        if argv[0].lower() == "-p":
                            popLeft(argv);
                            i.inputPath = argv[0];
                            popLeft(argv);
                        else:
                            raise Exception("Oops, invalid flag detected");
                    else:
                        raise Exception("Oops, not enough arguements provided");
                elif argv[0].lower() == "cmd":
                    i.inputType = "cmd";
                    popLeft(argv);
                else:
                    raise Exception("Oops, invalid input type selected");
            else:
                raise Exception("Oops, invalid flag detected");
        else:
            raise Exception("Oops, not enough arguements provided");

        #check the output parameters
        if len(argv) >= 2:
            if argv[0].lower() == "-o":
                popLeft(argv);
                if argv[0].lower() == "file":
                    i.outputType = "file";
                    popLeft(argv);

                    if len(argv) >= 2:
                        if argv[0].lower() == "-p":
                            popLeft(argv);
                            i.outputPath = argv[0];
                            popLeft(argv);
                        else:
                            raise Exception("Oops, invalid flag detected");
                    else:
                        raise Exception("Oops, not enough arguements provided");
                elif argv[0].lower() == "cmd":
                    i.outputType = "cmd";
                    popLeft(argv);
                else:
                    raise Exception("Oops, invalid input type selected");
            else:
                raise Exception("Oops, invalid flag detected");
        else:
            raise Exception("Oops, not enough arguements provided");

        if len(argv) > 0:
            raise Exception("Oops, too many arguements provided")

        i.valid = "valid";#set to be valid after everything parses
    except Exception as e:
        print(e)
    
    return i;


""" MAIN CODE """
i = parseFlags();
run = 1;
print(i)

if i.valid == "valid":
    #get text to encode/decode
    text = "";
    if i.inputType == "cmd":
        prompt = "Please enter text to " + i.function + ": ";
        text = input(prompt);
    else:
        try:
            if i.inputPath == "not set":
                raise Exception("invalid file selected")
            textFile = open(i.inputPath,"r");
            text = textFile.read();
            line = text.replace("\n", "");#concatenate into a single string
            textFile.close();
        except:
            print("Oops, there was an error reading from the file");
    #get text to encode/decode

    if len(text) > 0:
        #either encode the text with the provided shift value
        #or decode the text using the predicted shift value
        newLine = "";
        if i.function == "encode":
            newLine = encodeString(line,int(i.encodeShift));
        else:
            s = predictChi(text);
            newLine = encodeString(line,-s);
        updatedText = matchNewlines(text,newLine);
        #either encode the text with the provided shift value
        #or decode the text using the predicted shift value

        #either print the text to the command line or write it to a file
        if i.outputType == "cmd":
            print(updatedText);
        else:
            try:
                if i.outputPath == "not set":
                    raise Exception("invalid file selected")
                textFile = open(i.outputPath,"w");
                textFile.write(updatedText);
                textFile.close();
            except:
                print("Oops, there was an error writing to the file");
        #either print the text to the command line or write it to a file
    