import mss
import cv2
import numpy as np
import pyautogui
import time
from pandas import read_excel as re
import sys

mf = "~\Documents\mercenaries_tracker.xlsx"
STAGES_OF_GEAR = [0,100,150,175]
STAGES_OF_ABILITY = [0,50,125,150,150]
STAGES_OF_REWARD = [50,0,50,50,50,50,0] + [60]*5+ [70,70,70,70,75,80]
if len(sys.argv) > 1:
	print("number_of_mysterious_challenger: ", sys.argv[1])
	number_of_mysterious_challenger = int(sys.argv[1])
else:
	number_of_mysterious_challenger = 2

farm_blackhand = False
eot_pad = 1
monik=3
screenshot = "screenshot.png"
img = ""
gray_img = ""
pictures_brute_force = ["victory.png", "reward.png", "keep.png", "visit.png", "quests.png","reveal.png", "battlespoils.png","ok.png","start1.png"]
abilities = ["sneed","valeera","kurtrus2", "kurtrus","eudora2","eudora","illidan","mannoroth"]# MAINTAIN
#0 = drag
#1 = no drag
#2 = select option
#ONLY ADD TO THIS
ability_database = {"valeera":0, "sneed":0, "mannoroth":0,"kurtrus2":1,"kurtrus":0, "illidan":0,"eudora":0,"eudora2":3,"eudora3":1, "jaraxxus":0,"jaraxxus2":1,"jaraxxus3":1,"rokara2":0, "rokara":0,"alexstrasza3": 0,"alexstrasza": 0,"saurfang3": 1,"saurfang2": 1, "saurfang": 0, "brightwing3":1,"brightwing2":1,"brightwing":0,"guldan":0,"guldan3":0,"smite": 0, "smite2": 1, "krush": 0, "sylvanas": 0, "sylvanas2": 0, "voone": 0, "voone2": 1, "garrosh3":1, "garrosh2": 1, "garrosh": 0, "cookie": 0, "cookie2": 1, "tirion2": 0, "tirion": 0, "rexxar": 0, "rexxar2": 0, "rexxar3": 2, "gruul": 0, "gruul2": 1, "rathorian": 0, "rathorian2": 0}
def battle(action = 0):
	if action == 0: #drag
		time.sleep(0.2)
		pyautogui.dragTo(1920/2 - 50, 275, button='left', duration=0.05)
		time.sleep(0.05)
		pyautogui.click()
		time.sleep(eot_pad)
		pyautogui.moveTo((50,50))
	elif action == 1: #just click
		pyautogui.moveTo((50,50))
		time.sleep(eot_pad)
	elif action == 2: #select option
		time.sleep(0.2)
		pyautogui.click((1920/2, 1080/2))
		time.sleep(eot_pad)
	elif action == 3: #select option
		time.sleep(0.2)
		pyautogui.click((1920/2+70, 1080/2))
		time.sleep(0.2)
		pyautogui.moveTo((50,50))
		time.sleep(eot_pad)
			

		
def screen():
	sct = mss.mss()
	global img
	global gray_img
	try:
		sct.shot(mon=monik, output=screenshot)
		img = cv2.imread(screenshot)
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	except:
		print("screenshot failed")
	
def brute_force_find_what_to_click():
	for picture in pictures_brute_force:
		pyautogui.moveTo((50,50))
		print("Trying:", picture)
		if picture == "reward.png":
			if find_picture(picture) == 0:
				return 0
		elif picture == "visit":
			global mode
			if mode != "mc":
				if check(picture) == 0:
					return 0
		elif check(picture) == 0:
			if picture == "reveal.png":
				time.sleep(2)
				pyautogui.click(button="left")
				pyautogui.click(button="right")
				time.sleep(1)
				pyautogui.click(button="left")
				pyautogui.click(button="right")
				return 0
				
			return 0
		
	return 1

def find_mission():
	for picture in finding_mission:
		if pyautogui.locateOnScreen(picture):
			pyautogui.click(picture)
			return 0
		
		return 1
		
def find_picture(picture):
	print("find_picture: ", picture)
	#time.sleep(2)
	try:
		if pyautogui.locateOnScreen(picture):
			pyautogui.click(picture)
			if picture == "reveal.png":
				time.sleep(2)
				pyautogui.click()
			return 0
	except TypeError:
		pass
	return 1

