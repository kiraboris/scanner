
import numpy as np


def my_input_data():
    return np.loadtxt('data.txt')


def my_print_data(x):
    print('Data is: ')
    print(x)


# ==  main part ==
my_data = my_input_data()
my_print_data(my_data)
#make_super_plot(my_data)
