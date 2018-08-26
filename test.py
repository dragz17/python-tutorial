def count(n):
    # Your code here to count the units of time
    # it takes to execute clique
    timer = 2
    for j in range(n):
        timer = timer + 1
        for i in range(j):
            timer = timer + 1
    return timer

def clique(n):
    print "in a clique..."
    for j in range(n):
        for i in range(j):
            print i, "is friends with", j

print(count(6))