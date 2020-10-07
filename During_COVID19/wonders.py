WONDERS = """
Pyramids
Hanging Gardens
Colossus
Lighthouse
Library Gr.
Oracle
Wall Gr.
Magellan's Expedition
Michelangelo's Chapel
Copernicus' Observatory
Shakespeare's Theatre
Isaac Newton's College
J.S.Bach's Cathedral
Darwin's Voyage
Hoover Dam
Women's Suffrage
Manhattan Project
United Nations
Apollo Program
SETI Program
Cure For Cancer
""".split('\n')[1:-1]

text = """Pyramids
The Pyramids are the symbol of the strong rulers; destroying the Pyramids leads to instability that causes govts to collapse; in the light of events, new palaces and governments are reestablished, where rulers are unwilling to support rapid growing of the cities, so the irrigations are forgotten to prevent unwanted revolts and any sign of unhappiness is brutally suppressed. 
Handing Gardens
The desolation of the Gardens brought surprising benefits for the civilization, as this event allowed a lot of barbarian folks to ravage the ruins of the Gardens and live rich lives without any further attempts to terrorize civilians, to the greatest unpleasure of Atilla.
Colossus
The crumble of the Colossus, the symbol of the civilization protection and great victory, encouraged Atilla to seize scientists in a series of attacks to produce a new kind of weapon in his own hidden laboratory. With necessary technologies, this attempt turned the tables in the world of armed forces; cheap yet powerful improvement to the simple guerrilla muskets made the unit even more powerful than mechanized infantry. Such events consolidate the civil society against their irreconcilable enemies.
Lighthouse
The lighthouse has been abandoned due to technical difficulties, but the idea of ever-shining light brought its fruits for the advanced flight technologies of the future, such as airbases and aerial refueling. The bombers no longer run out of fuel in the air.
Great Library
Great Library has been ravaged. This tragedy shattered the civilized world and led to the apocalyptic disaster. The world has lost all knowledge, army, most of citizens. It’s up to the rulers to recover lost connections in order to rebuild the civilization from the remains, as the ability to discover technologies is recovered.
Oracle
The Oracle overthrow often understood as an act of unknown regicide who got harmed under the virtual reign of the greatest spiritual leader of all time. Once the dust settled, the money flowed from the fallen united regime to the nations, little and big, worldwide. New capitals emerged as a sign of freedom of the nations, thirsty for political independence.
Great Wall
The fall of the Great Wall happened under apocalyptic circumstances. Zombies destroyed the wall when they finished to expand their domination across the rest of the world. There’s only you and them, barbarians. Every foreign city belongs to them, allowing you to keep playing after world domination.
Magellan’s Expedition
The Magellan death did not diminish the results of his expedition. A lot of inspired followers tried to repeat his dangerous path across land and sea using various self-made vehicles, from yachts to hang-gliders. The settler units became near-invincible and experienced explorers of the air, as a result.
Michelangelo’s Chapel
Astonishingly brutal devastation and desecration of the Michelangelo’s Chapel by local communist party was made to prove the point that there’s no God to protect His own institutions. It got, however, quite the opposite reaction. A lot of believers across the world stood tall in the peaceful demonstration that forced the rulers to honor their rights and pacifist intentions. Since that day it was not possible to build offensive units for a long time.
Copernicus’ Observatory
The crusades against the barbarian cultists, who covert their misdeeds as seemingly innocuous institutions, result in the Dark Age, culminating in the event of burning the Copernicus’ Observatory. The knowledge gained from the observatory allowed people to live in prosperity, although new buildings and organizations were strictly prohibited for the centuries to come.
Shakespeare’s Theatre
People witnessing destruction of the Shakespeare’s Theatre are shocked to the point that they disobey any suppression of their freedom; modern convenience is not tolerated as luxury anymore, including irrigations; the events of the peaceful rebellion across the world do not lead to the direct revolutions, yet make it harder for a ruler to control the population.
Isaac Newton’s College
The Newton’s College has been closed on a short notice and a lot of jobless scientists left with no other option but to prove their worth to the society. The resulting advancement in the military technologies allowed to improve unit characteristics beyond imagination.
J.S.Bach’s Cathedral
The success of the crusades against the barbarian cultists was not flawless, as civilizations stagnated under the iron will of the zealots. The burning of the J.S.Bach’s Cathedral was the first strike among many others which lead to recovering of the society back to normal life. A lot of following pacts forced military non-nuclear units to restore their original unmodified state and stopped hegemony of the crusaders, so new buildings and organizations could live in the spirit of the entrepreneurship once again, avoiding radicalism.
Darwin’s Voyage
Darwin’s Voyage brought the research laboratories in the cities to revitalization, allowing spies to steal new technologies and providing the ways for military forces to renew their nuclear programs.
Hoover Dam
The tear in the Hoover Dam forced people to search for advanced forms of recycling. Current level of world radiation fades to zero, every city gets free settler.
Women’s Suffrage
Attempts of the masculine traditionalist government to shush the feminist movement opened the Pandora’s Box; radical response of the society led to uncontrollable shortage of military forces outside the city territories and mass sabotage of every single offensive unit except some air units, such as fighters and nuclear weapons. Peace treaties were signed worldwide as a sign of people union and insignificance of country borders. 
Manhattan Project
Unrest among the masses forced the govts around the world to freeze their nuclear programs, albeit this process does not conclude due to a failure in the futile attempt of disarming. False positive nuclear alarm triggered a chain reaction that forced the World War and prevented any attempts of negotiations.
United Nations
United Nations has been disbanded due to inability to provide the means for fruitful conversations between the national leaders. The threats and miscommunications triggered apocalyptic scenario, as the countries started to fall apart into independent groups. As this process of separation has reached its conclusion, new palaces have been installed, and restored ability to make negotiations between new nations allowed leaders to find the balance in this new shaky world.
Apollo Program
The famous first spaceport in the world has been lost in an artificial micro black hole when an experiment went out of control. The yet-to-be-explained quantum side effect results in the huge city growth.
SETI Program
SETI initiative consolidated the smartest scientists across the world and the high hopes that crumbled after the cancellation of the SETI Program along with other military research programs. A lot of units have been disbanded along the way, and the following Winter of Science prevented any further technological advances worldwide.
Cure for Cancer
The dismantling of the monument in honor of Cure for Cancer happened after the last research in that field and never darkened the effect it brought – overall advancement in the field of medicine that made people considerably happier, thus allowing rulers across the world to catch their breath and rule with ease.""".split("\n")

