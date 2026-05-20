#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Importing Libraries
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import os
from nltk.corpus import cmudict
import re
import requests
from bs4 import BeautifulSoup

# Download the required NLTK resources (only needed once)
nltk.download('punkt')
nltk.download('cmudict')


# In[2]:


##CREATING OUTPUT FILE
# Create a Tkinter root window
root = Tk()
root.withdraw()

# Open the "Choose Location" dialog to select the file name and location
file_path_1 = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

# Create a DataFrame (sample data)
data = {"URL_ID":[],"URL":[],"POSITIVE SCORE":[],"NEGATIVE SCORE":[],"POLARITY SCORE":[],"SUBJECTIVITY SCORE":[],
        "AVG SENTENCE LENGTH":[],"PERCENTAGE OF COMPLEX WORDS":[],"FOG INDEX":[],"AVG NUMBER OF WORDS PER SENTENCE":[],
        "COMPLEX WORD COUNT":[],"WORD COUNT":[],"SYLLABLE PER WORD":[],"PERSONAL PRONOUNS":[],"AVG WORD LENGTH":[]}
df = pd.DataFrame(data)

# Write the DataFrame to Excel file
df.to_excel(file_path_1, index=False)
print("Output file created sucessfully")


# In[3]:


print("Choose the Input file")
# Specify the path to your Excel file
excel_file_path = filedialog.askopenfilename()

# Read the Excel file into a pandas DataFrame
Input_file = pd.read_excel(excel_file_path)


# In[ ]:


# Create a Tkinter root window
root = Tk()
root.withdraw()

# Open the "Choose Directory" dialog
directory = filedialog.askdirectory()
for i in range(len(Input_file)):
    print(i)
    print(Input_file["URL_ID"][i])
    ID = Input_file["URL_ID"][i]
    if i != 7 and i !=20 and i != 107:
        # Specify the URL of the webpage
        url = Input_file['URL'][i]

        # Send a GET request to the webpage
        response = requests.get(url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title of the article
        title = soup.find('h1').text.strip()

        # Find the HTML elements that contain the article text
        article_elements = soup.find_all("p")

        # Extract the article text and concatenate it into a single string
        article_text = ' '.join([element.text.strip() for element in article_elements])

        # Split the text into words
        words = article_text.split()

        # Remove the desired number of words from the start
        remaining_words = words[136:]

        # Join the remaining words back into a single text
        updated_text = " ".join(remaining_words)

        # Split the text into words
        words_1 = updated_text.split()

        # Remove the desired number of words from the end
        remaining_words_1 = words_1[:-46]

        # Join the remaining words back into a single text
        updated_text_1 = " ".join(remaining_words_1)


        # Print the title and article text
        #print('Title:', title)
        #print('Article Text:', updated_text_1)

        # Save the article in a text file
        file_ID = f"{ID}.txt"

        # Construct the full file path
        file_name = directory + "/" + file_ID
        
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"{title}\n\n")
            file.write(updated_text_1)

        print(f"The article {ID} has been saved")
    else:
        print(f"No page found in URL_ID {ID}")


# In[4]:


##Importing Stop words as list
# Create the Tkinter root window
print("Choose all the Stop words files at once")
root = Tk()

# Hide the root window
root.withdraw()

# Ask the user to select multiple files
file_paths = filedialog.askopenfilenames()

# Convert the file paths to a list
file_paths = root.tk.splitlist(file_paths)

#Combining all the file into an list
Stop_words = []  # List to store the contents of each file

for file_path in file_paths:
    with open(file_path, "r") as file:
        content = file.read()
        Stop_words.append(content)

#Seperating each word and saving as a list
Stop_word_list = []

for paragraph in Stop_words:
    words = paragraph.replace('\n', ' ').split()
    Stop_word_list.extend(words)

Stop_word_list = [word.lower() for word in Stop_word_list]

##Importing Negative words as list
# Open the "Choose File" dialog
print("Choose the Negative words file")
file_path = filedialog.askopenfilename()
#file_path = r"C:\Users\vella\Downloads\20211030 Test Assignment-20230618T054034Z-001\20211030 Test Assignment\MasterDictionary\negative-words.txt"

# Open the file in read mode
with open(file_path, "r") as file:
    # Read the contents of the file
    Neg_words = file.read()
    
##Importing Positive words as list
# Open the "Choose File" dialog
print("Choose the Positive words file")
file_path = filedialog.askopenfilename()
# Open the file in read mode
with open(file_path, "r") as file:
    # Read the contents of the file
    Pos_words = file.read()
    


# In[7]:


##Importing Articals
# Create the Tkinter root window
print("Choose all the Artical files at once")
root = Tk()

# Hide the root window
root.withdraw()

# Ask the user to select multiple files
file_paths = filedialog.askopenfilenames()

# Convert the file paths to a list
file_paths = root.tk.splitlist(file_paths)


