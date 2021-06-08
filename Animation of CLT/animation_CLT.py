import numpy as np

import pandas as pd
import statsmodels.api as sm
import pylab

from scipy import stats
from scipy.stats import kurtosis, skew

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import time

import sqlite3

connection = sqlite3.connect('data_CLT.db')
c = connection.cursor()

plt.xkcd()
fig1 = plt.figure(constrained_layout=True,figsize=(14, 7))
gs = fig1.add_gridspec(2, 3)

ax1 = fig1.add_subplot(gs[1, 0])

ax2 = fig1.add_subplot(gs[1, 1])

ax3 = fig1.add_subplot(gs[0, 1])
ax3.set_title('Probability Plot')
ax3.set_xlabel('Theoretical Quantiles')
ax3.set_ylabel('Ordered Values')

ax4 = fig1.add_subplot(gs[0, 0])

ax5 = fig1.add_subplot(gs[:, 2])

# list for p-values
p_values_list=[]


def animate(i):
	query = ('SELECT * FROM random_numbers_mean')
	data = pd.read_sql_query(query, connection)
	x = data.Id
	y = data.rand_val_mean
	z=data.random_value

	ax1.cla()
	ax2.cla()
	ax3.cla()
	ax4.cla()
	ax5.cla()

	# for ax1
	ax1.set_title("Skewness, Kurtosis and \n Normality test p-value (Shapiro-Wilk Test)")
	ax1.axis('off')
	axbig = fig1.add_subplot(gs[1, 0])
	axbig.annotate(" skewness: {} \n kurtosis: {} \n statistic: {} \n p-value: {} ".format(round(skew(y, bias=False),4), round(kurtosis(y, bias=False),4),
		round(stats.shapiro(y).statistic,4), round(stats.shapiro(y).pvalue,4)), (0.3, 0.45) ,xycoords='axes fraction', va='center')

	# for p-values chart
	p_value=round(stats.shapiro(y).pvalue,4)
	p_values_list.append(p_value)
	
	# for ax2
	ax2.set_title("Historical p-values")
	ax2.plot(p_values_list)

	# for ax3
	stats.probplot(y, dist=stats.beta, sparams=(2,3), fit=False,plot=ax3)
	
	# for ax4
	ax4.set_title('Distribution of Means')
	ax4.hist(y)

	# for ax5
	ax5.set_title("Distribution of Outputs")
	ax5.hist(z,bins=6)
	
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

plt.show()