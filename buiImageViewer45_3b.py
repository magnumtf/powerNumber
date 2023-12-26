import os
import wx
import scipy.stats as ss
import numpy as np
import pandas as pd
import time
import sys
from random import randrange as rr

HOME = 1
WORK = 0
HOME_BETWEEN = 3
WORK_BETWEEN = 2
COLUMN_INDEX_STARTING_VAL = 14

PICS_DIR = "D:/groovyScripts/wxPython/cards"
BG_IMAGES = ["bg.jpg", "bg2.jpg", "bga.jpg", "bg2a.jpg"]
CARD_IMAGES = [
"ac.jpg",
"2c.jpg",
"3c.jpg",
"4c.jpg",
"5c.jpg",
"6c.jpg",
"7c.jpg",
"8c.jpg",
"9c.jpg",
"tc.jpg",
"jc.jpg",
"qc.jpg",
"kc.jpg",
"ad.jpg",
"2d.jpg",
"3d.jpg",
"4d.jpg",
"5d.jpg",
"6d.jpg",
"7d.jpg",
"8d.jpg",
"9d.jpg",
"td.jpg",
"jd.jpg",
"qd.jpg",
"kd.jpg",
"ah.jpg",
"2h.jpg",
"3h.jpg",
"4h.jpg",
"5h.jpg",
"6h.jpg",
"7h.jpg",
"8h.jpg",
"9h.jpg",
"th.jpg",
"jh.jpg",
"qh.jpg",
"kh.jpg",
"as.jpg",
"2s.jpg",
"3s.jpg",
"4s.jpg",
"5s.jpg",
"6s.jpg",
"7s.jpg",
"8s.jpg",
"9s.jpg",
"ts.jpg",
"js.jpg",
"qs.jpg",
"ks.jpg"]
CARD_TEXT = [
"ac",
"2c",
"3c",
"4c",
"5c",
"6c",
"7c",
"8c",
"9c",
"tc",
"jc",
"qc",
"kc",
"ad",
"2d",
"3d",
"4d",
"5d",
"6d",
"7d",
"8d",
"9d",
"td",
"jd",
"qd",
"kd",
"ah",
"2h",
"3h",
"4h",
"5h",
"6h",
"7h",
"8h",
"9h",
"th",
"jh",
"qh",
"kh",
"as",
"2s",
"3s",
"4s",
"5s",
"6s",
"7s",
"8s",
"9s",
"ts",
"js",
"qs",
"ks"]
CARD_VALS = [
-1,
1,
1,
1,
1,
1,
0,
0,
0,
-1,
-1,
-1,
-1,
-1,
1,
1,
1,
1,
1,
0,
0,
0,
-1,
-1,
-1,
-1,
-1,
1,
1,
1,
1,
1,
0,
0,
0,
-1,
-1,
-1,
-1,
-1,
1,
1,
1,
1,
1,
0,
0,
0,
-1,
-1,
-1,
-1]
DELAY1 = 2416   # last one was 3020
                # 4 card started at 3772
                # 3 card monty was 2620. Moving it up for 4 card monty. 
                #   started at 12000, last one was 5120, then 4096, then 3280
NUM_IMAGES = 14
DEBUG = 0

