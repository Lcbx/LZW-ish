#import string
#from bitstring import BitArray, BitStream


# min size of the sequence to be replaced
# (because the referring process is not free in both memory space and computation)
MIN_REF_SIZE = 5

def encode(input, simplify = True):
	
	# a dictionnary with the possible sequences
	# an entry is a reference to previous input
	# an entry consists of a tuple : (index, length)
	references = {}
	
	# the encoded result we're building
	code = [] #BitStream()
	
	INPUT_SIZE = len(input)
	if INPUT_SIZE<MIN_REF_SIZE:
		return input
	
	# the part of the input we are considering
	start, end = 0, MIN_REF_SIZE
	
	# while we haven't seen the whole input
	while end < INPUT_SIZE:
		
		lookahead = input[start:end]
		sequence  = lookahead[:-1]
		
		# if we know the result or it's too small
		# we just look farther
		if lookahead in references or len(lookahead) < MIN_REF_SIZE:
			end+=1
			
		else:
			# add the unknown sequence to our dict
			references[lookahead] = ( start, len(lookahead) )
			
			# if we know the current sequence, we add a reference to the original
			if sequence in references:
				ref = references[sequence]
				
				# simplify by merging continuous refs
				if simplify:
					pos, length = ref
					
					i = MIN_REF_SIZE
					while pos+i<start and input[pos+i] == input[start+i]:
						i+=1
					
					code.append( (pos, i) )
					start += i
				else:
					# we add the ref found as-is
					code.append(ref)
					start = end-1
			else:
				# if we don't know the sequence
				# we pass the start character
				code.append(sequence[0])
				start += 1
			
			# when we have added a new character/ref
			# we start from MIN_REF_SIZE again
			end = start + MIN_REF_SIZE
	
	# there is usually an unincoded sequence remaining
	if start < end:
		sequence = input[start:end]
		if sequence in references:
			code.append(references[sequence])
		else:
			code.extend(sequence)
	
	return code



def decode(code):
	
	# the string we'll  return
	word = ""
	
	# for each character in the word we are decoding
	for c in code:
		# if it a simple char, add it
		if isinstance(c, str):
			word += c
		else:
		# if it's a ref, find it and add it
			pos, length = c
			found = word[pos:pos+length]
			word += found
	
	return word

# TODO :
#	* use bytes, make an encoding for refs
#		something like
#		<? bytes till next ref>data<ref><? bits till next ref>data...
#		need to experiment with the sizes
#		maybe make the nBits of encoded distance be determined using the max(distance)



if __name__ == '__main__':

	TEST_STR = """I am Sam

Sam I am

That Sam-I-am!
That Sam-I-am!
I do not like
that Sam-I-am!

Do you like green eggs and ham?

I do not like them, Sam-I-am.
I do not like green eggs and ham.
	"""
	TEST = encode(TEST_STR, False)
	print(''.join(map(str, TEST)))
	resTest = decode(TEST)
	#print(resTest)
	print(TEST_STR == resTest)
	
	print()
	
	TEST2 = encode(TEST_STR)
	print(''.join(map(str, TEST2)))
	resTest2 = decode(TEST2)
	#print(resTest2)
	print(TEST_STR == resTest2)
	
	print()
	
	
	
	print('ratios', len(TEST_STR), len(TEST),len(TEST)/len(TEST_STR), len(TEST2), len(TEST2)/len(TEST_STR))
