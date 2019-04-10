import pyorient


#initializing Orient client
client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "tiger")
client.db_open("KevinBaconTEST", "root", "tiger")



baconVertex = "#33:33588"


def returnTargetVertex(actor):
    ans = client.query("select @rid from ActorNode where actor = " + "\'" + actor + "\'")
    for item in ans:
        data = item.oRecordData
        rid = data['rid']
        return rid

def generatePath(rid):
    outputList = []
    ans = client.query("select shortestpath(" + str(rid) + "," + str(baconVertex) + ")")
    for item in ans:
        path = item.oRecordData['shortestpath']
        for vertex in path:
            outputList.append(vertex)
    return outputList

def parseVertex(rid):
    ans = client.query("select from ActorNode where @rid = " + rid)
    for item in ans:
        actor = item.oRecordData['actor']
        movie = item.oRecordData['movie']
        role = item.oRecordData['role']
        tempDict = {
            "actor":actor,
            "movie":movie,
            "role":role  
            }
        return tempDict

def hasActor(actor):
    ans = client.query("select from ActorNode where actor = \'" + actor + "\'")
    if not ans:
        return False
    else:
        return True

def Engine(target):
    
    solution = ""

    if (hasActor(target) == False):
        return("Our database does not include that actor.  Sorry!")

    if (target == 'Kevin Bacon'):
        return("I bet you thought this would be a fail-case, didn\'t you?")

    targetVertex = returnTargetVertex(target)

    path = generatePath(targetVertex)

    pathUnpacked = []

    for vertex in path:
        unpacked = parseVertex(str(vertex))
        pathUnpacked.append(unpacked)


    if (pathUnpacked[0]['actor'] == pathUnpacked[1]['actor']):
        pathUnpacked.pop(0)

    if(pathUnpacked[-1]['actor'] == pathUnpacked[-2]['actor']):
        pathUnpacked.pop(-1)

    for item in pathUnpacked:
        actor = item['actor']
        movie = item['movie']
        role = item['role']
        if (actor == 'Kevin Bacon'):
            addition = actor + " played " + role + " in " + movie + "!"
        elif (actor == target):
            addition = actor + " played " + role + " in " + movie + ", \n"

        else:
            addition = actor + " played " + role + " in " + movie + ", \n"
        solution += addition
    return solution