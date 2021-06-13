import csv

group = {'솔로' : 1, '그룹' : 2}
sex = {'남성' : 1, '여성' : 2, '혼성' : 3}
genre = dict()
genre_idx = 1

songs = []
f = open('song.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    songs.append(line)

singers = []
f = open('singer.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    singers.append(line)

singers_dict = {}
for data in singers:
    singers_dict[data[0]] = [sex[data[1]], group[data[2]], int(data[3])]


f_x = open('data_x.csv', 'w', newline='', encoding='UTF-8')
wr_x = csv.writer(f_x)

f_y = open('data_y.csv', 'w', newline='', encoding='UTF-8')
wr_y = csv.writer(f_y)

for data in songs:
    tmp = [data[0], data[1], data[8]]
    date = data[7].split('.')
    tmp.append((int(data[0]) - int(date[0])) * 12 + int(data[1]) - int(date[1]))
    g = data[6].split(',')[0]
    if genre.get(g, 0) != 0:
        tmp.append(genre[g])
    else:
        genre[g] = genre_idx
        tmp.append(genre_idx)
        genre_idx += 1
    tmp.extend(singers_dict[data[4]])

    wr_x.writerow(tmp)
    wr_y.writerow([data[2]])