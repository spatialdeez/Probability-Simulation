# Luck simulation
# Made at 19/02/2025
# This is a luck simualtor. To start: run this code, and select the potions you want
# to use. Press roll after to see what auras you can get!

# Luck formula as from Sol's RNG: ((1 + basic buff) * bonus roll + special buff) * vip)

# Aura pulling system (1:1 replica, as stated from wiki)
# Highest rarity in aura list calcuates first
# randomly select a number bewteen 1 and {current aura rarity}
# to determine successful pull:
# if it is 1, the draw ends. Else, move on
# repeat

import random
import sys
import math
import time
import threading
import tkinter as tk
from math import prod
from tkinter import simpledialog
from datetime import datetime, date

random.seed(datetime.now().timestamp()) # setting the seed based on time

try:
    import matplotlib.pyplot as plt
    import numpy as np
    GRAPH_ENABLED = True
except:
    print('Either matplotlib or numpy is not installed.\nYou may continue, but most analytic features may not be available!')
    input('Press enter to continue >>>')
    GRAPH_ENABLED = False

basic = 0
bonus = 1
special = 0
vip = False
CONSOLE = False

biome_name = 'normal'
day_night = 'day'

# Heavenly, oblivion, and blood moon potions
heavenly_one = False
heavenly_two = False
oblivion = False
blood_moon = False

auras = []

tutorials = {'Normal Simulation Tutorial': '''Steps to use the graph function effectively:
Step one: Apply your luck first, such as your heavenly 1 or 2.

Step two: Key in the amount of auras you want to find the rate of (example: If you want to find the rate of Archangel and Overture, that would be 2)

Step three: Enter the names of the auras you want to find the rate of

Step four: Key in the amount of rolls you want to simulate

Setp five: Get your reports ready in a few seconds, or a few minutes.\n'''
             }


def aura_pull(graph=False, test=False):
    
    biome_check(check=True)
    biome_check()
    auras_sorted = dict(sorted(auras.items(), key=lambda item: item[1], reverse=True))
    # print(auras_sorted)
    total_luck = luck_calculator()
    
    for aura_name in auras:
        rarity = auras_sorted[aura_name]
        
        new_rarity = max(1, int((rarity / total_luck + 0.5))) # Use luck formula and make into new integer 
        
        if CONSOLE == True:
            print(f'[CONSOLE] New rarity of {aura_name}: {new_rarity}.')
            
        odds = random.randint(1, new_rarity) # do simple calculation

        if odds == 1 and graph == True and test == False:
            return aura_name
        elif odds == 1 and graph == False and test == False:
            print(f'You rolled: {aura_name} (1 in {auras[aura_name]}) with luck: {total_luck} | Biome {biome_name} on a {day_night}')
            break
        elif odds == 1 and test == True:
            return
        else:
            if CONSOLE == True:
                print(f'[CONSOLE] Missed pull of aura: {aura_name}')
            else:
                pass

            
def heavenly_potion(type_number):
    global heavenly_one, heavenly_two
    if heavenly_one == True and heavenly_two == True:
        print('You have both heavenly 1 and 2 on stack! Remove stacks? (yes/no)')
        if input('>') in ['yes', 'y']:
            print('Removed stacks!')
            heavenly_one = False
            heavenly_two = False
            luck_check()
            return
        else:
            print('Stacks were not removed')
            return
    if type_number == 1:
        if heavenly_two == True:
            print('In the real game, heavenly 1 and 2 cannot stack.\nDo you want to continue to stack? (yes/no)')
            if input('>') in ['yes', 'y']:
                print('Stacks applied!')
                print('Heavenly 1 applied to future rolls')
                heavenly_one = True
                heavenly_two = True
                luck_check()
                return
            else:
                print('Did not stack heavenly potion 1 together with heavenly potion 2')
                return
            
        if heavenly_one == False:
            print('Heavenly 1 applied to future rolls')
            heavenly_one = True
        else:
            print('Heavenly 1 disabled for future rolls!')
            heavenly_one = False
            
        
    else:
        if heavenly_one == True:
            print('In the real game, heavenly 1 and 2 cannot stack.\nDo you want to continue to stack? (yes/no)')
            if input('>') in ['yes', 'y']:
                print('Stacks applied!')
                print('Heavenly 2 applied to future rolls')
                heavenly_one = True
                heavenly_two = True
                luck_check()
                return
            else:
                print('Did not stack heavenly potion 2 together with heavenly potion 1')
                return
        if heavenly_two == False:
            print('Heavenly 2 applied to future rolls')
            heavenly_two = True
        else:
            print('Heavenly potion 2 disabled for future rolls!')
            heavenly_two = False
            
    luck_check()

