## Bit Strings

Bitstrings are an easy way of recording binary switches - such as whether or not a given board position has a piece on it. They provide a simple and fast way of manipulating binary data.

They are represented as simply bits chained together into a string. For example, if one row of the Checkers board looked like this:

|Position|1|2|3|4|5|6|7|8|
|---------|---|---|---|---|---|---|---|---|
| |Red|x|Black|Black|Red|x|x|x|

To represent this row, we have two bitstrings, one for Red and one for Black:

|Player|Bitstring|
|-------|----------|
|Red|`10001000`|
|Black|`00110000`|

## Bitstring Operations

There are various bitstring logical operations, mainly Boolean:

|Operation|Type|Python Equivalent|
|------------|------|---------------------|
|`NOT x`|boolean|`~x & (2**x.bit_length() - 1)`
|`x OR y`|boolean|`x` &#124; `y`|
|`x AND y`|boolean|`x & y`|
|`x NOR y`|boolean|`x ^ y`|
|`x LSHIFT n`|mutation|`x << n`|
|`x RSHIFT n`|mutation|`x >> n`|
|`x LCIRC n`|mutation|Nonexistent|
|`x RCIRC n`|mutation|Nonexistent|

Python has an "inversion" operator, `~`, but it isn't actually the `NOT` operation; instead, `~x` is equivalent to `-x - 1`.

So, I decided to add my own implementation:

```python
class Integer(int):
	'''A wrapper around native ints that allows for various logical operators'''
	def __invert__(self):
		'''Invert the current value with the logical NOT operator'''
		value = self.real
		return ~value & (2**value.bit_length() - 1)

	def rcirc(self, n):
		'''RCIRC the bitstring n times'''
		value = self.real
		numBits = value.bit_length()
		n = n % numBits # make sure n is within the range of (0, numBits) inclusive
|		if (n == numBits)|# RCIRC(x, n) for n = (number of bits in x) is| equal to x
			return value

		toShift = numBits - n
		right = value >> n # remove the last n bits
		left = (value << toShift) ^ (right << numBits) # get the first "toShift" bits
		return left | right # combine the left and right halves

	def lcirc(self, n):
		'''LCIRC the bitstring n times'''
		value = self.real
		numBits = value.bit_length()
		n = n % numBits # make sure n is within the range of (0, numBits) inclusive
|		if (n == numBits)|# LCIRC(x, n) for n = (number of bits in x) is| equal to x
			return value

		toShift = numBits - n
		right = value >> toShift # remove the last "toShift" bits
		left = (value << n) ^ (right << numBits) # get the first n bits
		return left | right # combine the left and right halves
```

Thus, the changed operations become:

|Operation|Type|Python Equivalent|
|------------|------|---------------------|
|`NOT x`|boolean|`~Integer(x)`
|`x LCIRC n`|mutation|`Integer(x).lcirc(n)`|
|`x RCIRC n`|mutation|`Integer(x).rcirc(n)`|

## Benchmark Testing

After doing some testing, I found out that my `Long` class (which wraps the `long` primitive) is actually significantly slower than using a list of bits.

Here is a benchmark for various operations that I will need to perform, between using a literal string of bits, a binary integer, and a list (for 100,000 calls):

|Function|Elapsed Time|
|----------|---------------|
|str.getBit|0.0192716030799s|
|str.moveBit|0.22296878136s|
|str.compare|0.0254751902129s|
|str.concat|0.0339446831609s|
|list.getBit|0.0135640748445s|
|list.moveBit|0.0431440098892s|
|list.compare|0.0325705429963s|
|list.concat|0.235995744157s|
|Long.getBit|0.332514551061s|
|Long.moveBit|1.16779904939s|
|Long.compare|0.0291004114438s|
|Long.concat|0.387784635174s|

If I have the time, I might re-implement the `Integer`/`Long` classes in C (using the Python API for integrating with C) and see if these end up being faster. This shouldn't be too hard because a lot of the operations are the same, but I will have to learn how to integrate with C to make it work.
