"""8-node directed routing: Dijkstra, Bellman-Ford, Floyd, Warshall."""
INF=float('inf'); V=list("ABCDEFGH")
BASE=[('A','B',2),('A','C',1),('C','E',5),('B','E',20),('B','D',4),('C','D',20),('D','F',3),('E','F',1),('F','G',2),('G','H',2),('C','F',15),('D','G',7)]
def dijkstra(vs,edges,s,allow_negative_demo=False):
    if any(w<0 for _,_,w in edges) and not allow_negative_demo:raise ValueError('Dijkstra requires non-negative weights')
    d={x:INF for x in vs};p={x:None for x in vs};d[s]=0;done=[];order=[]
    while len(done)<len(vs):
        cand=[x for x in vs if x not in done]
        u=min(cand,key=lambda x:d[x])
        if d[u]==INF:break
        done.append(u);order.append(u)
        for a,b,w in edges:
            if a==u and d[u]+w<d[b]:d[b]=d[u]+w;p[b]=u
    return d,p,order
def bellman(vs,edges,s):
    d={x:INF for x in vs};p={x:None for x in vs};d[s]=0;rounds=[]
    for k in range(len(vs)-1):
        changed=False
        for a,b,w in edges:
            if d[a]!=INF and d[a]+w<d[b]:d[b]=d[a]+w;p[b]=a;changed=True
        rounds.append((k+1,dict(d)))
        if not changed:break
    neg=any(d[a]!=INF and d[a]+w<d[b] for a,b,w in edges)
    return d,p,rounds,neg
def floyd(vs,edges):
    d={a:{b:(0 if a==b else INF) for b in vs} for a in vs}
    for a,b,w in edges:d[a][b]=min(d[a][b],w)
    for k in vs:
        for i in vs:
            for j in vs:
                if d[i][k]<INF and d[k][j]<INF:d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return d
def warshall(vs,edges):
    r={a:{b:(a==b) for b in vs} for a in vs}
    for a,b,_ in edges:r[a][b]=True
    for k in vs:
        for i in vs:
            for j in vs:r[i][j]=r[i][j] or (r[i][k] and r[k][j])
    return r
def path(prev,end):
    out=[];x=end
    while x is not None:out.append(x);x=prev[x]
    return list(reversed(out))
def main():
    d,p,order=dijkstra(V,BASE,'A')
    print('CO4B Task 3: baseline routes from A')
    print('finalisation order:',order)
    for x in V:print(x,d[x],path(p,x))
    neg=BASE+[('E','B',-10)]
    bd,bp,_,cycle=bellman(V,neg,'A')
    print('Prediction: Dijkstra is not valid after E->B=-10; E is settled after B in the baseline.')
    bad_d,_,bad_order=dijkstra(V,neg,'A',allow_negative_demo=True)
    print('Dijkstra diagnostic only (not a valid result):',bad_d,'order:',bad_order)
    print('Modified Bellman-Ford distances:',bd,'negative cycle:',cycle)
    cyc=neg+[('F','C',-30)]; cd,_,_,hascycle=bellman(V,cyc,'A')
    print('Reachable negative-cycle test:',hascycle)
    fw=floyd(V,BASE);wr=warshall(V,BASE)
    print('Floyd distance matrix (A-H):')
    for a in V:print(a,[fw[a][b] if fw[a][b]<INF else 'inf' for b in V])
    print('Warshall reachability (1/0):')
    for a in V:print(a,[int(wr[a][b]) for b in V])
    assert d['B']==2 and bad_d['D']==6 and bd['B']==-4 and bd['D']==0 and not cycle and hascycle
    assert fw['A']['H']==11 and wr['A']['H']
    print('Checks: passed (baseline, negative-edge failure, negative cycle, APSP/reachability)')
if __name__=='__main__':main()
