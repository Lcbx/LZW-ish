#import string
#from bitstring import BitArray, BitStream


def encode(input, MIN_REF_SIZE=5, MAX_REF_SIZE=0xFF):
	
	# MIN_REF_SIZE : min size of the sequence to be replaced
	# (because the referring process is not free in both memory space and computation)
	
	# MAX_REF_SIZE : max size of the sequence to be replaced
	# (because the encoding process uses a byte to encode length)
	
	# no need to enc ode if too small for it
	INPUT_SIZE = len(input)
	if INPUT_SIZE<MIN_REF_SIZE:
		return input
	
	# the encoded result we're building
	code = [] #BitStream()
	
	# a dictionnary with the possible sequences
	# an entry is a reference to previous input
	# an entry consists of a tuple : (index, length)
	knownSequences = {}
	
	# a list of references made in the past
	references = []
	
	# offset to next reference use
	ref_call_site = 0
	code.append(INPUT_SIZE)
	
	# the part of the input we are considering
	start, end = 0, MIN_REF_SIZE
	
	# while we haven't seen the whole input
	while end < INPUT_SIZE:
		
		lookahead = input[start:end]
		sequence  = lookahead[:-1]
		
		# if we know the result or it's too small
		# we just look farther
		if lookahead in knownSequences or len(lookahead) < MIN_REF_SIZE:
			end+=1
			
		else:
			# add the unknown sequence to our dict
			knownSequences[lookahead] = ( start, len(lookahead) )
			
			# if we know the current sequence, we add a reference to the original
			if sequence in knownSequences:
				ref = knownSequences[sequence]
				
				# this is a ref site, save the relative ref offset
				code[ref_call_site] = len(code) - ref_call_site
				
				# merge continuous refs
				if MIN_REF_SIZE < MAX_REF_SIZE:
					pos, length = ref
					
					i = MIN_REF_SIZE
					while i<MAX_REF_SIZE     and \
						  pos+i<start        and \
						  start+i<INPUT_SIZE and \
						  input[pos+i] == input[start+i]:
						i+=1
					
					ref = (pos, i)
					start += i
				else:
				# if there is no simplification
				# we add the ref found as-is
					start = end-1
				
				# translate the reference No to the actual ref entry
				if ref in references:
					code.append(references.index(ref))
				else:
					code.append(len(references))
					references.append(ref)
				
				# create the ref site for next ref
				ref_call_site = len(code)
				code.append(INPUT_SIZE)
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
		# if we know the remaining sequence we encode it
		if sequence in knownSequences:
			if ref in references:
				code.append(references.index(ref))
			else:
				code.append(len(references))
				references.append(ref)
		else:
			code.extend(sequence)
	
	return [len(references)] + references + code



def decode(code):
	
	references = code[1:code[0]+1]
	rawdata = code[code[0]+1:]
	
	nextRef = -1
	
	# the data we'll  return
	data = ""
	
	# for each byte in input
	for i, c in enumerate(rawdata):
		# first comes the offset to next ref
		if nextRef < i :
			nextRef = i + c
		# if it's a ref, find it and add it
		elif nextRef == i:
			pos, length = references[c]
			found = data[pos:pos+length]
			data += found
		# it's a simple char
		else:
			data += c
	
	return data

#
# encoding is :
# <referencesArrayLength:int><references=(<absolutePosition:int><length:int>)*><data=(<nextRefOffset:int><bytes:char*><referenceNo:int>)*>
# TODO :
#	* maybe just make the references list contain the ref sequence itself ?
#	* better than that : we can cache refs as we decode them using the references array
#	* use bytes instead of array (which means mingling ints with chars, more complexity)
#	* experiment with the sizes : maybe make the nBits of encoded distance be determined using the max(distance) ?



if __name__ == '__main__':

	TEST_STR = """I am Sam
Sam I am

That Sam-I-am!
That Sam-I-am!
I do not like
that Sam-I-am!

Do you like green eggs and ham?

I do not like them, Sam-I-am.
I do not like green eggs and ham."""
	TEST = encode(TEST_STR, 5, 5)
	print(TEST)
	#print(''.join(map(str, TEST)))
	resTest = decode(TEST)
	#print(resTest)
	print(TEST_STR == resTest)
	
	print()
	
	TEST2 = encode(TEST_STR)
	print(TEST2)
	#print(''.join(map(str, TEST2)))
	resTest2 = decode(TEST2)
	#print(resTest2)
	print(TEST_STR == resTest2)
	
	print()
	
	print('ratios', len(TEST_STR), len(TEST),len(TEST)/len(TEST_STR), len(TEST2), len(TEST2)/len(TEST_STR))
