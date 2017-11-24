import socket

def getipaddress(hostname,port =25) :
    results = socket.getaddrinfo(hostname, port, 0, 0, socket.IPPROTO_TCP)
    hosts = []
    for resule in results :
        hosts.append(resule[4][0])
        print(resule[4][0])
    return hosts

if __name__ == '__main__':
    hosts = []
    hosts = getipaddress('smtp.163.com',25)