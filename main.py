#%%
import requests
import json

headers={"token": "memorial-zW73Zcp4H5XAtdbNsuNCDmyDF3NtVMN9DR6moRh4ekZ3WWkuMSBH54FN3Dxhmiv5"}
r = requests.get('http://cec2019.ca/instance', headers=headers)
response = json.loads(r.text)

#%%

"""
b_map = [[[], [], [], [], ['O', 'G', 'R'], [], [], [], [], []],
         [[], ['O'], [], ['R'], [], ['G'], [], [], [], []],
         [[], [], [], [], [], [], [], ['O', 'G'], [], []],
         [[], [], [], ['R'], [], [], [], [], [], []],
         [[], ['O', 'G', 'R'], [], [], [], [], ['G', 'R'], ['O'], ['O'], []],
         [[], [], [], [], [], [], [], [], [], []],
         [[], [], [], [], [], ['O', 'G', 'R'], [], ['O'], [], []],
         [['G'], ['G'], [], [], [], [], [], [], [], []],
         [['G'], ['G'], ['G'], ['G'], [], [], ['O'], ['O'], ['O'], []],
         [['G'], ['G'], ['G'], [], [], [], [], [], [], []]]
"""


def get_score(rad, xc, yc, size, checked, b_map):
    """
    rad = radius of diamond
    xc = centre of diamond x
    yc = centre of diamond y
    checked = dict of square already used in a diamond
    size = square size of restourant
    """
    local_check = [[0 for x in range(size)] for y in range(size)]
    score = dict()
    score['O'] = 0
    score['G'] = 0
    score['R'] = 0
    
    for x in range(xc - rad, xc + rad + 1):
       if (x >=0 and x < size):
           for y in range(yc - (rad - abs(xc - x)), yc + (rad - abs(xc - x)) + 1):
               if y >= 0 and y < size:
                   if local_check[x][y] == 1 or checked[x][y] == 1:
                       score['O'] = 0
                       score['G'] = 0
                       score['R'] = 0
                       return score
                   for item in b_map[x][y]:
                       if item[0] == 'O':
                           score['O'] += 1
                       elif item[0] == 'G':
                           score['G'] += 1
                       elif item[0] == 'R':
                           score['R'] += 1          
                   local_check[x][y] = 1
    
    return score
                         

def sum_score(score):
    """
    score = dict of count of each type of waste
    """
    # print(score)
    return score['O'] + score['G'] + score['R']
    
    
def update_checked(score, taken, rad, size):
    xc = score['x']
    yc = score['y']

    for x in range(xc - rad, xc + rad + 1):
       if (x >=0 and x < size):
           for y in range(yc - (rad - abs(xc - x)), yc + (rad - abs(xc - x)) + 1):
               if y >= 0 and y < size:
                   taken[x][y] = 1
          
    return taken
    


def find_best_diamond(b_map, checked, rad, size):
    scores = dict()
    scores['O'] = 0
    scores['G'] = 0
    scores['R'] = 0
    
    max_score = dict()
    max_score['x'] = 0
    max_score['y'] = 0
    max_score['score'] = scores
    
    current_checked = checked
    
    for y in range(size):
        for x in range(size):
            score = get_score(rad, x, y, size, current_checked, b_map)
            if sum_score(score) > sum_score(max_score['score']):
                    max_score['x'] = x
                    max_score['y'] = y
                    max_score['score'] = score

    return max_score


