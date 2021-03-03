import socket
import myGif
import myMap

province_salary = []
edu_salary = []
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen()
print('服务器正在启动...')

conn, address = s.accept()
print(address)
gif = myGif.MyGif(1)
map = myMap.MyMap(1)
while True:
    data = conn.recv(1024).decode('utf-8')
    if data != '':
        print(data)
    if data[0] == '#':
        split_data = data[1:-1].split(';')
        for item in split_data:
            tmp = item.split(',')
            province_salary.append([tmp[0], float(tmp[1]), int(tmp[2])])
        map.add_data(province_salary)
    elif data[0] == '?':
        split_data = data[1:-1].split(';')
        for item in split_data:
            tmp = item.split(',')
            edu_salary.append([tmp[0], float(tmp[1])])
        gif.add_edu_data(edu_salary)
    edu_salary = []
    province_salary = []
conn.close()
s.close()
