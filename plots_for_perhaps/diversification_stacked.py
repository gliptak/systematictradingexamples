import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show, xticks, xlabel, ylabel, legend, yscale, title, savefig, rcParams, figure, hist, text, bar, subplots
import Image

def variance_f(sigma):
    x=[1.0/sigma.shape[0]]*sigma.shape[0]
    return 1.0/((np.matrix(x)*sigma*np.matrix(x).transpose())[0,0]**.5)

def make_corr(dimension, offdiag=0.0):

    corr=np.array([[offdiag]*dimension]*dimension)
    corr[np.diag_indices(dimension)]=1.0
    return corr

periodlabels=["Stocks", "Industries", "Countrys", "Regions"]
cfactors=[0.85]*4+      [0.75]*3+     [0.5]*2 +[0.6]*2 
ndimlist=[1, 5, 10, 15,  1, 5, 10,   1, 5,      1, 3]
## take these values from diversification benefits plot
basestd_stock=0.27
basestd_industry=basestd_stock/1.082
basestd_country=basestd_industry/1.136
basestd_region=basestd_country/1.2909
basestdlist=[basestd_stock]*4 + [basestd_industry]*3 + [basestd_country]*2 + [basestd_region]*2


basearithmean=0.05
riskfree=0.000

## apply blow up risk

applyzero=[False]*(len(cfactors))




results_sr=[]
results_gmm=[]
results_std=[]

for ( basestd, appzero, ndim, cfactor) in zip(
     basestdlist, applyzero, ndimlist, cfactors):

    if appzero:
        gsr=0.0
        gmm=0.0
        new_std=basestd
    else:
        div_factor=variance_f(make_corr(ndim, cfactor))
        new_std=basestd/div_factor
        variance=new_std**2
        gmm=basearithmean- variance/2.0
        gsr=(gmm - riskfree) / new_std
        

          
    results_sr.append(gsr)
    results_gmm.append(gmm*100.0)
    results_std.append(new_std)

print results_sr
print results_gmm
print results_std


## un stack up
results_sr=[results_sr[0:4], [None]*3+results_sr[4:7], [None]*5+results_sr[7:9], [None]*6+results_sr[9:]]
results_gmm=[results_gmm[0:4], [None]*3+ results_gmm[4:7], [None]*5+results_gmm[7:9], [None]*6+results_gmm[9:]]
results_std=[results_std[0:4], [None]*3+results_std[4:7], [None]*5+results_std[7:9], [None]*6+results_std[9:]]


from itertools import cycle

lines =           ["-",   "--",   "-.",     ":"]
linecycler = cycle(lines)    
colorcycler=cycle(["red", "blue", "green", "black"])

for r in range(len(results_sr)):
    plot(results_sr[r], color=next(colorcycler), linestyle=next(linecycler), linewidth=3)
    
#xticks(range(len(ndimlist))[0::2], ndimlist[0::2])
ndimlist=["1", "5", "10", "15 / 1",  "5", "10 / 1",  "5 / 1", "3"]
xticks(range(len(ndimlist)), ndimlist)
legend(periodlabels, loc="top left",  prop={'size': 18})
#title("Diversification for various average correlations")
ylabel("Sharpe ratio")
xlabel("Number of assets")

rcParams.update({'font.size': 18})
ax=plt.gca()
ax.get_legend().get_title().set_fontsize('18')

def file_process(filename):
    fig = plt.gcf()
    fig.set_size_inches(18.5,10.5)
    fig.savefig("/home/rob/%s.png" % filename,dpi=300)
    fig.savefig("/home/rob/%sLOWRES.png" % filename,dpi=50)
    
    Image.open("/home/rob/%s.png" % filename).convert('L').save("/home/rob/%s.jpg" % filename)
    Image.open("/home/rob/%sLOWRES.png" % filename).convert('L').save("/home/rob/%sLOWRES.jpg" % filename)

file_process("divbenefit_sr_all_stacked")

frame=plt.gca()
frame.set_ylim([0.05, 0.3])
frame.set_yticks([ 0.0, 0.1, 0.2, 0.3])

show()


for r in range(len(results_gmm)):
    plot(results_gmm[r], color=next(colorcycler), linestyle=next(linecycler), linewidth=3)
    
#xticks(range(len(ndimlist))[0::2], ndimlist[0::2])
xticks(range(len(ndimlist)), ndimlist)
legend(periodlabels, loc="top left",  prop={'size': 18})
#title("Diversification for various average correlations")
ylabel("Geometric mean %")
xlabel("Number of assets")

rcParams.update({'font.size': 18})
ax=plt.gca()
ax.get_legend().get_title().set_fontsize('18')

frame=plt.gca()
frame.set_ylim([1.0, 4.0])
frame.set_yticks([ 1.0, 2.0, 3.0, 4.0])


file_process("divbenefit_gmm_all_stacked")

show()

for r in range(len(results_std)):
    plot(results_std[r], color=next(colorcycler), linestyle=next(linecycler), linewidth=3)
    
#xticks(range(len(ndimlist))[0::2], ndimlist[0::2])
xticks(range(len(ndimlist)), ndimlist)
legend(periodlabels, loc="top left",  prop={'size': 18})
#title("Diversification for various average correlations")
ylabel("Standard deviation")
xlabel("Number of assets")

rcParams.update({'font.size': 18})
ax=plt.gca()
ax.get_legend().get_title().set_fontsize('18')

file_process("divbenefit_std_all_stacked")

show()
