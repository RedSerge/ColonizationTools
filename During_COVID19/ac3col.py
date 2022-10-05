from forcol import *
from random import random, randint, shuffle, choice 
from collections import defaultdict

BUILDING_GROUPS = [
	(45, 46, 47),
	(42, 43, 44),
	(39, 40, 41),
	(16, 17, 36, 37, 38),
	(33, 34, 35),
	(31, 32),
	(30,),
	(29,),
	(27, 28),
	(24, 25, 26),
	(21, 22, 23),
	(18, 19, 20),
	(13, 14, 15),
	(11, 12),
	(9, 10),
	(6, 7, 8),
]

BLIST = """
Stockade
Fort
Fortress
Armory
Magazine
Arsenal
Docks
Drydock
Shipyard
Town Hall
Town Hall
Town Hall
Schoolhouse
College
University
Warehouse
Warehouse Expansion
Stable
Custom House
Printing Press
Newspaper
Weaver's House
Weaver's Shop
Textile Mill
Tobacconist's House
Tobacconist's Shop
Cigar Factory
Rum Distiller's House
Rum Distillery
Rum Factory
Capitol
Capitol Expansion
Fur Trader's House
Fur Trading Post
Fur Factory
Carpenter's Shop
Lumber Mill
Church
Cathedral
Blacksmith's House
Blacksmith's Shop
Iron Works
""".strip("\n").split("\n")

FFLIST = """
Adam Smith
Jakob Fugger
Peter Minuit
Peter Stuyvesant
Jan de Witt
Ferdinand Magellan
Francisco Coronado
Hernando de Soto
Henry Hudson
Sieur De La Salle
Hernan Cortes
George Washington
Paul Revere
Francis Drake
John Paul Jones
Thomas Jefferson
Pocahontas
Thomas Paine
Simon Bolivar
Benjamin Franklin
William Brewster
William Penn
Jean de Brebeuf
Juan de Sepulveda
Bartolome de las Casas
""".strip("\n").split("\n")

CROSSLINE = "=" * 27
NATIONAL_CODES = set(range(4))
NATIONAL_NAMES = ('English', 'French', 'Spanish', 'Dutch')
DIRECTIONS = ('COLONY', 'TRIBE', 'LAND', 'SEA', 'SHORE', 'EUROPE')

STATUS_ADDR = (0xCF, 0x103, 0x137, 0x16B)

ASCEND_LVL = (0x0, 0x13, 0x14, 0x15, 0x16)
ASCEND_CHANCES = (95, 80, 75, 50)
ASCEND_NAMES = ('Initiate', 'Acolyte', 'Knight', 'Silencer', 'Master')
ASCEND_MAX = len(ASCEND_LVL) - 1

CONVERT_PROFESSIONS = (0x10, 0x14, 0x15, 0x16, 0x18)

CONTRACT_FARES = [10, 50, 100, 250, 500]

DEGRADE_UNITS = {
	0x1: 0x0,
	0x4: 0x1,
	0x5: 0x0,
	0x6: 0x0,
	0x7: 0x1,
	0x8: 0x1,
	0x9: 0x0,
	0xB: 0x0,
	0x11: 0xE,
	0x12: 0xF,
}

INTERACTIVE_UNITS = {
	0x0: None,
	0x1: 0x9,
	0x4: 0x7,
	0xB: None,
	0x11: 0x12,
}

SIGNS = [i for i in range(-1, 2) if i]

NATIVE_PROTECTION_DATA = [50, 16, 24, 32, 40]

merge_bytes = lambda x: b''.join(x)
apply_sys = lambda x, f, p: f(x)[2:].upper().zfill(p)
print_sys = lambda x, f, p: ' '.join([apply_sys(i, f, p) for i in x])
print_crd = lambda x: [j for j in x[:2]]
is_water = lambda maps, x, y: maps[0][y * 58 + x] % 32 in (25, 26)
valid_nation = lambda u, pc: (u[3] % 16) in pc
npc_nation = lambda u, pc: (u[3] % 16) in (NATIONAL_CODES - set(pc))
artillery_damaged = lambda x: (x >> 7) & 1
artillery_repair = lambda x: x & 0x7F
artillery_hurt = lambda x: x | 0x80

