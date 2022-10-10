import re

for i in range (4) :
    #with open('Final_data/11001-12000.txt', 'r', encoding='ISO-8859-1') as f :
    with open('Amount Check_' + str(i) + '.txt', 'r', encoding='ISO-8859-1') as f :
        aa = f.readlines()
        amount = 0
        for data in aa :
            num = int(re.search(' : (.+?)\s', data).group(1))
            if num >= 5000 :
                num = 5000
            amount = amount + num
        print('Amount Check_' + str(i) + ' : ' + str(amount))
