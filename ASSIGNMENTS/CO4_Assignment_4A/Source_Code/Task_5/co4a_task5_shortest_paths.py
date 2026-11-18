"""Dijkstra, Bellman-Ford, Floyd-Warshall for the supplied directed graph."""
INF=float("inf")
EDGES=[("A","B",4),("A","C",7),("B","C",2),("B","D",6),("C","D",1),("D","E",3),("C","E",8)]
VERTICES=list("ABCDE")
def dijkstra(vertices, edges, source):
    if any(w<0 for _,_,w in edges): raise ValueError("Dijkstra requires non-negative weights")
    dist={v:INF for v in vertices}; prev={v:None for v in vertices}; dist[source]=0; done=[]; trace=[]
    while len(done)<len(vertices):
        candidates=[v for v in vertices if v not in done]
        u=min(candidates,key=lambda v:dist[v])
        if dist[u]==INF: break
        done.append(u)
        for a,b,w in edges:
            if a==u and dist[u]+w<dist[b]: dist[b]=dist[u]+w; prev[b]=u
        trace.append((u,dict(dist)))
    return dist,prev,trace
def bellman_ford(vertices,edges,source):
    d={v:INF for v in vertices}; p={v:None for v in vertices}; d[source]=0; trace=[]
    for k in range(len(vertices)-1):
        changed=False
        for u,v,w in edges:
            if d[u]!=INF and d[u]+w<d[v]: d[v]=d[u]+w;p[v]=u;changed=True
        trace.append((k+1,dict(d)))
        if not changed: break
    cycle=any(d[u]!=INF and d[u]+w<d[v] for u,v,w in edges)
    return d,p,trace,cycle
def floyd_warshall(vertices,edges):
    d={u:{v:(0 if u==v else INF) for v in vertices} for u in vertices}
    for u,v,w in edges:d[u][v]=min(d[u][v],w)
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if d[i][k]!=INF and d[k][j]!=INF:d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return d
def path_to(prev,target):
    r=[]; cur=target
    while cur is not None:r.append(cur);cur=prev[cur]
    return list(reversed(r))
def main():
    d,p,t=dijkstra(VERTICES,EDGES,"A")
    print("CO4A Task 5: Dijkstra from A")
    for v in VERTICES:print(v,d[v],path_to(p,v))
    print("Finalisation:",[x[0] for x in t])
    neg=[(u,v,(-2 if (u,v)==("B","D") else w)) for u,v,w in EDGES]
    bd,bp,_,cycle=bellman_ford(VERTICES,neg,"A")
    print("Bellman-Ford with B->D=-2:",bd,"negative cycle:",cycle)
    matrix=floyd_warshall(VERTICES,EDGES)
    print("Floyd-Warshall rows:")
    for u in VERTICES:print(u,[matrix[u][v] if matrix[u][v]!=INF else "inf" for v in VERTICES])
    assert d["E"]==10 and bd["D"]==2 and not cycle
    cyc_edges=neg+[("E","B",-10)]
    cyc=bellman_ford(VERTICES,cyc_edges,"A")[3]
    print("Reachable negative cycle with E->B=-10:",cyc)
    # In this graph E->B=-10 creates a reachable negative cycle through B->C->D->E.
    assert cyc
    print("Checks: passed (given graph, negative edge, reachable negative cycle)")

if __name__ == "__main__": main()
