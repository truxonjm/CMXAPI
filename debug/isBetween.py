start = 1528917120000
end = 1528917300000
test = 1528917239643

def isBetween(start, end, test):
    inLeft = test > start
    inRight = test < end
    return inLeft and inRight

print(isBetween(start, end, test))