for file_path in file_paths:
    # Open the file in read mode
    with open(file_path, "r", encoding="utf-8") as file:
        # Read the contents of the file
        file_contents = file.read()

    # Number of lines to delete from the start
    lines_to_delete = 2

    # Split the text into lines
    lines = file_contents.splitlines()

    # Remove the desired number of lines from the start
    remaining_lines = lines[lines_to_delete:]

    # Join the remaining lines back into a single text
    updated_text = "\n".join(remaining_lines)
    updated_text = updated_text.replace('“', '')
    updated_text = updated_text.replace('”', '')

    ##SENTIMENT ANALYSIS
    # Split the paragraph into words
    words = updated_text.split()

    # Remove the words from the list
    filtered_words = [word for word in words if word.lower() not in Stop_word_list]

    # Join the filtered words back into a paragraph
    filtered_paragraph = " ".join(filtered_words)

    # Variable to store the count
    Pos_count = 0

    # Split the paragraph into words
    fill_words = word_tokenize(filtered_paragraph)

    # Iterate over each word in the paragraph
    for word in fill_words:
        # Check if the word is in the word list
        if word in Pos_words:
            Pos_count += 1

    # Print the Postive Score
    #print("Postive Score:", Pos_count)

    # Variable to store the count
    Neg_count = 0

    # Iterate over each word in the paragraph
    for word in fill_words:
        # Check if the word is in the word list
        if word in Neg_words:
            Neg_count += 1

    # Print the Negative Score
    #print("Negative Score:", Neg_count)

    #Calculating Polarity score
    Polarity_Score = (Pos_count - Neg_count)/ ((Pos_count + Neg_count) + 0.000001)
    #print("Polarity Score:", Polarity_Score)

    #Calculating Subjective score
    Subjective_Score = (Pos_count + Neg_count)/ (len(fill_words) + 0.000001)
    #print("Subjective Score:", Subjective_Score)

    ##ANALYSIS OF READABILITY
    #Finding number of words without removing stop words
    num_words = len(updated_text.split())

    #okenize the paragraph into Words
    words = word_tokenize(updated_text)

    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(updated_text)

    # Get the number of sentences
    num_sentences = len(sentences)

    #Calculating the Average sentence length
    Avg_Sent_len = num_words/num_sentences
    #print("Average sentence length:", Avg_Sent_len)

    #Calculating number of complex words
    # Load the CMU Pronouncing Dictionary
    pronouncing_dict = cmudict.dict()

    # Function to count the number of syllables in a word
    def count_syllables(word):
        if word.lower() not in pronouncing_dict:
            return 0
        return max([len(list(y for y in x if y[-1].isdigit())) for x in pronouncing_dict[word.lower()]])

    # Calculate the number of complex words
    num_complex_words = sum(1 for word in words if count_syllables(word) >= 3)

    #Calculating percentage of complex words
    per_complex_words = num_complex_words/num_words
    #print("Percentage of complex words:", per_complex_words)

    #Calculating Fog Index
    Fog_Index = 0.4 * (Avg_Sent_len + per_complex_words)
    #print("Fog Index:", Fog_Index)

    ##AVERAGE NUMBER OF WORDS PER SENTENCE
    #print("Average number of words per sentence:", Avg_Sent_len)

    ##COMPLEX WORD COUNTS
    #print("Number of complex words:", num_complex_words)

    ##WORD COUNT
    #print("Total Number of cleaned words:", num_words)

    ##SYLLABLE COUNT PER WORDS
    # Function to count the number of syllables in a word
    def count_syllables(word):
        vowels = 'aeiouAEIOU'
        exceptions = ['es', 'ed']
        syllable_count = 0
        prev_char = None
        for char in word:
            if char in vowels:
                if prev_char and prev_char.lower() not in vowels:
                    syllable_count += 1
            prev_char = char
        if word[-2:] in exceptions:
            syllable_count -= 1
        return max(1, syllable_count)

    # Calculate the total syllable count and word count
    total_syllables = 0
    word_count = num_words

    for word in words:
        total_syllables += count_syllables(word)

    # Calculate the average syllable count per word
    average_syllable_count = total_syllables / word_count

    # Print the average syllable count per word
    #print("Average syllable count per word:", average_syllable_count)

    ##PERSONAL PRONOUNS
    # Define the regex pattern to match the personal pronouns
    pattern = r'\b(I|we|my|ours|us)\b'

    # Find all matches of the pattern in the text
    matches = re.findall(pattern,updated_text, flags=re.IGNORECASE)

    # Filter out the occurrences of the country name "US"
    matches = [match for match in matches if match.lower() != "us"]

    # Count the occurrences of personal pronouns
    Pers_count = len(matches)

    # Print the count of personal pronouns
    #print("Count of personal pronouns:", Pers_count)

    ##AVERAGE WORD LENGTH
    # Tokenize the text into words
    words = updated_text.split()

    # Calculate the total number of characters in each word
    total_characters = sum(len(word) for word in words)

    # Calculate the average word length
    average_word_length = total_characters / num_words

    # Print the average word length
    #print("Average word length:", average_word_length)
    
    # Extract the file name
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_name = int(file_name)

    #GETTING THE URL ID
    URL = Input_file.loc[Input_file['URL_ID'] == file_name, 'URL'].values[0]

    #cONVERTING INTO DICTONARY
    data = {"URL_ID":[file_name],"URL":[URL],"POSITIVE SCORE":[Pos_count],"NEGATIVE SCORE":[Neg_count],"POLARITY SCORE":[Polarity_Score],
            "SUBJECTIVITY SCORE":[Subjective_Score],"AVG SENTENCE LENGTH":[Avg_Sent_len],"PERCENTAGE OF COMPLEX WORDS":[per_complex_words],
            "FOG INDEX":[Fog_Index],"AVG NUMBER OF WORDS PER SENTENCE":[Avg_Sent_len],"COMPLEX WORD COUNT":[num_complex_words],
            "WORD COUNT":[num_words],"SYLLABLE PER WORD":[average_syllable_count],"PERSONAL PRONOUNS":[Pers_count],"AVG WORD LENGTH":[average_word_length]}

    # Read the existing Excel file into a DataFrame
    existing_data = pd.read_excel(file_path_1)

    # Append the new data to the existing DataFrame
    updated_data = existing_data.append(pd.DataFrame(data), ignore_index=True)

    # Write the updated DataFrame to the Excel file
    updated_data.to_excel(file_path_1, index=False)

    # Print a confirmation message
    print('Data appended to the Excel file.')