import os
import random
import shutil

# ~ def change_type(t):
	# ~ c =(5, 12, 4) #riflemen -> infantry, mech -> musk
	# ~ if t == 4: #musk -> rifle 5
		# ~ return c[0]
	# ~ elif t == 5: #rifle -> mech 12
		# ~ return c[1]
	# ~ elif t == 12: #mech -> musk 4
		# ~ return c[2]
	# ~ return t

def city_mask_check(x, y):
	return not (abs(x) == abs(y) == 2)	

ENOUGH = 33
CITY_MASK=[(i, j) for i in range(-2, 3) for j in range(-2, 3) if city_mask_check(i, j)]

def redef_coords(x, y):
	if y < 0 or y >= 50:
		return None
	while x < 0:
		x += 80
	while x >= 80:
		x -= 80
	return x, y

def city_mask(x, y):
	return [redef_coords(x + c[0], y + c[1]) for c in CITY_MASK]

class sve:
	def __init__(self, n):
		fullname = f"Civil{n}" if type(n) == int else n
		with open(f"CIV{os.path.sep}{fullname}.sve", "rb") as f:
			self.raw = bytearray(f.read())
		self.rawlen = len(self.raw)
		self.index = n if type(n) == int else None				
		self.offsets = {
			"city" : 0x1508,
			"type" : 0x2308,
			"unit" : 0x26C0
		}
	
	def save(self, n):
		if self.index == None:
			return
		if self.index != n:
			shutil.copy(f"CIV{os.path.sep}Civil{self.index}.map", f"CIV{os.path.sep}Civil{n}.map")
		with open(f"CIV{os.path.sep}Civil{n}.sve", "wb") as f:
			f.write(self.raw)
	
	def split(self, start, finish, length):
		return [self.raw[i : i + length] for i in range(start, finish + 1, length)]
	
	def ush(self, pos, val = None):		
		if val is not None:
			self.raw[pos] = val
			if (pos + 1) < self.rawlen:
				self.raw[pos + 1] = 0
		return self.raw[pos]
	
	def val(self, start, finish = None, value = None):
		if finish is None:
			finish = start
		if value is not None:
			for i in range(start, finish + 1):
				self.raw[i] = value
		return self.raw[start : finish + 1]
	
	def bit(self, start, pos = None, value = None, finish = None):
		if finish is None:
			finish = start
		bits = [j for j in ''.join([bin(i)[2:].zfill(8) for i in self.raw[start : finish + 1]])]
		if pos is not None:
			pos_upd = -pos - 1
			if value is not None:
				bits [pos_upd] = str(value)
				ret_bits = [int(''.join(bits[i : i + 8]), 2) for i in range(0, len(bits), 8)]
				for i, j in enumerate(ret_bits):
					self.raw[start + i] = j
			return bits [pos_upd]
		return bits
	
	def val2(self, start, length):
		return [int(i) for i in self.val(start, start + length - 1)]
	
	def bits(self, start, length):
		return self.bit(start, None, None, start + length - 1)

