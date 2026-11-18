"""Reproduces the supplied WordBreak defect and the minimal DP repair."""
def supplied_faulty(text, dictionary):
    n=len(text); dp=[False]*(n+1); dp[0]=True
    for i in range(1,n+1):
        for j in range(i):
            if text[j:i] in dictionary:
                dp[i]=True; break
    return dp[n],dp

def corrected(text, dictionary):
    n=len(text); dp=[False]*(n+1); dp[0]=True
    for i in range(1,n+1):
        for j in range(i):
            if dp[j] and text[j:i] in dictionary:
                dp[i]=True; break
    return dp[n],dp

def main():
    text="ab"; words={"b"}
    bad,bad_states=supplied_faulty(text,words); good,states=corrected(text,words)
    print("CO4A Task 4: WordBreak defect")
    print(f"Failing input: text={text!r}, dictionary={sorted(words)}")
    print("Faulty states:",bad_states,"result:",bad)
    print("Corrected states:",states,"result:",good)
    reg=corrected("cat",{"cat"})
    print("Regression cat/{cat}:",reg)
    assert bad is True and good is False and reg[0] is True
    assert corrected("apple",{"app","le"})[0] is True
    print("Checks: passed (counterexample, regression, valid multiword split)")

if __name__ == "__main__": main()
