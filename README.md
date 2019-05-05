# LyricsProject05
This is the Lyrics Rating Project submitted by Ge Tian(gt2408) and Zixuan Lin(zl2725) from group Project 5.

## Installation
To run the main functions for lyrics rating, you need to install the nltk package with pip:
```
pip install nltk
```

## Introduction
...The project is designed for .....
....


## Characterization
We rate the song lyrics from the following five dimensions and return the rating scores of each song as a json output.

### Five Main Dimensions
#### Love
For the love dimension, we match the lyrics of each song with a list of 262 love-related words to calculate the percentage of love words in the length of the song. In our rating system, the higher the percentage, the more love-related the song is.  <br /> 
*Note: Since the wordlist named "love_word.txt" is saved as txt file in our repo. Users have to run the command from the root of our repo to ensure the file could be found.*  <br />

#### Mood
For the mood dimension, we first scrap a positive wordlist (2006 unique words) and a negative wordlist (add link) (4783 unique words) from the website of Patrick O. Perry (add a links), who was an Assistant Professor in the Statistics group at NYU Stern. Then we match the lyrics of each song with the lists to calculate the percentage of positive words and negative words in the length of the song. The mood in our analysis is defined as the difference of the positive and negative percentage. The higher the difference, the happier the song is. 
 <br />
### Kidsafe
For the kidsafe dimension, we use the similar criteria we use for the lovedimension. We match the lyrics of each song with a list of 1648 not-kidsafe words to calculate the percentage of bad words in the length of the song. The lower the percentage, the more kid-safe the song is. Besides, we also inlcude our weighted mood score as an influential factor of the kidsafe dimension based on the reasoning that the song lyrcis with higher negative mood will also be less kid safe.   <br />
*Note: Since the wordlist named "not_kidsafe.txt" is saved as txt file in our repo. Users have to run the command from the root of our repo to ensure the file could be found.*
 <br />
#### Length
For the length dimension, We count the number of words in each song. The more counts, the longer the song is.
 <br />
#### Complexity
![equation](https://latex.codecogs.com/gif.latex?Comp_%7Bs%7D%3D%20-%5Csum_%7Bi%7D%5E%7BN%7DP_%7Bi%7Dlog_%7B2%7D%7BP_%7Bi%7D%7D)
 <br />
### Rank the Result
The result of each dimension is saved as a dictionary. We sort the result of each dimension and rate the songs into 11 levels from 0 to 1 with a 0.1 increment. For example, if we have 1000 songs in database, then we rate the first 1000/11 songs with lowest love percentage as 0.0, the second 1000/11 songs as 0.1, and so forth. Note here that if the song is detected as a non-English song, then we will rate a constant 0.5 for the love, kid-safe and mood dimensions of the song. 

### Foreign Lyrics
We also try to detect the song lyrics with foreign language. Take the slangs such as "yo", "umm" that might be detected as non_english, we analyze the first 20 unique words in each song and set the criteria that an English song needs to have more than 70% of its first 20 words detected as English. If the lyrics is detected as non-English, we will return constant score 0.5 for its kidsafe, love and mood dimension.

## Output
We will have the jason output has the following format:
```
{
    "characterizations": [
        {
            "id": "241",
            "artist": "Connie Francis",
            "title": "I'll Close My Eyes",
            "mood": 0.7,
            "love": 0.6,
            "kidsafe": 0.6,
            "length": 0.1,
            "complexity": 0.6
        },
        {
	...
	}
    ]
}
```