def fp(picture):
	print("fp picture: ", picture)
	#time.sleep(2)
	if pyautogui.locateOnScreen(picture):
		return 0
	return 1

def post_play():
	print("entering post play")
	
	for i in range(0,240):
		if check("03played.png") == 0:
			while check("play.png") == 0:
				continue
			break
		time.sleep(0.1)
	
	print("exiting post play")
		
def check(picture,result_override=0.75, take_sh=True, click=True):
	print("checkpicture: ", picture)
	#time.sleep(2)
	if take_sh:
		screen()
		time.sleep(0.01)
	try:
		template = cv2.imread(picture,
							  cv2.IMREAD_GRAYSCALE)
		result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
		w, h = template.shape[::-1]
		loc = np.where(result >= result_override)
		if len(loc[0]) != 0:
			j = 0
			for pt in zip(*loc[::-1]):
				x = int((pt[0] * 2 + w) / 2)
				y = int((pt[1] * 2 + h) / 2)
			
			if click:
				pyautogui.click((x,y))
				time.sleep(0.25)
			return 0
	except OSError:
		print("Check failed with OSError")
		
	return 1
def crc(a1,a2,a3,g1,g2,g3):

    assert a1 >= 1 and a1 <= len(STAGES_OF_ABILITY)
    assert a2 >= 1 and a2 <= len(STAGES_OF_ABILITY)
    assert a3 >= 1 and a3 <= len(STAGES_OF_ABILITY)
    assert g1 >= 1 and g1 <= len(STAGES_OF_GEAR)
    assert g2 >= 1 and g2 <= len(STAGES_OF_GEAR)
    assert g3 >= 1 and g3 <= len(STAGES_OF_GEAR)
  
    rc = int(sum(STAGES_OF_ABILITY[a1:]) + sum(STAGES_OF_ABILITY[a2:]) + sum(STAGES_OF_ABILITY[a3:]) +
    sum(STAGES_OF_GEAR[g1:]) + sum(STAGES_OF_GEAR[g2:]) + sum(STAGES_OF_GEAR[g3:]))
    
    return rc
    
def rrt(s):
    assert s >= 0 and s <=len(STAGES_OF_REWARD)
    rr= sum(STAGES_OF_REWARD[s:])
    
    return rr

def final_calc(df):
	crc_rc = crc(df["a1"],df["a2"],df["a3"],df["g1"],df["g2"],df["g3"])
	rrt_rc = rrt(df["r"])
	c = df["c"]
	
	return crc_rc - rrt_rc - c
	
def token_check():
	screen()
	try:
		names=["diablo", "thrall", "jaina", "ragnaros","lich_king", "malfurion","mukla","natalie"]
		for name in names:
			
			if check(name+"_token.png",take_sh=False) == 0:
				print("found",name,"tokens")
				df = re(mf)
				df=df.set_index('index')
				df[name]["c"]+=10
				df.to_excel(mf)
				if final_calc(df[name]) <= 0:
					print(name, "IS DONE!!!!!!!")
				else:
					print(name, "needs", final_calc(df[name]))
				break
	except PermissionError:
		print("CLOSE THE SPREAD SHEET!")

def setup_first_time(zone):
	print("setup_first_time")
	todo = []
	setup = False
	reset()
	pyautogui.click((50,50))
	while not setup:
		print("loop")
		if check("playhs.png") == 0:
			pyautogui.click((50,50))
			time.sleep(12)
			find_picture("maximize.png")

		if check("mercenaries.png") == 0:
			pyautogui.click((50,50))
			time.sleep(6)
			
		if check("flightpoint.png") == 0:
			time.sleep(6)
		
		if exit() == 0:
			pyautogui.click((50,50))
			time.sleep(6)
			reset()
				
		if zone == "felwood":
			if (check("felwood.png") == 0 or check("felwood2.png") == 0) and (check("normal.png") == 0 or check("normal2.png") == 0):
				time.sleep(2)
				if check("start2.png") == 0:
					setup = True
		
		elif zone == "barrens":
			if (check("the_barrens.png") == 0 or check("the_barrens2.png") == 0) and (check("heroic.png") == 0):
				time.sleep(2)
				if check("start2.png") == 0:
					setup = True
				
			
		

