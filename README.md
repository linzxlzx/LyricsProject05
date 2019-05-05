# LyricsProject05
<img src="http://s5304.pcdn.co/guides/wp-content/uploads/cache/2017/12/Holiday_Song_Lyrics/2789392564.jpg" width="800" height="150"/>  <br /> 
This is the Lyrics Rating Project submitted by Group **Project 5** for Tools for Analytics taught by Professor Paul Logston.
Group members are:  <br />
**Ge Tian(gt2408)** <br />
**Zixuan Lin(zl2725)** <br />

## Installation
To run the main functions for lyrics rating, you need to install the nltk package with pip:
```
pip install nltk
```
## Usage
In order to make the codes run properly, you need to clone the repo and run the following command from the root of the repo:  <br /> 
```
$ python main.py \PathtoLyricsFolder
```
Here **\PathtoLyricsFolder** needs to be the path to a folder contains all the lyrics files that we need to rate.  <br /> 
For each lyrics file, it needs to have the extension of ".txt" and has the standard format as **"<song-id\>\~<song-artist\>\~<song-title\>.txt"**. Our codes will return the ratings of each song as described in the Output Section below.  <br /> 

## Characterization
We rate the song lyrics with the scale from 0.0 to 1.0 for the following five dimensions and return the rating scores of each song lyrics as a json output.

### - Five Main Dimensions
#### **Love**
For the love dimension, we match the lyrics of each song with a list of 262 love-related words to calculate the percentage of love words in the length of the song. In our rating system, the higher the percentage, the more love-related the song is.  <br /> 
*Note: Since the wordlist named "love_word.txt" is saved as txt file in our repo. Users have to run the command from the root of our repo to ensure the file could be found.*  <br />

#### **Mood**
For the mood dimension, we first scrap a [positive wordlist](http://ptrckprry.com/course/ssd/data/positive-words.txt) (2006 unique words) and a [negative wordlist](http://ptrckprry.com/course/ssd/data/negative-words.txt) (4783 unique words) from the website of Patrick O. Perry, who was an Assistant Professor in the Statistics group at NYU Stern. Then we match the lyrics of each song with the lists to calculate the percentage of positive words and negative words in the length of the song. The mood in our analysis is defined as the difference of the positive and negative percentage. The higher the difference, the happier the song is.    <br />

#### **Kidsafe**
For the kidsafe dimension, we use the similar criteria we use for the love dimension. We match the lyrics of each song with a list of 1648 not-kidsafe words to calculate the percentage of bad words in the length of the song. The lower the percentage, the more kid-safe the song is. Besides, we also inlcude our weighted mood score as an influential factor of the kidsafe dimension based on the reasoning that the song lyrcis with higher negative mood will also be less kid safe.   <br />
*Note: Since the wordlist named "not_kidsafe.txt" is saved as txt file in our repo. Users have to run the command from the root of our repo to ensure the file could be found.*   <br />

#### **Length**
For the length dimension, We count the number of words in each song. The more counts, the longer the song is.   <br />

#### **Complexity**
We refer to the information entropy concept to define the complexity of each song.  <br /> 
![equation](https://latex.codecogs.com/gif.latex?Comp_%7Bs%7D%3D%20-%5Csum_%7Bi%7D%5E%7BN%7DP_%7Bi%7Dlog_%7B2%7D%7BP_%7Bi%7D%7D)
 <br />
Where N is the number of unique words in the song *s* and *i* is the *i-th* unique word. Pi is the probability that the *i-th* word appears in the song *s*.  <br />

### - Rank the Result
The results of each dimension are saved as a dictionary. We sort the results of each dimension and rate the songs into 11 levels from 0 to 1 with an increment of 0.1. For example, if we have 1000 songs in database, then we rate the first 1000//11 songs with lowest love percentage as 0.0, the second 1000//11 songs as 0.1, and so forth. We perform the same ranking system to each of the five dimensions.  <br />

### - Foreign Lyrics
We also try to detect the song lyrics with foreign language. Take the slangs such as "yo", "umm" that might be detected as non_English, we analyze the first 20 unique words in each song and set the criteria that an English song needs to have more than 70% of its first 20 words detected as English words. If the lyrics of a song is detected as non-English, we will return constant score 0.5 for its kidsafe, love and mood dimensions.  <br />

## Output
We will have the json output with the following format:
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
