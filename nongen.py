#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2, re, random, math

def sanitize(string):
	p = re.compile(r'<[^>]+>') # remove HTML tags
	q = re.compile(r'\s+') # and extra spaces
	return q.sub(' ', p.sub(' ', string))

def getWords(source, dictionary):
	valid_words = set()
	word_list = open(dictionary, 'r')
	for line in word_list:
		line = line.rstrip()# no newlines
		valid_words.add(line)

	try:
		# use magic browser, enables browsing sites that block bots
		req = urllib2.Request(source, headers={'User-Agent' : "Magic Browser"})
		con = urllib2.urlopen(req)
		site_text = con.read()
	except:
		return None # can't read website!!

	try:
		site_text = site_text.split(site_text.split("<body")[1], "</body")[0]
	except:
		pass
	temp_words = sanitize(site_text).split(" ") # split sanitized body by spaces

	# remove invalid words
	words = [] # final words list
	for word in temp_words:
		if word.lower() in valid_words:
			words.append(word.lower())

	return words

def capitalize(text):
	# capitalizes all letters appearing after periods
	letter_list = list(text)
	last_char = ''
	for i in range(len(letter_list)):
		if last_char == '.' or i == 0:
			letter_list[i] = letter_list[i].upper()
		if letter_list[i] != ' ' and letter_list[i] != '\n':
			last_char = letter_list[i]
	return "".join(letter_list)

def genLines(word_list, num_lines, line_length):
	lines = []
	punctuation =  ['.', '.', '.', '.', ',', ',', ',', ':', ';'] # for random insertion
	for i in range(num_lines):
		# make a line, with length within length/2 range around length specified
		this_len = random.randint(max(1, line_length - math.ceil(line_length/4.0)), max(1, line_length + math.ceil(line_length/4.0)));
		line = ""
		for j in range(this_len): # add words
			if len(line): # we've already got something
				if random.random() < 0.04:
					# insert punctuation every ~25 words
					line += punctuation[random.randint(0, len(punctuation) - 1)]
				line += " "

			# add a word
			line += word_list[random.randint(0, len(word_list) - 1)]
		if random.random() < 0.25: #end on period or comma, ~4 lines
			line += punctuation[random.randint(0, len(punctuation) - 3)]
		lines.append(line)

	# handle end of the poem - should end in a period, or nothing
	last_index = len(lines) - 1
	if lines[last_index][len(lines[last_index]) - 1] in punctuation:
		# replace with '.'
		str_arr = list(lines[last_index])
		str_arr[len(str_arr) - 1] = '.'
		lines[last_index] = "".join(str_arr)
	elif random.random() < 0.7:
		lines[len(lines) - 1] += '.'

	return lines

def getPoem(url, num_lines, num_words, html):
	# get words
	if not "http" in url: url = "http://" + url
	word_list = getWords(url, "wordlist.txt")
	# build poem
	if word_list == None:
		return "The Nonsense Generator can't find \"" + target + "\""
	else:
		poem = ''
		for line in genLines(word_list, num_lines, num_words):
				poem += line
				poem += '\n' if not html else '<br/>'
		return capitalize(poem)

if __name__ == "__main__":
	print getPoem('http://eliotswasteland.tripod.com/twl.html', 5, 7, False)

