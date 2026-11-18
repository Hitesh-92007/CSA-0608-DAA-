"""Word-wrap DP with line reconstruction, state instrumentation, and width tests."""
def word_wrap(words,width):
    if width<=0: raise ValueError("Width must be positive")
    if any(len(w)>width for w in words): raise ValueError("A word exceeds the line width")
    n=len(words); dp=[float('inf')]*(n+1); nxt=[None]*(n+1); dp[0]=0; states=[]
    for end in range(1,n+1):
        chars=0
        for start in range(end-1,-1,-1):
            chars += len(words[start])
            used=chars+(end-start-1)
            if used>width: break
            slack=width-used
            penalty=0 if end==n else slack*slack
            cand=dp[start]+penalty
            states.append((start,end,used,slack,penalty,cand))
            if cand<dp[end]:dp[end]=cand;nxt[end]=start
    lines=[];end=n
    while end:
        start=nxt[end]
        if start is None: raise ValueError("No feasible layout")
        text=' '.join(words[start:end]); used=len(text); slack=width-used
        penalty=0 if end==n else slack*slack
        lines.append((text,used,slack,penalty));end=start
    return dp[n],list(reversed(lines)),dp,states
def main():
    words="Dynamic programming helps arrange words neatly in a document layout".split()
    print("CO4B Task 1: Word wrap; non-final penalty = unused^2")
    for width in (16,20,24):
        cost,lines,dp,states=word_wrap(words,width)
        print(f"Width {width}: cost={cost}, DP={dp}")
        for i,(line,used,slack,pen) in enumerate(lines,1):print(f"  line {i}: {line!r}; used={used}; unused={slack}; penalty={pen}")
    try:word_wrap(["toolong"],3)
    except ValueError as e:print("Boundary case (word wider than line):",e)
    else:raise AssertionError("boundary case should fail")
    print("Checks: passed (three widths, overlong word)")
if __name__=="__main__":main()
