import socket
import sys
from thread import *
import pickle


def register(conn, addr, nick,port):
    try:
        users = pickle.load(open("users", "rb"))
    # print users
    except:
        users = {}
        pickle.dump(users, open("users", "wb"))
    # print users[addr[0]]
    try:
        nickname = users[port]['nick']
        # print 'hi'
        conn.sendall('Registerd  : ' + nickname)
    except:
        users[port] = {}
        users[port]['port_local'] = addr[1]
        users[port]['port'] = port
        users[port]['ip'] = addr[0]
        users[port]['nick'] = nick
        users[port]['fileList'] = {}
        conn.sendall('Registerd ' + nick)

    pickle.dump(users, open("users", "wb"))

def upload_file(conn, file , portl):
    try:
        users = pickle.load(open("users", "rb"))
    # print users
    except:
        conn.sendall('You need to register first')
        return
    try:
        nickname = users[portl]['nick']
    except:
        conn.sendall('You need to register first')
        return

    fileName = file.split(',')[0]
    # print fileName
    filePath = file.split(',')[1]
    # print filePath
    users[portl]['fileList'][fileName] = filePath

    pickle.dump(users, open("users", "wb"))
    conn.sendall('File ' + fileName + ' added')


def search(conn, fileName, activePeers):
    try:
        users = pickle.load(open("users", "rb"))
    # print users
    except:
        conn.sendall('No users registered till now')
        return

    usersHavingFile = {}
    userList = users.keys()

    for user in userList:
        print user
        found = False
        # print users[user]['fileList'].keys()
        if fileName in users[user]['fileList'].keys():
            if user in activePeers:
                usersHavingFile[user] = {}
                usersHavingFile[user]['port'] = users[user]['port']
                usersHavingFile[user]['nick'] = users[user]['nick']
                usersHavingFile[user]['filePath'] = users[user]['fileList'][fileName]
                usersHavingFile[user]['ip'] = users[user]['ip']

    conn.sendall(str(usersHavingFile))




host = '127.0.0.1'
port = 55555

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
try:
    s.bind((host,port))
except socket.error, msg:
    print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
    sys.exit()
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'


activePeers = []
users = {}

def clientthread(conn,addr):

    conn.send('Select an option\n 1. Register\n  2. Upload file\n 3.Download\n 4.Exit')

    portl = int(conn.recv(1024))
    if not portl:
        return
    activePeers.append(portl)

    while 1:

        try:
            data = conn.recv(1024)
        except:
            print "connection is end"
            break
        if not data:
            break
        if (data.split('\n')[0] == 'REGISTER'):
            register(conn, addr, data.split('\n')[1] , portl)

        elif data.split('\n')[0] == 'register_file':
            upload_file(conn,data.split('\n')[1] , portl)
        elif data.split('\n')[0] == 'SEARCH':
            search(conn,data.split('\n')[1],activePeers)

    activePeers.remove(portl)
    conn.close()


    
    

while 1:
    conn, addr = s.accept()

    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (conn,addr))


s.close()