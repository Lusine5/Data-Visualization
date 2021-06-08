import sqlite3
import numpy as np
import time
from numpy import mean

connection = sqlite3.connect('data_CLT.db')
c = connection.cursor()

c.execute("DROP TABLE IF EXISTS random_numbers_mean")

c.execute("CREATE TABLE random_numbers_mean (Id int, rand_val_mean numeric,random_value numeric)")


i = 0
a = 0
b = 0

while True:
	x=+1
	i += 1
	b = np.random.randint(1,7)
	a = mean(np.random.randint(1,7,7))
	c.execute("INSERT INTO random_numbers_mean values ({},{},{})".format(i,a,b))
	connection.commit()

	time.sleep(0.5)


