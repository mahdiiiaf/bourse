from down_data import down_data
import pickle
import sys


num=int(sys.argv[1])

symbol=pickle.load(open("symbol.pkl","rb"))
for i in range(2):
	down_data(comp=symbol["namad"][i],num=num)



