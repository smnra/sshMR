#coding=utf-8

import paramiko
from stat import S_ISDIR
import os


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

    def exec(self,cmd = 'ls -l /'):
        try:
            self.stdin,self.stdout,self.stderr = self.ssh.exec_command(cmd)    #调用远程执行命令方法 exec_command() 执行 linux命令 ls -l
            return self.stdout.readlines()    #以列表的形式返回命令的返回值
        except Exception as e :
            print(str(e))

    def getFile(self, remotefile, localfile):
        try:
            self.sftp = self.ssh.open_sftp()
            self.sftp.get(remotefile, localfile)    #下载文件
        except Exception as e :
            print(str(e))

    def putFile(self, localfile, remotefile):
        try:
            self.sftp = self.ssh.open_sftp()
            #print(self.sftp.listdir('/'))    #打印目录列表
            self.sftp.put(localfile, remotefile)    #下载文件
        except Exception as e :
            print(str(e))


    # ------获取远端linux主机上指定目录及其子目录下的所有文件------
    def getRemoteDir(self, remote_dir):
        # 保存所有文件的列表
        all_files = list()

        # 去掉路径字符串最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取当前指定目录下的所有目录及文件，包含属性值

        try:
            self.sftp = self.ssh.open_sftp()
            #print(self.sftp.listdir('/'))    #打印目录列表
            files = self.sftp.listdir_attr(remote_dir)   #listdir_attr 获取远程主机路径上的文件列表包含文件属性
            for x in files:
                # remote_dir目录中每一个文件或目录的完整路径
                filename = remote_dir + '/' + x.filename
                # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
                if S_ISDIR(x.st_mode):
                    all_files.extend(self.getRemoteDir(filename))
                else:
                    all_files.append(filename)
            return all_files
        except Exception as e :
            print(str(e))

    def getDir(self, remotepath, localpath):
            # 获取远端linux主机上指定目录及其子目录下的所有文件
            all_files = self.getRemoteDir(remotepath)
            # 依次get每一个文件
            for x in all_files:
                filename = x.split('/')[-1]
                local_filename = os.path.join(localpath, filename)
                print(u'Get文件%s传输中...' % filename)
                self.sftp.get(x, local_filename)

    def getPathDir(self, remotepath, localpath):
            # 获取远端linux主机上指定目录及其子目录下的所有文件
            all_files = self.getRemoteDir(remotepath)
            # 依次get每一个文件
            for x in all_files:
                filename = x.split('/')[-1]             #取列表最后一个元素
                otherpath = x.replace(remotepath + "/","").replace(filename,"")      #把远程完整文件名  中包含的远程路径 删除,并且把文件名删除
                if len(otherpath) > 0 :     #如果远程存在文件夹,
                    local_dir = localpath  + otherpath      #拼接本地文件夹路径
                    if  not os.path.exists(local_dir) :
                        os.makedirs(local_dir)       #在本文件夹建立远程文件夹
                    local_filename = os.path.join(local_dir, filename)     #本地完整文件名
                else :
                    local_filename = os.path.join(localpath, filename)
                print(u'Get文件%s传输中...' % local_filename)
                self.sftp.get(x, local_filename)

if __name__ == '__main__' :
    remote = RemoteManage(hostname, username, password, port = 22, cmd = 'ls -l')
    result = remote.exec('ls -l /')
    print(result)
    #remote.getFile('/home/smnra/getip/requirements.txt', 'requirements.txt')
    remote.getPathDir('/etc/acpi',"./")
    remote.ssh.close() #关闭连接