class city:	
	def __init__(self, s, n):
		self.valid = True
		if n < 0 or n >= 128:
			self.valid = False
			return
		pos = s.offsets['city'] + 28 * n
		if s.raw[pos + 6] == 0xFF:
			self.valid = False		
		
		#if (s.raw[pos + 4], s.raw[pos + 5]) not in gz:
		#	return
		
		self.valid = True	
		self.buildings = s.bits(pos, 4)
		pos += 4
		self.x = s.raw[pos]
		self.y = s.raw[pos + 1]
		pos += 2
		self.status = s.bit(pos)
		if self.status == 0xFF:
			self.valid = False
		pos += 1
		self.size = s.raw[pos]
		if self.size < 1 or self.size > 127:
			self.valid = False
		pos += 1
		self.seen = s.raw[pos]
		pos += 1
		self.product = s.raw[pos]
		pos += 1
		self.trade = s.raw[pos]
		pos += 1
		self.nation = s.raw[pos]
		pos += 1
		self.flag = s.val2(pos, 10)
		pos += 10
		self.nameid = s.raw[pos]
		namepos = 0x6970 + 13 * self.nameid		
		self.name = s.raw[namepos : namepos + 13].decode('ascii').strip('\0')		
		pos += 1
		self.routes = s.val2(pos, 3)
		pos += 3
		self.unit1 = s.raw[pos]
		pos += 1
		self.unit2 = s.raw[pos]		
	
	def raw(self):
		raw_data = [int(''.join(self.buildings[i:i+8]), 2) for i in range(0, len(self.buildings), 8)]
		raw_data += [self.x, self.y, int(''.join(self.status), 2), self.size, self.seen, self.product, self.trade, self.nation]
		raw_data += self.flag
		raw_data += [self.nameid]
		raw_data += self.routes
		raw_data += [self.unit1, self.unit2]
		return raw_data
		
class unittype:
	def __init__(self, s, n):
		self.valid = True
		if n < 0 or n >= 28:
			self.valid = False
			return
		pos = s.offsets['type'] + 34 * n
		self.name = s.raw[pos : pos + 12].decode('ascii').strip('\0')
		pos += 12		
		self.absolete, self.type, self.moves, self.turns, self.attack, self.defense, self.cost, self.sight, self.carry, self.role, self.tech = [s.val2(pos + i * 2, 2) for i in range(11)]

	def raw(self):
		raw_data = [int(i) for i in self.name.encode('ascii')]		
		raw_data += [0] * (12 - len(raw_data))
		for i in (self.absolete, self.type, self.moves, self.turns, self.attack, self.defense, self.cost, self.sight, self.carry, self.role, self.tech):
			raw_data += i		
		return raw_data

class unit:
	def __init__(self, s, n):
		self.nation = n // 128
		self.valid = True
		if n < 0 or n >= 1024:
			self.valid = False
			return	
		pos = s.offsets['unit'] + 12 * n
		if s.raw[pos + 3] == 0xFF:
			self.valid = False		
		self.state, self.x, self.y, self.type, self.left, self.spec, self.gx, self.gy, self.flag, self.visible, self.next, self.city = [s.raw[pos + i] for i in range(12)]		
	
	def raw(self):
		raw_data = []
		for i in (self.state, self.x, self.y, self.type, self.left, self.spec, self.gx, self.gy, self.flag, self.visible, self.next, self.city):
			raw_data += [i]		
		return raw_data
	
		#print([x, y], "->", self.pos)
		
		#cities_raw = sve.split(0x1508, 0x2307, 28)
		#citynames_raw = sve.split(0x6970, 0x766F, 13)
		#cityX_raw = sve.split(0x91B8, 0x92B7, 1)
		#cityY_raw = sve.split(0x92B8, 0x93B7, 1)
		#wonders_raw = sve.split(0x8672, 0x869D, 2)
		
		
		# ~ self.nameid = s.raw[pos]
		# ~ namepos = 0x6970 + 13 * self.nameid
		# ~ self.name = s.raw[namepos : namepos + 13].decode('ascii').strip('\0 ')