# QK or KQ is still a problem
# practiceCard not working.
class Hand:
    def __init__(self, card1, card2=None):
        self.card1 = card1
        self.card2 = card2
        self.isSuited = False
        self.handStr = ""
        tempCard = Card()
        if card2:
        # figure out diagonal
        # if suited - aboveDiagonal
        # if not suited belowDiagonal
            print(f"Hand:: card1.rank = {card1.rank}, card1.rank2 = {card1.rank2}, card1.suit = {card1.suit}, card1.index = {card1.index}")            
            print(f"Hand:: card2.rank = {card2.rank}, card2.rank2 = {card2.rank2}, card2.suit = {card2.suit}, card2.index = {card2.index}")
            
            #if suited and belowDiagonal or if not suited and aboveDiagonal:
            if card2.suit == card1.suit:
                self.isSuited = True
                # if suited, use lower card for column, then test.
                if card2.rank2 < card1.rank2:
                    # switchCards
                    tempCard.copy(self.card1)
                    self.card1.copy(self.card2)
                    self.card2.copy(tempCard)
                    print(f"Hand:: SwitchCard1(): card1.rank = {card1.rank}, card2.rank = {card2.rank}, suit = {card1.suit}")
                    
                card1Card2AboveDiagonal = self.isCardAboveDiagonal(self.card1, self.card2)
                card2Card1AboveDiagonal = self.isCardAboveDiagonal(self.card2, self.card1)
                err = 0
                if card1Card2AboveDiagonal:
                    pass
                elif card2Card1AboveDiagonal:
                    # switchCards again
                    tempCard.copy(self.card1)
                    self.card1.copy(self.card2)
                    self.card2.copy(tempCard)
                    print(f"Hand:: SwitchCard2(): card1.rank = {card1.rank}, card2.rank = {card2.rank}, suit = {card1.suit}")
                else:
                    print(f"Hand:: Shouldn't be here. card1.rank = {card1.rank}, card2.rank = {card2.rank}, suit = {card1.suit}")
                    err = 1 
            else:
                # if suited, use lower card for column, then test.
                if card1.rank2 < card2.rank2:
                    # switchCards
                    tempCard.copy(self.card1)
                    self.card1.copy(self.card2)
                    self.card2.copy(tempCard)
                    print(f"Hand:: SwitchCard3(): card1.rank = {card1.rank}, card2.rank = {card2.rank}, suit = {card1.suit}")
                    
                card1Card2AboveDiagonal = self.isCardAboveDiagonal(self.card1, self.card2)
                card2Card1AboveDiagonal = self.isCardAboveDiagonal(self.card2, self.card1)
                err = 0
                if not card1Card2AboveDiagonal:
                    pass
                elif not card2Card1AboveDiagonal:
                    # switchCards again
                    tempCard.copy(self.card1)
                    self.card1.copy(self.card2)
                    self.card2.copy(tempCard)
                    print(f"Hand:: SwitchCard4(): card1.rank = {card1.rank}, card2.rank = {card2.rank}, suit = {card1.suit}")
                else:
                    print(f"Hand:: Shouldn't be here2. card1.rank = {card1.rank}, card2.rank = {card2.rank}, suit = {card1.suit}")
                    err = 1 

                
            self.handStr = self.card1.rank + self.card2.rank
            if self.isSuited:
                self.handStr += 's'
            print(f"Hand::(2) Hand = {self.handStr}, card1.rank = {card1.rank}, card1.suit = {card1.suit}, card1.index = {card1.index}")
            print(f"Hand::(2) card2.rank = {card2.rank}, card2.suit = {card2.suit}, card2.index = {card2.index}")

    def isCardAboveDiagonal(self, card1, card2):
        retVal = False
        if card2.index < card1.index:
            retVal = True
        return retVal
       
class Card:
    def __init__(self, name=""):
        self.name = name
        self.rank = ""
        self.rank2 = -1
        self.suit = ""
        self.index = -1
        if self.name:
            tup = self.getRankSuitIndex(self.name)
            self.rank = tup[0]
            self.rank2 = tup[1]
            self.suit = tup[2]
            self.index = tup[3]

    def copy(self, oCard):
        self.name = oCard.name
        self.rank = oCard.rank
        self.rank2 = oCard.rank2
        self.suit = oCard.suit
        self.index = oCard.index
        
    def getTableIndex(self, rankChar):
        retInd = -1
        err = 0
        rankInt = -1
        rankInt2 = -1
        try:
            rankInt = int(rankChar)
        except:
            err = 1
        
        if rankChar == 'A':
            retInd = 0
            rankInt2 = 14

        elif rankChar == 'K':
            retInd = 1
            rankInt2 = 13
        elif rankChar == 'Q':
            retInd = 2
            rankInt2 = 12
        elif rankChar == 'J':
            retInd = 3
            rankInt2 = 11
        elif rankChar == 'T':
            retInd = 4
            rankInt2 = 10
        elif rankInt >= 0:
            retInd = COLUMN_INDEX_STARTING_VAL - rankInt
            rankInt2 = rankInt
        
        if DEBUG:
            print(f"getTableIndex(): retInd = {retInd}, rankChar = {rankChar}, rank2 = {rankInt2}, rankInt = {rankInt}")
        return (retInd, rankInt2)
        
    def getRankSuitIndex(self, name):
        retRank = ""
        retRank2 = -1
        retSuit = ""
        retIndex = -1
        if name:
            retRank = name[0].upper()
            retSuit = name[1]
            retTup = self.getTableIndex(retRank)
            retIndex = retTup[0]
            retRank2 = retTup[1]
        if DEBUG:
            print(f"getRankSuitIndex(): retRank = {retRank}, retSuit = {retSuit}, retIndex = {retIndex}")
        return (retRank, retRank2, retSuit, retIndex)

