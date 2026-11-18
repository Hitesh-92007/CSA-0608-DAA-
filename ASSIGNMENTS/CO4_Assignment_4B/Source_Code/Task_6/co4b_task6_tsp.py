"""Held-Karp TSP DP, route reconstruction, exhaustive check, and state counts."""
from itertools import permutations
from time import perf_counter
def held_karp(cost,locations):
    m=len(locations);dp={};parent={};count=0
    for j in range(m):dp[(1<<j,j)]=cost[0][locations[j]];parent[(1<<j,j)]=None;count+=1
    for size in range(2,m+1):
        for subset in __import__('itertools').combinations(range(m),size):
            mask=sum(1<<x for x in subset)
            for j in subset:
                prev=mask^(1<<j);best=min((dp[(prev,k)]+cost[locations[k]][locations[j]],k) for k in subset if k!=j)
                dp[(mask,j)]=best[0];parent[(mask,j)]=best[1];count+=1
    full=(1<<m)-1;last=min(range(m),key=lambda j:dp[(full,j)]+cost[locations[j]][0])
    total=dp[(full,last)]+cost[locations[last]][0];route=[last];mask=full;j=last
    while parent[(mask,j)] is not None:
        k=parent[(mask,j)];mask^=1<<j;j=k;route.append(j)
    route=[0]+[locations[x] for x in reversed(route)]+[0]
    return total,route,count,dp
def exhaustive(cost,locations):
    best=float('inf');route=None
    for p in permutations(locations):
        r=(0,)+p+(0,);v=sum(cost[r[i]][r[i+1]] for i in range(len(r)-1))
        if v<best:best=v;route=r
    return best,route
def main():
    points=[(0,0),(2,3),(5,1),(6,5),(1,7),(8,2),(9,7),(3,9),(0,4)]
    c=[[abs(x1-x2)+abs(y1-y2) for x2,y2 in points] for x1,y1 in points]
    print('CO4B Task 6: Held-Karp TSP')
    value,route,count,dp=held_karp(c,list(range(1,9)))
    print('cost matrix (hub=0, locations=1..8; Manhattan cost):');[print(row) for row in c]
    print('route:',route,'minimum cost:',value,'states evaluated:',count)
    small=held_karp(c,list(range(1,5)))[:2];ref=exhaustive(c,list(range(1,5)))
    print('4-location DP:',small,'exhaustive:',ref,'match:',small[0]==ref[0])
    growth=[]
    for m in range(4,9):
        start=perf_counter();result=held_karp(c,list(range(1,m+1)));elapsed=perf_counter()-start
        growth.append((m,result[2],f'{elapsed:.6f}s'))
    print('Measured state growth (m, DP states, elapsed):',growth)
    assert count==8*(2**7) and small[0]==ref[0]
    print('Checks: passed (eight locations, exhaustive 4-location validation, state counts)')
if __name__=='__main__':main()
