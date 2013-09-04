
#-*- encoding: utf-8 -*-
import numpy as np
import scipy as sp
import pylab as pl
from scipy.optimize import leastsq as lq
def generate_point(x,p1,p2,noise=True):       #产生点，可选是否加高斯噪声
    if noise is True:
        ynoise=np.cos(p1*np.pi*x)+p2        # 拟合余弦函数
        ynoise=[i+np.random.normal(0,0.1) for i in ynoise]
        return ynoise
    else:
        return np.cos(p1*np.pi*x)+p2
def error(p,y,x):
    return y-generate_point(x,p[0],p[1],False)
p=np.random.randn(2)
x=np.linspace(0,2,20)
y=generate_point(x,p[0],p[1])   #随即产生样本点
print "初始参数:",p
result=lq(error,p,args=(y,x))     #最小二拟合
print "拟合参数:",result[0]

x_result=np.linspace(0,2,1000)           #绘图点
y_result=generate_point(x_result,result[0][0],result[0][1],False)
y_result_src=generate_point(x_result,p[0],p[1],False) 
 
pl.plot(x,y,'bo',label='sample point')
pl.plot(x_result,y_result,label='fit model')
pl.plot(x_result,y_result_src,'r',label='src model')
pl.legend()
pl.show()
 