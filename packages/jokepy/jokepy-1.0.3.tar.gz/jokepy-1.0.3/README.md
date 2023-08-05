# Jokepy

Python Wrapper for sv443 JokeApi

## Installation (Install versions > 1.0.0)

    pip install jokepy

## Importing Jokepy

    from jokepy import Jokepy

## Creating Jokepy object

  

    j = Jokepy(categories=[],flags  =  [],idRange=[(startId),(endId)],type  =  (single/twopart),searchstring  = (searchstring))

## Getjoke

    j.getjoke()
   

## Params

 - Categories : ['Programming' , 'Miscellaneous' , 'Dark']
 - Blacklist flags :['nsfw' , 'religious' , 'political' , 'racist' ,
   'sexist' ]
 - types : single / twopart

## Exceptions

 - InvalidCategoryException (if the api doesnt supported categories)
 - InvalidFlagException (if the api doesnt support blackList flags)
 - InvalidTypeException(if the type is invalid)
 - InvalidIdRangeException (if the idRange is invalid)

## Dependencies

 - [Requests](https://pypi.org/project/requests/)

## API Documentation

 - [sv443 JokeAPI](https://sv443.net/jokeapi/v2)

