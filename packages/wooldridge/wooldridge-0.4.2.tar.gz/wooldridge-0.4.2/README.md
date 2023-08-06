# Wooldridge Meets Python
### Data sets from _Introductory Econometrics: A Modern Approach_ (6th ed, J.M. Wooldridge)

## Description
A Python package which contains 111 data sets from one of the most famous **econometrics** textbooks for undergraduates.

It is used in [Using Python for Introductory Econometrics](http://www.urfie.net), which is a sister book [Using R for Introductory Econometrics](http://www.urfie.net).

It is also extensively used in [Pythonで学ぶ入門計量経済学](https://haruyama-kobeu.github.io/book_etrics/docs/index.html) (Japanese). 

## How to Use
First things first.
```
import wooldridge
```
To load a data set named `<dataset>`:
```
wooldridge.data('<dataset>')
```
It returns pandas `DataFrame`. Note that `<dataset>` is entered in strings. For example, to load a data set `mroz` into `df`:
```
df = wooldridge.data('mroz')
```
To show the description (e.g. variable definitions and sources) of a data set:
```
wooldridge.data('mroz', description=True)
```
To show the list of 111 data sets contained in the package
```
wooldridge.data()
```

## How to Install
```
pip install wooldridge
```
or
```
git clone https://github.com/spring-haru/wooldridge.git
pip install .
```

## Note
The function `dataWoo()` introduced in the previous versions also works:
```
from wooldridge import *

df = dataWoo('<dataset>')

dataWoo('<dataset>', description=True)

dataWoo()
```

#### Reference
J.M. Wooldridge (2016) _Introductory Econometrics: A Modern Approach_, Cengage Learning, 6th edition.
