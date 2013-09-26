import math
import sys
def file2graph(filename):
	try:
		fr = open(filename)
	except:
		print "Error: Unable to open graph file."
		exit()
	arrayOLines = fr.readlines()
	edgeNumbers = len(arrayOLines)
	edgeList = []
	for line in arrayOLines:
		line = line.strip()
		listFromLine = line.split('\t')
		if(len(listFromLine) == 2):
			if [listFromLine[0],listFromLine[-1]] in edgeList:
				print "Error: Duplicate link on line LINE."
				exit()	
			if listFromLine[0] == listFromLine[-1]:
				print "Error: Self-loop on line LINE."
				exit()
			else:
				edgeList.append([listFromLine[0],listFromLine[-1]])
		if (not (len(listFromLine) == 2)) and (not (len(listFromLine) == 0)):
			print "Error: Malformed graph file on line LINE."
			exit()
	return edgeList

# Total vertexs and links
def totalVertexsAndLinks(edgeList):
	dicVertexs = {}
	dicVertexInDegree = {}
	dicVertexOutDegree = {}
	edges = len(edgeList)
	for edge in edgeList:
		dicVertexs[edge[0]] = True
		dicVertexs[edge[1]] = True
		if(dicVertexInDegree.has_key(edge[1])):
			(dicVertexInDegree.get(edge[1])).append(edge[0])
		else:
			dicVertexInDegree[edge[1]] = [edge[0]]
		if(not dicVertexInDegree.has_key(edge[0])):
			dicVertexInDegree[edge[0]] = []

		if(dicVertexOutDegree.has_key(edge[0])):
			(dicVertexOutDegree.get(edge[0])).append(edge[1]);
		else:
			dicVertexOutDegree[edge[0]] = [edge[1]]
		if(not dicVertexOutDegree.has_key(edge[1])):
			dicVertexOutDegree[edge[1]] = []
	print("Nodes: " + str(len(dicVertexs)));
	print("Links: " + str(len(edgeList)));
	print("Symmetric links: %.5f%%" % symmetricLinks(edgeList))
	return dicVertexs,dicVertexInDegree,dicVertexOutDegree
def symmetricLinks(edgeList):
	edgeDic = {}
	symCount = 0
	for edge in edgeList:
		if(edgeDic.has_key(tuple([edge[1],edge[0]]))):
			edgeDic[tuple(edge)] = 1
			edgeDic[tuple([edge[1],edge[0]])] = 1
			symCount += 2
		if(not edgeDic.has_key(tuple(edge))):
			edgeDic[tuple(edge)] = 0
	edgeNum = len(edgeList)
        #print symCount
 	return (symCount / (edgeNum + 0.00)) * 100

# Average out-degree and in-degree

def averateDegrees(dicVertexInDegree,dicVertexOutDegree,dicVertexs):
	vertexsNum = len(dicVertexs)
	inDegrees = dicVertexInDegree.values()
	sum = 0
	for val in inDegrees:
		sum += len(val)
	aveInDegree = (sum + 0.0) / vertexsNum 
	outDegrees = dicVertexOutDegree.values()
	sum = 0
	for val in outDegrees:
		sum += len(val)
	aveOutDegree = (sum + 0.0) / vertexsNum

	print("Average outdegree: %.5f" % aveOutDegree)
	print("Average indegree: %.5f" % aveInDegree)
	return 

# Clustering coefficient
def coefficient(vertexsDic,inDegreeDic,outDegreeDic,edgeList):
	vertexs = vertexsDic.keys()
	c = 0.0
	summ = 0.0
	V = 0
	for vertex in vertexs:
		neighbours = findNeighbours(vertex,inDegreeDic,outDegreeDic)
		neborsNum = len(neighbours)
		if(neborsNum < 2):
			continue
		existLinksNum = actualNeighboursEdgesNum(neighbours,edgeList)
		possibleLinksNum = neborsNum * (neborsNum - 1.00)
		c = existLinksNum / possibleLinksNum
		summ += c
		V += 1
	if V == 0:
		c = 0
	else:
		c = summ / V
	#something wrong while coefficient is zero
	print("Clustering coefficient: %.5f" % c)
	return
def findNeighbours(vertex,inDegreeDic,outDegreeDic):
	inNebs = inDegreeDic.get(vertex)
	outNebs = outDegreeDic.get(vertex)
	if(inNebs == None):
		inNebs = []
	if(outNebs == None):
		outNebs = []
	neighbours = inNebs + outNebs
	return list(set(neighbours))