def find_possible_challenger():
	searching = True
	i=0
	while searching and i < 25:
		pyautogui.click((1920/2, 1080/2))
		if check("possible_mysterious_challenger.png") == 0:
			print("possible_mysterious_challenger_position:",pyautogui.position())
			searching = False
			
		pyautogui.scroll(10)
		i+=1 
	
	for i in range(0,i):
		pyautogui.scroll(-10)
		
	if pyautogui.position()[0]< 775:
		return 0 #left
	else:
		return 1 #right
		
			
def exit():
	print("in exit")
	global done
	global failsafe
	time.sleep(4)
	if check("view_party.png") == 0:
		time.sleep(4)
		if check("retire2.png") == 0:
			time.sleep(4)
			if check("retire.png") == 0:
				done = False
				time.sleep(2)
				pyautogui.click(button="left")
				pyautogui.click(button="right")
				time.sleep(2)
				pyautogui.click(button="left")
				pyautogui.click(button="right")
				time.sleep(2)
				check("battlespoils.png")
				pyautogui.click(button="left")
				pyautogui.click(button="right")
				
				return 0
				
	return 1
		
		
		
def battle_loop(picture = "you.png"):
	print(picture)
	if fp(picture) == 0:
		print("in")
		taken_turn = False
		i=0
		time.sleep(1)
		screen()
		while (check("victory.png",take_sh=False) == 1 and check("defeat.png",take_sh=False) == 1) and i <= 30 and check("pick_treasure.png", 0.6,take_sh=False) == 1 and check("pick_treasure2.png", 0.6,take_sh=False) == 1 and check("pick_treasure3.png", 0.6,take_sh=False) == 1 and fp("rewards.png") == 1:
			screen()
			check("03played.png",take_sh=False, result_override=0.6)
			if check("1st.png", take_sh=False, result_override=0.6, click=False) == 1:
				i+=1
				time.sleep(1)
				continue
				
			
			time.sleep(1)
			screen()	

			for ability in abilities:
				if check(ability+".png", take_sh=False) == 0:
					battle(ability_database[ability])
					i=0
					taken_turn = True
					break 
					
			if taken_turn == True:
				taken_turn = False
				continue
							
			if check("demon_summon.png",take_sh=False) == 0:
				time.sleep(0.1)
				pyautogui.dragTo(1920/2 - 50, 275, button='left', duration=0.05)
				time.sleep(0.05)
				pyautogui.click()
				time.sleep(eot_pad)
				pyautogui.moveTo((50,50))
				taken_turn = True
				i=0
				continue
			
			if check("sword.png",take_sh=False) == 0:
				time.sleep(0.2)
				pyautogui.dragTo(1920/2 - 50, 275, button='left', duration=0.05)
				time.sleep(0.05)
				pyautogui.click()
				time.sleep(eot_pad)
				taken_turn = True
				pyautogui.moveTo((50,50))
				i=0
				continue
			
			if check("potato.png",take_sh=False) == 0:
				time.sleep(eot_pad)
				taken_turn = True
				pyautogui.moveTo((50,50))
				i=0
				continue
			
			i+=1
			if taken_turn == False:
				time.sleep(1)
				pyautogui.click((1550, 1080/2 - 50))
				pyautogui.click(button="right")
			else:
				taken_turn = False
				
			
			
		time.sleep(1)
		pyautogui.click(button="right")
		pyautogui.click((1550, 1080/2 - 50))
		
		return 0
	return 1

