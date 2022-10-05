import os.path

def taxpatch():
	with open(f"COLONIZE{os.path.sep}Viceroy.exe", "rb") as f:
		cnt = bytearray(f.read())
		untax = bytearray([0x7E, 0x19, 0x8A, 0x47, 0x01, 0x8B, 0xC8, 0x98, 0x2D])
		if untax in cnt:
			pos = cnt.index(untax)
			cnt[pos - 1] = cnt[pos + 9] = 0
			with open(f"COLONIZE{os.path.sep}Vicetax.exe", "wb") as f:
				f.write(cnt)
			print("Patched.")

def rndpatch():
	with open(f"COLONIZE{os.path.sep}Viceroy.exe", "rb") as f:
		cnt = bytearray(f.read())
		unrnd = bytearray([0xA3, 0xEE, 0x28, 0xC7, 0x06])
		tornd = bytearray([0x5D, 0xCB])
		if unrnd in cnt:
			pos = cnt.index(unrnd)
			cnt[pos : pos + 2] = tornd
			with open(f"COLONIZE{os.path.sep}Vicernd.exe", "wb") as f:
				f.write(cnt)
			print("Patched.")

#rndpatch(); exit() #-- not my idea; Randomizer for Colonization

#taxpatch(); exit() #-- my idea; No-Taxes Mode for Colonization

ABBR = ["in", "az", "ar", "ir", "ch", "ap", "si", "tu"]
BASE = 4

def new_tribe(x, y, nation, size):
	tribe = bytearray([x, y, nation, 0x00, size, 0xFF, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])	
	return tribe

def col2tribe(f):
	tribes, units, colonies = f.short(0x2A, 0x2E)
	
	offset = 0
	length = 0x186
	intro = f.raw[offset : offset + length]
	offset += length
	length = 202 * colonies
	colonies = f.raw[offset : offset + length]
	offset += length
	length = 28 * units
	units = f.raw[offset : offset + length]
	offset += length
	length = 316 * 4
	nations = f.raw[offset : offset + length]
	offset += length
	length = 18 * tribes
	tribes = f.raw[offset : offset + length]
	offset += length
	length = 1351
	middle = f.raw[offset : offset + length]
	offset += length
	length = 4 * 4176
	maps = f.raw[offset : offset + length]
	offset += length
	final = f.raw[offset : ]
	
	split_maps = [maps[i : i + 4176] for i in range(0, len(maps), 4176)]
	
	units_xy = []
	split_units = [units[i : i + 28] for i in range(0, len(units), 28)]
	for i in split_units:
		units_xy += [(i[0], i[1])]
	units_xy = set(units_xy)	
		
	split_tribes = [tribes[i : i + 18] for i in range(0, len(tribes), 18)]
	
	all_info = bytearray()
	all_info += intro
	
	to_erase = 0
	split_colonies = [colonies[i : i + 202] for i in range(0, len(colonies), 202)]

	for i in split_colonies:	
		first_char = chr(i[2])
		test_char = i[3:5].decode('ascii').lower()		
		if first_char == '*' and test_char in ABBR:
			xy = (i[0], i[1])
			if xy not in units_xy:
				nation = ABBR.index(test_char) + BASE				
				flags = f"{bin(nation)[2:].zfill(4)[:4]}0000"
				to_erase += 1
				split_tribes += [new_tribe(i[0], i[1], nation, i[0x1F] * 3)]
				pos = xy[1] * 58 + xy[0]
				split_maps[1][pos] = 0b10
				split_maps[2][pos] = int(flags, 2)
				continue
		all_info += i
	
	all_info += units
	all_info += nations
	
	for i in split_tribes:
		all_info += i
	
	all_info += middle
	for i in split_maps:
		all_info += i
	all_info += final
	
	f.raw = all_info
	f.save_short(0x2A, [len(split_tribes)])
	f.save_short(0x2C, [len(split_units)])
	f.save_short(0x2E, [len(split_colonies) - to_erase])
	return to_erase != 0

