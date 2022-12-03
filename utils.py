from Crypto.Cipher import AES
from Crypto import Random
import struct
import json

max_buff_size = 1024
key = b'fdj27pFJ992FkHQb'

# 功能描述: encrypt函数对数据进行加密
def encrypt(data):
    code = Random.new().read(AES.block_size)
    # 密钥，密码反馈模式，
    cipher = AES.new(key, AES.MODE_CFB, code)
    return code + cipher.encrypt(data)

# 功能描述: decrypt函数对数据进行解密。
def decrypt(data):
    return AES.new(key, AES.MODE_CFB, data[:16]).decrypt(data[16:])

# 功能描述: 发送数据前会在数据前部加上指明数据大小的一个二字节数。
def pack(data):
    # 打包为字节流，返回一个包装后的字符串。
    return struct.pack('>H', len(data)) + data

def send(socket, data_dict):
    # json.dumps将一个Python数据结构转换为JSON
    socket.send(pack(encrypt(json.dumps(data_dict).encode('utf-8'))))

# 功能描述：接收数据时先接收这个二字节数，获取将要接收的数据包的大小，然后接收这个大小的数据作为本次接收的数据包。
def recv(socket):
    data = b''
    # pack打包，然后可以用unpack解包。
    surplus = struct.unpack('>H', socket.recv(2))[0]
    socket.settimeout(5)
    while surplus:
        recv_data = socket.recv(max_buff_size if surplus > max_buff_size else surplus)
        data += recv_data
        surplus -= len(recv_data)
    socket.settimeout(None)
    return json.loads(decrypt(data))