def swirl_icon(exit_on_find = True):
	global number_of_mysterious_challenger
	if check("swirl_icon.png") == 0 or check("swirl_icon2.png") == 0 or check("swirl_icon3.png") == 0:
		time.sleep(2)
		pyautogui.click((50,50))
		time.sleep(2)
		check("swirl_icon.png")
		check("swirl_icon2.png")
		time.sleep(2)
		pyautogui.click((50,50))
		time.sleep(2)
		check("swirl_icon.png")
		check("swirl_icon2.png")
		time.sleep(2)
		pyautogui.click((50,50))
		time.sleep(2)
		check("swirl_icon.png")
		check("swirl_icon2.png")
		if check("mysterious_stranger.png") == 0:
			if check("visit.png") == 0:
				time.sleep(2)
				if check("pick_a_visitor.png") == 0:
					pyautogui.click((1920/2 - 350, 1080/2 - 100))
					time.sleep(1)
					check("choose.png")
					number_of_mysterious_challenger+=1
					time.sleep(4)
					pyautogui.click()
					if exit_on_find:
						exit()
					return 0
		else:
			if check("visit.png", click=False) == 1 and check("pickup.png", click=False) == 1 and check("warp.png", click=False) == 1:
				print("premature find")
				return 1
			else:
				if exit_on_find:
					exit()
				else:
					check("visit.png") 
					check("pickup.png", take_sh = False)
					check("warp.png", take_sh = False)
					
				return 0 
	
	
	return 1
				
def find_what_to_do_mc(side):
	global done
	global number_of_mysterious_challenger
	#print("searching for mysterious_challenger")
	#side = find_possible_challenger()
			
	if swirl_icon() == 0:
		done = False
		return 0
	if check("pick_a_visitor.png") == 0:
		done = False
		pyautogui.click((1920/2 - 350, 1080/2 - 100))
		time.sleep(1)
		check("choose.png")
		number_of_mysterious_challenger+=1
		time.sleep(4)
		pyautogui.click()
		time.sleep(4)
		exit()
		return 0
		
	brute_force_find_what_to_click()
	if check("play.png") == 0:
		return 0
		#post_play()
	
	if battle_loop("you2.png") == 0:
		return 0
		
		
	if check("need_to_select.png") == 0:
		if check("play.png") == 0:
			return 0
					
		elif check("visit.png") == 0:
			return 0
		
		elif check("reveal.png") == 0:
			time.sleep(2)
			pyautogui.click(button="left")
			pyautogui.click(button="right")
			time.sleep(1)
			pyautogui.click(button="left")
			pyautogui.click(button="right")
			return 0
			
		else:
			if side == 0: #left
				for i in range(350,1920-350,50):
					pyautogui.click((i,1080/2-50))
					pyautogui.click((50,50))
					if swirl_icon() == 0:
						return 0
					elif check("play.png") == 0:
						return 0
					elif check("visit.png") == 0:
						return 0
					
					elif check("reveal.png") == 0:
						time.sleep(2)
						pyautogui.click()
						return 0
			else: #right 
				for i in range(int(1920*0.6),350,-50):
					pyautogui.click((i,1080/2-50))
					pyautogui.click((50,50))
					if swirl_icon() == 0:
						return 0
					elif check("play.png") == 0:
						return 0
					elif check("visit.png") == 0:
						return 0
					
					elif check("reveal.png") == 0:
						time.sleep(2)
						pyautogui.click(button="left")
						pyautogui.click(button="right")
						time.sleep(1)
						pyautogui.click(button="left")
						pyautogui.click(button="right")
						return 0
						return 0
						
	if check("rewards2.png") == 0:
		time.sleep(1)
		pyautogui.click((1000, 317))
		time.sleep(0.25)
		pyautogui.click((640, 435))
		time.sleep(0.25)
		pyautogui.click((760, 850))
		time.sleep(0.25)
		pyautogui.click((1250, 850))
		time.sleep(0.25)
		pyautogui.click((1340, 460))
		time.sleep(1)
		#screen()
		#token_check()				
		pyautogui.click((953,555))
		pyautogui.click()
		time.sleep(4)
		pyautogui.click()
		time.sleep(4)
		check("ok.png")
		time.sleep(4)
		done = False
		return 0
	
	if check("merc_collection.png", click=False) == 0:
		pyautogui.click((1450, 850))
		time.sleep(0.5)
		pyautogui.click((1920/2 - 150 , 1080/2 +100))
		return 0
	
	#if check("lordbanehollow.png") == 0:
	#	if check("start2.png") == 0:
	#		time.sleep(4)
	#		side = find_possible_challenger()
	if check("pick_treasure.png") == 0 or check("pick_treasure2.png",0.6,take_sh=False) == 0 or check("pick_treasure3.png", 0.6,take_sh=False) == 0:
		pyautogui.click((1920/2, 1080/2))
		time.sleep(0.01)
		check("take.png",)
		check("take2.png")
		return 0
		
	return 1

