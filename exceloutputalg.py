
import networkx as nx
import time
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style
from operator import itemgetter
import numpy as np
import random
import pandas as pd


def neighcolours(G, nodenum, adjlist, color_map):
    #COMMENT:find the coloured neighbours of a specfic node and their proportions
    red = 0
    blue = 0
    gray = 0
    
    if color_map[nodenum] != "gray":
        return ["coloured", -1]

    for x in range(1, len(adjlist[nodenum])):
        # print(x)
        nodewereon = int(adjlist[nodenum][x])
        if color_map[nodewereon] == "blue":
            blue +=1
        elif color_map[nodewereon] == "red":
            red += 1
        else:
            gray += 1
    

    blueperc = blue / (red + gray + blue)
    redperc = red / (red + gray + blue)
    grayperc = gray / (red + gray + blue)
    

    if redperc > blueperc:
        return ["red", redperc]
    
    elif blueperc > redperc:
        return ["blue", blueperc]
    
    elif blueperc == redperc and grayperc !=1:
       
        return ["gray", -1]
    
    else:
        return ["gray", 0]
        
    

def findproportions(G, adjlist, color_map):
    #COMMENT: find proportions of coloured neighbours 
    
    currentproplist = []
    for x in range (len(G.nodes)):
        currentproplist.append(neighcolours(G, x, adjlist, color_map))
    return currentproplist
        

def whosnext (G, adjlist, color_map):
    #COMMENT: find who is next and colour them
    
    currentprops = findproportions(G, adjlist, color_map)
    highest= -1
    highestnode = -1
    
    
    #COMMENT: find the first viable option and make that highest
    for x in range (len(currentprops)):
        if currentprops[x][1] > 0 and currentprops[x][0] != "coloured":
            highest = currentprops[x][1]
            highestnode = x
            break
      
    #COMMENT: see if we can find one higher, if so we set this to highest
    for x in range (len(currentprops)):
        if currentprops[x][1] > highest and currentprops[x][0] != "coloured":
            highest = currentprops[x][1]
            highestnode = x
            
             
    #COMMENT: otherwise colour it and print it
    
    
    if currentprops[highestnode][1] > 0: 
        color_map[highestnode] = currentprops[highestnode][0] 
 

    

def generate_adjlist_with_all_edges(G, delimiter=" "):
    #COMMENT: adj list generator from stackoverflow
    
    for s, nbrs in G.adjacency():
        line = str(s) + delimiter
        for t, data in nbrs.items():
            line += str(t) + delimiter
        yield line[: -len(delimiter)]
        
               
def howmanyleft(G, adjlist, color_map):  
    total = 0
    for x in color_map:
        if x == "gray":
            total += 1
    return total
               
def colournextstalled(G, adjlist, color_map):              
      total = 0
      currentprops = findproportions(G, adjlist, color_map)
      
      for x in range (len(currentprops)):
          if currentprops[x][1] < 0 and currentprops[x][0] != "coloured":
              total +=1
              if x%2 == 0:
                  color_map[x] = "red"
              else:
                  color_map[x] = "blue"
      return total
            
          
               
def percent(G, adjlist, color_map):   
    bluenum = 0
    rednum = 0
    other = 0
    total = 0
    for x in color_map:
        total += 1
        
        if x == "blue":
            bluenum +=1 
        elif x == "red":
            rednum += 1
        else:
            other += 1 
       
    if total > 0:
        return [(rednum/total)*100, (bluenum/total)*100, (other/total)*100]
    else: 
        print ("graph has no nodes. BROKEN!!!")
        return [0,0,0]
    
    
def pullfrommatrix(G, seed1, seed2, seed1type, seed2type, matrix):
    winner = matrix[seed1][seed2]
    if winner == -1:
        return "VOID"
    if winner == seed1:
        return seed1type
    elif winner == seed2:
        return seed2type
    else:
        print ('something has gone awry')
    
 
