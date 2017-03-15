# BOSWatch WebSocket Plugin
This plugin adds websocket support to [BOSWatch](https://github.com/Schrolli91/BOSWatch).

### Installation
Copy files from `src` directory to `plugins/webSocket`.

### Dependencies
This plugin requires the [SimpleWebsocketServer](https://github.com/dpallot/simple-websocket-server) python lib.

### Config
Add following values to `config/config.ini`:

##### Section `[Plugins]`
```
webSocket = 1
```

##### Section `[webSocket]`
```
port = 8112
```