# Luck setting section

def vip_check():
    global vip
    if vip == False:
        print('VIP enabled. Enable VIP+ now?')
        if simpledialog.askstring('Yes/No response', 'VIP enabled. Enable VIP+ now?')  in ['yes', 'y']:
            print('VIP+ Enabled!')
            vip = 'plus'
        else:
            print('VIP+ not enabled.')
            vip = True
    elif vip == True:
        if vip == 'plus':
            print('VIP+ disabled!')
            vip = False
        else:
            print('VIP disabled!')
            vip = False
        
def luck_check():
    global special
    if  heavenly_one == True and heavenly_two == True:
        special = 220000
    elif heavenly_one == True:
        special = 20000
    elif heavenly_two == True:
        special = 200000
    else:
        special = 0
        
def luck_calculator():
    if vip == True:
        luck = (((1 + basic) * bonus + special) * 1.2)
    elif vip == 'plus':
        luck = (((1 + basic) * bonus + special) * 1.3)
    else:
        luck = (((1 + basic) * bonus + special) * 1)
    return luck

# Biome setting section
def biome_check(check=False):
    global auras, biome_name, day_night
    
    if biome_name == 'rainy':
        auras['Abyssal Hunter'] = 100000000
        auras['Sailor'] = 4000000
        auras['Poseidon'] = 1000000
        auras['Sailor: Flying Dutchman'] = 20000000
        
    elif biome_name == 'windy':
        auras['Stormal: Hurricane'] = 4500000
        auras['Stormal'] = 30000
        auras['Wind'] = 300
        
    elif biome_name == 'snowy':
        auras['Permafrost'] = 12250
        auras['Glacier'] = 768
    elif biome_name == 'sandstorm':
        auras['Atlas'] = 90000000
        auras['Jackpot'] = 194
    elif biome_name == 'hell':
        auras['Undead'] = 2000
        auras['Undead: Devil'] = 12000
        auras['Hades'] = 1111111
        auras['Bloodlust'] = 50000000
    elif biome_name == 'starfall':
        auras['Starlight'] = 5000
        auras['Star Rider'] = 5000
        auras['Comet'] = 12000
        auras['Galaxy'] = 5000000
        auras['Sirius'] = 1400000
        auras['Starscourge: Radiant'] = 10000000
        auras['Gargantua'] = 42000000
    elif biome_name == 'corruption':
        auras['Hazard'] = 1400
        auras['Corrosive'] = 2400
        auras['Hazard: Rays'] = 14000
        auras['Astral'] = 267000
        auras['Impeached'] = 42000000
    elif biome_name == 'null':
        auras['Undefined'] = 1111
        auras['Nihility'] = 9000
    elif biome_name == 'dreamspace':
        auras['One Star'] = 100
        auras['Two Star'] = 1000
        auras['Three Star'] = 10000
    elif biome_name == 'glitch':
        auras['Fault'] = 3000
        auras['Gltich'] = 12210110
        auras['Oppression'] = 220000000        
    elif check == True or biome_name == 'normal':
        auras = {'Luminosity': 1200000000,
         'Aegis': 825000000,
         'Soverign': 750000000,
         'Matrix: Reality': 601020102,
         'Matrix: Overdrive': 503000000,
         'Ruins': 500000000,
         'Apostolos': 444000000,
         'Gargantua': 430000000,
         'Abyssal Hunter': 400000000,
         'Atlas': 360000000,
         'Bloodlust': 300000000,
         'Overture: History': 300000000,
         'Archangel': 250000000,
         'Impeached': 200000000,
         'Symphony': 175000000,
         'Overture': 150000000,
         'Starscourge: Radiant': 100000000,
         'Chromatic: Genesis': 99999999,
         'Sailor: Flying Dutchman': 80000000,
         'Twilight: Iridescent Memory': 60000000,
         'Matrix': 50000000,
         'Exotic: Apex': 49999500,
         'Overseer': 45000000,
         'Ethereal': 35000000,
         'Arcane: Dark': 30000000,
         'Exotic: Void': 29999999,
         'Aviator': 24000000,
         'Chromatic': 20000000,
         'Arcane: Legacy': 15000000,
         'Stormal: Hurricane': 13500000,
         'Sailor': 12000000,
         'Starscourge': 10000000,
         'Nihility': 9000000,
         'Hyper-Volt': 7500000,
         'Celestial: Divine': 7000000,
         'Hades': 6666666,
         'Origin': 6500000,
         'Twilight': 6000000,
         'Lunar: Full Moon': 5000000,
         'Galaxy': 5000000,
         'Solar: Solstice': 5000000,
         'Zeus': 4500000,
         'Poseidon': 4000000,
         'Aquatic: Flame': 4000000,
         'Savior': 3200000,
         'Virtual': 2500000,
         'Bounded: Unbound': 2000000,
         'Gravitational': 2000000,
         'Astral': 1336000,
         'Rage: Brawler': 1280000,
         'Undefined': 1111000,
         'Magnetic: Reverse Polarity': 1024000,
         'Arcane': 1000000,
         'Kyawthuite': 850000,
         'Celestial': 350000,
         'Bounded': 200000,
         'Aether': 180000,
         'Jade': 125000,
         'Comet': 120000,
         'Undead: Devil': 120000,
         'Diaboli: Void': 100400,
         'Exotic': 99999,
         'Stormal': 90000,
         'Permafrost': 36750,
         'Nautilus': 70000,
         'Hazard: Rays': 70000,
         'Flushed: Lobotomy': 69000,
         'Star Rider': 50000,
         'Starlight': 50000,
         'Lunar': 50000,
         'Solar': 50000,
         'Aquatic': 40000,
         'Powered': 16384,
         'Ink: Leak': 14000,
         'Rage: Heated': 12800,
         'Corrosive': 12000,
         'Undead': 12000,
         'Lost Soul': 9200,
         'Quartz': 8192,
         'Hazard': 7000,
         ':Fluhsed:': 6900,
         'Bleeding': 4444,
         'Sidereum': 4096,
         'Player': 3000,
         'Glacier': 2304,
         'Ash': 2300,
         'Magnetic': 2048,
         'Glock': 1700,
         'Precious': 1024,
         'Diaboli': 1004,
         'Wind': 900,
         'Aquamarine': 900,
         'Sapphire': 800,
         'Jackpot': 777,
         'Ink': 700,
         'Gilded': 512,
         'Emerald': 500,
         'Forbidden': 404,
         'Ruby': 350,
         'Topaz': 150,
         'Rage': 128,
         'Crystalised': 64,
         'Divinus': 32,
         'Rare': 16,
         'Natural': 8,
         'Good': 5,
         'Uncommon': 4,
         'Common': 2
         }

    # check day night cycle
    
    if day_night == 'day':
        auras['Solar'] = 5000
        auras['Solar: Solstice'] = 500000
    elif day_night == 'night':
        auras['Lunar'] = 5000
        auras['Lunar: Full Moon'] = 500000


        
