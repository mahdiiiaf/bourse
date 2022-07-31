from down_data import down_data
import pickle



symbol=pickle.load(open("symbol.pkl","rb"))
for i in range(1):
	down_data(comp=symbol["namad"][i])


