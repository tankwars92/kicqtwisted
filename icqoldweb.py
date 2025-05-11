# -*- coding: utf-8 -*-
# ICQ bot

# UIN
UIN = "1111111" # Your UIN here.
PASS = "..."  # Your password here.

# Server
host = ("kicq.ru", 5190)
icqMode = 1

# Status message
AMSG = "I'm here +)"

from twisted.words.protocols import oscar
from twisted.internet import protocol, reactor
import urllib2
import sys
import socket

# Class Bot
class Bot(oscar.BOSConnection):
    capabilities = [oscar.CAP_CHAT] # oscar.CAP_CHAT = AOL AIM.

    def initDone(self):
        print "Connect ",UIN," to server", host[0], host[1]

        self.requestSelfInfo().addCallback(self.gotSelfInfo)
        self.requestSSI().addCallback(self.gotBuddyList)
        self.setAway(AMSG)

    def gotSelfInfo(self, user):
        print user.__dict__
        self.name = user.name

    def gotBuddyList(self, l):
        print l
        self.activateSSI()
        self.setProfile("""ICQBot""")
        self.setIdleTime(0)
        self.clientReady()

 

    def gotAway(self, away, user):
        if away:
            print "User ", user,": ",away

    def receiveMessage(self, user, multiparts, flags):
        print "\n< From: ", user.name
        print "< Message: ", multiparts[0][0].decode('cp1251')

        command = multiparts[0][0].replace("\x00", "")
        print(multiparts[0])

        if command == "!logout" and user.name == "3739186":
            self.sendMessage("3739186", "Goodbye!")
            sys.exit()

        if command.startswith("!"):
            if command.startswith("!topics"):
                HOST = "localhost"
                PORT = 8024

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))

                s.send("GET /old-web HTTP/1.0\r\nHost: localhost\r\n\r\n")

                response = ""
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    response += data
                s.close()

                headers, quote = response.split("\r\n\r\n", 1)

                try: 
                    self.sendMessage(user.name, quote.decode('utf-8').encode("cp1251"))
                except Exception, e:
                    print(e)   
            elif command.startswith("!news"): # !news - last news on old-web.com
                HOST = "localhost"
                PORT = 8024

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))

                s.send("GET /old-news HTTP/1.0\r\nHost: localhost\r\n\r\n")

                response = ""
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    response += data
                s.close()

                headers, quote = response.split("\r\n\r\n", 1)

                try: 
                    self.sendMessage(user.name, quote.decode('utf-8').encode("cp1251"))
                except Exception, e:
                    print(e)
            elif command.startswith("!help"):
                self.sendMessage(user.name, "---------->>> HELP <<<----------\n\n!topics - Last topics on the forum of old-web.com.\n!news - Last downgrade news on the old-web.com.")
            else:
                self.sendMessage(user.name, "Unknown command. Use !help to see list of all supported commands.")
        else:
            self.sendMessage(user.name, "Unknown command. Use !help to see list of all supported commands.")

class BotAuth(oscar.OscarAuthenticator):
    BOSClass = Bot

protocol.ClientCreator(reactor, BotAuth, UIN, PASS, icq=icqMode).connectTCP(*host)
reactor.run()