# Graphing Section
def ask_for_aura_name():
    category = {}
    while True:
        try:
            aura_amount = int(simpledialog.askstring('Input a number', 'How many auras do you want to discover the rate of?'))
            break
        except:
            if aura_amount == None or aura_amount == '':
                print('Graph plotting process cancelled.')
                return
            print('Not an integer/number')
            continue
    
    for i in range(aura_amount):
        while True:
            aura_name = simpledialog.askstring('Aura name', f'Aura {i + 1} name')
            if aura_name in auras:
                category[aura_name] = 0
                break
            else:
                if aura_name == None:
                    print('Graph plotting process cancelled.')
                    return
                print('Aura is not in the list! Maybe check your spelling? it is case sensitive.')
                continue
    while True:
        try:
            repeat = int(simpledialog.askstring('Input a number', 'How many rolls to simulate?'))
            break
        except:
            if repeat == None:
                print('Graph plotting process cancelled.')
                return
            else:
                print('not an integer/number')
                continue

    return repeat, category


def plot_graph(x_label='', y_label='', title='', axis_horizontal=[], axis_vertical=[], graph_type=None, data=None, values=None):
    # axis_horizontal or axis_vertical should be passed the arguments, example: [0, color='black', linewidth=2]
    
    try:
        if axis_horizontal != []:
            x_axis_ref_line, colour, line_thickness = axis_horizontal
            
        if axis_vertical != []:
            y_axis_ref_line, colour, line_thickness = axis_vertical
    except:
        print('Specified too little/much variables')
        
    if graph_type == None:
        print('Not able to plot a graph if no type is specified!')
        return
    
    if graph_type == 'bar graph':
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(data, values, color='Blue')
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.axhline(x_axis_ref_line, color=colour, linewidth=line_thickness)  # Vertical line at 0 for reference
        plt.show()

    return
    