def foodbaskets(baskets, food, maxf=32767):
	if not baskets or not food:
		return food, baskets		
	k = [[i, j] for i, j in enumerate(baskets)]
	quantity = len(k)
	shuffle(k)
	k, f = sorted(k, key=lambda x:-x[1]), []
	
	while True:
		amount = max(1, food // len(k))		
		for n in range(quantity, 0, -1):
			if not food:
				break
			i = k[n - 1]
			capacity = maxf - i[1]
			actual_load = min(amount, capacity, food)
			i[1] += actual_load
			food -= actual_load
			if i[1] == maxf:
				f.append(i)
				del k[k.index(i)]
		if not food or not k:
			break
	f.extend(k)
	return food, [i[1] for i in sorted(f, key=lambda x:x[0])]

def ff_kidnaplogic(ffs_origin, veteran):
	ffs = [[int(i) for i in j] for j in ffs_origin]
	ffsi = [[i for i, v in enumerate(j) if (i > 6) and (v == (0 if n else 1))] for n, j in enumerate(ffs)]
	important = {}
	for i in ffsi[0]:
		row = []
		for n, j in enumerate(ffsi[1:]):
			if i in j:
				row.append(n)
		important[i] = row
	if not important:
		return None
	priority = [i for i in important if important[i]] if veteran else None
	if not priority:
		priority = list(important.keys())
	x = choice(priority)
	ffs[0][x] = 0
	enriched = None
	if important[x]:
		enriched = choice(important[x]) + 1
		ffs[enriched][x] = 1
	ffs = [''.join([str(i) for i in j]) for j in ffs]
	return ffs, enriched, 31 - x

def royal_hurt(soldiers, cavalry, artillery, ships, rounds=32):
	values = [[soldiers, 'S'], [cavalry, 'C'], [artillery, 'A'], [ships, 'N']]
	values = [[max(0, i[0]), i[1]] for i in values]
	
	artillery_round = 0
	
	while rounds or artillery_round:
		
		special_case = (not rounds and artillery_round)
		
		at_stake = []
		for pos, value in enumerate(values):
			count, mark = value
			if special_case and mark == 'A':
				artillery_round, rounds = 0, 1
				continue
			if (count > 1) or (mark != 'N' and count > 0):
				at_stake.append(values[pos])
		
		if not at_stake:
			break
		
		while True:
			x = choice(at_stake)
			mark = x[1]
			if len(at_stake) == 1 or mark != 'N' or random() < 0.25:
				break
		
		if mark == 'A':
			if artillery_round == 0:
				artillery_round = 1
			else:
				x[0] -= 1
				artillery_round = 0
		elif mark == 'C':
			x[0] -= 1
			values[0][0] += 1
		else:
			x[0] -= 1
			
		rounds -= 1
	
	values[0][0] = min(32767, values[0][0])
	return [i[0] for i in values]

def parse_f(f):
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
	split_units = [units[i : i + 28] for i in range(0, len(units), 28)]
	split_tribes = [tribes[i : i + 18] for i in range(0, len(tribes), 18)]
	split_colonies = [colonies[i : i + 202] for i in range(0, len(colonies), 202)]
	split_nations = [nations[i: i + 316] for i in range(0, len(nations), 316)]
	
	return intro, split_colonies, split_units, split_nations, split_tribes, middle, split_maps, final

def unify_f(f, bunch):
	intro, split_colonies, split_units, split_nations, split_tribes, middle, split_maps, final = bunch
	f.raw = merge_bytes([
		intro,
		merge_bytes(split_colonies),
		merge_bytes(split_units),
		merge_bytes(split_nations),
		merge_bytes(split_tribes),
		middle,
		merge_bytes(split_maps),
		final,
	])

def rank(actor):
	current_state = actor[2]
	max_lvl = len(ASCEND_LVL) - 1
	try:
		current_lvl = ASCEND_LVL.index(current_state)
	except ValueError:
		current_lvl = 0
	current_rank = ASCEND_NAMES[current_lvl]
	print(f"The rank of the assassin is: {current_rank}")
	return current_lvl

def ascend(actor, current_lvl):
	if current_lvl >= ASCEND_MAX:
		print(f"Further growth is not possible; time to put the skills in action")
	elif randint(0, 99) < ASCEND_CHANCES[current_lvl]:
		current_lvl += 1
		current_rank = ASCEND_NAMES[current_lvl]
		print(f"The assassin has been promoted upon finishing the task and is known now as the {current_rank}")
		actor[2] = ASCEND_LVL[current_lvl]
	return current_lvl

def search(bunch, pc, task_data):
	intro, colonies, units, nations, tribes, middle, maps, final = bunch
	
	converts = []
	assassin = None
	
	for u in units:
		if valid_nation(u, pc):
			if u[2] == 0x0 and u[23] == 0x1b:
				converts.append(u)
			elif u[23] == 0x1d:
				assassin = u
				break
	
	if not assassin:
		print("There's no assassin to control")
		if not converts:
			print("There's no converts to draft yet")
			return
		v = prompt("The convert has been found. Do you want him to start his journey towards assassins ranks? (y/n) ")
		if v:
			x = choice(converts)
			x[23]=0x1D
			print(f"He deserts from his floak, ascending as the assassin at ({x[0]}, {x[1]})")
		return
	print(f"There's the assassin at ({assassin[0]}, {assassin[1]})")
	
	current_lvl = rank(assassin)
	
	if task_data is None:
		print("Can not provide assassin with the task")
		return assassin, current_lvl
	crds, how = task_data
	x, y = crds
	success = achieved_task(assassin[0], assassin[1], x, y, how=='EUROPE')
	success_str = "has been" if success else "is not"
	print(f"The previous task {success_str} accomplished at {x, y} ({how})")
	
	if success:
		ascend(assassin, current_lvl)
		result = force_task(bunch)
		if not result:
			print("Failed to create new task")
			return assassin, current_lvl
		crds, how = result
		x,y = crds
		print(f"The new task is to reach the {how} at {x, y}")
	
	return assassin, current_lvl
			
task_supp = lambda x, x0, y0: [(i[0], i[1]) for i in x if i[0] != x0 and i[1] != y0]
coords = lambda x, x0, y0: [(i[0], i[1], i) for i in x if vicinity(x0, y0, i[0], i[1], 1)]
coords_units = lambda x, x0, y0, pc: [(i[0], i[1], i) for i in x if vicinity(x0, y0, i[0], i[1], 1) and npc_nation(i, pc) and i[2] in DEGRADE_UNITS]
coords_at_me = lambda x, u, x0, y0: [(i[0], i[1], i) for i in x if i != u and i[0] == x0 and i[1] == y0 and i[2] in INTERACTIVE_UNITS]
coords_show = lambda x: [(i[0], i[1]) for i in x]
vicinity = lambda x, y, xt, yt, r: (x >= xt - r) and (x <= xt + r) and (y >= yt - r) and (y <= yt + r) 
in_eu = lambda x, y: (x > 56 or x < 1 or y > 70 or y < 1)

def achieved_task(x, y, xt, yt, eu = False, r = 1):
	return in_eu(x, y) if eu else vicinity(x, y, xt, yt, r)

def force_task(bunch):
	result = task(bunch)
	if result:
		crds, how, code = result
		with open("ac3.task", "w", encoding="UTF-8") as f:
			f.write(code)
		return crds, how

def load_task(bunch):
	try:
		with open("ac3.task", encoding="UTF-8") as f:
			c = f.read()
			x, y, i = int(c[1:3], 16), int(c[3:5], 16), int(c[:1])
			return [x, y], DIRECTIONS[i]
	except IOError:
		return force_task(bunch)

def task(bunch, x0=None, y0=None, in_euro=False):
	intro, colonies, units, nations, tribes, middle, maps, final = bunch
	
	euro_place = [] if in_euro else [0, 0]
	
	col_xy = task_supp(colonies, x0, y0)
	tribe_xy = task_supp(tribes, x0, y0)
	settlements = set(col_xy) | set(tribe_xy)
	
	land = []
	water = []	
	shore = []
	
	for y in range(2, 70):
		for x in range(2, 56):
			if (x == x0 and y == y0) or ((x, y) in settlements):
				continue
			if is_water(maps, x, y):
				water.append((x, y))
			else:
				land.append((x, y))
				is_shore = False 
				for iy in SIGNS:
					for ix in SIGNS:
						if is_water(maps, x + ix, y + iy):
							is_shore = True
							break
					if is_shore:
						shore.append((x, y))
						break
	
	results = [col_xy, tribe_xy, land, water, shore, euro_place]
	final_ids = [i for i in range(len(DIRECTIONS)) if results[i]]

	if not final_ids:
		print("FATAL ERROR: no destination found")
		return
	
	final_id = choice(final_ids)
	final_choice = choice(results[final_id])
	encode = f"{final_id}{apply_sys(final_choice[0], hex, 2)}{apply_sys(final_choice[1], hex, 2)}"
	
	return final_choice, DIRECTIONS[final_id], encode

def versus_mayor(colonies, colonies_nearby):
	if not colonies_nearby:
		return []
	
	col_by_nat = defaultdict(list)
	
	for i in colonies:
		nation = i[26]
		if nation in NATIONAL_CODES:
			col_by_nat[nation].append((i[0], i[1], i))
	
	col_by_one = [col_by_nat[i][0] for i in NATIONAL_CODES if len(col_by_nat[i]) == 1]
	return [i for i in col_by_one if i in colonies_nearby]

submenu = lambda x: ([print(f"{i+1}) {j[0], j[1]};", end="\t" if (i + 1) % 4 != 0 else "\n") for i, j in enumerate(x)], print() if len(x) % 4 != 0 else None)

def menu_input(objects, prompt):
	try:
		return objects[int(input(prompt)) - 1]
	except (ValueError, IndexError):
		pass

magnitude = lambda lvl: 2 ** (lvl - 2)

def ask_kindly(cols):
	choice = None if len(cols) > 1 else cols[0]
	while not choice:
		print("Please provide precise colony coordinates (choose a number):")
		submenu(cols)
		choice = menu_input(cols, "Number is: ")
		print()
	return choice

def act_natives(act_args):
	level, tribes_nearby, bunch, pc = act_args
	intro, split_colonies, split_units, split_nations, split_tribes, middle, split_maps, final = bunch
	
	all_colonies = [c for c in split_colonies if c[26] in pc]
	
	baskets = []
	for c in all_colonies:
		mode = col(extra=c)
		baskets.append(mode.short(0x9A, signed=True)[0])
	
	max_protection = NATIVE_PROTECTION_DATA[level]
	
	food = 0
	for t in tribes_nearby:
		increment = max_protection - t[2][4]
		if increment <= 0:
			continue
		t[2][4] = max_protection
		food += increment * NATIVE_PROTECTION_DATA[0]
	
	food_left, baskets = foodbaskets(baskets, food)
	
	for n, c in enumerate(all_colonies):
		mode = col(extra=c)
		mode.save_short(0x9A, [baskets[n]], signed=True)
	
	if food == 0:
		print("No protection is needed at the moment")
	else:
		print(f"Natives brought {food - food_left} food units to feed the colonists for the provided protection")

def act_contract(act_args):
	level, bunch, pc = act_args
	intro, split_colonies, split_units, split_nations, split_tribes, middle, split_maps, final = bunch
	p = choice(pc)
	value = randint(CONTRACT_FARES[0], CONTRACT_FARES[level])
	mode = col(extra=split_nations[p])
	current_value = mode.short(0x2A, signed=True, length=4)[0]
	cash = min(2147483647, current_value + value)
	mode.save_short(0x2A, [cash], signed=True, length=4)
	print("The contract has been fulfilled")
	if current_value < cash:
		print(f"The {NATIONAL_NAMES[p]} cash grows from {current_value} to {cash} (by {cash - current_value})")

def hard_labor(level, upon, lambda_upon, direct=False):
	m = level if direct else magnitude(level)
	current = 0
	while True:
		c = choice(upon)
		if not lambda_upon(c):
			del upon[upon.index(c)]
		current += 1
		if current >= m or not upon:
			break
	return current
	
def act_promote(act_args):
	
	def change(x):
		x[2][23] = choice(CONVERT_PROFESSIONS)
	
	level, colonists = act_args
	current = hard_labor(level, colonists, change)
	s = '' if current == 1 else 's'
	print(f"{current} convert{s} found the new job{s}")

def act_repair(act_args):
	
	def change(x):
		x[2][4] = artillery_repair(x[2][4])
	
	level, artillery = act_args
	current = hard_labor(level, artillery, change)
	s = 'y has' if current == 1 else 'ies have'
	print(f"{current} artiller{s} been successfully repaired")

def global_act_change(x):
	x[2][2] = INTERACTIVE_UNITS[x[2][2]]
	
def global_act_demote(x):
	unit_type = x[2][2]
	if unit_type == 0xB:
		if not artillery_damaged(x[2][4]):
			x[2][4] = artillery_hurt(x[2][4])
			return
	new_type = DEGRADE_UNITS[unit_type]
	x[2][2] = new_type
	return new_type not in DEGRADE_UNITS
	
def act_train(act_args):
	level, army = act_args
	current = hard_labor(level, army, global_act_change)
	print(f"Promoted units: {current}")
	
def act_navy(act_args):
	level, frigate = act_args
	current = hard_labor(level, frigate, global_act_change)
	print(f"New Man-O-Wars: {current}")
	
def act_ff(act_args):
	level, colonies_nearby, bunch, pc = act_args
	intro, split_colonies, split_units, split_nations, split_tribes, middle, split_maps, final = bunch
	menu_choice = ask_kindly(colonies_nearby)
	nations = [menu_choice[2][26]]
	nations.extend(pc)
	nation_in_question_code = nations[0]
	nation_in_question_name = NATIONAL_NAMES[nation_in_question_code]
	
	ffs = [print_sys(col(extra=split_nations[n]).short(0x7, length=4), bin, 32) for n in nations]
	ffs_result = ff_kidnaplogic(ffs, level > 3)
	
	if not ffs_result:
		print(f"The {nation_in_question_name} Congress Hall seems to be empty")
		return
	
	act_ff_support = lambda code, line: col(extra=split_nations[code]).save_short(0x7, [int(ffs[line], 2)], length=4)
	
	ffs, enriched, ff_index = ffs_result
	act_ff_support(nation_in_question_code, 0)
	print(f"The Founding Father, {FFLIST[ff_index]}, has been disposed recently from the {nation_in_question_name} Congress;")
	if enriched is None:
		print("Noone heard of him ever since")
	else:
		nation_in_benefit_code = nations[enriched]
		nation_in_benefit_name = NATIONAL_NAMES[nation_in_benefit_code]
		act_ff_support(nation_in_benefit_code, enriched)
		print(f"Under the death threats this person eventually was forced to flee and join the {nation_in_benefit_name} Congress")
	
def act_fire(act_args):
	level, colonies_nearby = act_args
	menu_choice = ask_kindly(colonies_nearby)
	city = col(extra=menu_choice[2])
	buildings = [i for i in print_sys(city.short(0x84, length=6), bin, 48)]
	available = [i for i, v in enumerate(buildings) if i >= 6 and v != '0']
	
	if level > 3:
		city.save_short(0x92, [0])
		print("All hammers are gone")
	
	if not available:
		print(f"The colony has already been ruined to the core")
		return
	
	building = choice(available)
	group_to_blow = [i for i in [b for b in BUILDING_GROUPS if building in b][0] if i in available]
	building = BLIST[47 - group_to_blow[0]]
	for i in group_to_blow:
		buildings[i] = '0'	
	buildings_updated = int(''.join(buildings), 2)
	city.save_short(0x84, [buildings_updated], length=6)
	print(f"The {building} has been blown to smithereens by an unknown force")
	
def act_taxes(act_args):
	level, bunch, pc = act_args
	intro, split_colonies, split_units, split_nations, split_tribes, middle, split_maps, final = bunch
	for p in pc:
		mode = col(extra=split_nations[p])
		tax = mode.short(1, signed = True, length = 1)[0]
		new_tax = max(-75, tax - randint(3, 7 if level < 4 else 21))
		if tax == new_tax:
			print(f"The {NATIONAL_NAMES[p]} tax rate is already at its lowest")
		else:
			mode.save_short(1, [new_tax], True, 1)
			print(f"The {NATIONAL_NAMES[p]} tax rate has changed from {tax} to {new_tax} %")
	
def act_massacre(act_args):
	current = hard_labor(8, act_args[0], global_act_demote, True)
	s = '' if current == 1 else 's'
	print(f"{current} successful strike{s}")
	
def act_royal(act_args):
	mode = col(extra=act_args[0][0])
	soldiers, cavalry, ships, artillery = mode.short(0x6A, 0x71, True)
	print(f"Royal forces before: {soldiers} Regulars, {cavalry} Cavalry, {artillery} Artillery, {ships} Man-O-Wars")
	soldiers, cavalry, artillery, ships = royal_hurt(soldiers, cavalry, artillery, ships)
	mode.save_short(0x6A, [soldiers, cavalry, ships, artillery], True)	
	print(f"Royal forces after: {soldiers} Regulars, {cavalry} Cavalry, {artillery} Artillery, {ships} Man-O-Wars")
	
def act_mayor(act_args):
	colonies_alone, bunch = act_args
	choice = ask_kindly(colonies_alone)
	nation = choice[2][26]
	mode = col(extra=bunch[0])
	if mode.hex(STATUS_ADDR[nation])[0] == 2:
		print(f"The {NATIONAL_NAMES[nation]} viceroy has already been forced out of the office")
	else:
		mode.save_hex(STATUS_ADDR[nation], [2])
		print(f"The {NATIONAL_NAMES[nation]} viceroy is gone")

def menu(assassin, pc, level, colonies_nearby, tribes_nearby, units_nearby, units_at_me, colonies_alone, europe_status, bunch):
	pts = []
	print(CROSSLINE)
	
	if tribes_nearby:
			pts.append(("Protect natives", act_natives, (level, tribes_nearby, bunch, pc), 93))
	if colonies_nearby:
		pts.append(("Execute a contract", act_contract, (level, bunch, pc), 86))
		if level > 2:
			pts.append(("Kidnap the Founding Father", act_ff, (level, colonies_nearby, bunch, pc), 49))
			pts.append(("Blow up the colony buildings", act_fire, (level, colonies_nearby), 42))
	if units_nearby:
			pts.append(("Ravage the enemy units", act_massacre, (units_nearby,), 27))
	if colonies_alone:
			pts.append(("Assassinate the Mayor", act_mayor, (colonies_alone, bunch), 12))
	if units_at_me:
		colonists, artillery, army, frigate = [], [], [], []
		for u in units_at_me:
			utype = u[2][2]
			if utype == 0x0 and u[2][23] in (0x1b, 0x1d):
				colonists.append(u)
			elif utype == 0x1 or utype == 0x4:
				army.append(u)
			elif utype == 0xB and artillery_damaged(u[2][4]):
				artillery.append(u)
			elif utype == 0x11:
				frigate.append(u)
		if colonists:
			pts.append(("Promote converts", act_promote, (level, colonists), 78))
		if artillery:
			pts.append(("Repair an artillery", act_repair, (level, artillery), 71))
		if army:
			pts.append(("Train the army", act_train, (level, army), 64))
		if frigate:
			pts.append(("Improve a frigate", act_navy, (level, frigate), 56))
	if europe_status:
		pts.append(("Decrease taxes rate", act_taxes, (level, bunch, pc), 34))
		if level > 3:
			pts.append(("Massacre the Royal Army", act_royal, (bunch,), 19))
	
	for n,p in enumerate(pts):
		print(f"{n + 1}) {p[0]}")
	
	print(CROSSLINE)
	selection = menu_input(pts, "Enter the action number, ENTER - nothing to do: ")
	if not selection:
		return
	
	print(CROSSLINE)
	if randint(0, 99) < selection[3]:
		selection[1](selection[2])
	else:
		print("The task has been failed or the target has not been found")
	print()
	assassin[2] = 0x0
	print("The assassin has lost its power and need to accomplish more tasks to regain abilities")
	input("< Press ENTER to exit >")

def action(bunch, ass, lvl, pc):
	intro, colonies, units, nations, tribes, middle, maps, final = bunch
	
	x, y = ass[0], ass[1]
	
	europe_status = in_eu(x, y)
	colonies_nearby, tribes_nearby, units_nearby, units_at_me, colonies_alone = [], [], [], [], []
	
	if not europe_status:
		if lvl >= 1:
			colonies_nearby = coords(colonies, x, y)
			tribes_nearby = coords(tribes, x, y)
		if lvl >= 2:		
			units_at_me = coords_at_me(units, ass, x, y)
		if lvl >= 4:
			units_nearby = coords_units(units, x, y, pc)
			colonies_alone = versus_mayor(colonies, colonies_nearby)
	else:
		if lvl <= 2:
			europe_status = False
	
	menu(ass, pc, lvl, colonies_nearby, tribes_nearby, units_nearby, units_at_me, colonies_alone, europe_status, bunch)		

def pcs(f):	
	npc_status = [f.hex(i)[0] for i in STATUS_ADDR]
	pc = [pos for pos, state in enumerate(npc_status) if not state]
	return pc

def main():
	f = col(0)
	b = parse_f(f)
	
	pc = pcs(f)
	result = search(b, pc, load_task(b))
	if not result:
		return
	assassin, lvl = result
	
	if lvl > 0:
		action(b, assassin, lvl, pc)
	
	unify_f(f, b)
	f.save(0)


if __name__ == '__main__':
	main()
