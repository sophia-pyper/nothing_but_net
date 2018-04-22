import select
import socket
import sys
import Queue

sockIn = [server]
sockOut = []
messages = {}

readable = select.select(sockIn)
