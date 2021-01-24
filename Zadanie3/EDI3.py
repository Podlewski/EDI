import re
import arff
import io
import pandas as pd
from sklearn.metrics import jaccard_score
import numpy as np
import random 
import sys
from random import getrandbits
from io import StringIO
import pandas

# How To?!
# EDI3.py 5 T -> 5 klastrów, uzytkownik randomowy - True- tworzy losowego uzytkownika
# EDI3.py 8 F -> 8 klastrów, uzytkownik randomowy - False - stały uzytkownik
# EDI3.py -1 F -> klastry użytkonika, plik: ./clusters/cluster_custom.csv , uzytkownik randomowy - False - stały uzytkownik

n_cl = int(sys.argv[1])#int(input("Ilość klastrów(5, 8, 13): "))
user_arg = sys.argv[2]
print(n_cl)
if n_cl == 5:
    cluster_source = "./clusters/cluster5.csv"
elif n_cl == 8:
    cluster_source = "./clusters/cluster8.csv"
elif n_cl == 13:
    cluster_source = "./clusters/cluster13.csv"
elif n_cl == -1:
    cluster_source = "./clusters/cluster_custom.csv"
else:
    print("error")
    sys.exit()


#cluster = pd.read_csv("./clusters/cluster13.csv", header=None,delim_whitespace=True)
cluster = pd.read_csv(cluster_source, header=None,delim_whitespace=True)
pages = cluster.loc[:,0]
cluster = cluster.drop(cluster.columns[0], axis=1)  #Pages
cluster = cluster.drop(cluster.columns[0], axis=1)  #FullData
print(cluster)
print("pages")
print(pages)
    


def generate_user(n_pages):
    user = []
    for i in range(n_pages): 
        temp = random.choice([True, False])
        user.append(temp)
    return(user) 

def calc_jaccard_similarity(list1, list2):
    return jaccard_score(list1, list2)

# user + matrix z klastrami. Dla każdego klastra obliczamy wartosc Jaccarda (nr_klastra, wartość)
def compare(user, clusters):
    jaccard_per_cluster     = []
    for i in range(len(clusters.columns)):
        cluster_sim = calc_jaccard_similarity(user, cluster[cluster.columns[i]].to_numpy() )
        jaccard_per_cluster.append([i, cluster_sim])
    return jaccard_per_cluster


# wybor najlepszego klastra, zwraca index, wiec nr klastra = +1 
def get_the_most_similar_cluster(user, clusters):
    similarities = compare(user, clusters)
    max_index = np.argmax(similarities, axis=0)
    return max_index[1]

def printSim(sim):
    for i in range(len(sim)):
        print("Klaster: {0}\t podobieństwo: {1:.4f}".format(sim[i][0]+1, sim[i][1]))
    print("\n")

def recomend(user_sites, similar_sites):
    recommended = []
    for i in range(len(user_sites)):
        if user_sites[i] == False and similar_sites[i] == True:
            recommended.append(i)
    return recommended

def show_recomendation(recomendation_index_tab):
    if len(recomendation_index_tab) == 0:
        print("Brak")
    else:
        for i in range(len(recomendation_index_tab)):
            print(pages.iloc[ recomendation_index_tab[i] ])


#MAIN

#Ilość stron
n_pages = len(pages)

#Tworzenie użytkownika o zdefiniowanej ilości stron
if user_arg == "T":
    print("Tworzę użytkownika...")
    user = generate_user(n_pages)
else:
    user = [True, False, False, False, False, True, False, True, True, True, False, False, False, False, True, True, False, False, True, False, False, True, True, False, False, False, False, True, False, True]
print("Użytkownik: ", user ,"\n")

#Obliczam podobieństwa pomiędzy klastrami a użytkownikiem
similarities = compare(user,cluster)
printSim(similarities)
    
#Wybieram najbardziej podobny klaster. Wyświetlamy info o nim, i tworzymy kopie klastra do rekomendacji
cluster_id = get_the_most_similar_cluster(user,cluster)
print("Najbardziej podobny klaster to: ", cluster_id + 1) 
print("Podobieństwo z wybranym klasterem: ", similarities[cluster_id][1])
cluster_val = cluster[cluster.columns[cluster_id]].to_numpy()

# Wykorzystując użytkownika i wybrany klaster porównujemy je i rekomendujemy strony nieodwiedzone przez uyżytkownika a odwiedzone przez uczestników klastra.
rec = recomend(user, cluster_val)
print("Rekomenacje...")
show_recomendation(rec)


