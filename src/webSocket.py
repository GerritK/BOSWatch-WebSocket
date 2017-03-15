#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
WebSocket plugin to send pocsag, zvei and fms via websocket to webclients.

@author: Gerrit Kaul

@requires: none
"""

#
# Imports
#
import logging  # Global logger
import json  # for data-transfer
import thread
from includes import globalVars  # Global variables

# Helper function, uncomment to use
# from includes.helper import timeHandler
# from includes.helper import wildcardHandler
from includes.helper import configHandler

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

server = None
clients = []


##
#
# onLoad (init) function of plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
    """
    While loading the plugins by pluginLoader.loadPlugins()
    this onLoad() routine is called one time for initialize the plugin

    @requires:  nothing

    @return:    nothing
    @exception: Exception if init has an fatal error so that the plugin couldn't work

    """
    try:
        if configHandler.checkConfig('webSocket'):
            try:
                global server
                server = SimpleWebSocketServer('', globalVars.config.getint("webSocket", "port"), EventSocket)
                thread.start_new_thread(server.serveforever, ())
            except:
                logging.error("could not create web socket server. check config!")
                logging.debug("could not create web socket server. check config!", exc_info=True)
                return
    except:
        # something very mysterious
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)


##
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ, freq, data):
    """
    This function is the implementation of the Plugin.

    If necessary the configuration hast to be set in the config.ini.

    @type    typ:  string (FMS|ZVEI|POC)
    @param   typ:  Typ of the dataset
    @type    data: map of data (structure see readme.md in plugin folder)
    @param   data: Contains the parameter for dispatch
    @type    freq: string
    @keyword freq: frequency of the SDR Stick

    @requires:  If necessary the configuration hast to be set in the config.ini.

    @return:    nothing
    @exception: nothing, make sure this function will never thrown an exception
    """
    try:
        supportedTypes = ["FMS", "ZVEI", "POC"]
        if typ in supportedTypes:
            sendData = json.dumps(data)
            for client in clients:
                client.sendMessage(u'' + sendData)
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)


class EventSocket(WebSocket):

    def handleMessage(self):
        return

    def handleConnected(self):
        logging.debug("new web socket client connected from %s", self.address)
        clients.append(self)

    def handleClose(self):
        logging.debug("web socket client '%s' disconnected", self.address)
        clients.remove(self)