class tricks:
	def __init__(self, n):
		self.save = sve(n)
		
		#gx = [ord(i) for i in self.save.split(0x91B8, 0x92B7, 1)]
		#gy = [ord(i) for i in self.save.split(0x92B8, 0x93B7, 1)]
		#gz = [i for i in zip(gx, gy) if i[0] != 0xFF]
		
		self.cities = [city(self.save, i) for i in range(128)]
		self.types = [unittype(self.save, i) for i in range(28)]
		self.units = [unit(self.save, i) for i in range(1024)]
	
	def redraw(self, what, offset_name):
		index = self.save.offsets[offset_name]
		for i in what:
			for j in i.raw():
				self.save.raw[index] = j
				index += 1
		
	def store(self):
		self.redraw(self.cities, 'city')
		self.redraw(self.types, 'type')
		self.redraw(self.units, 'unit')
		
	def drop(self, n):
		self.store()
		self.save.save(n)
	
	def clear_human(self, n = None):
		for i in range(0x4, 0x5 + 1):
			self.save.raw[i] = 0
		for i in range(0x758, 0x767, 2):
			self.save.raw[i] = 0xFF
			self.save.raw[i+1] = 0x7F
		for i in range(0xE, 0xF + 1):
			self.save.raw[i] = 0xFF
		if n is not None:
			self.save.ush(0x2, n)
	
	def reelect(self):
		electable = []
		for k in [8-i for i,j in enumerate(bin(self.save.raw[0xC])[2:-1].zfill(8)) if j!='0']:
			validation = len([i for i in self.cities if i.valid and i.nation == k])
			if validation:
				electable+=[k]	
		
		ai = [(random.randint(1, 7)) + 8 * random.randint(0, 1) for i in list(range(1, 8))]
		random.shuffle(ai)		
		ai_flags = int(f"{''.join(['0' if i<=7 else '1' for i in ai[::-1]])}0", 2)
		self.save.ush(0x93de, ai_flags)
		for i in range(0x77a, 0x787, 2):
			head, ai = ai[0], ai[1:]
			self.save.ush(i, head)
		
		self.clear_human(random.choice(electable))
		
	def kmean(self):					
		cities = [[i.x, i.y, 0] for i in self.cities if i.valid]
		count = 7
		truec = 0
		centroids = []		
		while True:
			x = [c for c in cities if c[2] == 0]
			if not len(x):
				break			
			x = cities[cities.index(random.choice(x))]
			truec += 1			
			x[2] = truec
			centroids += [[x[0], x[1], x[2]]]
			if truec >= count:
				break
		if truec == 0:
			return		
		while True:
			changes = False
			for c in cities:
				if c in centroids:
					continue
				l = [self.distance(j[0], j[1], c[0], c[1]) for j in centroids]
				old = c[2]
				c[2] = centroids[l.index(min(l))][2]
				if old != c[2]:
					changes = True
			if not changes:
				break
			for r in centroids:
				z = [c for c in cities if c[2] == r[2]]
				r[0] = sum([i[0] for i in z])/len(z)
				r[1] = sum([i[1] for i in z])/len(z)
		
		r = list(range(1,8))
		random.shuffle(r)
		
		for i, c in enumerate(centroids):
			c[2] = r[i]
						
		self.lost_civilization(trunc = True, sizeval = 2)
		self.save.val(0x56C0, 0x665F, 0xFF)
		
		for	c in self.cities:
			if c.valid:				
				if c.buildings[7] != '0':
					c.buildings[7] = '0'
				x = [i[2] for i in cities if i[0] == c.x and i[1] == c.y]
				if x:	
					c.nation = centroids[x[0] - 1][2]

		self.save.ush(0xC, 0)
		[self.save.bit(0xC, i[2], 1) for i in centroids]
		self.clear_human(centroids[0][2])
		self.noneunit(0x1, 0x0, 3, (-1, -1))
		[self.capital(i) for i in range(1, 8)]
	
	def settlers_fly(self):
		self.types[0].type = [1, 0]
	
	def bombers_move(self):
		self.types[15].turns = [0, 0]
	
	def eliminate_barbarians(self):
		self.clear_national_units(0)		
		self.save.bit(0xC, 0, 0)
	
	def improve_barbarians(self):
		if len([i for i in self.types if i.name == 'Guerrilla']) != 0:
			return		
		Guerrilla = self.types[12]
		Shooters = self.types[4]
		Infantry = self.types[5]
		self.types[4], self.types[5], self.types[12] = Guerrilla, Shooters, Infantry		
		self.types[4].name, self.types[5].name, self.types[12].name = 'Guerrilla', 'Shooters', 'Infantry'
		# ~ for u in self.units:
			# ~ if u.valid:
				# ~ u.type = change_type(u.type)
		# ~ for c in self.cities:
			# ~ if c.valid:
				# ~ r = bin(c.unit1)[2:].zfill(8)
				# ~ c.unit1 = int(r[:3] + bin(change_type(int(r[3:], 2)))[2:].zfill(5), 2)
				# ~ r = bin(c.unit2)[2:].zfill(8)
				# ~ c.unit2 = int(r[:3] + bin(change_type(int(r[3:], 2)))[2:].zfill(5), 2)

		self.save.bit(0xC, 0, 1)
	
	def elevate_types(self):
		typedef = [[], [], []]
		for t in self.types:
			t.attack[1] = t.defense[1] = 0
			a, d, k = t.attack[0], t.defense[0], t.type[0]
			if k != 0 or a <= 0:
				continue
			r = -1 if not d else a//d
			if a <= d and d != 1:
				typedef[0] += [t]
			elif a > d and r % 2 == 0 and r < 6:
				typedef[1] += [t]
			elif a > d and (r % 2 == 1 or r >= 6):
				typedef[2] += [t]
		
		vals=((1, 1), (2, 1), (2, 0))
		
		check = True
		for i, j in enumerate(typedef):
			for k in j:
				if max(k.attack[0] + vals[i][0], k.defense[0] + vals[i][1]) > ENOUGH:
					check = False
					return
		for i, j in enumerate(typedef):
			for k in j:
				k.attack[0] += vals[i][0]
				k.defense[0] += vals[i][1]
		
		seair = [t for t in self.types if t.type[0] in (1, 2) and t.attack[0] > 0 and t.defense[0] > 0 and t.carry[0] <= 0]		
		values_1 = [(k.attack[0], k.defense[0]) for k in typedef[1]]
		values_2 = [(k.attack[0], k.defense[0]) for k in typedef[2]]
		
		seair[0].attack[0], seair[0].defense[0] = values_1[1]
		seair[1].attack[0] = values_2[3][0]
		seair[2].attack[0] = seair[2].defense[0] = values_1[1][0]
		seair[3].attack[0] = seair[3].defense[0] = values_2[1][0]
		seair[4].attack[0], seair[4].defense[0] = min(ENOUGH, values_2[3][0] + values_2[1][0]), values_2[3][0]
		seair[5].attack[0] = values_2[2][0]
		seair[6].defense[0] = values_2[3][0]
	
	def capital_cash(self):
		[self.capital(i) for i in range(1, 8)]
		for i in range(1, 8):
			l = len([c for c in self.cities if c.valid and c.nation==i])
			if not l:
				continue
			self.capital(i)			
			offset = 0x138 + 2 * i
			self.save.raw[offset : offset + 2] = min(32000, l * 250 + int.from_bytes(self.save.raw[offset : offset + 2], byteorder = 'little', signed = False)).to_bytes(2, byteorder = 'little', signed = False)
	
	def no_radiation(self):
		self.save.ush(0x8AA0, 0)	
	
	def easy_life(self, difficulty = (0xFF, 0xFF)):
		self.save.raw[0xA] = difficulty[0]
		self.save.raw[0xB] = difficulty[1]
	
	def disable_nukes(self, n = 25, v = (0x7F,)):		
		self.types[n].tech[0] = v[0]
		self.types[n].tech[1] = 0x00 if len(v) < 2 else v[1]
	
	def no_offence(self):
		offenders = [3, 6, 7, 8, 9, 10, 11, 13, 14, 15, 19, 20, 21, 22, 25]
		for i in offenders:
			self.disable_nukes(i)		
	
	def too_hostile(self, state = 0):
		self.save.bit(0x8BAE, 0, state)
	
	def too_quiet(self, state = 0):
		self.save.bit(0x8BAE, 1, state)
	
	def too_inhospitable(self, state = 0):
		if not state:
			for i in self.cities:
				if i.valid:
					i.buildings	= ['1'] * len(i.buildings)
		self.save.bit(0x8BAE, 2, state)
		
	def too_primitive(self, state = 0):
		# ~ if not state:
			# ~ self.save.val(0x4E8, 0x537, 0xFF)
		self.save.bit(0x8BAE, 3, state)
	
	def peacemaker(self, peace = 1, basecode = 0x41):
		code = basecode + peace
		for i in range(0x648, 0x6C7, 2):
			self.save.ush(i, code)

	def spy_paradise(self):
		for i in self.cities:
			if i.valid:
				i.status[-6] = '0'
			
	def distance(self, x1, y1, x2, y2):
		return pow(pow(x2 - x1, 2) + pow(y2 - y1, 2), 0.5)
		
	def capital(self, n):
		cities = [i for i in f.cities if i.valid and i.nation == n]
		if len(cities) == 0:
			return
		capital = [i for i in cities if i.buildings[7] == '1']
		if len(capital) == 0:
			middle = (sum([i.x for i in cities])/len(cities), sum([i.y for i in cities])/len(cities))
			d = [self.distance(i.x, i.y, middle[0], middle[1]) for i in cities]			
			new_capital = cities[d.index(min(d))]
			new_capital.buildings[7] = '1'
			return new_capital
		else:
			return capital[0]
				
	def settlers_back(self):
		for i in self.cities:
			if i.valid:
				i.size = min(127, i.size * 2)
		# ~ for i in self.cities:
			# ~ if not i.valid:
				# ~ continue
			# ~ u = [j for j in self.units if j.valid and j.x == i.x and j.y == i.y and j.type == 0]
			# ~ for j in u:
				# ~ j.state = 0xFF
				# ~ if i.size < 127:
					# ~ i.size += 1
	
	def converge(self, c, pt):
		x = redef_coords(c[0] + pt[0], c[1] + pt[1])
		if x is None:
			for i in range(-1, 2):
				for j in range(-1, 2):
					x = redef_coords(c[0] + i, c[1] + j)
					if x is not None:
						return x
		else:
			return x
		return c
	
	def noneunit(self, t, st = 0, moves = 0, pt = (0, 0)):
		for j in range(128, 1024, 128):			
			cities = set([(i.x, i.y) for i in self.cities if i.valid and i.nation == self.units[j].nation])
			for k, c in enumerate(cities):							
				pos = j
				off = 0
				proceed = True
				while self.units[pos + off].valid:
					off += 1
					if off >= 128:
						proceed = False
						break
				if proceed:
					pos += off
				else:
					break
				self.save.raw[0x158 + 28 * 2 * self.units[j].nation + 2 * t] += 1
				self.units[pos].state = st
				self.units[pos].type = t
				ptx, pty = self.converge(c, pt)
				self.units[pos].x = ptx
				self.units[pos].y = pty
				self.units[pos].left = moves
				self.units[pos].spec = 0
				self.units[pos].gx = c[0] if pt != (0, 0) else 0xFF 
				self.units[pos].gy = c[1] if pt != (0, 0) else 0
				self.units[pos].flag = 0xFF
				self.units[pos].visible = 0xFF
				self.units[pos].next = 0xFF
				self.units[pos].city = 0xFF
				self.units[pos].valid = True
	
	def eliminate_citybusters(self):
		slots = [[] for i in range(8)]
		prohibited = []
		for c in self.cities:
			if c.valid:
				slots[c.nation].extend([i for i in city_mask(c.x, c.y) if i])
		slots = [set(i) for i in slots]
		for u in self.units:
			if u.valid and (u.x, u.y) not in slots[u.nation]:
				self.clear_unit(u, True)
	
	def restore_default_types(self, include = None, exclude = []):
		default = sve("default")
		for i in range(28):
			if (include is None) or ((i in include) and (i not in exclude)):
				self.types[i] = unittype(default, i)
	
	def eliminate_movement(self):
		for t in self.types:			
			if not ((t.type[0] == 1 and t.turns[0] == 1) or t.attack[0] == 0):				
				if t.type[0] == 2 or t.attack[0] > t.defense[0]:
					t.tech  = [0x7F, 0]
				t.type  = [1, 0]
				t.moves = [0, 0]
				t.turns = [0, 0]
		for u in self.units:
			if u.valid:
				u.left = 0
				u.city = 0xFF
	
	def clear_unit(self, i, cleartable = False):
		if cleartable:
			offset = 0x158 + 56 * i.nation + 2 * i.type
			if self.save.raw[offset] >= 1:
				self.save.raw[offset] -= 1
		i.state = 0
		i.type = 0xFF
		i.x = 0
		i.y = 0
		i.left = 0
		i.spec = 0
		i.gx = 0xFF
		i.gy = 0
		i.flag = 0xFF
		i.visible = 0
		i.next = 0xFF
		i.city = 0xFF
		i.valid = False
	
	def clear_except_cities(self):
		coords = [(c.x, c.y) for c in self.cities if c.valid]		
		for i in self.units:
			if (i.x, i.y) in coords:
				continue
			self.clear_unit(i, True)
	
	def clear_national_units(self, n):
		offset1s = 0x158 + 56 * n
		offset1e = offset1s + 56 - 1
		offset2s = 0x318 + 56 * n
		offset2e = offset2s + 56 - 1
		self.save.val(offset1s, offset1e, 0)
		self.save.val(offset2s, offset2e, 0)
		for i in self.cities:
			if i.nation == n:
				i.unit1 = 0xFF
				i.unit2 = 0xFF
		for i in self.units:
			if i.nation == n:
				self.clear_unit(i)
	
	def clear_units(self, incity = True, cleartable = True):
		if cleartable:
			self.save.val(0x158, 0x4D7, 0)
		if incity:
			for i in self.cities:			
				i.unit1 = 0xFF
				i.unit2 = 0xFF
		for i in self.units:
			self.clear_unit(i)
	
	def lost_civilization(self, mode = True, trunc = False, sizeval = 1):
		if not trunc:
			if mode:
				# No money
				self.save.val(0x138, 0x147, 0)
				# No knowledge
				self.save.val(0x4E8, 0x537, 0)
				self.save.val(0x148, 0x157, 0)
				self.save.val(0xE, 0xF, 0xFF)		
				# Despotism everywhere
				for i in range(0x538, 0x547 + 1, 2):
					self.save.ush(i, 1)
			else:			
				[self.save.bit(0xC, i, 1 if i==self.save.raw[0x2] or i==0 else 0) for i in range(8)]
		# Militia in prod., size of city is 1
		for i in self.cities:
			if not i.valid:
				continue
			if not trunc:
				if mode:
					i.state = 0
					is_palace = i.buildings[7]
					i.buildings = ['0'] * len(i.buildings)
					i.buildings[7] = is_palace
					i.product = 1
					i.size = sizeval
					i.seen = 1
					for j in range(len(i.flag)):
						i.flag[j] = 0xFF if j == 2 else 0
				else:				
					if i.nation != self.save.raw[0x2]:
						i.nation = 0
			else:
				i.size = max (sizeval, i.size)
			i.unit1 = 0xFF
			i.unit2 = 0xFF

		#self.state, self.x, self.y, self.type, self.left, self.spec, self.gx, self.gy, self.flag, self.visible, self.next, self.city
		#[[0, 53, 23, 0, 3, 0, 255, 0, 255, 128, 1, 8], [8, 53, 23, 1, 0, 0, 255, 0, 255, 128, 0, 8]]
		
		# No units
		self.clear_units(False)
		
		self.peacemaker(0, 0)
		
		if trunc:
			return
		
		#NONE Militia per city
		self.noneunit(0x1, 0x4)
		
		[self.capital(i) for i in range(1, 8)]
		
		
		
		
		

