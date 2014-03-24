#load text file : numpy.loadtxt('dmatrix.txt', skiprows=1)
numpy.loadtxt(fname, dtype=<type 'float'>, comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)
numpy.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')

# specify converter
converters = {0: lambda s: float(s.strip('"')}
data = np.loadtxt("Data/sim.csv", delimiter=',', skiprows=1, converters=converters)

# specify col range : usecols=(1,2,3) OR
data = np.loadtxt("Data/sim.csv", delimiter=',', skiprows=1, usecols=range(1,15))

# skip column without knowing number of columns
with open("Data/sim.csv") as f:
    ncols = len(f.readline().split(','))

data = np.loadtxt("Data/sim.csv", delimiter=',', skiprows=1, usecols=range(1,ncols+1))