def runthealgmatrix(G, seed1, seed2):
    
     color_map = []
     for node in G:
         
         if node == int(seed1):
             color_map.append('red')
         
           
         elif node == int(seed2):
             color_map.append('blue')
             
                    
         else: 
             color_map.append('gray')  
     
     adjlist = []
     for line in generate_adjlist_with_all_edges(G):
         tempadj = line.split()
         adjlist.append(tempadj)
         


     for node in range (len(G)-2):
         whosnext (G, adjlist, color_map)  
     totalstalled = 0
     firstcolourstats = []
    
     
     left = howmanyleft(G, adjlist, color_map)
     while left != 0:
         totalstalled += colournextstalled(G, adjlist, color_map)
         left = howmanyleft(G, adjlist, color_map)
             
         if left != 0:
             for node in range (left):
                 whosnext (G, adjlist, color_map)
             left = howmanyleft(G, adjlist, color_map)
             
         
     
     # nx.draw(G, node_color=color_map, with_labels=True)
     # plt.show()
     
     currentstats = percent(G, adjlist, color_map)
     
     if seed1 == seed2:
         return -1
     elif currentstats[0] > currentstats[1]:
         return seed1
     elif currentstats[1] > currentstats[0]:
         return seed2
     else:   
         return -1   
 
def handlethevoids (G, theList1, theList2, node1, node1num, node2, node2num, node1desc, node2desc, listnum1, listnum2, matrix ):
    node1sisters = [node1]
    node2sisters = [node2]    
    winnerlist = []
    for x in theList1:
        if x[1] == node1num:
            node1sisters.append(x[0])
            
    for y in theList2:
         if y[1] == node2num:
             node2sisters.append(y[0])
             
    node1sisters = list(set(node1sisters))
    node2sisters = list(set(node2sisters))
    
    for q in node1sisters:
        for k in node2sisters:
            winnerlist.append(pullfrommatrix(G, q, k, node1desc, node2desc, matrix))
            testper[listnum1] += 1
            testper[listnum2] += 1
    return winnerlist
    
    
    
