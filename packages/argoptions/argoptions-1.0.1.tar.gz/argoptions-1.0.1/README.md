
see tornado.options

```pycon
>>> from argoptions import options
>>> options.define('appname', default='', type=str, help='the app name')
>>> options.define('flag', default='', type=str, help='load config file by this specified flag')
>>> options.define('port', default=65535, type=int, help='run server on this specified port')
>>> options.parse_command_line()
>>> 
>>> 
>>> 
>>> from argoptions import options
>>> port = options.options.port
>>> print(port)
```

---------------------------------------------------------------------
