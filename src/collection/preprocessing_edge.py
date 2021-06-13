import csv

songs = []
f = open('song.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    songs.append(line)


f = open('data_edge.csv', 'w', newline='', encoding='UTF-8')
wr = csv.writer(f)


for i in range(len(songs)):
    for j in range(i + 1, len(songs)):
        if songs[i][4] == songs[j][4]:
            wr.writerow([i, j])
        elif songs[i][0] == songs[j][0] and songs[i][1] == songs[j][1] and int(songs[j][2]) - int(songs[i][2]) <= 5:
            wr.writerow([i, j])