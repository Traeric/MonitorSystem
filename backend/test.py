import paramiko

transport = paramiko.Transport(('192.168.43.213', 22))
transport.connect(username='ericjin', password='0528')

sftp = paramiko.SFTPClient.from_transport(transport)
# 将location.py 上传至服务器 /tmp/test.py
sftp.put('/media/ericjin/Data/python/projects/crazyEye/MonitorSystem/statics/file_save_dir/upload/test1547456440.349681.sh',
         '/home/ericjin/Desktop/test1547456440.349681.sh')

transport.close()
