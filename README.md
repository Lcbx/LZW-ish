## What's this ?
my take on making a [LZW-style compression algorithm](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch)  
  
this version has some features/optimizations :
* the minimal size of a duplicated section can be configured
* contiguous references are merged together

### Is it usable as is ?
NO  
the encoder only accepts strings  
the encoded output isn't fit for saving into a file as-is  

### Can i use it ?
Sure, just don't say it's your original code.

### Example
```
  0: I am Sam
  9:
 10: Sam I am
 19:
 20: That Sam-I-am!
 35: That Sam-I-am!
 50: I do not like
 64: that Sam-I-am!
 79: 
 80: Do you like green eggs and ham?
112:
113: I do not like them, Sam-I-am.
143: I do not like green eggs and ham.
```

becomes (minimum ref size = 5)

```
I am Sam

Sam I am

That Sam-I-am!(19, 15)
I do not like
t(21, 14)
Do you(58, 5) green eggs and ham?
(49, 14) them,(24, 9).(112, 15)(92, 18).
```

