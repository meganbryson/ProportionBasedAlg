import networkx as nx
import time
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style
from operator import itemgetter


def neighcolours(G, nodenum, adjlist, color_map):
    #COMMENT:find the coloured neighbours of a specfic node and their proportions
    red = 0
    blue = 0
    gray = 0
    
    if color_map[nodenum] != "gray":
        return ["coloured", -1]

    for x in range(1, len(adjlist[nodenum])):
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
        
    

def findproportions(G, adjlist, color_map, pos):
    #COMMENT: find proportions of coloured neighbours 
    
    currentproplist = []
    for x in range (len(G.nodes)):
        currentproplist.append(neighcolours(G, x, adjlist, color_map))
    return currentproplist
        

def whosnext (G, adjlist, color_map, pos):
    #COMMENT: find who is next and colour them
    
    currentprops = findproportions(G, adjlist, color_map, pos)
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
             
    #COMMENT: if we never found a viable option print stalled
    # if highest < 0 or highestnode < 0:
    #     print (Back.BLACK + "stalled", end = " ")
        
        
    #COMMENT: otherwise colour it and print it
    else:
        # time.sleep(0.2)
        if currentprops[highestnode][1] > 0: 
            color_map[highestnode] = currentprops[highestnode][0] 
            
            if currentprops[highestnode][0] == "blue":
               print (Back.BLUE + str(highestnode), end = " ")
            else: 
               print (Back.RED + str(highestnode), end = " ")
        
        

    nx.draw(G, pos=pos, node_color=color_map, with_labels=True)
    time.sleep(0.5)
    plt.show()
    
    

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
               
def colournextstalled(G, adjlist, color_map, pos):              
      total = 0
      currentprops = findproportions(G, adjlist, color_map, pos)
      

      for x in range (len(currentprops)):
          
          if currentprops[x][1] < 0 and currentprops[x][0] != "coloured":
              print ("colouring stalled node: ", end ="")
              total +=1
              if x%2 == 0:
                  color_map[x] = "red"
                  print(Back.RED + str(x), end =" ") 
                  print(Style.RESET_ALL) 
       
              else:
                  color_map[x] = "blue"
                  print(Back.BLUE + str(x), end =" ") 
                  print(Style.RESET_ALL) 
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
        if rednum > 0:
            print (Back.RED + "\nout of", end = " ")
            print (total, end = " ")
            print ("nodes,", end = " ")
            print (Back.RED + str(rednum), end = "")
           
            print (" is/are red. across the graph, red is",end = " ")
            print((rednum/total)*100, end = "%.")
            print(Style.RESET_ALL, end = "")
           
        if bluenum > 0:
            print (Back.BLUE + "\nout of", end = " ")
            print (total, end = " ")
            print ("nodes,", end = " ")
            print (Back.BLUE + str(bluenum), end = "")
            
            print (" is/are blue. across the graph, blue is",end = " ")
            print((bluenum/total)*100, end = "%.")
            print(Style.RESET_ALL, end = "")
        if other > 0:
            print ("\nout of", end = " ")
            print (total, end = " ")
            print ("nodes,", end = " ")
            print (other, end = " ")
            print ("is/are neither red nor blue. across the graph, this is",end = " ")
            print((other/total)*100, end = "%.")
        return [(rednum/total)*100, (bluenum/total)*100, (other/total)*100]
    else: 
        print ("graph has no nodes. BROKEN!!!")
        return [0,0,0]
               