def find_what_to_do_blackhand(side):
	global done
	global number_of_mysterious_challenger
	#print("searching for mysterious_challenger")
	
			
	if swirl_icon(False) == 0:
		done = False
		side = find_possible_challenger()
		return 0
		
	if check("pick_a_visitor.png") == 0:
		done = False
		pyautogui.click((1920/2 - 350, 1080/2 - 100))
		time.sleep(1)
		check("choose.png")
		number_of_mysterious_challenger+=1
		time.sleep(4)
		pyautogui.click()
		time.sleep(4)
		return 0
		
	brute_force_find_what_to_click()
	if check("play.png") == 0:
		return 0
		#post_play()
	
	if battle_loop("you3.png") == 0:
		return 0
		
		
	if check("need_to_select.png") == 0:
		if check("play.png") == 0:
			return 0
					
		elif check("visit.png") == 0:
			return 0
		
		elif check("reveal.png") == 0:
			time.sleep(2)
			pyautogui.click(button="left")
			pyautogui.click(button="right")
			time.sleep(1)
			pyautogui.click(button="left")
			pyautogui.click(button="right")
			return 0
			
		else:
			if side == 0: #left
				for i in range(450,1920-450,50):
					pyautogui.click((i,1080/2-50))
					if swirl_icon() == 0:
						return 0
					elif check("play.png") == 0:
						return 0
					elif check("visit.png") == 0:
						return 0
					
					elif check("reveal.png") == 0:
						time.sleep(2)
						pyautogui.click()
						return 0
			else: #right 
				for i in range(int(1920*0.6),450,-50):
					pyautogui.click((i,1080/2-50))
					if swirl_icon() == 0:
						return 0
					elif check("play.png") == 0:
						return 0
					elif check("visit.png") == 0:
						return 0
					
					elif check("reveal.png") == 0:
						time.sleep(2)
						pyautogui.click(button="left")
						pyautogui.click(button="right")
						time.sleep(1)
						pyautogui.click(button="left")
						pyautogui.click(button="right")
						return 0
						
						
	if False and check("rewards3.png") == 0:
		time.sleep(1)
		pyautogui.click((1000, 317))
		time.sleep(0.25)
		pyautogui.click((640, 435))
		time.sleep(0.25)
		pyautogui.click((760, 850))
		time.sleep(0.25)
		pyautogui.click((1250, 850))
		time.sleep(0.25)
		pyautogui.click((1340, 460))
		time.sleep(1)
		#screen()
		#token_check()				
		pyautogui.click((953,555))
		pyautogui.click()
		time.sleep(4)
		pyautogui.click()
		time.sleep(4)
		check("ok.png")
		time.sleep(4)
		done = False
		return 0
	
	if check("merc_collection.png", click=False) == 0:
		pyautogui.click((1450, 850))
		time.sleep(0.5)
		pyautogui.click((1920/2 - 150 , 1080/2 +100))
		return 0
	
	#if check("lordbanehollow.png") == 0:
	#	if check("start2.png") == 0:
	#		time.sleep(4)
	#		side = find_possible_challenger()
	if check("pick_treasure.png") == 0 or check("pick_treasure2.png",0.6,take_sh=False) == 0 or check("pick_treasure3.png", 0.6,take_sh=False) == 0:
		pyautogui.click((1920/2, 1080/2))
		time.sleep(0.01)
		check("take.png")
		check("take2.png")
		return 0
		
	return 1
	