class bits:
	def __init__(self, bits):
		self.bits = bits
	def __len__(self):
		return len(self.bits)
	def __getitem__(self, key):
		return int(self.bits[-1-key])
	def __setitem__(self, key, value):
		self.bits[-1-key] = str(value)
	def __repr__(self):
		return str(''.join(self.bits))

class col:
	
	def short(self, n, m = None, signed = False, length = 2):
		if m is None:
			m = n
		res = [self.raw[i : i + length] for i in range(n, m + 1, length)]
		return [int.from_bytes(i, byteorder = 'little', signed = signed) for i in res]
	
	def save_short(self, n, vals, signed = False, length = 2):
		res = [i.to_bytes(length, byteorder = 'little', signed = signed) for i in vals]
		l = n
		for i, j in enumerate(res):	
			self.raw[l : l + length] = j
			l += length
	
	def hex(self, n, m = None):
		if m is None:
			m = n
		return [int(self.raw[i]) for i in range(n, m + 1)]
	
	def save_hex(self, n, vals):
		for i, j in enumerate(vals):
			self.raw[n + i] = j
	
	def bits(self, n, m = None):
		if m is None:
			m = n
		return bits([j for j in ''.join([bin(self.raw[i])[2:].zfill(8) for i in range(n, m + 1)])])
		
	def save_bits(self, n, vals):		
		res  = [int(''.join(vals.bits[i : i + 8]), 2) for i in range(0, len(vals), 8)]
		for i, j in enumerate(res):
			self.raw[n + i] = j
	
	def name(self, n = None):
		if n is None:
			n = self.id
		return f"COLONIZE{os.path.sep}Colony{str(n).zfill(2)}.sav"
		
	def __init__(self, n = None, extra = None):
		self.id = n
		if n is None:
			self.raw = extra
		else:
			with open(self.name(), "rb") as f:
				self.raw = bytearray(f.read())
	
	def save(self, n):
		if self.id is None:
			return
		with open(self.name(n), "wb") as f:
			f.write(self.raw)

def check_colonies(f):
	is_colony = [False] * 4
	colonies = f.short(0x2E)[0]
	if colonies:
		offset = 0x186
		steps = 202
		finish = offset + colonies * steps			
		for i in range(offset, finish, steps):
			val = f.hex(i + 0x1A)[0]				
			if val >= 0 and val <= 3:
				is_colony[val] = True
				if all(is_colony):
					return True
	return all(is_colony)

def find_colony(f, x, y, n):
	is_colony = [False] * 4
	colonies = f.short(0x2E)[0]
	if colonies:
		offset = 0x186
		steps = 202
		finish = offset + colonies * steps			
		for i in range(offset, finish, steps):
			if f.hex(i)[0] == x and f.hex(i + 1)[0] == y:
				f.save_hex(i + 26, [n])

def food(f, n, a):
	colonies = f.short(0x2E)[0]
	rebel_count = 0
	citizens_overall = 0
	if colonies:
		offset = 0x186
		steps = 202
		finish = offset + colonies * steps
		gain_flag = True
		while gain_flag:
			gain_flag = False
			for i in range(offset, finish, steps):			
				nation = f.hex(i + 26)[0]
				if nation != n:
					continue
				count = f.short(i + 0x9A, signed = True)[0]
				gain = 0
				if count >= 32000:
					continue
				elif count + 100 > 32000:
					gain = 32000 - count				
				else:
					gain = 100			
				gain = min(a, gain)
				if not gain:
					continue
				a -= gain
				count += gain
				f.save_short(i + 0x9A, [count], signed = True)
				gain_flag = True

