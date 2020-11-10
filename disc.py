import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

R = 10000 # radius of disk in units of Gravitational radii Rg = GM/c^2
a = 10 # number of annuli
R0 = 1 # inner edge of disc
alpha = 1 # viscocity parameter
H = 1 #disc height
t = 1000000 #number of time values at which we measure Mdot
res = 50 #number of values calculated per timescale

def annuli_displacements(Radius, MinRad, Annuli):
    displacements = np.logspace(np.log10(Radius), np.log10(MinRad), Annuli)
    return displacements

def viscous_frequency(displacements, Radius, Height, alpha):
    f = lambda displacements: displacements**(-3/2)*((Height/Radius)**2)*(alpha/(2*np.pi))
    frequencies = f(displacements)
    return frequencies
    
def toy_viscoustimescale(r, rmod):
    t = (2*np.pi*rmod*r)
    return t

def sample_times(tau, ts, res):
    t = int(round(tau/res))
    times = ts[::t]
    return times 

def toy_accretion_rate(M0, r, ts, rmod):
    f = lambda ts: (r*np.sin(ts/(rmod*r)))/100000
    m = f(ts)
    M0 = np.take(M0, ts)
    ys = np.multiply(M0, 1+(m))
    
    return ys


annuli = annuli_displacements(R, R0, a)

M0 = np.ones(t)
ts = range(t)
Ms = []
rmod = 4

for i in range(len(annuli)):  

    r = annuli[i]
    tau = toy_viscoustimescale(r, rmod)
    times = sample_times(tau, ts, res)
    print(times)
    M = toy_accretion_rate(M0, r, times, rmod)
    
    M = np.interp(ts, times, M)
    
    Ms.append(M)
    M0 = M

plt.plot(times, Ms[0])
plt.show()
plt.plot(times, M)
plt.show()
freq, power = signal.welch(M)
psd = np.multiply(power, freq)
plt.loglog(freq, psd)
plt.show()