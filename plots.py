import matplotlib.pyplot as plt


# coeficientes LP
X, Y = [], []
for line in open('lp_2_3.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(1)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('LP',fontsize=18)
plt.xlabel('coeficient 1')
plt.ylabel('coeficient 2')
plt.savefig('lp_2_3.png')
#plt.show()

# coeficientes LPCC
X, Y = [], []
for line in open('lpcc_2_3.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(2)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('LPCC',fontsize=18)
plt.xlabel('coeficient 1')
plt.ylabel('coeficient 2')
plt.savefig('lpcc_2_3.png')
#plt.show()

# coeficientes MFCC
X, Y = [], []
for line in open('mfcc_2_3.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(3)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('MFCC',fontsize=18)
plt.xlabel('coeficient 1')
plt.ylabel('coeficient 2')
plt.savefig('mfcc_2_3.png')
#plt.show()