list=[1000,999,998,1200,1201,1202,1199,1503,1501,1505,1498]

list2 = []
list2.append(list[0])

for i in list:
	for j in list2:
		k = 0
		if i/j < 1.05 and j/i < 1.05:
			k += 1
	
		else:
			list2.append(i)
		print(i,j,k)