def report_producer(important_info='', extra_info=''):
    print('-----REPORT READY-----')
    print(f'Report as of {date.today()} ' + extra_info)
    for info_index in important_info:
        print(important_info[info_index])
        
    return

    
def aura_simulation():
    info = []
    aura_to_values = {}
    biome_check(check=True)
    biome_check(check=False)
    
    print('Do you want a tutorial of how to use normal simualation visualiser? ')
    if simpledialog.askstring('Tutorial', 'Would you want a tutorial?') in ['yes', 'y']:
        print(tutorials['Normal Simulation Tutorial'])
        input('Press enter when ready >>>')
        


    test_sample, aura_to_values = ask_for_aura_name()
    sample_luck = luck_calculator()

    time_1 = time.time()
    for i in range(20):
        aura_pull(test=True)
    time_2 = time.time()
    total_time = time_2 - time_1
    total_time *= (test_sample / 20)

    print("Estimated time of finishing report: {:.2f} seconds".format(total_time))
            
    for rolling in range(test_sample):            
        aura_obtained = aura_pull(True)
        if aura_obtained in aura_to_values:
            aura_to_values[aura_obtained] += 1

    test_sample_names = list(aura_to_values.keys())
    test_sample_values = list(aura_to_values.values())

    for aura in aura_to_values:
        aura_percent = (aura_to_values[aura] / test_sample) * 100
        aura_percent = '{:.2f}'.format(aura_percent)
        info.append(f'{aura}: rolled {aura_to_values[aura]} times, with a rolled to rolls percentage of: {aura_percent} percent')

    report_producer(important_info=info, extra_info=f'| Simulated {test_sample} rolls')
    title_for_graph = f'Auras obtained from {test_sample} times rolled with luck of {sample_luck} | Biome {biome_name} at {day_night}'
    plot_graph('Auras', 'Amount of times rolled', title_for_graph, [0, 'black', 2], [],'bar graph', test_sample_names, test_sample_values)
    
    
    
    


