#coding=utf-8

import paramiko

hostname = '192.168.192.130'
username = 'smnra'
password = 'smnra000'
paramiko.util.log_to_file('syslogin.log')    #发送日志到文件

class RemoteManage():
    def __init__(self,hostname, username, password, port = 22, cmd = 'ls -l'):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.cmd = cmd
        self.ssh = paramiko.SSHClient()    #创建ssh客户端实例
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    #自动接收位置服务器的key
        self.ssh.connect(hostname = self.hostname, username = self.username, password = self.password)    #创建ssh连接

    def exec(self,cmd = 'ls -l /www'):
        try:
            self.stdin,self.stdout,self.stderr = self.ssh.exec_command(cmd)    #调用远程执行命令方法 exec_command() 执行 linux命令 ls -l
            return self.stdout.readlines()    #以列表的形式返回命令的返回值
        except Exception as e :
            print(str(e))

    def putfile(self, localpath, remotepath):
        try:
            self.sftp = self.ssh.open_sftp()
            print(self.sftp.listdir('/'))    #打印目录列表
            self.sftp.put(localpath, remotepath)    #下载文件
        except Exception as e :
            print(str(e))

if __name__ == '__main__' :
    remote = RemoteManage(hostname, username, password, port = 22, cmd = 'ls -l')
    result = remote.exec('ls -l /')
    print(result)
    remote.putfile('ssh.py','/home/smnra/ssh.py')

    #remote.ssh.close()    #关闭连接




