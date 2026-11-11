# The Challenge

A haiku is a style of Japanese poetry that, when written in English, follows a defined pattern: a three-line poem where the first line has 5 syllables, the second line has 7 syllables, and the third line also has 5 syllables.

Write a program that generates the remainder of a haiku from an allowable list of words, after you give it an input or starter word, also from the list. Your program should work no matter which starter word you use as input. The haikus do not need to sound aesthetically pleasing or make logical sense, but they must follow these rules.

Each haiku must include:

- The input or starter word as the first word of the first line.
- Three lines of text: 5 syllables in the first line, 7 syllables in the second line, and 5 syllables in the third line.
- At least one adjective, one adverb, one noun, and one verb. Other parts of speech are optional.
- No repeated words.

To show that your program works, choose at least five starter words with at least three different syllable lengths and generate five different haikus. Display the total number of syllables in each line to show that it follows the 5–7–5 pattern.

> **Note:** In spoken language, a word’s syllable count or part of speech may vary by dialect, accent, or context. For this challenge, use the attributes given for each word.

## Examples

The following haikus are examples of what your output could look like. They may not follow all the rules above. The first is borrowed from [this question on Writing Stack Exchange](https://writing.stackexchange.com/); the second was written by the challenge author.

### Example 1

**Input:** Here (1)

**Output:**

> Here is my haiku (5)  
> I wrote it for this question (7)  
> Is it any good (5)

### Example 2

**Input:** Challenging (3)

**Output:**

> Challenging you with (5)  
> Writing haikus via code (7)  
> Good luck and have fun (5)

## The Rules

All correct answers will be designated as winners.

Please include:

- Your code.
- A brief description of your approach.
- Your input: five starter words with at least three different syllable lengths.
- Your output: five haikus, including syllable counts.

Your entry must not be written by AI.

**Challenge deadline:** December 9, 2026

For feedback about this challenge, please visit the feedback post on Meta.

Have fun!


## The Data

Below is the list of allowable words you may pull from for your starter words and haikus.
[words.json](./words.json)