def biome_set():
    global biome_name, day_night
    biome_name = simpledialog.askstring('Biome Selection', 'What biome do you want to set?')
    try:
        biome_name.lower()
    except:
        print('Biome selection cancelled')
        return
    while biome_name not in ['normal','windy', 'rainy', 'snowy', 'starfall', 'corruption', 'glitch', 'dreamspace', 'sandstorm' 'hell']:
        biome_name = simpledialog.askstring('Biome Selection', 'Not a biome! What biome do you want to set?')
        try:
            biome_name.lower()
        except:
            print('Biome selection cancelled')
            return
    day_night = simpledialog.askstring('Biome Selecrion', 'Day or night? (Type none if you do not want a day-night cycle)')
    try:
        day_night.lower()
    except:
        print('Biome selection cancelled')
        return
    while day_night not in [None, 'day', 'night']:
        day_night = simpledialog.askstring('Biome Selecrion', 'Not a valid answer! Day or night? (Type none if you do not want a day-night cycle)')
        try:
            day_night.lower()
        except:
            print('Biome selection cancelled')
            return
    
    biome_check(check=True)
    biome_check()

# Aura probability
def aura_probabiity_gui():
    answer = simpledialog.askstring('Aura Selection', 'What aura to find probability of?')
    aura_index = get_key_index(auras, answer)
    if answer in auras:
        probability = aura_probability(auras, aura_index)
        if auras[answer] > 10000000:
            print('Probability of rolling aura: {:.10f}%'.format(probability))
        else:
            print('Probability of rolling aura: {:.5f}%'.format(probability))
        
    else:
        print('Aura not in aura list! Maybe check your ')
    
def aura_probability(auras_prob, i):
    print('Aura probability calculator')
    rarity_values = list(auras_prob.values())

    if i == 0:
        rarity = 1 / rarity_values[i]
        return rarity
    elif i < 1:
        raise ValueError("Invalid aura index")
    else:
        p_i = 1 / rarity_values[i - 1]

        product_term = prod(1 - (1 / rarity_values[k]) for k in range(i - 1))

        return p_i * product_term


def get_key_index(d, key):
    keys_list = list(d.keys())
    try:
        return keys_list.index(key)
    except ValueError:
        return None


    
# Gear placement part

def main():
    print('Aura Rolling Simulation. Auras are updated from Eon 1.')
    print('''NOTE: VERSION IS IN ALPHA.
Also, take note that all aura names are spelt captial letters first. (Example: Common, Lunar: Full Moon)''')
    input('Press enter to acknowledge understanding >>>')
    
    biome_check(check=True)
    
    root = tk.Tk()
    root.title("RNG simulation")
    root.geometry("500x400")


    # Create sections (Frames)
    left_frame = tk.Frame(root)
    center_frame = tk.Frame(root)
    right_frame = tk.Frame(root)

    # Place frames using `pack` (left, center, right alignment)
    left_frame.pack(side="left", padx=20, pady=20, fill="y")
    center_frame.pack(side="left", padx=20, pady=20, fill="y")
    right_frame.pack(side="left", padx=20, pady=20, fill="y")

    roll_button = tk.Button(left_frame, text="roll aura", font=("Helvetica", 14), command=lambda: aura_pull())
    roll_button.pack(pady=10)


    hp_one_button = tk.Button(left_frame, text="Use heavenly potion 1", font=("Helvetica", 14), command=lambda: heavenly_potion(1))
    hp_one_button.pack(pady=10)

    hp_two_button = tk.Button(left_frame, text="Use heavenly potion 2", font=("Helvetica", 14), command=lambda: heavenly_potion(2))
    hp_two_button.pack(pady=10)

    enable_vip_button = tk.Button(left_frame, text="Enable VIP", font=("Helvetica", 14), command=lambda: vip_check())
    enable_vip_button.pack(pady=10)

    if GRAPH_ENABLED == True:
        graph_button = tk.Button(left_frame, text="Graph tools", font=("Helvetica", 14), command=aura_simulation)
        graph_button.pack(pady=10)
    else:
        pass

    probability_button = tk.Button(left_frame, text="Calculate probability", font=("Helvetica", 14), command=aura_probabiity_gui)
    probability_button.pack(pady=10)
    
    biome_button = tk.Button(center_frame, text="Select Biome", font=("Helvetica", 14), command=biome_set)
    biome_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()


