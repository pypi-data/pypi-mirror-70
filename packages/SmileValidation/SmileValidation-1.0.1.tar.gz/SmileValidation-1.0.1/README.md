# SmileValidation
![smilevalidator](https://user-images.githubusercontent.com/227092/83977155-7da56a00-a928-11ea-9f9b-66df0791a9c6.png)

Python3 Validation in another way

I hurt enough for validating those form's elements. Time to bring a new reference type.

It's gonna solve like this way:

```
from Validator import Validator
from Rule import Rule

```
## Rule
It is the collection of what we wanna validate to those element objects

Example: \
Add this to Rule.py as piece of an element validation.
```
# field
self.__emailOne		= self.__type.getString(
    require= True
    , maxLength= 75
    , minLength= 8
    , unicode= False
    , regex= None
)
``` 

Create a test.py for testing reason.\

```
from Validator import Validator
from Rule import Rule

# instance 
rule			= Rule()
validator		= Validator()

# emailOne is an element of html form
validator.addElement(
    elementName ='emailOne'
    , elementValue= 'masako'
    , rule= rule.getEmailOne()
)

if validator.isValid():
	print(f'Valid')
else:
	print(f'Invalid')
    # get error with showing the happening of the element
    print(f'{validator.getError()}')
```  