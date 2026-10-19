#Wind-Turbine-Analysis



#IMPORTS
import os 
import numpy as np
import matplotlib.pyplot as plt

#QUESTION 1

#read data 
#FILE HAS TO BE IN THE SAME FOLDER AS THIS PYTHON SCRIPT
#search and assign new file path ()
#code to ensure it is in the same folder as python script
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "windturbinepower_dea26f037a90f143f1168aceb54c2ae7.txt")

#load data from text file
data = np.loadtxt(DATA_FILE)

#put data into respective arrays
t = data[:, 0]
P = data[:, 1]

#testpoint (test files read properly)
#print ("Time:", t[:5])
#print ("Power:", P[:5])

#analysis of maximum power P_max (W), mean power P_mean (W), and standard deviation of power P_std (W) using numpy functions.
P_max = np.max(P)     
P_mean = np.mean(P)  
P_std = np.std(P)    

#print results
#.6e to limit the decimal places"
print(f"Maximum power: {P_max:.6e}W")
print(f"Mean power :{P_mean:.6e}W") 
print(f"Standard deviation: {P_std:.6e}W")

#plot curve showing variation in power with time using mathplotlib functions 
plt.figure()
plt.plot(t,P)
plt.xlabel("Time (s)") 
plt.ylabel("Power (W)")
plt.title("Variation of Power with Time")
plt.grid(True)

#print graph
plt.show()

#Estimating the rate of change of power with time  (dP/dt) 
dt = t[1] - t[0]  #time interval
dPdt = np.zeros_like(P) #creating all zeroes array equal size to P with numpy functions 

#using taylor series expansion end points and central difference formulas with second order accuracy 0(dt^2) 

dPdt[0] = (-3*P[0] + 4*P[1] - P[2]) / (2*dt) #first point (Forward difference)
dPdt[-1] = (3*P[-1] - 4*P[-2] + P[-3]) / (2*dt) #last point (backward difference)
dPdt[1:-1] = (P[2:] - P[:-2]) / (2*dt) #middle points (central difference)

#Testpoint (plot graph of dP/dt against time to verify it works)
#plt.figure()
#plt.plot(t, dPdt)
#plt.xlabel("Time (s)")
#plt.ylabel("dP/dt (W/s)")
#plt.title("Rate of Change of Power")
#plt.grid(True)

#show graph
plt.show()



#QUESTION 2

#CONSTANTS DEFINITION 
#EFFECT OF BLADE IS IGNORED
#DIAMETER OF CIRCULAR CROSS SECTION OF D IS CONSTANT 
C_drag = 0.6 #drag coefficient
D = 10.0 #diameter of tower (m)
d_air = 1.29 #air density (kg/m^3)
h = 150.0 #height of hub(m)
H = 10.0 #reference height (m)
V_H = 12.5 #forcast wind speed at reference height H = 10m (m/s)

#define the V(z) function
def V(z):
    return V_H * (z / H) ** 0.12

#Tower division 
#change in z is equal to (max - min) / number of divisions, (150-0)/6 = 25
z_points = np.array([0, 25, 50, 75, 100, 125, 150]) #height points with 25m increments (m)

#calculating V values with z values 
V_points = V(z_points)

#plotting graph with mathplotlib functions
plt.figure()
plt.plot(z_points, V_points, marker='o') #marker to clearly show points
plt.xlabel("Height z (m)")
plt.ylabel("Wind speed V(z) (m/s)")
plt.title("Wind speed at fixed height points of tower (6 divisions)")
plt.grid(True)

#show graph
plt.show()

#Evaluating the Wind Drag  using Simpson and Trapezium rules repeadtedly 
#using the formula  given in the brief 
#evaluating V(z)^2 at each height 
def V_sqr(z): #V(z) squared function
    return V(z)**2

#defining integral multiplier from the formula
multiplier = 0.5 * C_drag * d_air * D

#defining the trapezium rule function using z_points
def trapezium_rule(f, z_points):
    dz = z_points[1] - z_points[0]  #dz should be 25
    f_values = f(z_points)

    return dz* (0.5 * f_values[0] + np.sum(f_values[1:-1]) + 0.5 * f_values[-1]) # Trapezium rule formular (0.5 multiplier for first and last points (half weight))

#applying rule to data values 
integral_trapezium = trapezium_rule(V_sqr, z_points)
F_trapezium = multiplier * integral_trapezium

#display results
print (f"Trapezium Integral (V(z)^2 dz) = {integral_trapezium:.6e}") #.6e to limit the decimal places"
print (f"Wind Drag Force (Trapezium) F_drag = {F_trapezium:.6e}N")

#defining the simpson's rule function using z_points
def simpsons_rule(f, z_points):

    n = len(z_points) - 1  #number of intervalS

    multiplier = 0.5 * C_drag * d_air * D
    dz = z_points[1] - z_points[0]  #dz should be 25
    f_values = f(z_points)
   
    odd_sums = np.sum(f_values[1:-1:2]) #this is the summation of y1 + y3 + y5
    even_sums = np.sum(f_values[2:-1:2]) #this is the summation of y2 + y4 + y6

    return (dz/3) * (f_values[0] + 4*odd_sums + 2*even_sums + f_values[-1]) #This is Simpson's rule formula

#applying rule to data values
integral_simpson = simpsons_rule(V_sqr, z_points)
F_simpson = multiplier * integral_simpson

#display results
print(f"Simpson's Integral (V(z)^2 dz) = {integral_simpson:.6e}") #.6e to limit the decimal places"
print(f"Wind Drag Force (Simpson) F_drag = {F_simpson:.6e}N")

#The accuracy of this prediction depends mainly on the height of the tower and the number of divisions used 
#If you increase the number of  divisions, the integral approximation is better and therefore more accurate


#Repeating integration using repeated simpson's rule starting at n=12
#define new simpson's rule function 
def repeated_simpsons_rule (f, upper_lim, lower_lim, n):
    dz = (upper_lim - lower_lim) / n  
    z = np.linspace(lower_lim, upper_lim, n + 1) 
    f_values = f(z)

    odd_sums = np.sum(f_values[1:-1:2]) #summation of y1 + y3 + y5 + ...
    even_sums = np.sum(f_values[2:-1:2]) #summation of y2 + y4 + y6 + ...

    return (dz/3) * (f_values[0] + 4*odd_sums + 2*even_sums + f_values[-1]) #This is Simpson's rule formula

#create multiplier variable
multiplier = 0.5 * C_drag * d_air * D

#defining tolerance and other variables
tolerance = 1e-4  #this is the limit that decideds when the loop stops
n = 12  #starting number of divisions
F_simpson_old = None  #this is to store previous force value (none is used so theres no error for first iteration)

#while loop to calculate and dispaly results until tolerance is met
print("Simpson's convergence results are as follows:")

while True:
    new_integral = repeated_simpsons_rule(V_sqr, h, 0.0, n)
    F_simpson_new = multiplier * new_integral

    if F_simpson_old is None:    #firt iteration (should not be able to calculate difference)
        print(f"n={n}, F_drag={F_simpson_new:.6e}N")
    else:
        difference = abs(F_simpson_new - F_simpson_old) #abs is added in case of negative values 
        print(f"n={n}, F_drag={F_simpson_new:.6e}N, Difference={difference:.6e}N")

        if difference < tolerance:    #tolerance limit check
            print("The tolerance limit has been met.")
            break

    F_simpson_old = F_simpson_new
    n = n * 2  #double 12 for next iteration like in brief example
