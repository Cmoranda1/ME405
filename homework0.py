from matplotlib import pyplot as plt

x = []
y = []

with open('eric.csv') as a_file:
	lines = a_file.readlines()
for line in lines:
	data = line.split(',')
	if(len(data) > 1):
		try:
			x_val = float(data[0])
			y_val = float(data[1])
		except ValueError:
			pass
		else:
			x.append(x_val)
			y.append(y_val)
plt.plot(x,y, marker='o')
plt.xlabel('Weight of a Duck')
plt.ylabel('Probability of being a witch')
plt.show()