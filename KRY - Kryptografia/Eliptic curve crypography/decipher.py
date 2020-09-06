#Eliptic curve cryptography key decipher
#Author: Michael Halinar
#usage: make decipher publicKey="(0x477...3e, 0xaa0...dc)"

import sys
#public key
publicX=0x52910a011565810be90d03a299cb55851bab33236b7459b21db82b9f5c1874fe
publicY=0xe3d03339f660528d511c2b1865bcdfd105490ffc4c597233dd2b2504ca42a562

#key parameters
a=-0x3
p=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff

#parse args
args = (sys.argv[1].split(" "))
argX = args[0]
argY = args[1]
baseX = int(argX[1:len(argX) - 1], 16)
baseY = int(argY[:len(argY) - 1], 16)

#compute inversion
def inv(x):
    return pow(x, p-2, p)

#point doubling
def pointDoubling(xP,yP):
    s = ((3 * (xP ** 2) + a) * (inv(2 * yP)))%p
    xR = (s ** 2 - xP - xP)%p
    yR = (s * (xP - xR) - yP)%p
    return xR,yR

#point addtion
def pointAddition(xP,yP,xQ,yQ):
    s = ((yQ - yP) * (inv(xQ - xP)))%p
    xR =(s**2 - xP - xQ)%p
    yR = (s*(xP - xR) - yP)%p
    return xR,yR

#find key
key=2
X,Y=pointDoubling(baseX,baseY)
while(X!=publicX and Y!=publicY):
    X,Y = pointAddition(X,Y,baseX,baseY)
    key+=1

#print computed key
print(key)