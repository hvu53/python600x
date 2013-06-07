def isPalindrome(s):
    def toChars(s):
        s = s.lower()
        ans =""
        for i in s:
            if i in "abcdefghijklmnopqrstuvwxyz":
                ans = ans+ i
            return ans

    def isPal(s):
        if len(s) <=1:
            return True
        else:
            return s[0] == s[-1] and isPal(s[1:-1])
    return isPal(toChars(s))