class Deck:
    def __init__(self):
        self.startingDeck = range(52)
        self.usedCards = []
        
    def shuffle(self):
        self.usedCards = []
        
    def takeCards(self, numCards=1):
        i = 0
        retArr = []
        while i < numCards:
            cardIndex = self.getCardOffDeck()
            retArr.append(cardIndex)
            i += 1
        return retArr
                    
    def getCardOffDeck(self):
        i = 0
        retval = 0
        usedInd = -1
        rand = 0
        while i < 1000:
            err = 0
            usedInd = -1
            rand = rr(len(self.startingDeck))
            try:
                usedInd = self.usedCards.index(rand)
            except:
                err = 1
            if err:
                break
            i += 1
        if usedInd < 0:
            retval = rand
            self.usedCards.append(rand)
        return retval
            
class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None, delayFactor=1.0):
        wx.App.__init__(self, redirect, filename)
        self.delayFactor = delayFactor
        self.frame = wx.Frame(None, title='Photo Control')
 
        self.panel = wx.Panel(self.frame)
 
        self.imageCtrl1 = None
        self.imageCtrl2 = None
        self.imageCtrl3 = None
        self.imageCtrl4 = None
        self.imageCtrl5 = None
        self.imageCtrl6 = None
        self.imageCtrl7 = None
        self.imageCtrl8 = None
        self.imageCtrl9 = None
        self.imageCtrl10 = None
        self.imageCtrl11 = None
        self.imageCtrl12 = None
        self.imageCtrl13 = None
        self.imageCtrl14 = None

        self.instructLbl = None
        self.startingNumBins = self.getGaussianBins()
        self.cardIndexArr = []
        self.sessionLog = []
        self.deck = Deck()
        self.startingNum = 0
        self.numCards = 2
        self.numHands = 1
        self.answerVal = 0
        self.numTests = 1
        self.powerNumber = -1
        self.handArr = []
        self.location_ind = HOME
        self.location_ind2 = HOME_BETWEEN
        self.df = pd.read_csv('power_number_data.csv')
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.Image(134,230)
        img2 = wx.Image(134,230)
        img3 = wx.Image(100,230)
        img4 = wx.Image(134,230)
        img5 = wx.Image(134,230)
        img6 = wx.Image(100,230)
        img7 = wx.Image(134,230)
        img8 = wx.Image(134,230)
        img9 = wx.Image(100,230)
        img10 = wx.Image(134,230)
        img11 = wx.Image(134,230)
        img12 = wx.Image(100,230)
        img13 = wx.Image(134,230)
        img14 = wx.Image(134,230)

        self.imageCtrl1 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img))
        self.imageCtrl2 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img2))
        self.imageCtrl3 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img3))
        self.imageCtrl4 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img4))

        self.imageCtrl5 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img5))
        self.imageCtrl6 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img6))
        self.imageCtrl7 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img7))
        self.imageCtrl8 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img8))

        self.imageCtrl9 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img9))
        self.imageCtrl10 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img10))
        self.imageCtrl11 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img11))
        self.imageCtrl12 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img12))

        self.imageCtrl13 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img13))
        self.imageCtrl14 = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img14))

                                         
        self.photoTxt = wx.TextCtrl(self.panel, size=(120,-1))       
        font1 = wx.Font(24, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.photoTxt.SetFont(font1)

        self.numTestsTxt = wx.TextCtrl(self.panel, size=(50,-1))       
        
        browseBtn = wx.Button(self.panel, label='Browse')
        btn2 = wx.Button(self.panel, label='Bowser sux!')
        browseBtn.Bind(wx.EVT_BUTTON, self.runBatchByHand)
        btn2.Bind(wx.EVT_BUTTON, self.setNumTests)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(btn2, 0, wx.ALL, 5)        
        self.sizer.Add(self.numTestsTxt, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
#        self.sizer3.Add(browseBtn, 0, wx.ALIGN_RIGHT, 5)        
        self.sizer3.Add(browseBtn, 0, 5)        
#        self.sizer3.Add(self.photoTxt, 0, wx.ALIGN_RIGHT, 5)
        self.sizer3.Add(self.photoTxt, 0, 5)
#        self.mainSizer.Add(self.sizer3, 0, wx.ALIGN_RIGHT, 5)
        self.mainSizer.Add(self.sizer3, 0, 5)
        
        self.sizer2.Add(self.imageCtrl1, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl2, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl4, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl5, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl6, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl7, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl8, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl9, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl10, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl11, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl12, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl13, 0, wx.ALL, 5)
        self.sizer2.Add(self.imageCtrl14, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer2, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
        between = True
        self.setBitmap(self.imageCtrl1)
        self.setBitmap(self.imageCtrl2)
        self.setBitmap(self.imageCtrl3, between)        
        self.setBitmap(self.imageCtrl4)
        self.setBitmap(self.imageCtrl5)
        self.setBitmap(self.imageCtrl6, between)
        self.setBitmap(self.imageCtrl7)
        self.setBitmap(self.imageCtrl8)
        self.setBitmap(self.imageCtrl9, between)
        self.setBitmap(self.imageCtrl10)
        self.setBitmap(self.imageCtrl11)        
        self.setBitmap(self.imageCtrl12, between)
        self.setBitmap(self.imageCtrl13)
        self.setBitmap(self.imageCtrl14)

        self.numTestsTxt.SetValue(str(self.numTests))
        self.panel.Refresh()
 
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        self.photoTxt.SetValue(PICS_DIR)
        self.onView()
 
    def onView(self):
        between = False
        self.setBitmap(self.imageCtrl1, between, 0)
        between = True
        self.setBitmap(self.imageCtrl2, between)
        between = False
        self.setBitmap(self.imageCtrl3, between, 1)
        self.panel.Refresh()
    
    def reset(self):
        self.deck.shuffle()
        self.cardIndexArr = []
        self.answerVal = 0
        
    def runBatchByHand(self, event):
        num = 0
        sleepTime = DELAY1 / 1000.0
        if self.numTests > 20:
            event.Skip()
            for i in range(self.numTests):
                num = self.getStartingNum()
                #print(f"{i+1}: {num}")
                time.sleep(sleepTime)
        else:
            self.runBatchByHand_p(event)
            
    def runBatchByHand_p(self, event):
        i = 0
        delay2 = int(DELAY1 * self.delayFactor)
        futchCallDelay = int(delay2 / 4)
        self.sessionLog = []
        print(f"\n")
        while i < self.numTests:
            wx.CallLater(futchCallDelay, self.nextTest1_powerNumber)
            futchCallDelay += delay2
            i += 1
        futchCallDelay += int(delay2 / 4)
        wx.CallLater(futchCallDelay, self.printSessionLog)        
        event.Skip()
        
    def nextTest1(self):
        self.reset()
        self.grayAllCards()
        self.numCards = self.getNumCards()
        self.numHands = self.numCards / 2
        self.startingNum = self.getStartingNum()
        self.answerVal = self.startingNum
        self.flashStartingNum(self.startingNum)
        wx.CallLater(700, self.displayIt)
        
    def nextTest1_powerNumber(self):
        self.reset()
        self.grayAllCards()
        self.numCards = 2
        self.numHands = self.numCards / 2
#        self.flashBigOleTitties(self.numCards)
        self.startingNum = self.powerNumber
        self.flashStartingNum(self.startingNum)
        wx.CallLater(700, self.displayIt)

    def getTableIndex(self, rankChar):
        retColumnInd = -1
        err = 0
        startVal = 14
        rankInt = -1
        try:
            rankInt = int(rankChar)
        except:
            err = 1
        
        if rankChar == 'A':
            retColumnInd = 0
        elif rankChar == 'K':
            retColumnInd = 1
        elif rankChar == 'Q':
            retColumnInd = 2
        elif rankChar == 'J':
            retColumnInd = 3
        elif rankInt >= 0:
            retColumnInd = startVal - rankInt
        
    def getPowerNumber(self, cardIndex1, cardIndex2=-1):
        card1_cardName = CARD_TEXT[cardIndex1]        
        powerNumber = -1
        card1 = Card(card1_cardName)
        print(f"getPowerNumber(): card1.name = {card1_cardName}, card1.name2 = {card1.name}, card1.rank = {card1.rank}, card1.suit = {card1.suit}")
        handy = None
        card2 = None

        if cardIndex2 >= 0:
            card2_cardName = CARD_TEXT[cardIndex2]
            card2 = Card(card2_cardName)
            handy = Hand(card1, card2)
            print(f"getPowerNumber(): card2.name = {card2_cardName}, card2.name2 = {card2.name}, card2.rank = {card2.rank}, card2.suit = {card2.suit}")
            print(f"getPowerNumber(): handy.card1.rank = {handy.card1.rank}, handy.card2.index = {handy.card2.index}")
            if handy.card2.index >= 0:
                powerNumber = self.df[handy.card1.rank][handy.card2.index]
                print(f"getPowerNumber(): {handy.handStr}: powerNumber = {powerNumber}")
            else:
                powerNumberTemp = self.df['Q'][11]
                print(f"getPowerNumber(): {powerNumberTemp}")
                powerNumberTemp = self.df['3'][2]
                print(f"getPowerNumber():2 {powerNumberTemp}")

        return (handy, powerNumber)
        
    def doCardsContain(self, cardIndex1, cardIndex2, practiceCards):
        retVal = False
        card1_cardName = CARD_TEXT[cardIndex1]
        card2_cardName = CARD_TEXT[cardIndex2]
        for practiceCard in practiceCards:
            if card1_cardName[0] == practiceCard:
                retVal = True
                break
            elif card2_cardName[0] == practiceCard:
                retVal = True
                break
        return retVal

    def flashBigOleTitties(self, numCards, practiceCards=['a', 'k']):
        err = 0
        fullfilename_base = PICS_DIR + '/'
        self.cardIndexArr = self.deck.takeCards(numCards)

        k = 0
        while True:
            card1 = self.cardIndexArr[0]
            card2 = self.cardIndexArr[1]
            if self.doCardsContain(card1, card2, practiceCards) or k > 100:
                break
            self.cardIndexArr = self.deck.takeCards(numCards)
            k+= 1
                
        ctrl = None
        ctrl2 = None
        img = None
        i = 0
        handNum = 0
        if DEBUG:
            print(f"flashBigOleTitties(): numCards = {numCards}. Len cardIndexArr = {len(self.cardIndexArr)}")
        filename = BG_IMAGES[self.location_ind]
        fullfilename = fullfilename_base + filename
        img_bg = wx.Image(fullfilename, wx.BITMAP_TYPE_ANY)
        filename = ""
        self.powerNumber = -1
        self.handArr = []
        oldInd = -1
        for ind in self.cardIndexArr:
            ctrl = None
            ctrl2 = None
            img = None
            try:
                filename = CARD_IMAGES[ind]
            except:
                err = 1
            if err:
                filename = CARD_IMAGES[0]
            fullfilename = fullfilename_base + filename
            img = wx.Image(fullfilename, wx.BITMAP_TYPE_ANY)
            if i % 2:
                firstCard = False
                powerTup = self.getPowerNumber(oldInd, ind)
                self.handArr.append(powerTup[0])
                self.powerNumber = powerTup[1]
                handNum += 1
            else:
                firstCard = True
                handNum += 1

            ctrl_tup = self.getImageCtrl(handNum, firstCard)
            ctrl = ctrl_tup[0]
            ctrl2 = ctrl_tup[1]
            if ctrl and img:
                ctrl.SetBitmap(wx.Bitmap(img))
            else:
                print(f"flashBigOleTitties(): u should not be here")
            self.answerVal = self.powerNumber
            oldInd = ind
            i += 1
        self.panel.Refresh()
        

    def nextTest2(self, event):
        self.displayIt()
        event.Skip()

    def setNumTests(self, event):
        self.numTests = int(self.numTestsTxt.GetLineText(0))
        print(f"setNumTests(): {self.numTests}")
        event.Skip()
        
    def displayIt(self):
        self.flashStartingNum()
        numCards = self.numCards
        self.flashBigOleTitties(numCards)
        self.logTest2()

    def flashStartingNum(self, startingNum=-99):
        instructions = 'Browse for an image'
        instructions2 = ''
        if startingNum > -50:
#            self.instructLbl.SetLabel(str(startingNum))
            self.photoTxt.SetValue(str(startingNum))
        else:
#            self.instructLbl.SetLabel(instructions2)
            self.photoTxt.SetValue(instructions2)
        self.panel.Refresh()

    def getImageCtrl_base(self, imageNum):
        ctrl = None
        if imageNum == 1:
            ctrl = self.imageCtrl1
        elif imageNum == 2:
            ctrl = self.imageCtrl2
        elif imageNum == 3:
            ctrl = self.imageCtrl3
        elif imageNum == 4:
            ctrl = self.imageCtrl4
        elif imageNum == 5:
            ctrl = self.imageCtrl5
        elif imageNum == 6:
            ctrl = self.imageCtrl6
        elif imageNum == 7:
            ctrl = self.imageCtrl7
        elif imageNum == 8:
            ctrl = self.imageCtrl8
        elif imageNum == 9:
            ctrl = self.imageCtrl9
        elif imageNum == 10:
            ctrl = self.imageCtrl10
        elif imageNum == 11:
            ctrl = self.imageCtrl11
        elif imageNum == 12:
            ctrl = self.imageCtrl12
        elif imageNum == 13:
            ctrl = self.imageCtrl13
        elif imageNum == 14:
            ctrl = self.imageCtrl14
        return ctrl
        
    def getImageCtrl(self, handNum, firstCard):
        ind = NUM_IMAGES - (handNum * 2) + 1
        ind2 = -1
        ctrl2 = None
        skipNums = handNum - 1
        if skipNums < 0:
            skipNums = 0
        if not firstCard:
            ind -= 1
        imageNum = ind + 1 - skipNums
        if firstCard and handNum > 1:
            ind2 = imageNum
            ctrl2 = self.getImageCtrl_base(ind2+1)
        if ind2 > -1 and DEBUG:
            print(f"getImageCtrl(): handNum = {handNum}, firstCard = {firstCard}, imageNum = {imageNum}, skippedImageNum = {ind2+1}. skipNums = {skipNums}")
        elif DEBUG:
            print(f"getImageCtrl(): handNum = {handNum}, firstCard = {firstCard}, imageNum = {imageNum}, skipNums = {skipNums}")
        ctrl = self.getImageCtrl_base(imageNum)
        return (ctrl, ctrl2)
        
    def flashNextHand(self, numCards):
        err = 0
        fullfilename_base = PICS_DIR + '/'
        self.cardIndexArr = self.deck.takeCards(numCards)
        ctrl = None
        ctrl2 = None
        img = None
        i = 0
        handNum = 0
        if DEBUG:
            print(f"flashNextHand(): numCards = {numCards}. Len cardIndexArr = {len(self.cardIndexArr)}")
        filename = BG_IMAGES[self.location_ind]
        fullfilename = fullfilename_base + filename
        img_bg = wx.Image(fullfilename, wx.BITMAP_TYPE_ANY)
        filename = ""
        for ind in self.cardIndexArr:
            ctrl = None
            ctrl2 = None
            img = None
            try:
                filename = CARD_IMAGES[ind]
            except:
                err = 1
            if err:
                filename = CARD_IMAGES[0]
            fullfilename = fullfilename_base + filename
            img = wx.Image(fullfilename, wx.BITMAP_TYPE_ANY)
            if i % 2 == 0:
                firstCard = True
                handNum += 1
            else:
                firstCard = False
            ctrl_tup = self.getImageCtrl(handNum, firstCard)
            ctrl = ctrl_tup[0]
            ctrl2 = ctrl_tup[1]
            if ctrl and img:
                ctrl.SetBitmap(wx.Bitmap(img))
            else:
                print(f"flashNextHand(): u should not be here")
            self.answerVal += CARD_VALS[ind]
            i += 1
        self.panel.Refresh()
        
    def getNumCards(self):
        retval = 1
        rand = rr(100)
        if rand < 33:
            retval = 6
        elif rand < 66:
            retval = 8
        else:
            retval = 10
        return retval

    def logTest(self):
        str1 = str(self.startingNum)
        str1 += '\t'
        for ind in self.cardIndexArr:
            cardText = CARD_TEXT[ind]
            str1 += cardText
            str1 += ', '
        if len(self.cardIndexArr) > 1:
            str2 = str1[0:len(str1) - 2]
        else:
            str2 = str1
        str2 += '\n'
        self.sessionLog.append(str2)

    def logTest2(self):
        for ha in self.handArr:
            str2 = ha.handStr
            str1 = str(self.answerVal)
            self.sessionLog.append(str2 + ', ' + str1)

    def printSessionLog(self):
        for lo in self.sessionLog:
            print(f"{lo}")
        
    def grayAllCards(self, updateDisplay=False):
        between = True
        self.setBitmap(self.imageCtrl1)
        self.setBitmap(self.imageCtrl2)
        self.setBitmap(self.imageCtrl3, between)
        self.setBitmap(self.imageCtrl4)
        self.setBitmap(self.imageCtrl5)
        self.setBitmap(self.imageCtrl6, between)
        self.setBitmap(self.imageCtrl7)
        self.setBitmap(self.imageCtrl8)
        self.setBitmap(self.imageCtrl9, between)
        self.setBitmap(self.imageCtrl10)
        self.setBitmap(self.imageCtrl11)
        self.setBitmap(self.imageCtrl12, between)
        self.setBitmap(self.imageCtrl13)
        self.setBitmap(self.imageCtrl14)
        if updateDisplay:
            self.panel.Refresh()        

    def getGaussianBins(self, endPoint=20, std=6.0):
        leftEnd = -endPoint
        rightEnd = endPoint + 1
        x = np.arange(leftEnd, rightEnd)
        xU, xL = x + 0.5, x - 0.5
        prob = ss.norm.cdf(xU, scale = std) - ss.norm.cdf(xL, scale = std)
        prob = prob / prob.sum()
        retNumArr = np.random.choice(x, size = 20000, p = prob)
        return retNumArr
        
    def getStartingNum(self):
        rand = rr(len(self.startingNumBins))
        retval = self.startingNumBins[rand]
        return retval
        
    def setBitmap(self, ctrl, between=False, imageIndex=-1):
        err = 0
        filename = ""
        fullfilename = PICS_DIR + '/'
        if imageIndex < 0 and between:
            try:
                filename = BG_IMAGES[self.location_ind2]
            except:
                err = 2
        elif imageIndex < 0:
            try:
                filename = BG_IMAGES[self.location_ind]
            except:
                err = 3
        else:
            try:
                filename = CARD_IMAGES[imageIndex]
            except:
                err = 1
        if not err:
            fullfilename += filename
            img = wx.Image(fullfilename, wx.BITMAP_TYPE_ANY) 
            ctrl.SetBitmap(wx.Bitmap(img))
 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        df = float(sys.argv[1])
    else:
        df = 1.0
    app = PhotoCtrl(False, None, df)
    app.MainLoop()