def find_what_to_do_coins():
	brute_force_find_what_to_click()
	if check("play.png") == 0:
		return 0
		#post_play()
	
	if battle_loop() == 0:
		return 0
		
		
		
	if check("need_to_select.png") == 0:
		if check("full_angel.png",0.90) == 0:
			time.sleep(0.2)
			check("visit.png")
			
		elif check("play.png") == 0:
			pass					
		
		elif check("visit.png") == 0:
			pass

		else:
			for i in range(450,1920-450,50):
				pyautogui.click((i,1080/2))
				if check("play.png") == 0:
					return 0
					
	if fp("rewards.png") == 0:
		time.sleep(1)
		pyautogui.click((973, 297))
		time.sleep(0.25)
		pyautogui.click((750, 700))
		time.sleep(0.25)
		pyautogui.click((1250, 750))
		time.sleep(1)
		#token_check()				
		pyautogui.click((953,625))
		done = False
		return 0
	
	if fp("done_quilboard.png") == 0:
		pyautogui.click((973,850))
	
	if find_picture("start_quilboar.png") == 0 or fp("quilboar.png") == 0:
		pyautogui.click((1450, 850))
	
	if check("merc_collection.png",click=False) == 0:
		check("coin_team.png")
		time.sleep(1)
		pyautogui.click((1450, 850))
		time.sleep(0.5)
		pyautogui.click((1920/2 - 150 , 1080/2 +100))
		return 0
	
	if check("pick_treasure.png") == 0 or check("pick_treasure2.png",0.6,take_sh=False) == 0 and check("pick_treasure3.png", 0.6,take_sh=False) == 0:
		pyautogui.click((1920/2, 1080/2))
		time.sleep(0.01)
		check("take.png")
		check("take2.png")
		pyautogui.click((1100, 850))
		return 0
		
	return 1	
	
def reset():
	pyautogui.click(50,50)
	time.sleep(0.1)
	while check("back.png") == 0:
		pyautogui.click(50,50)
		time.sleep(3)
		
	
	
	
		
side = 0 
setup = False
done = False 
spammed_back = False
setup_ft = False
failsafe = 0
bad_exit = 0
mode = ""

while True:
	if number_of_mysterious_challenger < 4 and not farm_blackhand:
		while not setup or mode != "mc":
					
			if mode != "mc":
				setup_first_time("felwood")
				setup_ft = True
				mode = "mc"
				print("mode: ", mode)
			
			if check("start_banehollow.png",0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
				
			if check("stranger_team.png",0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
					setup = True
											
		if not done and failsafe < 50:
			failsafe+=1
			if check("start_banehollow.png", 0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
				
			if check("stranger_team.png",0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
			check("lock_in.png")
			if check("encounter normal.png") == 0:
					print("searching for mysterious_challenger")
					side = find_possible_challenger()
					setup = True
					done = True
					failsafe=0
					time.sleep(5)
			
		else:
			failsafe = 0
			if check("stranger_team.png",0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
			
			if find_what_to_do_mc(side) == 1:
				pyautogui.click((50,50))
				if bad_exit < 30:
					bad_exit+=1
				else:
					bad_exit=0
					check("closehs.png")
					setup=False
					
			else:
				bad_exit=0
	elif not farm_blackhand:
		print("number_of_mysterious_challenger=4")
		while not setup or mode != "coin":
			print("loop")
			if mode != "coin":
				setup_first_time("barrens")				
				setup_first_time = True
				mode = "coin"
				print("mode:",mode)
				
			if check("start_quilboar.png") == 0:
				time.sleep(2)
				check("start2.png")
				time.sleep(2)
				
			if check("coin_team.png") == 0:
				time.sleep(2)
				check("start2.png")
				setup = True
					
				time.sleep(1)
								
		if find_what_to_do_coins() == 1:
			time.sleep(10)
			pyautogui.click((50,50))
			if bad_exit < 30:
				bad_exit+=1
			else:
				bad_exit=0
				check("closehs.png")
				setup=False
				
		else:
			bad_exit=0
	
	else:
		if not done and failsafe < 50:
			failsafe+=1
			if check("blackhand.png", 0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
				
			if check("mongofarm_team.png",0.82) == 0:
				if check("start2.png") == 0:
					time.sleep(1)
											
			if check("encounter normal.png") == 0:
					print("searching for mysterious_challenger")
					side = find_possible_challenger()
					setup = True
					done = True
					failsafe=0
					time.sleep(5)
			
		else:
			print("farm_blackhand")
			failsafe = 0
			if find_what_to_do_blackhand(side) == 1:
				pyautogui.click((50,50))
				if bad_exit < 30:
					bad_exit+=1
				else:
					bad_exit=0
					check("closehs.png")
					setup=False
					
			else:
				bad_exit=0