def mainfunction():
    G = nx.Graph()
    innerlist = []
    matrix = []
   
    G = nx.connected_watts_strogatz_graph(graphsize, k, 0.2, tries=100, seed=None)
    # G = nx.erdos_renyi_graph(graphsize, k, directed=False)
    # G = nx.barabasi_albert_graph(graphsize, k, seed=None, initial_graph=None)
    
    while nx.is_connected(G) == False:
        G = nx.connected_watts_strogatz_graph(graphsize, k, 0.2, tries=100, seed=None)
        # G = nx.erdos_renyi_graph(graphsize, k, directed=False)
        # G = nx.barabasi_albert_graph(graphsize, k, seed=None, initial_graph=None)
        
    # MUST BE THE SAME GRAPH GENERATION TYPE HERE AS ABOVE
            
                
    for i in range(graphsize):
        G.add_node(i)
    # nx.draw(G, with_labels=True)
    # plt.show()
    winningtype = []
 
    
    # Initialize matrix with -1
    matrix = [[-1 for _ in range(graphsize)] for _ in range(graphsize)]

    # Fill symmetric matrix with results from runthealgmatrix
    for i in range(graphsize):
        for j in range(i + 1, graphsize):
            result = runthealgmatrix(G, i, j)
            matrix[i][j] = result
            matrix[j][i] = result
        
    clustlist = []
    
    for i in range(graphsize):
        x = nx.clustering(G, i)
        clustlist.append((i, x))
  
    degreelist = []
    for i in range(graphsize):
        degreelist.append((i,G.degree(i) ))
    
    
    el = nx.eccentricity(G)
    ecclist = list(el.items())
 
    
    # Sort once per list
    sorted_degree = sorted(degreelist, key=lambda x: x[1], reverse=True)
    sorted_clust = sorted(clustlist, key=lambda x: x[1], reverse=True)
    sorted_ecc = sorted(ecclist, key=lambda x: x[1], reverse=True)
    
    # Degree values
    highestdegree, hdv = sorted_degree[0]
    lowestdegree, ldv = sorted_degree[-1]
    approxmiddledegree, mdv = sorted_degree[graphsize // 2]
    
    # Clustering values
    highestclust, hcv = sorted_clust[0]
    lowestclust, lcv = sorted_clust[-1]
    approxmiddleclust, mcv = sorted_clust[graphsize // 2]
    
    # Eccentricity values
    highestecc, hev = sorted_ecc[0]
    lowestecc, lev = sorted_ecc[-1]
    approxmiddleecc, mev = sorted_ecc[graphsize // 2]
    
    # Random from clustering list
    randomvalue = random.randint(0, graphsize - 1)
    rand1 = sorted_clust[randomvalue][0]
    rv = -1  

    

    
    # All strategies: each element = [list, node, value, label, index]
    strategies = [
    [degreelist, lowestdegree, ldv, "lowest degree", 0],
    [degreelist, highestdegree, hdv, "highest degree", 1],
    [clustlist, lowestclust, lcv, "lowest clustering", 2],
    [clustlist, highestclust, hcv, "highest clustering", 3],
    [degreelist, approxmiddledegree, mdv, "approx middle degree", 4],
    [clustlist, approxmiddleclust, mcv, "approx middle clustering", 5],
    [ecclist, lowestecc, lev, "lowest ecc", 6],
    [ecclist, highestecc, hev, "highest ecc", 7],
    [ecclist, approxmiddleecc, mev, "approx middle ecc", 8],
    [clustlist, rand1, rv, "rand", 9]
    ]

    # Do all pairwise comparisons (unique pairs only)
    winningtype = []
    for i in range(len(strategies)):
        for j in range(i + 1, len(strategies)):
            a = strategies[i]
            b = strategies[j]
            result = handlethevoids(G, a[0], b[0], a[1], a[2], b[1], b[2], a[3], b[3], a[4], b[4], matrix)
            winningtype.extend(result)

    # Prepare to collect win statistics
    winstats = []

    labels = [
    "lowest degree", "highest degree", "lowest clustering", "highest clustering",
    "approx middle degree", "approx middle clustering",
    "lowest ecc", "highest ecc", "approx middle ecc", "rand"
    ]

    for i, label in enumerate(labels):
        count = winningtype.count(label)
        # print(f"{label} wins:", end=" ")
        # print(count)
        winstats.append(count / testper[i])
    
    # print (Back.RED + "VOIDs:", end = " ")
    # print (winningtype.count("VOID"))
    winstats.append(winningtype.count("VOID"))
    # print(Style.RESET_ALL)
    return winstats

def main():
    tallydata = []
    d = {str(graphsize) + str(k): ['lowest degree wins:', 'highest degree wins:','lowest clustering wins:', "highest clustering wins:", "middle degree wins:", "middle clustering wins:", "lowest ecc wins:", "highest ecc wins:", "middle ecc wins:", "rand wins:", "VOIDs"]}
        
    for x in range (0,100):
        tallydata.append(mainfunction())
        d["test" + str(x)] =  [tallydata[x][0], tallydata[x][1], tallydata[x][2],tallydata[x][3],tallydata[x][4],tallydata[x][5],tallydata[x][6],tallydata[x][7],tallydata[x][8],tallydata[x][9], tallydata[x][10]]
               
    
    pf = pd.DataFrame(d)
    print(d)
    print ("Finished " + str(graphtype) + str(k))  
    with pd.ExcelWriter('GraphTestJuly24th2025.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        wb = writer.book
        ws = wb.active
        pf.to_excel(writer, sheet_name= graphtype + str(k), index=False)
        
graphtype = "WS"      
graphsize = 50

for k in [10,25,39,47]:
    testper = [0] * 11
    main()

