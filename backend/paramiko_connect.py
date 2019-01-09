#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input

import paramiko

try:
    import interactive
except ImportError:
    from . import interactive


def manual_auth(t, username, pw):
    default_auth = "p"
    # auth = input(
    #     "Auth by (p)assword, (r)sa key, or (d)ss key? [%s] " % default_auth
    # )
    # if len(auth) == 0:
    #     auth = default_auth
    auth = default_auth   # TODO: 后续需要修改
    if auth == "r":
        default_path = os.path.join(os.environ["HOME"], ".ssh", "id_rsa")
        path = input("RSA key [%s]: " % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass("RSA key password: ")
            key = paramiko.RSAKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    elif auth == "d":
        default_path = os.path.join(os.environ["HOME"], ".ssh", "id_dsa")
        path = input("DSS key [%s]: " % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.DSSKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass("DSS key password: ")
            key = paramiko.DSSKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    else:
        # pw = getpass.getpass("Password for %s@%s: " % (username, hostname))
        t.auth_password(username, pw)


def ssh_connect(ssh_interactive_instance, host_to_remote_user_obj):
    hostname = host_to_remote_user_obj.host.ip_addr
    port = host_to_remote_user_obj.host.port
    username = host_to_remote_user_obj.remote_user.username
    password = host_to_remote_user_obj.remote_user.password
    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        print("*** Connect failed: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    t = None
    try:
        t = paramiko.Transport(sock)
        # 生成socket相关链接
        try:
            t.start_client()
        except paramiko.SSHException:
            print("*** SSH negotiation failed.")
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(
                os.path.expanduser("~/.ssh/known_hosts")
            )
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(
                    os.path.expanduser("~/ssh/known_hosts")
                )
            except IOError:
                print("*** Unable to open host keys file")
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if hostname not in keys:
            print("*** WARNING: Unknown host key!")
        elif key.get_name() not in keys[hostname]:
            print("*** WARNING: Unknown host key!")
        elif keys[hostname][key.get_name()] != key:
            print("*** WARNING: Host key has changed!!!")
            sys.exit(1)
        else:
            print("*** Host key OK.")

        if not t.is_authenticated():
            # 进行登录认证
            manual_auth(t, username, password)
        # 认证完之后再次进行判断，如果还是未认证程序就退出了
        if not t.is_authenticated():
            print("*** Authentication failed. :(")
            t.close()
            sys.exit(1)

        chan = t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        # 登录成功，调用interactive_shell()进行交互
        print("*** Here we go!\n")
        # 记录登录日志
        models = ssh_interactive_instance.models
        models.AuditLog.objects.create(
            crazy_eye_account=ssh_interactive_instance.user,
            host_to_remote_users=host_to_remote_user_obj,
            log_type=0,     # 登录日志
            content="%s登录" % ssh_interactive_instance.user.name,
        )
        # 将主机信息以及堡垒机账号信息传入以便于后续记录日志
        chan.host_info = host_to_remote_user_obj
        chan.crazy_eye_account = ssh_interactive_instance.user
        # 将models也赋值给chan
        chan.models = models
        interactive.interactive_shell(chan)
        chan.close()
        t.close()
        # 退出日志
        models.AuditLog.objects.create(
            crazy_eye_account=ssh_interactive_instance.user,
            host_to_remote_users=host_to_remote_user_obj,
            log_type=2,  # 退出日志
            content="%s登出" % ssh_interactive_instance.user.name,
        )
    except Exception as e:
        print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
        traceback.print_exc()
        try:
            t.close()
        except Exception as e:
            print(e)
            pass
        sys.exit(1)