#[f.capital(i) for i in range(1, 8)]
#f.lost_civilization(False)
#f.disable_nukes(v=(0xFE, 0xFF))
#f.clear_by_type([0xF])

#f.reelect()
#f.kmean()

#f.eliminate_citybusters()
#f.eliminate_movement()
#f.restore_default_types()
#f.improve_barbarians()

#f.elevate_types()

#f.capital_cash()

print("# to load [0]:",end=" ")
x = input()
x = int(x) if x and all([i.isdigit() for i in x]) else 0
f = tricks(x)

wonders = [int.from_bytes(f.save.raw[i:i+2], byteorder = 'little', signed = True) for i in range(0x8674, 0x869D, 2)]
cities = [(f.cities[i], n) if i >= 0 and i < 128 and f.cities[i].valid else None for n, i in enumerate(wonders)]
true_wonders = [i[1] for i in cities if i and i[0].nation == f.save.raw[0x2]]

#true_wonders = [i for i in range(21)] #DEBUG

while True:
	name_wonders = []
	while len(name_wonders) != 1:
		if not len(name_wonders):
			name_wonders = [WONDERS[i] for i in true_wonders]
			if not len(name_wonders):
				print('No wonders are currently available to your civilization.')
				exit()
		print()
		for i,j in enumerate(name_wonders):
			print(j, end='\n' if (i+1)%4==0 else '\t\t')
		if (i+1)%4!=0:
			print()
		print("\nInput first letters of the wonder (just ENTER to exit):", end=" ")
		first = input()
		if not first:
			exit()
		name_wonders = [i for i in name_wonders if i.lower().startswith(first.lower())]

	selected_wonder = name_wonders[0]
	w_ind = WONDERS.index(selected_wonder)

	print("Available wonder:", selected_wonder)

	print()
	w_str =  w_ind * 2
	for t in text[w_str : w_str + 2]:
		print(t)
	print()

	print("Do you want to use it? (y/n)")
	sure = input()
	if sure.lower().startswith('y'):
		break

