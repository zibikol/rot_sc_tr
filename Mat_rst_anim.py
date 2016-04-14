#!/usr/bin/python
# coding=utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

if len(sys.argv)!=7 and len(sys.argv)!=8:
	print "\n Program tworzy animację obrotu, skalowania i translacji zbioru punktów na płaszczyznie.\n Użycie:\n %s <nazwa_pliku_z_danymi> <trans_x> <trans_y> <scala_x> <scala_y> <rotacja> [ślad]\n" % (sys.argv[0])
        print " Wersja 2016.04.10, (ZK)\n"
	exit()

fname=sys.argv[1]
tx=float(sys.argv[2])
ty=float(sys.argv[3])
sx=float(sys.argv[4])
sy=float(sys.argv[5])
r=np.deg2rad(float(sys.argv[6]))

dane=open(fname,'r')
a=np.loadtxt(dane,unpack="True")
dane.close()
lxy=4
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-lxy, lxy), ylim=(-lxy, lxy))
bx = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-lxy, lxy), ylim=(-lxy, lxy))
ax.grid()
#ax.set_axis_off()
#bx.set_axis_off()
size_a=np.size(a[0])
a=np.matrix(a).copy()
pxy=np.resize(a,(3,size_a))
pxy[2,0:]=1
nc=np.size(pxy[0])
#line1, = ax.plot(pxy[0,:nc], pxy[1,:nc],'ob',markersize=1)
line1, = ax.plot(pxy[0,:nc], pxy[1,:nc],'ob',markersize=0.7)
line2, = bx.plot(pxy[0,:nc], pxy[1,:nc],'or',markersize=3,linestyle='-',linewidth=0.5)
start, end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(start, end+1, 1))
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end+1, 1))
nstep=100
d1=[]
d2=[]

def init():
    global pxy, nc
    line1.set_data(pxy[0,:nc], pxy[1,:nc])
    line2.set_data(pxy[0,:nc], pxy[1,:nc])
    return line1, line2, 

def mmatrix(tx,ty,sx,sy,r,pxy,nc):
    r3=[0.0,0.0,1.0]
    o=np.matrix([[np.cos(r), -np.sin(r), 0],[np.sin(r), np.cos(r), 0],r3])
    t=np.matrix([[0.0, 0.0, tx],[0.0, 0.0, ty],r3])
    s=np.matrix([[sx, 0.0, 0.0],[0.0, sy, 0.0],r3])
    c=(o*s+t)*pxy
    if len(sys.argv)==8:
       d1.extend(c[0,:nc])
       d2.extend(c[1,:nc])
    return c[0,:nc],c[1,:nc]

def iter_par(i, dp, vp, pp):
    if abs(i*dp+pp) <= abs(vp): 
       ip = i*dp + pp
    else:
       ip = vp
    return ip
    
def animatrix(i):
    global tx,ty,sx,sy,r,pxy,nc,nstep
    dtx=float(tx)/nstep
    dty=float(ty)/nstep
    dsx=float(sx-1.0)/nstep
    dsy=float(sy-1.0)/nstep
    dr=float(r)/nstep  
    itx=iter_par(i,dtx,tx,0)
    ity=iter_par(i,dty,ty,0)
    isx=iter_par(i,dsx,sx,1)
    isy=iter_par(i,dsy,sy,1)
    ir=iter_par(i,dr,r,0)
    c1, c2 = mmatrix(itx,ity,isx,isy,ir,pxy,nc)
    if len(sys.argv)==8:
       line1.set_data(d1, d2)
    line2.set_data(c1, c2)
    return line1, line2, 

anim = animation.FuncAnimation(fig, animatrix, init_func=init, interval=60, frames=nstep+5, blit=True, repeat=False)
plt.show()
#anim.save('RST_anim.mp4', fps=25, extra_args=['-vcodec', 'libx264'])
