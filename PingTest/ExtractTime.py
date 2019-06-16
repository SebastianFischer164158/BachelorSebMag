path = "/Users/Home/Desktop/BachelorSebMag-master 2/PingTest/ICMPAttack_pingtest.txt"
f = open(path, "r")
print(f.readline())

xis = []
convertedInt = []

for x in f:
    thisX = x
    try:
        if thisX[51] != "=":
            print("time:", (thisX[51:56]))
            xis.append(thisX[51:56])

        else:
            print("time:", (thisX[52:57]))
            xis.append(thisX[52:57])
    except:
        print("time:", "0")
        xis.append('0')


print(xis)