offset = 0x8674 + 2 * w_ind
f.save.raw[offset] = f.save.raw[offset + 1] = 0xFF

if selected_wonder == "Pyramids":
	f.too_quiet(1)
	f.reelect()
	pass
elif selected_wonder == "Hanging Gardens":
	f.eliminate_barbarians()
	pass
elif selected_wonder == "Colossus":
	f.improve_barbarians()
	f.peacemaker()
	pass
elif selected_wonder == "Lighthouse":
	f.bombers_move()
	pass
elif selected_wonder == "Library Gr.":
	f.too_primitive(1)
	f.lost_civilization()
	pass
elif selected_wonder == "Oracle":
	f.capital_cash()
	pass
elif selected_wonder == "Wall Gr.":
	f.lost_civilization(False)
	pass
elif selected_wonder == "Magellan's Expedition":
	f.settlers_fly()
	pass
elif selected_wonder == "Michelangelo's Chapel":
	f.no_offence()
	pass
elif selected_wonder == "Copernicus' Observatory":
	f.too_inhospitable()
	pass
elif selected_wonder == "Shakespeare's Theatre":
	f.easy_life((6, 0))
	f.too_quiet()
	pass
elif selected_wonder == "Isaac Newton's College":
	f.elevate_types()
	pass
elif selected_wonder == "J.S.Bach's Cathedral":
	f.restore_default_types(exclude=[25])
	f.too_inhospitable(1)
	pass
elif selected_wonder == "Darwin's Voyage":
	f.spy_paradise()
	f.restore_default_types(include=[25])
	pass
elif selected_wonder == "Hoover Dam":
	f.no_radiation()
	f.noneunit(0x0)
	pass
elif selected_wonder == "Women's Suffrage":
	f.eliminate_citybusters()
	f.eliminate_movement()
	f.peacemaker()
	pass
elif selected_wonder == "Manhattan Project":
	f.disable_nukes()
	f.too_hostile()
	f.peacemaker(8)
	pass
elif selected_wonder == "United Nations":
	f.too_hostile(1)
	f.kmean()
	pass
elif selected_wonder == "Apollo Program":
	f.settlers_back()
	pass
elif selected_wonder == "SETI Program":
	f.too_primitive()
	f.clear_except_cities()
	pass
elif selected_wonder == "Cure For Cancer":
	f.easy_life()
	pass

print("# to save [1]:",end=" ")
x = input()
x = int(x) if x and all([i.isdigit() for i in x]) else 1
f.drop(x)
