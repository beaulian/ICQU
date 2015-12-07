#coding=utf-8

import os
from app import create_app
from flask.ext.script import Manager, Server

app = create_app()
manager = Manager(app)
server = Server(host='localhost', port=8000)
manager.add_command('server', server)

if __name__ == '__main__':
	manager.run()
