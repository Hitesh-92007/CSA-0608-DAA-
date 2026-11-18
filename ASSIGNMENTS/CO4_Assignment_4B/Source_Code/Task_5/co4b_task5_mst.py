"""Kruskal, Prim and Boruvka with edge traces and tied-weight experiment."""
class DSU:
    def __init__(self,vs):self.p={v:v for v in vs};self.rank={v:0 for v in vs}
    def find(self,x):
        if self.p[x]!=x:self.p[x]=self.find(self.p[x])
        return self.p[x]
    def union(self,a,b):
        a=self.find(a);b=self.find(b)
        if a==b:return False
        if self.rank[a]<self.rank[b]:a,b=b,a
        self.p[b]=a
        if self.rank[a]==self.rank[b]:self.rank[a]+=1
        return True
V=list('ABCDEFGH')
EDGES=[('A','B',4),('A','C',3),('B','C',1),('B','D',2),('C','D',4),('C','E',6),('D','E',3),('D','F',5),('E','F',2),('E','G',4),('F','G',1),('G','H',2),('F','H',6)]
def kruskal(vs,edges):
    d=DSU(vs);out=[];trace=[]
    for e in sorted(edges,key=lambda x:(x[2],x[0],x[1])):
        take=d.union(e[0],e[1]);trace.append((e,take))
        if take:out.append(e)
        if len(out)==len(vs)-1:break
    if len(out)!=len(vs)-1:raise ValueError('Graph is disconnected')
    return out,sum(e[2] for e in out),trace
def prim(vs,edges,start='A'):
    used={start};out=[];trace=[]
    while len(used)<len(vs):
        cand=[e for e in edges if (e[0] in used)^(e[1] in used)]
        if not cand:raise ValueError('Graph is disconnected')
        # Deterministic tie rule: for equal weights prefer the lexicographically later endpoints.
        e=min(cand,key=lambda x:(x[2],tuple(-ord(ch) for ch in x[0]+x[1])));out.append(e);trace.append((e,set(used)))
        used.update((e[0],e[1]))
    return out,sum(e[2] for e in out),trace
def boruvka(vs,edges):
    d=DSU(vs);out=[];trace=[]
    while len({d.find(v) for v in vs})>1:
        cheapest={}
        for e in edges:
            a,b,w=e;ra,rb=d.find(a),d.find(b)
            if ra==rb:continue
            for root in (ra,rb):
                if root not in cheapest or (w,a,b)<(cheapest[root][2],cheapest[root][0],cheapest[root][1]):cheapest[root]=e
        chosen=list(dict.fromkeys(cheapest.values()))
        if not chosen:raise ValueError('Graph is disconnected')
        for e in chosen:
            joined=d.union(e[0],e[1]);trace.append((e,joined))
            if joined:out.append(e)
    return out,sum(e[2] for e in out),trace
def main():
    print('CO4B Task 5: MST algorithms')
    for name,fn in [('Kruskal',kruskal),('Prim',prim),('Boruvka',boruvka)]:
        out,cost,trace=fn(V,EDGES);print(name,'trace:',[(e,ok) for e,ok in trace]);print(name,'MST:',out,'cost:',cost)
        assert len(out)==len(V)-1
    tied=[(a,b,(3 if (a,b)==('A','B') else w)) for a,b,w in EDGES]
    k=kruskal(V,tied);p=prim(V,tied);b=boruvka(V,tied)
    print('Equal-weight change A-B: edge sets:',k[0],p[0],b[0])
    print('Equal-weight change costs:',k[1],p[1],b[1])
    assert k[1]==p[1]==b[1] and set(k[0])!=set(p[0])
    print('Disconnected-graph boundary:')
    for name,fn in [('Kruskal',kruskal),('Prim',prim),('Boruvka',boruvka)]:
        try:fn(V,[e for e in EDGES if e[0]!='G' and e[1]!='G'])
        except ValueError as exc:print(name,':',exc)
        else:raise AssertionError(name+' should reject a disconnected graph')
    print('Checks: passed (connected graph, all three costs, tied MST test)')
if __name__=='__main__':main()