def check_left():
    headers={"token": "memorial-zW73Zcp4H5XAtdbNsuNCDmyDF3NtVMN9DR6moRh4ekZ3WWkuMSBH54FN3Dxhmiv5"}
    r = requests.get('http://cec2019.ca/instance', headers=headers)
    response = json.loads(r.text)
    o_left = response['payload']['constants']['TOTAL_COUNT']['GARBAGE']
    g_left = response['payload']['constants']['TOTAL_COUNT']['ORGANIC']
    r_left = response['payload']['constants']['TOTAL_COUNT']['RECYCLE']
    
    for item in response['payload']['itemsHeld']:
        if item['type'] == 'ORGANIC':
            o_left -= 1
        if item['type'] == 'GARBAGE':
            g_left -= 1
        if item['type'] == 'RECYLE':
            r_left -= 1
    
    for item in response['payload']['itemsCollected']:
        if item['type'] == 'ORGANIC':
            o_left -= 1
        if item['type'] == 'GARBAGE':
            g_left -= 1
        if item['type'] == 'RECYLE':
            r_left -= 1
        
    return o_left, g_left, r_left
            
from operator import itemgetter

def sort_diamonds(diamonds):
    o_left, g_left, r_left = check_left()
    
    for diamond in diamonds:
        diamond['weight'] = diamond['score']['O']*o_left + diamond['score']['G']*g_left + diamond['score']['R']*r_left
    
    return sorted(diamonds, key=itemgetter('weight'), reverse=True) 


def find_diamonds(b_map, rad, size):
    checked = [[0 for x in range(size)] for y in range(size)]
    diamonds = []
    
    while True:
        recent_score = find_best_diamond(b_map, checked, rad, size)
        checked = update_checked(recent_score, checked, rad, size)
        
        if sum_score(recent_score['score']) == 0:
            break
        
        diamonds.append(recent_score)
    
    return sort_diamonds(diamonds)
    
