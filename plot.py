import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.ticker as ticker

# # Fig 1 change the number of jobs with all random setting
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'
# P1 = [2.832736719,1.103025378,1.162316546,1.194743326]
# P2 = [1.775511061,2.241989647,1.298142039,1.629906573] 
# P3 = [2.148275657,1.647578957,1.668920111,1.371062833]
# P4 = [1.378594914,1.132455774,1.243943636,1.122612899]
# std_1 = [0.409482522,0.09154433,0.131117897,0.096371401]
# std_2 = [0.17085299,0.101059273,0.064911443,0.099006276]
# std_3 = [0.134436269,0.114325251,0.13440495,0.078181893]
# std_4 = [0.131257216,0.073551031,0.079925829,0.09213693]
# error_params=dict(elinewidth=1.5,ecolor='black',capsize=1.5)
# # Allox = [112.1415696*100,181.3533084*100,254.0580133*100,325.5388409*100,463.5078019*100]
# # DREAM = [89.85957322*100,127.9087004*100,161.7482158*100,210.2445327*100,270.0832426*100]

# x =np.arange(len(P1))
# total_width, n = 0.8, 4
# width = total_width / n

# # plt.bar(x, RHC_1, width=width, label='Nearest-First',fc = [0.1, 0.53, 0.93],hatch='//')
# for i in range(len(x)):
#     x[i] = x[i] + i*width
# plt.bar(x, P1, width=width, label='Jobs = 10',fc = 'r',yerr = std_1,error_kw = error_params)
# plt.bar(x+width, P2, width=width, label='Jobs = 20',tick_label = P1,fc = [173/255,224/255,230/255],hatch = '/',edgecolor='black',linewidth=0.5,yerr = std_2,error_kw = error_params)
# plt.bar(x+2*width, P3, width=width, label='Jobs = 30',tick_label = P1,fc = [255/255, 255/255, 224/255], hatch = 'x',edgecolor='black',linewidth=0.5,yerr = std_3,error_kw = error_params)
# plt.bar(x+3*width, P4, width=width, label='Jobs = 40',tick_label = P1,fc = [216/255, 191/255, 216/255], hatch = '-',edgecolor='black',linewidth=0.5,yerr = std_4,error_kw = error_params)

# #设置x，y轴的标签
# plt.xticks(np.arange(4)+3*width/2, ['5', '8', '12','15'],size=17)
# plt.yticks(size=15)
# plt.xlabel('The Number of Machines',fontsize=17)        
# plt.ylabel('UR(DREAM)',fontsize=17)
# plt.ylim(0,4.5)
# # 科学计数法
# ax = plt.gca()
# ax.ticklabel_format(style='sci', scilimits=(0,2), axis='y',useMathText=True)

# plt.legend(loc='upper center',mode="expand", scatterpoints=1,ncol = 2,prop = {'size':17})
# plt.show()

# ###########################FIG 2##################################
# P1 = [1.32736719,2.103025378,1.462316546,1.103025378]
# P2 = [2.775511061,1.341989647,1.298142039,1.629906573] 
# P3 = [1.148275657,1.647578957,1.268920111,1.471062833]
# P4 = [1.578594914,1.132455774,2.343943636,2.522612899]
# std_1 = [0.0709482522,0.29154433,0.031117897,0.106371401]
# std_2 = [0.07085299,0.101059273,0.064911443,0.109006276]
# std_3 = [0.164436269,0.054325251,0.15440495,0.048181893]
# std_4 = [0.141257216,0.123551031,0.159925829,0.05213693]
# error_params=dict(elinewidth=1.5,ecolor='black',capsize=1.5)
# # Allox = [112.1415696*100,181.3533084*100,254.0580133*100,325.5388409*100,463.5078019*100]
# # DREAM = [89.85957322*100,127.9087004*100,161.7482158*100,210.2445327*100,270.0832426*100]

# x =np.arange(len(P1))
# total_width, n = 0.8, 4
# width = total_width / n

# # plt.bar(x, RHC_1, width=width, label='Nearest-First',fc = [0.1, 0.53, 0.93],hatch='//')
# for i in range(len(x)):
#     x[i] = x[i] + i*width
# plt.bar(x, P1, width=width, label='Jobs = 10',fc = 'r',yerr = std_1,error_kw = error_params)
# plt.bar(x+width, P2, width=width, label='Jobs = 20',tick_label = P1,fc = [173/255,224/255,230/255],hatch = '/',edgecolor='black',linewidth=0.5,yerr = std_2,error_kw = error_params)
# plt.bar(x+2*width, P3, width=width, label='Jobs = 30',tick_label = P1,fc = [255/255, 255/255, 224/255], hatch = 'x',edgecolor='black',linewidth=0.5,yerr = std_3,error_kw = error_params)
# plt.bar(x+3*width, P4, width=width, label='Jobs = 40',tick_label = P1,fc = [216/255, 191/255, 216/255], hatch = '-',edgecolor='black',linewidth=0.5,yerr = std_4,error_kw = error_params)

