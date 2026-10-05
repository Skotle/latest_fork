"""Small lossless NBT reader/writer; numeric arrays stay as raw bytes."""
import struct

class Tag:
    def __init__(self, kind, value): self.kind, self.value = kind, value

def read(data):
    pos = 0
    def take(n):
        nonlocal pos
        b = data[pos:pos+n]; pos += n; return b
    def number(fmt): return struct.unpack(fmt, take(struct.calcsize(fmt)))[0]
    def string(): return take(number('>H')).decode('utf-8', errors='surrogateescape')
    def payload(k):
        if k in (1,2,3,4,5,6): return number({1:'>b',2:'>h',3:'>i',4:'>q',5:'>f',6:'>d'}[k])
        if k in (7,11,12):
            n=number('>i'); return (n,take(n*{7:1,11:4,12:8}[k]))
        if k==8: return string()
        if k==9:
            subtype=number('>B'); n=number('>i'); return (subtype,[payload(subtype) for _ in range(n)])
        if k==10:
            d={}
            while True:
                t=number('>B')
                if t==0: return d
                name=string(); d[name]=Tag(t,payload(t))
        raise ValueError(k)
    k=number('>B'); name=string(); root=Tag(k,payload(k)); assert pos==len(data)
    return name,root

def write(name,root):
    out=bytearray()
    def num(fmt,v): out.extend(struct.pack(fmt,v))
    def string(s):
        b=s.encode('utf-8',errors='surrogateescape');num('>H',len(b));out.extend(b)
    def payload(k,v):
        if k in (1,2,3,4,5,6): num({1:'>b',2:'>h',3:'>i',4:'>q',5:'>f',6:'>d'}[k],v)
        elif k in (7,11,12): num('>i',v[0]);out.extend(v[1])
        elif k==8:string(v)
        elif k==9:
            num('>B',v[0]);num('>i',len(v[1]))
            for item in v[1]:payload(v[0],item)
        elif k==10:
            for key,t in v.items():num('>B',t.kind);string(key);payload(t.kind,t.value)
            num('>B',0)
        else:raise ValueError(k)
    num('>B',root.kind);string(name);payload(root.kind,root.value);return bytes(out)
