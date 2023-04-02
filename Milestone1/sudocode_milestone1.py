# Format of paragraph list is as follows: [paragraph1, paragraph2]
# Each individual paragraph is simply a string example: ["lol is the start of a sentence imho.!!? blah blah", "this is a second sentence"]
paragraph_list = Read_Paragraph_List()

# Format of replacement list is a list of tuples in the form (word to replace, replacement)
# Example replacement list: [("imho", "in my humble opinion"), ("can't", "can not")]
replacement_list = Read_Replacement_List()

# Any common punctuation gets added here
punctuation_list = [",", ".", "!", "?"]

for paragraph_index, paragraph in enumerate(paragraph_list):
	word_list = paragraph.split()

	for word_index, word in enumerate(word_list):

		# Split the punctuation from the word itself
		punctuation = ""
		while word[-1] in punctuation_list:
			# Add the character to punctuation string
			punctuation += word[-1]
			# Remove the character from word string
			word = word[:-1]
		# Flip punctuation string as they were read backwards (LOL!? would read punctuation as ?! rather than !?)
		punctuation = punctuation[::-1] 

		# Check if the word needs to be replaced
		for replacement_pair in replacement_list:
			if word.lower() == replacement_pair[0].lower():
				# Capitalize first letter if it was capitalized in initial text
				if word[0].isupper():
					word_list[word_index] = replacement_pair[1].capitalize() + punctuation
				else:
					word_list[word_index] = replacement_pair[1] + punctuation
				break

	# Add the fixed word list back to your list of paragraphs
	paragraph_list[paragraph_index] = " ".join(word_list)

# Print results
for paragraph in paragraph_list:
	print(paragraph)