def rebels(f, n):	
	colonies = f.short(0x2E)[0]
	rebel_count = 0
	citizens_overall = 0
	if colonies:
		offset = 0x186
		steps = 202
		finish = offset + colonies * steps			
		for i in range(offset, finish, steps):			
			nation = f.hex(i + 26)[0]
			if nation != n:
				continue
			citizens = f.hex(i + 31)[0]
			count = f.short(i + 194)[0]
			total = f.short(i + 198)[0]
			citizens_overall += citizens
			rebel_count += int(citizens * count / total)	
	granted = rebel_count >= 80
	print(f"{rebel_count} out of {citizens_overall} support idea of Independence. {'E' if granted else 'Not e'}nough to request independence.")
	return granted

def riots(f):
	colonies = f.short(0x2E)[0]
	if colonies:
		offset = 0x186
		steps = 202
		finish = offset + colonies * steps			
		for i in range(offset, finish, steps):			
			flags = f.hex(i + 28)[0]
			if flags % 2 != 0:
				f.save_hex(i + 28, [flags - 1])

def tribeforce(f, doit = False):
	howmuch = 0
	tribes, units, colonies = f.short(0x2A, 0x2E)
	offset = 0x186 + 202 * colonies + 28 * units + 316 * 4 + 4
	for i in range(tribes):
		pos = offset + i * 18
		if doit:
			f.save_hex(pos, [32])
		else:
			power = f.hex(pos)[0]
			if power < 32:
				howmuch += 32 - power
	return howmuch

def mapval(f, n, x, y, bits = None):
	tribes, units, colonies = f.short(0x2A, 0x2E)
	offset = 0x186 + 202 * colonies + 28 * units + 316 * 4 + 18 * tribes + 1351 + n * 4176
	pos = offset + y * 58 + x
	if bits is None:
		return f.bits(pos)
	else:
		f.save_bits(pos, bits)

def tax(f, n, v):
	units, colonies = f.short(0x2C, 0x2E)
	offset = 0x186 + 202 * colonies + 28 * units + 1 + 316 * n
	tax_value = f.hex(offset)[0]
	if tax_value >= 0 and tax_value <= 127:
		print("As a winner, you force the European Powers to provide you with a better tax rate...")
		f.save_hex(offset, [v])

def prompt(s):
	return input(s).lower().startswith('y')

def main_routine():
	f = col(0)
	if not col2tribe(f):
		status = f.bits(18)

		succession = f.short(0x62, signed = True)[0]
		if succession < 0:	
			if prompt(f"Do you want to suspend the War of Succession? (y/n) "):
				succession = 10
				print("War of Succession has been suspended.")
		elif succession == 10:
			year = f.short(0x1A, signed = True)[0]
			if year < 1600:
				print("War of Succession can't be restarted before 1600 AD.")
			elif check_colonies(f):
				print("Every rival has at least one colony. War of Succession can't be restarted.")
			else:
				if prompt(f"Do you want to restart the War of Succession? (y/n) "):
					succession = -1
					print("War of Succession has been restarted.")
		else:
			print("War of Succession has already been finished.")
			player = None
			status_addr = (0xCF, 0x103, 0x137, 0x16B)
			npc_status = [f.hex(i)[0] for i in status_addr]
			if 0 in npc_status:
				player = npc_status.index(0)
				if rebels(f, player):
					f.save_short(0x6A, [0, 0, 0, 0])
				if status[3] == 1:
					print("You've won the War of Independence!")			
					if status[0] != 0:				
						status[0] = 0	
						succession = -1
						npc_status = [i if i != 2 else 1 for i in npc_status]				
						[f.save_hex(j, [npc_status[i]]) for i, j in enumerate(status_addr)]
						riots(f)
					tax(f, player, 0x83) # -125 % if taxes are positive			
					a = tribeforce(f) * 5
					if a >= 100 and prompt(f"Do you want to help indian people for {a} amounts of food? (y/n) "):
						tribeforce(f, True)
						food(f, player, a)
			else:
				print("There's no player.")

		f.save_hex(50, [0]) # hide map
		f.save_bits(18, status)
		f.save_short(0x62, [succession], signed = True)
	else:
		print("The Indian Extended Aid Initiative has been activated.")
	f.save(1)

if __name__ == '__main__':
	main_routine()
