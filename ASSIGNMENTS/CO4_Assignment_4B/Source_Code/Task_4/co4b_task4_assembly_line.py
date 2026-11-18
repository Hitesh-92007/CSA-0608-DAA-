"""Two-line assembly scheduling with predecessor decisions and route recovery."""
def assembly(a1,a2,t12,t21,e1,e2,x1,x2):
    n=len(a1)
    if not n or len(a2)!=n or len(t12)!=n-1 or len(t21)!=n-1:raise ValueError('Inconsistent station/transfer arrays')
    f1=[0]*n;f2=[0]*n;prev1=[0]*n;prev2=[0]*n;trace=[]
    f1[0]=e1+a1[0];f2[0]=e2+a2[0]
    for j in range(1,n):
        s1=f1[j-1]+a1[j];tr1=f2[j-1]+t21[j-1]+a1[j]
        s2=f2[j-1]+a2[j];tr2=f1[j-1]+t12[j-1]+a2[j]
        if s1<=tr1:f1[j]=s1;prev1[j]=1;d1='stay L1'
        else:f1[j]=tr1;prev1[j]=2;d1='transfer L2->L1'
        if s2<=tr2:f2[j]=s2;prev2[j]=2;d2='stay L2'
        else:f2[j]=tr2;prev2[j]=1;d2='transfer L1->L2'
        trace.append((j+1,s1,tr1,d1,s2,tr2,d2,f1[j],f2[j]))
    line=1 if f1[-1]+x1<=f2[-1]+x2 else 2
    total=min(f1[-1]+x1,f2[-1]+x2);route=[0]*n;cur=line
    for j in range(n-1,-1,-1):route[j]=cur;cur=prev1[j] if cur==1 else prev2[j]
    transfers=[i+1 for i in range(1,n) if route[i]!=route[i-1]]
    return total,route,transfers,trace,(f1,f2)
def main():
    a1=[7,9,3,4,8,4];a2=[8,5,6,4,5,7];t12=[2,3,1,3,4];t21=[2,1,2,2,1]
    args=(a1,a2,t12,t21,2,4,3,2)
    best,route,changes,trace,dp=assembly(*args)
    print('CO4B Task 4: baseline assembly schedule')
    for r in trace:print('station',r[0],'L1 stay/transfer',r[1:4],'L2 stay/transfer',r[4:7],'DP',r[7:9])
    print('route:',route,'transfers before stations:',changes,'minimum:',best)
    t12_hi=t12.copy();t12_hi[2]+=15
    print('Prediction: raising L1->L2 transfer before station 4 from 1 to 16 should avoid that transfer, change the route, and raise the minimum time.')
    print('High-transfer result:',assembly(a1,a2,t12_hi,t21,2,4,3,2)[:3])
    a1_slow=a1.copy();a1_slow[2]+=20
    print('Slow L1 station 3 result:',assembly(a1_slow,a2,t12,t21,2,4,3,2)[:3])
    assert best==38 and route==[1,2,1,2,2,1]
    print('Checks: passed (baseline, modified transfer, station disruption)')
if __name__=='__main__':main()
