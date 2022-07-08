from rdflib.namespace import FOAF, XSD, RDFS, RDF, OWL
from rdflib import Graph, URIRef, RDF, Literal, Namespace, BNode
import textdistance

# curated: persons, agentrole, objectrole, eventcore, timeperiod
# observed: all from people + copy of event (observed_1)

# file for results
f = open("/home/marta/Documents/2022_ISWS/researchTask/results.csv", "w")
f.write("observed file,curated file,score,\n")

## define maximum number of files
max_curated = 5
max_observed = 22
max_arco = 3

## indexes
i = 1
j = 1
k = 1

## lists of file paths
curated_list = []
observed_list = []
arco_list = []

## add file paths to list
while i <= max_observed:
    observed_file = "observed_" + str(i) + ".ttl"
    observed_list.append(observed_file)
    i = i + 1
while j <= max_curated:
    curated_file = "curated_" + str(j) + ".owl"
    curated_list.append(curated_file)
    j = j + 1
while k <= max_arco:
    arco_file = "/home/marta/Documents/2022_ISWS/researchTask/files/arco_" + str(k) + ".ttl"
    arco_list.append(arco_file)
    k = k + 1
    
checked = []
curated_sim = {}
observed_curated = {}

m = 0


for o in observed_list: ## for each observed
    observed=Graph()
    observed.parse("/home/marta/Documents/2022_ISWS/researchTask/files/" + o) # create graph from file
    
    observed_curated[o.split(".")[0]] = {}
    observedSubjects = [] # list for subject names
    observedPredicates = [] # list for subject names
    observedObjects = [] # list for subject names
    

    for s,p,ob in observed:
        if "://" not in s: # deal with blank nodes
            continue
            ## they still have to taken into account somehow
        else:
            prefix, namespace, name = observed.compute_qname(s)
            observedSubjects.append(name)
        if "://" not in p: # deal with blank nodes
            continue
            ## they still have to taken into account somehow  
        else:
            prefix, namespace, name = observed.compute_qname(p)
            observedPredicates.append(name)
        
        ## cannot handle objects the same way
        
        ## section capable of handling blank nodes (which will have extra triples connected to them), literals, and URIs
    
    for c in curated_list: ## compare against all curated
        curated=Graph()
        curated.parse("/home/marta/Documents/2022_ISWS/researchTask/files/" + c)
        
        n = 0
        observed_curated[o.split(".")[0]][c.split(".")[0]] = {}
        
        for s,p,ob in curated:
            if (s,p,ob) in observed:
                n = n + 1
                #observed_curated[o.split(".")[0]][c.split(".")[0]] = n
            
        curatedSubjects = []
        curatedPredicates = []
        for s,p,ob in curated:
            if "://" not in s: ## deal with blank nodes
                ## they still have to taken into account somehow
                continue
            else:
                prefix, namespace, name = curated.compute_qname(s)
                curatedSubjects.append(name)
            if "://" not in p: ## deal with blank nodes
                ## they still have to taken into account somehow
                continue
            else:
                prefix, namespace, name = curated.compute_qname(p)
                curatedPredicates.append(name)
            
            #while m < 10000:
            for oS in observedSubjects:
                for cS in curatedSubjects:
                        #print(oS + " -> " + cS)
                    if oS == cS:
                        if oS in checked:
                            continue
                        else:
                            n = n + 0.5
                            checked.append(str(oS))
                    else:
                        sim = textdistance.jaccard.similarity(cS,oS)
                        if sim >= 0.7:
                            n = n + 0.25
                        #m = m + 1
        observed_curated[o.split(".")[0]][c.split(".")[0]] = n
        f.write(o.split(".")[0] + "," + c.split(".")[0] + "," + str(n) + "\n") 

            #for cP in curatedPredicates:
                #for oP in observedPredicates:
                    #sim = textdistance.jaccard.similarity(cP, oP)
                    #if sim > 0.5:
                        #print(sim)
                        #continue
                        
print(observed_curated)
f.close()
