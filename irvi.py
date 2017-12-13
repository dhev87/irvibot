# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()


wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + "\nThanks for ADD\nSalam Kenal, Kak")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + "\n\nWELLCOME KAKAK\nSELAMAT BERGABUNG disini yaaa\nSALKOMSEL" )
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + "\nInalilahi\nKenapa Out yakk???")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_INVITE_INTO_GROUP(op):
	#id dhev
    Amid = "u32b63e6b0d4b514632c574746843a0dc"
    if op.param2 in Amid:
        client.acceptGroupInvitation(op.param1)
    else:
		pass

tracer.addOpInterrupt(13,NOTIFIED_INVITE_INTO_GROUP)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param3).displayName + " kenapa Di kick ???\nKakak di tikung kah???,hahahaha")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return
	
	#id dhev
    Amid = "u32b63e6b0d4b514632c574746843a0dc"
    if Amid in op.param3:
                client.inviteIntoGroup(op.param1,[op.param3])
                sendMessage(op.param1, "BUZZEETTTT dahh loe " +client.getContact(op.param2).displayName + "\nLaki Ane Kok di Kick!!!")
                client.kickoutFromGroup(op.param1,[op.param2])
    else:
		pass

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        if msg.toType == 2:
            if "mvi" in msg.text:
                sendMessage(msg.to, "miss beauty lg sibuk kerja\n,mlm mojok,jangan ganggu dulu ya\nntar nongol sendiri")
            if "smule" in msg.text:
                sendMessage(msg.to,"Follow aq yaaak!!!!\n\n@GVIC_GSmviA1HAFN")
            if "Smule" in msg.text:
                sendMessage(msg.to,"Follow aq donkkk!!!!\n\n@GVIC_GSmviA1HAFN")
            if "smulle" in msg.text:
                sendMessage(msg.to,"Follow aq ya kak!!!!\n\n@GVIC_GSmviA1HAFN")
            if "Smulle" in msg.text:
                sendMessage(msg.to,"Follow aq donk kak!!!!\n\n@GVIC_GSmviA1HAFN")
        else:
            pass
    except:
        pass
			
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)


def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
			
        if msg.toType == 2:
            if msg.text in ["tag all","Tagall","tagall"]:
                  group = client.getGroup(msg.to)
                  nama = [contact.mid for contact in group.members]

                  cb = ""
                  cb2 = ""
                  strt = int(0)
                  akh = int(0)
                  for md in nama:
                      akh = akh + int(6)

                      cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""

                      strt = strt + int(7)
                      akh = akh + 1
                      cb2 += "@nrik \n"

                  cb = (cb[:int(len(cb)-1)])
                  msg.contentType = 0
                  msg.text = cb2
                  msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}

                  try:
                      client.sendMessage(msg)
                  except Exception as error:
                      print error
            if msg.text in ["speedbot","speed"]:
				start = time.time()
				sendMessage(msg.to, "please wait....")
				elapsed_time = time.time() - start
				sendMessage(msg.to, "%ss" % (elapsed_time))
            elif "#spam" in msg.text:
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				sendMessage(msg.to, "UP")
				
            elif "bye @" in msg.text:
                if msg.toType == 2:
                    _name = msg.text.replace("bye @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                            for target in targets:
						        client.kickoutFromGroup(msg.to,[target])
            elif "get @" in msg.text:
                if msg.toType == 2:
                    print "[Get]"
                    _name = msg.text.replace("get @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                            client.findAndAddContactsByMid(g.mid)
                            for target in targets:
                                M = Message()
                                M.to = msg.to
                                M.contentType = 13
                                M.contentMetadata = {'mid': g.mid}
                                client.sendMessage(M)
	
            if msg.contentType == 0:
                if msg.text == "help":
                    sendMessage(msg.to,text="**USER**\nmid\ngift\n\n**GROUP**\ntag all / Tagall / tagall\non\noff\ngift\ntime\nme\nget @\nbye @\nmvi cancel\nurl\nqr open\nqr close\nmid\ngid\nginfo\nspeedbot / speed")
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[ GROUP NAME ]\n" + group.name + "\n\n[ GROUP ID ]\n" + group.id + "\n\n[ Cover Group ]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL : Refusing\n"
                    if group.invitee is None: md += "\nMembers : " + str(len(group.members)) + "人\n\nInviting : 0 People"
                    else: md += "\nMembers : " + str(len(group.members)) + "People\nInvited : " + str(len(group.invitee)) + " People"
                    sendMessage(msg.to,md)
                if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "qr open":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "Already Open")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Open")
                if msg.text == "qr close":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "Already Close")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Close")

                if msg.text == "mvi cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "inviting Empty")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Done")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if msg.text == "time":
                    sendMessage(msg.to, "Waktu sekarang :\n" + datetime.datetime.today().strftime('%d-%m-%Y || %H:%M:%S'))
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "on":
                    sendMessage(msg.to, "Ga ada yg on kah?")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "off":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "----T E R C I D U K---- %s\n\n\n--T E R S A N G K A--\n%s\n\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "on kan dulu Bosssss")
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
