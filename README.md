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
We rate the song lyrics from the following five dimensions and output the rating of each song as a json output.

### love

### mood

### kidsafe

### length

### complexity
![equation](https://latex.codecogs.com/gif.latex?Comp_%7Bs%7D%3D%20-%5Csum_%7Bi%7D%5E%7BN%7DP_%7Bi%7Dlog_%7B2%7D%7BP_%7Bi%7D%7D)


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





