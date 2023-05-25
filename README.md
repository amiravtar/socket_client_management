# python

## req

```shell
pip install -r requirements.txt
```

### running

```shell
python server/server.py
```

On a diffrent terminal

```shell
python client/client.py
```

### compiling

```shell
pip install pyinstaller
```

```shell
pyinstaller --name="server" --windowed --onefile -p ./server server/main.py
pyinstaller --name="client" --windowed --onefile -p ./client client/main.py
```

then run the executables in shell

```shell
./dist/server
./dist/client
```
