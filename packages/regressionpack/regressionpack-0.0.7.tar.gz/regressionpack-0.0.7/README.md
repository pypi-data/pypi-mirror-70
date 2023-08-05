# regressionpack

A library of higher level regression functions that also include errorbars computed using a provided confidence interval. 
Available regressions so far include  
* [Linear](https://en.wikipedia.org/wiki/Linear_regression)
    * [Polynomial](https://en.wikipedia.org/wiki/Polynomial_regression)
* GenericCurveFit
    * CosineFit
    * Exponential


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This package was developped using:  
* python 3.8.3
* numpy 1.18.1
* scipy 1.4.1

While it may still work with older versions, I did not take the time to verify. 

### Installing

``
pip install regressionpack
``

Note that this will also install numpy 1.18.1 and scipy 1.4.1 if they are not already present. 
Once installation is done, you may use the package by importing it this way:  
``
import regressionpack
``

## Example applications

For examples on how to use this package, look at the following [jupyter notebook](tests/test_regressionpack.ipynb). You will need [matplotlib](https://pypi.org/project/matplotlib/).  

## Built With
* [Python](https://www.python.org/) - The language
* [numpy](https://numpy.org/) - the numeric library
* [scipy](https://docs.scipy.org/) - the scientific library

## Contributing
Contact me and discuss your ideas and ambitions. 

## Authors

* **FusedSilica** - *Initial work*

## License

This project is licensed under the GNU LGPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

