import csv
import os
import time


def Print_Csv(path, filename, data):
	filepath = path + filename
	with open(filepath, 'w', encoding='utf8') as csvfile:
		writer = csv.writer(csvfile, lineterminator='\n')
		data = [[element] for element in data]
		writer.writerows(data)

# Format of paragraph list is as follows: [paragraph1, paragraph2]
# Each individual paragraph is simply a string example: ["lol is the start of a sentence imho.!!? blah blah", "this is a second sentence"]
def Read_Paragraph_List(path, filename):
	filepath = path + filename
	rows = []
	with open(filepath, encoding='utf8') as csvfile:
		reader = csv.reader(x.replace('\0', '') for x in csvfile)
		for row in reader:
			try:
				rows.append(row[3])
			# Exception only occurs in empty csv files
			except:
				return []
		# Return without the header row
		return rows[1:]

# Format of replacement list is a list of tuples in the form (word to replace, replacement)
# Example replacement list: [("imho", "in my humble opinion"), ("can't", "can not")]
def Read_Replacement_List(path, filename):
	replacement_list = []
	filepath = path + filename
	with open(filepath, encoding='utf8') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			replacement_list.append((row[0], row[1]))
	# Return without the header row
	return replacement_list[1:]


def Word_Replacement(test_iteration_n, test_iteration_m):
	### CONFIG ###

	# Load filepaths of whole dataset
	read_path = '../Dataset/'
	write_path = '../TransformedDataset/'
	replacement_list_path = '../'
	replacement_list_filename = 'Replacement_List.csv'
	
	# Any common punctuation gets added here
	punctuation_list = [",", ".", "!", "?", ":", ";"]

	### END CONFIG ###

	# Get list of csv files in dataset
	filenames = next(os.walk(read_path), (None, None, []))[2]
	if not os.path.exists(write_path):
		os.makedirs(write_path)

	replacement_list = Read_Replacement_List(replacement_list_path, replacement_list_filename)

	total_words = 0

	if test_iteration_n is not None:
   		filenames = filenames[:min(len(filenames), test_iteration_n)]
	if test_iteration_m is not None:
		replacement_list = replacement_list[:min(len(replacement_list), test_iteration_m)]

	replacement_list_length = len(replacement_list)

	print(f'There are {len(filenames)} files to process')
	i = 0
	for file in filenames:

		if i % 100 == 0:
			print(f'{i/len(filenames)*100}% complete')
		i += 1

		paragraph_list = Read_Paragraph_List(read_path, file)
		for paragraph_index, paragraph in enumerate(paragraph_list):
			word_list = paragraph.split()
			total_words += len(word_list)

			for word_index, word in enumerate(word_list):

				# Split the punctuation from the word itself
				punctuation = ""
				while len(word) > 0 and word[-1] in punctuation_list:
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
							word_list[word_index] = replacement_pair[1].lower() + punctuation
						break

			# Add the fixed word list back to your list of paragraphs
			paragraph_list[paragraph_index] = " ".join(word_list)

		# Write updated contents to new file
		Print_Csv(write_path, file, paragraph_list)

	return total_words, replacement_list_length


if __name__ == '__main__':
	# Can uncomment below to generate times for different values of n and m

	# # Tests keeping n constant, changing m
	# for m_val in range(0, 121, 10):
	# 	t1 = time.perf_counter()
	# 	n, m = Word_Replacement(None, m_val)
	# 	t2 = time.perf_counter()
	# 	time_taken = t2 - t1
	# 	print(f'With n = {n}, m = {m}, it took {time_taken} seconds')

	# # Tests keeping m constant, changing n
	# for n_val in range(0, 3691, 369):
	# 	t1 = time.perf_counter()
	# 	n, m = Word_Replacement(n_val, None)
	# 	t2 = time.perf_counter()
	# 	time_taken = t2 - t1
	# 	print(f'With n = {n}, m = {m}, it took {time_taken} seconds')

	t1 = time.perf_counter()
	Word_Replacement(None, None)
	t2 = time.perf_counter()
	time_taken = t2 - t1
	print(f'It took {time_taken} seconds to go through the whole dataset')