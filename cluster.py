import math
import pdb

def assign_new_cluster(cluster,similarity,oldsent):
	new_sim_avg = []

	for i in range(len(cluster)):
		nsd = 0
		for sent in cluster[i]:
			nsd = nsd + similarity[oldsent][sent]
		new_sim_avg.append( (nsd * 1.0)/(len(cluster[i])*1.0))
	maxsim = max(new_sim_avg)
	#print "similarity avg"
	#print new_sim_avg
	newcluster = new_sim_avg.index(maxsim)
	cluster[newcluster].append(oldsent)
	return cluster

def checkreplace(cl_elements, similarity,check_sent):
	osm = 0
	nsm = 0
	for sent in cl_elements:
		osm = osm + similarity[cl_elements[0]][sent]
		nsm = nsm + similarity[check_sent][sent]
	if nsm > osm:
		return True
	else:
		return False

def medoid_rearrange(inicluster, similarity):
	no_clusters = len(inicluster)
	cluster = inicluster
	no_sent = len(similarity)
	for i in range(no_sent):
		for j in range(no_clusters):
			if i in cluster[j]:
				#replace medoid with same cluster element
				if i != cluster[j][0]:
					#not medoid element
					if checkreplace(cluster[j],similarity,i):
						old = cluster[j][0];
						new = i 
						cluster[j].remove(i)
						cluster[j][0] = i 
						cluster = assign_new_cluster(cluster, similarity,old)
						break
			else:
				is_medoid = False
				cluster_id = j
				for k in range(no_clusters):
					if cluster[k][0] == i:
						is_medoid = True
					if i in cluster[k]:
						cluster_id = k

				if is_medoid == False :
					if checkreplace(cluster[j],similarity,i):
						old = cluster[j][0]
						new = i
						cluster[cluster_id].remove(i)
						cluster[j][0] = i
						cluster = assign_new_cluster(cluster,similarity,old)
						break
	return cluster



def kmedoid(sentence_similarity,k):
	
	clustsen = []
	for i in range(0,k):
		clust = []
		clust.append(i)
		clustsen.append(clust)

	#print(clustsen)
	
	for i in range(k,len(sentence_similarity)):
		maxval = 0
		maxindex = 0

		for j in range(len(clustsen)):
			if(sentence_similarity[i][clustsen[j][0]] > maxval and clustsen[j][0] != i):
				maxval = sentence_similarity[i][clustsen[j][0]]
				maxindex = j
		clustsen[maxindex].append(i)
	#print "Initial clusters"
	#print clustsen
	#print "medoid rearrange"
	for i in range(k):
	   clustsen = medoid_rearrange(clustsen,sentence_similarity)
	   #print clustsen	
	
	return clustsen