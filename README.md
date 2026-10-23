Wind Turbine Numerical Analysis

A Python-based engineering coursework project investigating wind turbine power output and wind-induced drag forces on a turbine tower using numerical methods.

Project Overview

This project consists of two engineering analysis tasks:

1. Wind Turbine Power Analysis

* Import time-series power data from a text file.
* Calculate maximum power, mean power and standard deviation.
* Visualise power variation over time.
* Estimate the rate of change of power using second-order finite difference methods.

2. Wind Loading on a Turbine Tower

* Model wind speed variation with tower height using a power-law relationship.
* Estimate wind drag force using the composite trapezium rule.
* Apply composite Simpson’s rule to approximate the same integral.
* Investigate numerical convergence by increasing the number of subdivisions until a specified tolerance is reached.

Technologies Used

* Python
* NumPy
* Matplotlib
* Numerical differentiation
* Numerical integration

Running the Project

Install the required Python libraries:

pip install -r requirements.txt

Keep the Python script and the original wind turbine power dataset in the same folder, then run the script using Python.

Engineering Skills Demonstrated

* Numerical modelling and approximation
* Scientific data processing
* Engineering mathematics
* Data visualisation
* Iterative convergence analysis

Project Status

Original university coursework preserved for portfolio development. Further testing, documentation improvements and code refinement are planned.

Disclaimer

This project was developed for educational purposes and is not a validated tool for real-world wind turbine design or structural assessment.
