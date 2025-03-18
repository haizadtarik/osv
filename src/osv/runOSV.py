#############################################################################
"""
Demo of optimal surface voting for automatic fault interpretation
Author: Xinming Wu, University of Texas at Austin
Version: 2018.05.12
"""

from utils import * 
setupForSubset("unet")
s1,s2,s3 = getSamplings()
n1,n2,n3 = s1.count,s2.count,s3.count
f1,f2,f3 = s1.getFirst(),s2.getFirst(),s3.getFirst()
d1,d2,d3 = s1.getDelta(),s2.getDelta(),s3.getDelta()
#############################################################################
gxfile = "xs" # input seismic image
gxsfile = "xss" # smoothed seismic image
epfile = "ep"  # planarity
p2file = "p2"  # inline slopes
p3file = "p3"  # crossline slopes
effile = "ef"  # 1-planarity
fefile = "fe"  
flfile = "fl"  # fault likelihood
fpfile = "fp"  # fault strike;
ftfile = "ft"  # fault dip;
fvfile = "fv"  # voting score map;
vpfile = "vp"  # voting strike;
vtfile = "vt"  # voting dip;
fetfile = "fet" 
fptfile = "fpt" # fault strike thinned
fttfile = "ftt" # fault dip thinned
fskfile = "skin" # fault skins/surfaces
fslfile = "fsl" # fault skins/surfaces with fault slips
ft1file = "ft1"
ft2file = "ft2"
ft3file = "ft3"
gwfile = "gw"

plotOnly = False
# These parameters control the scan over fault strikes and dips.
# See the class FaultScanner for more information.
minTheta,maxTheta = 65,80
minPhi,maxPhi = 0,360
sigmaPhi,sigmaTheta=8,8


def main(args):
  goPlanar()
  goFaultOrientScan()
  goSurfaceVoting()
  goFaultSurfaces()   

# computes seismic planarity as an input fault attribute
def goPlanar():
  print "compute seismic planarity..."
  gx = readImage3DL(gxfile)
  if not plotOnly:
    lof = LocalOrientFilter(2,1,1)
    u1 = zerofloat(n1,n2,n3)
    u2 = zerofloat(n1,n2,n3)
    u3 = zerofloat(n1,n2,n3)
    ep = zerofloat(n1,n2,n3)
    lof.applyForNormalPlanar(gx,u1,u2,u3,ep)
    mask = ZeroMask(gx)
    mask.apply(1,ep)
    print min(ep)
    print max(ep)
    writeImage(epfile,ep)
  else:
    ep = readImage3D(epfile) # computed planarity

# approximately estimates fault orientations
def goFaultOrientScan():
  print "scan for approximate fault orientations..."
  gx = readImage3DL(gxfile) # seismic
  ep = readImage3D(epfile) # computed planarity
  fos = FaultOrientScanner3(sigmaPhi,sigmaTheta)
  if not plotOnly:
    fe,fp,ft = fos.scan(minPhi,maxPhi,minTheta,maxTheta,ep)
    fet,fpt,ftt=fos.thin([fe,fp,ft])
    writeImage(fefile,fe)
    writeImage(fetfile,fet)
    writeImage(fptfile,fpt)
    writeImage(fttfile,ftt)
  else:
    fe = readImage3D(fefile)
    fp = readImage3D(fpfile)
  print min(fe) 
  print max(fe) 
  ep = sub(1,pow(ep,8))

# computes voting surfaces and a final voting score map
def goSurfaceVoting():
  print "optimal surface voting..."
  gx = readImage3DL(gxfile)
  gx = gain(gx)
  osv = OptimalSurfaceVoter(10,20,30)
  if not plotOnly:
    fet = readImage3D(fetfile)
    fpt = readImage3D(fptfile)
    ftt = readImage3D(fttfile)
    osv.setStrainMax(0.25,0.25)
    osv.setSurfaceSmoothing(2,2)
    fv,vp,vt = osv.applyVoting(4,0.3,fet,fpt,ftt)
    writeImage("vp",vp)
    writeImage("vt",vt)
    writeImage(fvfile,fv)
  else:
    fv = readImage3D(fvfile)
    vp = readImage3D(vpfile)
    vt = readImage3D(vtfile)
  ep = readImage3DL(epfile)
  ep = sub(1,pow(ep,8))

# construct fault surfaces
def goFaultSurfaces():
  print "construct fault surfaces..."
  gx = readImage3DL(gxfile)
  gx = gain(gx)
  if not plotOnly:
    osv = OptimalSurfaceVoter(10,20,30)
    fv = readImage3D(fvfile)
    vp = readImage3D(vpfile)
    vt = readImage3D(vtfile)
    u1 = zerofloat(n1,n2,n3)
    u2 = zerofloat(n1,n2,n3)
    u3 = zerofloat(n1,n2,n3)
    ep = zerofloat(n1,n2,n3)
    lof = LocalOrientFilter(4,2,2)
    lof.applyForNormalPlanar(fv,u1,u2,u3,ep)
    ft,pt,tt = osv.thin([fv,vp,vt])
    writeImage("fvt",ft)
    fsk = FaultSkinner()
    fsk.setGrowing(10,0.3)
    seeds = fsk.findSeeds(10,0.8,ep,ft,pt,tt)
    skins = fsk.findSkins(0.65,200,seeds,fv,vp,vt)
    sks = []
    for skin in skins:
      skin.smooth(5)
      if(skin.getX1max()>80):
        sks.append(skin)
    removeAllSkinFiles(fskfile)
    writeSkins(fskfile,sks)
  else:
    fv = readImage3D(fvfile)
    ft = readImage3D("fvt")
    sks = readSkins(fskfile)
  for skin in sks:
    skin.updateStrike()


def goSmooth():
  print "goSmooth ..."
  flstop = 0.1
  fsigma = 8.0
  gx = readImage3D(gxfile)
  skins = readSkins(fskfile)
  flt = FaultSkin.getFl(n1,n2,n3,skins)
  p2,p3,ep = FaultScanner.slopes(8.0,2.0,2.0,5.0,gx)
  gxs = FaultScanner.smooth(flstop,fsigma,p2,p3,flt,gx)
  writeImage(p2file,p2)
  writeImage(p3file,p3)
  writeImage(gxsfile,gxs)

def gain(x):
  g = mul(x,x) 
  ref = RecursiveExponentialFilter(10.0)
  ref.apply1(g,g)
  y = zerofloat(n1,n2,n3)
  div(x,sqrt(g),y)
  return y

def smooth(sig,u):
  v = copy(u)
  rgf = RecursiveGaussianFilterP(sig)
  rgf.apply0(u,v)
  return v

def smooth2(sig1,sig2,u):
  v = copy(u)
  rgf1 = RecursiveGaussianFilterP(sig1)
  rgf2 = RecursiveGaussianFilterP(sig2)
  rgf1.apply0X(u,v)
  rgf2.applyX0(v,v)
  return v


def normalize(e):
  emin = min(e)
  emax = max(e)
  return mul(sub(e,emin),1.0/(emax-emin))


# Run the function main on the Swing thread
import sys
class _RunMain(Runnable):
  def __init__(self,main):
    self.main = main
  def run(self):
    self.main(sys.argv)
def run(main):
  SwingUtilities.invokeLater(_RunMain(main)) 
run(main)
