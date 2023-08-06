###BinoGaus_Probability##########


Calculates Binomial and Gaussians Distributions,

-mean and standard Deviations and more.

Help on Gaussian in module BinoGauss_Probability.Gaussiandistribution object:

class Gaussian(BinoGauss_Probability.Generaldistribution.Distribution)
 |  Gaussian(mu=0, sigma=1)
 |
 |  Gaussian distribution class for calculating and
 |  visualizing a Gaussian distribution.
 |
 |  Attributes:
 |          mean (float) representing the mean value of the distribution
 |          stdev (float) representing the standard deviation of the distribution
 |          data_list (list of floats) a list of floats extracted from the data file
 |
 |  Method resolution order:
 |      Gaussian
 |      BinoGauss_Probability.Generaldistribution.Distribution
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  __add__(self, other)
 |      Function to add together two Gaussian distributions
 |
 |      Args:
 |              other (Gaussian): Gaussian instance
 |
 |      Returns:
 |              Gaussian: Gaussian distribution
 |
 |  __init__(self, mu=0, sigma=1)
 |      Generic distribution class for calculating and
 |      visualizing a probability distribution.
 |
 |      Attributes:
 |              mean (float) representing the mean value of the distribution
 |              stdev (float) representing the standard deviation of the distribution
 |              data_list (list of floats) a list of floats extracted from the data file
 |
 |  __repr__(self)
 |      Function to output the characteristics of the Gaussian instance
 |
 |      Args:
 |              None
 |
 |      Returns:
 |              string: characteristics of the Gaussian
 |
 |  calculate_mean(self)
 |      Function to calculate the mean of the data set.
 |
 |      Args:
 |              None
 |
 |      Returns:
 |              float: mean of the data set
 |
 |  calculate_stdev(self, sample=True)
 |      Function to calculate the standard deviation of the data set.
 |
 |      Args:
 |              sample (bool): whether the data represents a sample or population
 |
 |      Returns:
 |              float: standard deviation of the data set
 |
 |  pdf(self, x)
 |      Probability density function calculator for the gaussian distribution.
 |
 |      Args:
 |              x (float): point for calculating the probability density function
 |
 |
 |      Returns:
 |              float: probability density function output
 |
 |  plot_histogram(self)
 |      Function to output a histogram of the instance variable data using
 |      matplotlib pyplot library.
 |
 |      Args:
 |              None
 |
 |      Returns:
 |              None
 |
 |  plot_histogram_pdf(self, n_spaces=50)
 |      Function to plot the normalized histogram of the data and a plot of the
 |      probability density function along the same range
 |
 |      Args:
 |              n_spaces (int): number of data points
 |
 |      Returns:
 |              list: x values for the pdf plot
 |              list: y values for the pdf plot
 |
 |  ----------------------------------------------------------------------
 |  Methods inherited from BinoGauss_Probability.Generaldistribution.Distribution:
 |
 |  read_data_file(self, file_name)
 |      Function to read in data from a txt file. The txt file should have
 |      one number (float) per line. The numbers are stored in the data attribute.
 |
 |      Args:
 |              file_name (string): name of a file to read from
 |
 |      Returns:
 |              None
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from BinoGauss_Probability.Generaldistribution.Distribution:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
