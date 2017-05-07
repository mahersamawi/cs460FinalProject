#CS 460 Project: Malicious Math Library

Infected Machine

Call any function from the library
```python
import ourmathlib
print ourmathlib.add(5,4)
```



How to use attack_server.py
Server
```python
python attack_server.py
Enter a command to run: 
```
Our final project is a malicious Python library that doesn’t require any elevated permissions. When the user imports the library, it spawns a UDP client that listens for commands from our server. The server can force the victim to DOS a target, encrypt/decrypt their home directory for ransom purposes, and steal their files. The malicious python code is hidden within the library until runtime.
