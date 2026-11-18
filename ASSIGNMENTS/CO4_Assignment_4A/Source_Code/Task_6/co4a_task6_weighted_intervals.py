"""Weighted interval scheduling by DP, sorted by finish time."""
from bisect import bisect_right
def weighted_schedule(jobs):
    jobs=sorted(jobs,key=lambda x:(x[2],x[1],x[0])); finishes=[j[2] for j in jobs]
    pred=[]
    for i,(_,start,finish,value) in enumerate(jobs): pred.append(bisect_right(finishes,start,0,i)-1)
    dp=[0]*(len(jobs)+1)
    for i,(_,s,f,v) in enumerate(jobs,1):dp[i]=max(dp[i-1],v+dp[pred[i-1]+1])
    chosen=[];i=len(jobs)
    while i:
        if jobs[i-1][3]+dp[pred[i-1]+1]>dp[i-1]:chosen.append(jobs[i-1][0]);i=pred[i-1]+1
        else:i-=1
    chosen.reverse()
    return dp[-1],chosen,jobs,pred,dp
def main():
    jobs=[("J1",1,3,20),("J2",2,5,50),("J3",4,6,30),("J4",6,8,40),("J5",5,9,60),("J6",8,10,30),("J7",9,11,50),("J8",11,13,40)]
    best,chosen,ordered,pred,dp=weighted_schedule(jobs)
    print("CO4A Task 6: Weighted interval scheduling")
    for i,j in enumerate(ordered,1):print(f"{j[0]} p={pred[i-1]} include={j[3]+dp[pred[i-1]+1]} exclude={dp[i-1]} DP={dp[i]}")
    print("Selected:",chosen,"total:",best)
    challenge=[("A",1,2,8),("B",2,3,8),("C",3,4,8),("X",1,4,20),("E",4,5,3)]
    v,c,*_=weighted_schedule(challenge);print("Challenge optimum:",c,v,"(highest single-value job X is not selected)")
    assert best==200 and chosen==["J2","J5","J7","J8"] and v==27
    assert weighted_schedule([])[0]==0
    print("Checks: passed (given data, adversarial case, empty input)")

if __name__ == "__main__": main()
