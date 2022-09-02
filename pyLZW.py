#import string
#from bitstring import BitArray, BitStream


# min size of the sequence to be replaced
# (because the referring process is not free in both memory space and computation)
MIN_SIZE = 6

def encode(word, simplify = True):
	
	# a dictionnary with the possible sequences
	# an entry is reference of previous input
	# a tuple of (index, length)
	references = {}
	
	# the code we'll  return
	code = [] #BitStream()
	
	# the sequence of characters being evaluated
	sequence = ""
	# for each character in the word we are encoding
	for c in word:
		
		# add it to the sequence we are currently considering
		temp = sequence + c
		
		# if we know the result or it's too small
		# we just keep looking
		if temp in references or len(temp) < MIN_SIZE:
			sequence = temp
			
		else:
			# add the unknown sequence to our dict
			references[temp] = ( len(code), len(temp) )
			
			# if we know the current sequence, we add a reference to the original
			if sequence in references:
				ref = references[sequence]
				pos, length = ref
				
				# simplify by merging contiguous refs
				if simplify and isinstance(code[-1], tuple):
					oldPos, oldLength = code[-1]
					if oldPos+oldLength == pos:
						ref = (oldPos,oldLength+length)
						code[-1] = ref
						#print("replaced", sequence, ref)
					
				# add the ref
					else:
						code.append(ref)
						#print("after", sequence, ref)
				else:
					code.append(ref)
					#print("as-is", sequence, ref)
				
				# the sequence is reset to only the new character
				sequence = c
			else:
				# if we don't know the sequence
				# we add the current character to the code
				# and keep moving by removing the first char of the sequence
				code.append(sequence[0])
				sequence = temp[1:]
	
	# there is usually an unincoded sequence remaining
	if sequence:
		if sequence in references:
			code.append(references[sequence])
		else:
			code.extend(sequence)
	
	return code



def decode(code, toDecode = None):
	
	# the string we'll  return
	word = ""
	
	if not toDecode: toDecode = code
	
	# for each character in the word we are decoding
	for c in toDecode:
		
		if isinstance(c, str):
			word += c
		else:
			pos, length = c
			found = code[pos:pos+length]
			#print(pos, length, found)
			
			# sometimes, a ref is within the sequence being referred to !
			shouldDecode = any( [ (isinstance(ch, tuple)) for ch in found] )
			res = decode(code,found) if shouldDecode else ''.join(found)
			
			if len(res) > length:
				res = res[:length]
			word += res
	
	return word

# TODO :
#	* there's a bug in simplify ->
#		sometimes when a 'as-is' follows an 'after' (see prints) the ref is wrong
#		try with MIN_SIZE = 5 to reproduce
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
	TEST2 = encode(TEST_STR)
	
	print()
	
	#print(TEST)
	print(''.join(map(str, TEST)))
	#print(decode(TEST))
	
	print()
	
	#print(TEST2)
	print(''.join(map(str, TEST2)))
	#print(decode(TEST2))
	
	
	print('ratios', len(TEST_STR), len(TEST),len(TEST)/len(TEST_STR), len(TEST2), len(TEST2)/len(TEST_STR))
