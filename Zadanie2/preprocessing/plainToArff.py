import re
import arff
import io
import pandas as pd
df = pd.DataFrame(columns = ['Title', 'data'])   

#---------------------
# Aplikacja zmiania plik tekstowy (plainText) na plik arff.
# Dzieli plik wejściowy na poszczególne elementy, za pomocą słowa kluczowego 'Page'
# Tworzy df zawierającą numer strony (np.'Page 1') oraz jej zawartość.
# Uwaga: istniały sytaucje, gdy numer znajdował się w następnej lini niż słowo 'Page' - program rozwiązuje takie sytuacje.
#---------------------


#########################
# Uzupełnij nazwę pliku #
#########################

file_name = 'ul.txt'

line_back = ""
term = "Page "
page_counter = 0
data = ""
title = ""
file = open(file_name, encoding="utf8")
for line in file:
    line.strip().split('/n')
    #print(line)
    if term in line:
        if title != "":
            title = 'Page ' + str(page_counter)
            page_counter += 1
            df.loc[-1] = [title, data]  # adding a row
            df.index = df.index + 1     # shifting index
            df = df.sort_index()        # sorting by index
            print(title)
        out = line.partition("[")[2].partition("]")[0]
        if out == "":
            out = line_back.partition("[")[2].partition("]")[0]
            print(out)
        title =  out
        data = ""
    else:
        data += line
    line_back= line
file.close()
df = df[::-1]
df.to_csv("Output.csv", sep=',', index=False, header=False)
print(df)

arff.dump('Out.arff',
          df.values,
          relation='ul',
          names=df.columns)
