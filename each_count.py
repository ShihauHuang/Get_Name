import re
from os import _exit

with open('Amount Check_1.txt', 'r', encoding='ISO-8859-1') as f :
    aa = f.readlines()

with open('Name list_1.csv', 'r', encoding='ISO-8859-1') as f :
    bb = f.readlines()

csv_list = []
count = 0
for data in bb :
    current_id = data.strip().split(',')[0]

    if count == 0 :
        count = count + 1
        last_id = current_id
        continue

    elif current_id == last_id :
        count = count + 1
        continue

    else :
        #print(str(last_id) + ' count : ' + str(count))
        csv_list.append(str(last_id) + ' count : ' + str(count))
        count = 1
        last_id = current_id
        continue
csv_list.append(str(last_id) + ' count : ' + str(count)) # 最後一筆補回去

txt_list = []
for data in aa :
    try : 
        id = int(re.search('(.+?)_', data).group(1))
        num = int(re.search(' : (.+?)\s', data).group(1))
        if num >= 5000 :
            num = 5000
        
        txt_list.append(str(id) + ' count : ' + str(num))
    except :
        print(data)
        _exit(0)
        

for i in txt_list :
    if i not in csv_list and i.find('count : 0') == -1:
        print(i)