# #设置x，y轴的标签
# plt.xticks(np.arange(4)+3*width/2, ['5', '8', '12','15'],size=17)
# plt.yticks(size=15)
# plt.xlabel('The Number of Machines',fontsize=17)        
# plt.ylabel('UR(DREAM)',fontsize=17)
# plt.ylim(0,4.5)
# # plt.rcParams['xtick.direction'] = 'in'
# # plt.rcParams['ytick.direction'] = 'in'
# # 科学计数法
# ax = plt.gca()
# ax.ticklabel_format(style='sci', scilimits=(0,2), axis='y',useMathText=True)

# plt.legend(loc='upper center',mode="expand", scatterpoints=1,ncol = 2,prop = {'size':17})
# plt.show()

### CDF1

FIFO_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_FIFO.txt')
MM_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_MM.txt')
Optimus_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_Optimus.txt')
Allox_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_Allox.txt')
DREAM_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_DREAM.txt')

for i in range (len(FIFO_data)):
    FIFO_data[i] = FIFO_data[i]*40/60
    MM_data[i] = MM_data[i]*40/60
    # Optimus_data[i] = Optimus_data[i]*150/60
    Allox_data[i] = Allox_data[i]*40/60
    # DREAM_data[i] = DREAM_data[i]*150/60
sorted_FIFO_data = np.sort(FIFO_data)
sorted_MM_data = np.sort(MM_data)
sorted_Optimus_data = np.sort(Optimus_data)
sorted_Allox_data = np.sort(Allox_data)
# sorted_DREAM_data = np.sort(DREAM_data)

yvals = np.arange(len(sorted_FIFO_data))/float(len(sorted_FIFO_data)-1)
# xvals = [i for i in range (100)]
# plt.plot(xvals,yvals)
plt.plot(sorted_MM_data,yvals, 'darkorange', label = 'FIFO')
plt.plot(sorted_FIFO_data,yvals, 'green', label = 'MM')
# plt.plot(sorted_Optimus_data,yvals, 'blue', label = '$A_{\{Allox\}}$')
plt.plot(sorted_Allox_data,yvals, 'black', label = '$A_{\{Optimus\}}$')
# plt.plot(sorted_DREAM_data,yvals, 'red', label = 'DREAM')
plt.xticks(size=17)
plt.yticks(size=17)
plt.xlabel('JCT (Min)',fontsize=17)        
plt.ylabel('Fraction of Jobs',fontsize=17)
plt.ylim(0, 1)
plt.grid(c = 'silver', ls = '-.')
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'
# ax = plt.gca()
# ax.ticklabel_format(style='sci', scilimits=(0,2), axis='x',useMathText=True)
plt.legend(loc='lower right', scatterpoints=1,ncol = 2,prop = {'size':12})
plt.show()

### CDF 2

# FIFO_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_FIFO_random.txt')
# MM_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_MM_random.txt')
# Optimus_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_Optimus_random.txt')
# Allox_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_Allox_random.txt')
# DREAM_data = np.loadtxt('/Users/chenfahao/Desktop/论文/Multi-tasks/Code/Simulation/Fig/cdf_DREAM_random.txt')

# for i in range (len(FIFO_data)):
#     FIFO_data[i] = FIFO_data[i]*0.8/60
#     MM_data[i] = MM_data[i]*0.8/60
#     Optimus_data[i] = Optimus_data[i]*400/60
#     Allox_data[i] = Allox_data[i]*1.4/60
#     DREAM_data[i] = DREAM_data[i]*400/60
# sorted_FIFO_data = np.sort(FIFO_data)
# sorted_MM_data = np.sort(MM_data)
# sorted_Optimus_data = np.sort(Optimus_data)
# sorted_Allox_data = np.sort(Allox_data)
# sorted_DREAM_data = np.sort(DREAM_data)

# yvals = np.arange(len(sorted_FIFO_data))/float(len(sorted_FIFO_data)-1)
# # xvals = [i for i in range (100)]
# # plt.plot(xvals,yvals)
# plt.plot(sorted_MM_data,yvals, 'darkorange', label = 'FIFO')
# plt.plot(sorted_FIFO_data,yvals, 'green', label = 'MM')
# plt.plot(sorted_Optimus_data,yvals, 'blue', label = '$A_{\{Allox\}}$')
# plt.plot(sorted_Allox_data,yvals, 'black', label = '$A_{\{Optimus\}}$')
# plt.plot(sorted_DREAM_data,yvals, 'red', label = 'DREAM')
# plt.xticks(size=17)
# plt.yticks(size=17)
# plt.xlabel('JCT (Min)',fontsize=17)        
# plt.ylabel('Fraction of Jobs',fontsize=17)
# plt.ylim(0, 1)
# plt.grid(c = 'silver', ls = '-.')
# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
# # plt.rcParams['xtick.direction'] = 'in'
# # plt.rcParams['ytick.direction'] = 'in'
# # ax = plt.gca()
# # ax.ticklabel_format(style='sci', scilimits=(0,2), axis='x',useMathText=True)
# plt.legend(loc='lower right', scatterpoints=1,ncol = 2,prop = {'size':12})
# plt.show()