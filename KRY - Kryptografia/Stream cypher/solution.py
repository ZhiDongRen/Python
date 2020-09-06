import sys
path=sys.argv[1]

#nacitanie suborov
b = bytearray(open(path+"bis.txt", 'rb').read())
enc = bytearray(open(path+"bis.txt.enc", 'rb').read())

#vytvorenie keystreamu pomocou XOR
keystream=bytearray(len(b))
for i in range(len(b)):
    b[i]^=enc[i]
    keystream[i]=b[i]

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B

#myInt-premenna uchovava keystream
myInt=int.from_bytes(keystream[:N_B], byteorder='little')

#vytvorenie povodneho sifrovacieho suboru
result=[]
super = bytearray(open(path+"super_cipher.py.enc", 'rb').read())
for i in range(len(b)):
    b[i]^=super[i]
#open("result.txt", 'wb').write(b)

#podla bitu zisti kandidatov na predchodcu
def getCandidates(x):
    if(x==1): return [1,2,4,6]
    else: return [0,3,5,7]

#vrati posledne dva bity
def lastTwo(x):
    lsb= (x & 1)
    msb= (x>>1)&1
    return (1 * lsb + 2 * msb)

#vrati prve dva bity
def firstTwo(x, i):
    lsb = (x>>i)&1
    msb = (x>>i+1)&1
    return (1*lsb+2*msb)

#zisti ci je mozne spojit kandidatov na prechodcov
def canMerge(x,y,i):
    last=lastTwo(x)
    first=firstTwo(y,i)
    if(first==last):
        return True
    else:
        return False

#nastavenie bitu na pozicii index v premennej v, na hodnotu x
def set_bit(v, index, x):
  mask = 1 << index
  v &= ~mask
  if x:
    v |= mask
  return v

#zistenie hodnoty bitu na pozicii idx
def get_bit(byteval,idx):
    return ((byteval&(1<<idx))!=0);

#spojenie dvoch bitovych postupnosti(prve dva bity a posledne dva sa prelinaju)
def mergeTwo(x,y,index):
    bit=get_bit(x,2)
    y=set_bit(y,index+2,bit)
    return y

#spojenie vsetkych kandidatov na predchodcov
def mergeCandidates(initCandidates,candidates,index):
    new=[]
    for i in range(len(initCandidates)):
        for j in range(len(candidates)):
            if(canMerge(candidates[j],initCandidates[i],index)):
                new.append(mergeTwo(candidates[j],initCandidates[i],index))
    return new

#povodny step
def step(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= SUB[(x >> i) & 7] << i
  return y

#inverzna funkcia ku hodnote y v povodnom stepe
def invY(x):
    temp=x
    initCandidates=getCandidates(x&1)

    for i in range(1,N):
        bit=(x>>i)&1
        candidates=getCandidates(bit)
        initCandidates=mergeCandidates(initCandidates,candidates,i)

    for i in range(len(initCandidates)):
        initCandidates[i]=invX(initCandidates[i])

    for i in range(len(initCandidates)):
        if(temp==step(initCandidates[i])):
            return initCandidates[i]

#inverzna funkcia pre hodnotu x v povodnom stepe
def invX(x):
    lenght=x.bit_length()
    if(get_bit(x,1)):
        x=set_bit(x,lenght-1,False)
        x=x>>1
    else:
        x=x>>1
    return x

#inverzna funkcia k step
def invStep(x):
    x=invY(x)
    return x

#opakujeme inverziu tolko krat, kolko bola povodne prevedena
for i in range(N//2):
  myInt = invStep(myInt)

#ziskane tajomstvo
secret = myInt.to_bytes(N_B, 'little')
for i in range(29):
    print(chr(secret[i]),end='')
print("")
