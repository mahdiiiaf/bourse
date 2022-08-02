from down_data import down_data,closi
import time
import pickle
import sys
start=time.perf_counter()
if len(sys.argv)>=1:
	num=int(sys.argv[1])
else:
	num=50

symbol=pickle.load(open("symbol.pkl","rb"))
for i in symbol["namad"]:
	starti=time.perf_counter()
	print(i)
	down_data(comp=i,num=num)
	print(f"{i} done in {time.perf_counter()-starti}")

closi()


