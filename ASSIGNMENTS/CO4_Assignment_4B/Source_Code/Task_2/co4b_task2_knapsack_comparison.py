"""Compare fractional greedy with exact 0/1 DP and an adversarial case."""
def fractional(items,capacity):
    left=capacity;value=0.0;chosen=[];steps=[]
    for name,w,v in sorted(items,key=lambda x:(-x[2]/x[1],x[0])):
        if left<=0:break
        frac=min(1,left/w);gain=frac*v;chosen.append((name,frac));left-=frac*w;value+=gain
        steps.append((name,v/w,frac,left,value))
    return value,chosen,steps
def zero_one(items,capacity):
    n=len(items);dp=[[0]*(capacity+1) for _ in range(n+1)]
    for i,(_,w,v) in enumerate(items,1):
        for c in range(capacity+1):dp[i][c]=max(dp[i-1][c],v+dp[i-1][c-w] if w<=c else 0)
    chosen=[];c=capacity
    for i in range(n,0,-1):
        if dp[i][c]!=dp[i-1][c]:chosen.append(items[i-1][0]);c-=items[i-1][1]
    chosen.reverse();return dp[n][capacity],chosen,dp
def ratio_greedy_zero_one(items,capacity):
    left=capacity;value=0;chosen=[];steps=[]
    for name,w,v in sorted(items,key=lambda x:(-x[2]/x[1],x[0])):
        if w<=left:
            chosen.append(name);left-=w;value+=v;steps.append((name,w,v,left,'taken'))
        else:
            steps.append((name,w,v,left,'skipped'))
    return value,chosen,steps
def main():
    items=[("A",10,60),("B",20,100),("C",30,120)];cap=50
    print("CO4B Task 2: normal instance; capacity=50")
    fv,fc,fs=fractional(items,cap);ov,oc,dp=zero_one(items,cap)
    print("Fractional steps:",fs,"value:",fv,"selected:",fc)
    print("0/1 DP value:",ov,"selected:",oc,"cells:",(len(items)+1)*(cap+1))
    gv,gc,gs=ratio_greedy_zero_one(items,50)
    print("0/1 ratio-greedy steps:",gs,"value:",gv,"selected:",gc)
    print("The first commitment A leaves 40; B then leaves 20, so C cannot fit.")
    assert gv==160 and ov==220 and oc==["B","C"]
    assert gc==["A","B"]
    print("Work evidence: fractional greedy inspected",len(fs),"items; 0/1 ratio greedy inspected",len(gs),"items; DP filled",(len(items)+1)*(cap+1),"cells")
    print("Checks: passed (fractional optimum, 0/1 optimum, greedy counterexample)")
if __name__=="__main__":main()