b_map = [[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [['G', 0], ['R', 1], ['O', 2]], [], [], [], [], [], [], [], [], [], [], [['G', 64], ['R', 65], ['R', 66]], [], [], [], [], []], [[], [], [['R', 4], ['O', 5], ['O', 6]], [], [], [], [], [], [], [], [], [], [], [['G', 67], ['R', 68], ['R', 69], ['O', 70]], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [['G', 72], ['G', 74], ['R', 77], ['O', 78], ['O', 79]], [], [], [], [], []], [[], [], [], [], [], [['R', 110]], [], [], [], [], [], [], [], [['G', 80], ['G', 81], ['R', 84]], [], [['G', 85], ['R', 86]], [['R', 88]], [['G', 91]], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [['O', 120], ['O', 121]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [['G', 17]], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [['R', 21]], [['G', 29], ['O', 30], ['O', 31]], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [['O', 26]], [['R', 32], ['R', 33]], [['G', 38], ['O', 39], ['O', 40]], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [['G', 34], ['R', 35], ['O', 36], ['O', 37]], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [['R', 8], ['O', 9], ['O', 10]], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [['G', 11], ['R', 12], ['O', 13], ['O', 14]], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [['G', 52], ['R', 53], ['O', 54], ['O', 55]], [], [], [], [['G', 93], ['R', 94], ['R', 95], ['O', 96], ['O', 97]], [['R', 101]]], [[], [], [], [], [], [], [], [], [], [], [], [], [['G', 45], ['R', 47], ['O', 48], ['O', 49]], [['G', 56], ['R', 57], ['O', 58], ['O', 59]], [], [], [], [['G', 98], ['O', 99], ['O', 100]], [['G', 102]]], [[], [], [], [], [], [], [], [], [], [], [], [], [['R', 50], ['R', 51]], [['G', 60], ['R', 61], ['O', 62], ['O', 63]], [], [], [], [], []]]

diamonds = find_diamonds(b_map, 3, 19)
#%%

def turnTo(dir):       
    strin = "http://cec2019.ca/turn/" + str(dir)
    r = requests.post(strin, headers=headers)
    if r == 200:
        return True
    else:
        return False
    
def moveTo(x1, y1):
    r = requests.get('http://cec2019.ca/instance', headers=headers)
    dic = json.loads(r.text)
    x0 = dic["payload"]["location"]["x"]
    y0 = dic["payload"]["location"]["y"]
    print(str(dic["payload"]["location"]["x"]) + ", " + str(dic["payload"]["location"]["y"]))
    
    if x0 == x1 and y0 ==y1:
        return True
    elif x0 < x1:
        if dic["payload"]["direction"] == 'E':
            r = requests.post('http://cec2019.ca/move', headers=headers)
        else:
            turnTo('E')
    elif x0 > x1:
        if  dic["payload"]["direction"] == 'W':
            r = requests.post('http://cec2019.ca/move', headers=headers)
        else:
            turnTo('W')
    elif y0 < y1:
        if  dic["payload"]["direction"] == 'N':
            r = requests.post('http://cec2019.ca/move', headers=headers)
        else:
            turnTo('N')
    elif y0 > y1:
        if  dic["payload"]["direction"] == 'S':
            r = requests.post('http://cec2019.ca/move', headers=headers)
        else:
            turnTo('S')
    moveTo(x1, y1)
     


#%%

def cycles_in_diamond(diamond):
    headers={"token": "memorial-zW73Zcp4H5XAtdbNsuNCDmyDF3NtVMN9DR6moRh4ekZ3WWkuMSBH54FN3Dxhmiv5"}
    r = requests.get('http://cec2019.ca/instance', headers=headers)
    response = json.loads(r.text)
    
    moves_till_cycle = response['payload']['timeSpent'] % response['payload']['constants']['BIN_COLLECTION_CYCLE']*2
    current_pos_x = response['payload']['location']['x']
    current_pos_y = response['payload']['location']['y']
    move_cost = response['payload']['constants']['TIME']['MOVE']
    turn_cost = response['payload']['constants']['TIME']['TURN']
    moves_to_diamond = abs(current_pos_x - diamond['x'])*move_cost + abs(current_pos_y - diamond['y'])*move_cost + turn_cost
    cycles_in_diamond = moves_till_cycle - moves_to_diamond*2 + 5 # saftey factor of 5
    
    return cycles_in_diamond


def select_diamond(diamonds):  
    headers={"token": "memorial-zW73Zcp4H5XAtdbNsuNCDmyDF3NtVMN9DR6moRh4ekZ3WWkuMSBH54FN3Dxhmiv5"}
    r = requests.get('http://cec2019.ca/instance', headers=headers)
    response = json.loads(r.text)
    
    moves_till_cycle = response['payload']['timeSpent'] % response['payload']['constants']['BIN_COLLECTION_CYCLE']*2
    current_pos_x = response['payload']['location']['x']
    current_pos_y = response['payload']['location']['y']
    move_cost = response['payload']['constants']['TIME']['MOVE']
    turn_cost = response['payload']['constants']['TIME']['TURN']
    unload_cost = response['payload']['constants']['TIME']['UNLOAD_ITEM']
    can_pos_x = response['payload']['constants']['BIN_LOCATION']['GARBAGE']['X']
    can_pos_y = response['payload']['constants']['BIN_LOCATION']['GARBAGE']['Y']
    moves_to_cans = abs(current_pos_x - can_pos_x)*move_cost + abs(current_pos_y - can_pos_y)*move_cost + turn_cost + 2
    moves_to_unload_2sets = response['payload']['constants']['BIN_CAPACITY']['GARBAGE'] + response['payload']['constants']['BIN_CAPACITY']['ORGANIC'] + response['payload']['constants']['BIN_CAPACITY']['RECYCLE']
    cycles_to_unload_2sets = moves_to_unload_2sets* unload_cost
    
    if moves_till_cycle - moves_to_cans - cycles_to_unload_2sets/3 > 0 and len(response['payload']['itemsLocated']) > moves_to_unload_2sets/1.5:
        return 'unload'
    
    for diamond in diamonds:
        if cycles_in_diamond(diamond) > 20:
            return diamond
    
    return 'unload'
    
diamonds = find_diamonds(b_map, 3, 19)
best_diamod = select_diamond(diamonds)