def actualNeighboursEdgesNum(neighbours,edgeList):
	summ = 0
	while(len(neighbours) > 1):
		vertex = neighbours.pop()
		for neibor in neighbours:
			if [vertex,neibor] in edgeList:
				summ += 1
			if [neibor,vertex] in edgeList:
				summ += 1
	return summ

# Assortativity
def assortativity(edgeList, dictInDegree,dictOutDegree):
	averInJ,averInK = getAverageDegree(edgeList,dictInDegree)
	averOutJ,averOutK = getAverageDegree(edgeList,dictOutDegree)
	assoII = getAssortativity(averInJ,averInK,edgeList,dictInDegree)
	assoOO = getAssortativity(averOutJ,averOutK,edgeList,dictOutDegree)
	print("Assortativity (in/in): %.5f" % assoII)
	print("Assortativity (out/out): %.5f" % assoOO)
	return
def getAverageDegree(edgeList,dictDegree):
	summJ = 0.00
	summK = 0.00
	for edge in edgeList:
		summJ += len(dictDegree.get(edge[0]))
		summK += len(dictDegree.get(edge[1]))
	E = len(edgeList)
	try:
		J = summJ / E
		K = summK / E
	except:
		print "Error: No vertex in this graph exist!."
		exit()
	return J,K

def getAssortativity(J,K,edgeList,dictDegree):
	E = len(edgeList)
	numerator = 0.0
	denominator = 0.0
	summ = 0.0
	for edge in edgeList:
		jiDegree = len(dictDegree.get(edge[0]))
		kiDegree = len(dictDegree.get(edge[1]))
		summ += (jiDegree - J) * (kiDegree - K)
	numerator = summ / E
	denominator = getDenominator(E,J,K,edgeList,dictDegree)
	if numerator == 0:
		return 0
	else:
		return (numerator / denominator)
def getDenominator(E,J,K,edgeList,dictDegree):
	sumK = 0.0
	sumJ = 0.0
	for edge in edgeList:
		ji = len(dictDegree.get(edge[0]))
		ki = len(dictDegree.get(edge[1]))
		sumJ += math.pow(ji - J, 2)
		sumK += math.pow(ki - K, 2)
	denum = math.sqrt(sumJ / E) * math.sqrt(sumK / E)
	return denum
# Radius and diameter
def radiusAndDiameter(dicVertexs, dicOutDegrees):
  eccs = {}
  shortPaths = {}
  radious = sys.maxint
  diameter = 0
  for vertex in dicVertexs.keys():
      if hasNeighbours(vertex, dicOutDegrees):
        eccs[vertex],vertexShortestPaths = BFS4maxShortestPath(vertex,dicOutDegrees)
        if eccs[vertex] < radious:
          radious = eccs[vertex]
        if eccs[vertex] > diameter:
          diameter = eccs[vertex]
        shortPaths.update(vertexShortestPaths)
  print("Radius: " + str(radious))
  print("Diameter: " + str(diameter))
  return shortPaths
def hasNeighbours(vertex,dicOutDegrees):
  return (not len(dicOutDegrees[vertex]) == 0)
def BFS4maxShortestPath(vertex,dicOutDegrees):
  distance = 0
  shortestPaths = {}
  visited = [vertex]
  vists = [vertex]
  while True:
    subvists = []
    for vist in vists:
      unvisitedNeighbours = getUnvisitedNeighbours(visited,dicOutDegrees[vist])
      for each in unvisitedNeighbours:
        shortestPaths[tuple([vertex,each])] = distance + 1
      subvists.extend(unvisitedNeighbours)
      visited.extend(unvisitedNeighbours)
    vists = subvists
    if len(vists) == 0:
      break
    distance += 1
  return distance, shortestPaths
def getUnvisitedNeighbours(visitedList,neighbours):
    unvsNbors = []
    for neighbour in neighbours:
      if not neighbour in visitedList:
        unvsNbors.append(neighbour)
    return unvsNbors
#Average path length
def averagePathLength(shortestPaths):
  distances = shortestPaths.values()
  denominator = len(shortestPaths)
  summ = sum(distances)
  averagePath = summ / (denominator + 0.000)
  print("Average path length: %.5f" % averagePath)
  return
#Connected components
def connectedComponent(dicDegrees):
	size = len(dicDegrees.keys())
	print("Weakly connected components: " + str(size))

#thanks
def thanks():
	print "So long and thanks for all the fish!"
