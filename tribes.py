#Recover every native tribe (from slot #0) that's possible to place w/o conflicts
#At slot #1, saving the result at slot #2.  

# {"Dirty" implementation, w/o statistics correction for Indian Adviser}.

#Slot w/native tribes
SLOT_ELDER  =	0
#Slot w/current status
SLOT_LATER  =	1
#Slot to save result
SLOT_RESULT =	2

def cut(x,size):	
	result=x[:size]
	del x[:size]
	return result

class Save():
	def __init__(self, num):
		self.Id=num
		self.Name=''.join(("colony0",str(num),".sav"))
		with open(self.Name,"rb") as f:
			x=[int(i) for i in f.read()]
		Tribes, Units, Colonies = [int(x[0x2a+i]) for i in range(0,6,2)]
		self.Intro=cut(x,0x186)
		self.Tribe, self.Unit, self.Colony, self.Nation, self.Maps = [], [], [], [], []
		for i in range(Colonies):
			self.Colony+=[cut(x,202)]
		for i in range(Units):
			self.Unit+=[cut(x,28)]
		for i in range(4):
			self.Nation+=[cut(x,316)]
		for i in range(Tribes):
			self.Tribe+=[cut(x,18)]
		self.Middle=cut(x,1351)
		for i in range(4):
			self.Maps+=[cut(x,4176)]
		self.Final=x
		
	def drop(self, num):
		x=[]
		x.extend(self.Intro)
		for i in self.Colony:
			x.extend(i)
		for i in self.Unit:
			x.extend(i)
		for i in self.Nation:
			x.extend(i)
		for i in self.Tribe:
			x.extend(i)
		x.extend(self.Middle)
		for i in self.Maps:
			x.extend(i)
		x.extend(self.Final)
		y=[len(self.Colony), len(self.Unit), len(self.Tribe)]
		for i in range(0,6,2):
			x[0x2a+i]=y.pop()
		with open(''.join(("colony0",str(num),".sav")), "wb") as f:
			f.write(bytes(x))

	@staticmethod
	def map(x, y):
		# 0,0 - 57,71 [58,72] -> 1,1 - 56,70
		return y*58+x
	
d0=Save(SLOT_LATER)
d1=Save(SLOT_ELDER)

a=set()
for i in d0.Colony:
	a.add((i[0],i[1]))
for i in d0.Unit:
	a.add((i[0],i[1]))
for i in d0.Tribe:
	a.add((i[0],i[1]))

for i in d1.Tribe:
	chk=(i[0],i[1])
	if not chk in a:
		z=Save.map(i[0],i[1])
		d0.Tribe+=[i]
		for j in range(4):
			d0.Maps[j][z]=d1.Maps[j][z]

#d0.Middle=d1.Middle  -- Should work with this part to correct statistics for Indian Adviser.

d0.drop(SLOT_RESULT)
