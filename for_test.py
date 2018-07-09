
prob = "ddd123"
tmpst = ''

for i in range(len(prob)):
    if(prob[i].isnumeric()):
        tmpst = tmpst+prob[i]


print(tmpst)
