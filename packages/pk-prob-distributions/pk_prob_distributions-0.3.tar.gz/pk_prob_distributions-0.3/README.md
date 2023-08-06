# pk_prob_distributions

Summary of the package

## Files

Explanation of files in the package

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pk_prob_distributions.

```bash
pip install pk_prob_distributions
```

## Usage

```python
from pk_prob_distributions import Gaussian, Binomial

gaussian_one = Gaussian(10, 7) # a Gaussian Distribution with mean 10 and standard deviation 7

gaussian_one.calculate_mean() # returns the mean of the Gaussian Distribution

gaussian_one.calculate_stdev() # returns the standard deviation of the Gaussian Distribution

gaussian_one.pdf(k) # probability density function, being k the point for calculating the probability density function

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)