def main():
    #G = nx.Graph()
    graphsize = 15
    G = nx.connected_watts_strogatz_graph(graphsize, 2, 0.2, tries=100, seed=None)
    for i in range(graphsize):
        G.add_node(i)
  
    color_map = []
    pos = nx.spring_layout(G, seed = 100)
    nx.draw(G,  pos=pos, with_labels=True)
    plt.show()
 
    print ("\n~~~clustering of G (for some graph generations, the highest and lowest clust are both 0)~~~")
    clustlist = []
    for i in range(graphsize):
        x = nx.clustering(G, i)
        clustlist.append((i, x))
    print ("highest clust:", end = " ")
    print (sorted(clustlist, key=lambda x: x[1], reverse=True)[0])
    print ("lowest clust:", end = " ")
    print (sorted(clustlist, key=lambda x: x[1], reverse=True)[-1])
    print ("aprox middle clust:", end = " ")
    print (sorted(clustlist, key=lambda x: x[1], reverse=True)[len(clustlist)//2], end = " ")
    print ("(calculated with: sorted(clustlist, key=lambda x: x[1], reverse=True)[len(clustlist)//2])")
    
    
    print ("\n~~~degrees of G~~~")
    degreelist = []
    for i in range(graphsize):
        degreelist.append((i,G.degree(i) ))
    print ("highest degree:", end = " ")
    print (sorted(degreelist, key=lambda x: x[1], reverse=True)[0])
    print ("lowest degree:", end = " ")
    print (sorted(degreelist, key=lambda x: x[1], reverse=True)[-1])
    print ("aprox middle degree:", end = " ")
    print (sorted(degreelist, key=lambda x: x[1], reverse=True)[len(degreelist)//2], end = " ")
    print ("(calculated with: sorted(degreelist, key=lambda x: x[1], reverse=True)[len(degreelist)//2])")
    

    seed1 = input(Back.BLUE + '\nblue seed: ')
    seed2 = input (Back.RED + 'red seed: ')
    # seed3 = input(Back.BLUE + '\nblue seed 2: ')
    print ("\n")
    print(Style.RESET_ALL)
    
    

    for node in G:
        
        if node == int(seed1):
            color_map.append('blue')
          
        elif node == int(seed2):
            color_map.append('red')
            
        else: 
            color_map.append('gray')  
            
    nx.draw(G, pos=pos, node_color=color_map, with_labels=True)
    plt.show()
    time.sleep(1)
    print (" ")
    adjlist = []
    for line in generate_adjlist_with_all_edges(G):
        tempadj = line.split()
        adjlist.append(tempadj)
        
    print ("colouring order:")
    for node in range (len(G)-2):
        whosnext (G, adjlist, color_map, pos)
    print(Style.RESET_ALL)     
    totalstalled = 0
    firstcolourstats = []
    chosetocolor = input('\n\nif there are uncoloured nodes, do you run code to colour rest of graph? (y / n): ') 
    
    if chosetocolor == "y":
        print ("\nCURRENT STATS:")
        firstcolourstats = percent(G, adjlist, color_map)
        left = howmanyleft(G, adjlist, color_map)
        while left != 0:
            print ("\n")
            print (left, end= " ")
            print ("nodes left to colour. it may be the case that not all are stalled however, just not reachable.")
            totalstalled += colournextstalled(G, adjlist, color_map)
        
            left = howmanyleft(G, adjlist, color_map)
            
            if left != 0:
                print ("\nrestarting colouring alg. \ncolouring order:")
                for node in range (left):
                    whosnext (G, adjlist, color_map, pos)
                left = howmanyleft(G, adjlist, color_map)
            
        print(Style.RESET_ALL)
        
    
    nx.draw(G, pos=pos, node_color=color_map, with_labels=True)
    plt.show()
    print ("\n")
    print(Back.GREEN + "\n~~~~~FINAL STATS~~~~~")
    print(Style.RESET_ALL) 
    print ("\nthis graph is undirected, unweighted, connected and has no self-loops")
    print ("the graph type is connected watts strogatz")
    print ("\nthe graph has a density of ", end = "")
    print (nx.density(G))
    print ("the final graph colouring coloured in", end = " ")
    print (totalstalled, end = " ")
    print ("stalled nodes (this is only nodes that were stalled by the end of the colouring alg, not nodes that were temporarily stalled in the alg, this also does not include stalled nodes the user chose not to colour)")
    print ("\nblue starting node was", end = " ")
    print (Back.BLUE + str(seed2), end = "")
    print(Style.RESET_ALL)  
    print ("red starting node was", end = " ")
    print (Back.RED + str(seed1), end = "")
    # print ("\nblue2 starting node was", end = " ")
    # print (Back.BLUE + str(seed3), end = "")
    print(Style.RESET_ALL)  
    currentstats = percent(G, adjlist, color_map)
   
    if totalstalled >0:
        print ("\nfor red, that is up", end = " ")
        print (Back.RED + str(currentstats[0] - firstcolourstats[0]), end = "")
        print (Style.RESET_ALL, end = "% from the first colouring")
        print ("\nfor blue, that is up", end = " ")
        print (Back.BLUE + str(currentstats[1] - firstcolourstats[1]) , end = "")
        print (Style.RESET_ALL, end = "% from the first colouring")
    
    again = input("\n\nrun again? y/n ")
    if again == "y":
        main()
    
main()
      