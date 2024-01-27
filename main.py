from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.core.audio import SoundLoader
import speech_recognition as spreg
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
import os
import time
import playsound
from gtts import gTTS
from kivy.clock import Clock
from threading import Thread
from kivy.uix.floatlayout import FloatLayout
import mmap
from kivy.uix.gridlayout import GridLayout
import pygame
from io import BytesIO
from kivy.uix.button import Button

Window.fullscreen = 'auto'





class LoginScreen(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.user.text, self.password.text):
            MainWindow.current = self.user.text
            HelloScreen.current = self.user.text
            WaitTwoScreen.current = self.user.text
            StartScanScreen.current = self.user.text
            WaitScreen.current = self.user.text
            StartWorkScreen.current = self.user.text
            NeedHelpOneScreen.current = self.user.text
            ErrorOneScreen.current = self.user.text
            AskOneScreen.current = self.user.text
            ReadyOneScreen.current = self.user.text
            ErrorTwoScreen.current = self.user.text
            AskTwoScreen.current = self.user.text
            ReadyTwoScreen.current = self.user.text
            ErrorThreeScreen.current = self.user.text
            AskThreeScreen.current = self.user.text
            ReadyThreeScreen.current = self.user.text
            CheckScreen.current = self.user.text
            ByeScreen.current = self.user.text
            ExpertOneScreen.current = self.user.text
            ExpertTwoScreen.current = self.user.text
            ExpertThreeScreen.current = self.user.text
            AskExpertOneScreen.current = self.user.text
            AskExpertTwoScreen.current = self.user.text
            AskExpertThreeScreen.current = self.user.text
            LoadOneScreen.current = self.user.text
            LoadTwoScreen.current = self.user.text
            self.reset()
            sm.current = "hello"
            #manager.transition.direction ="left"
        else:
            invalidLogin()


    def reset(self):
        self.user.text = ""
        self.password.text = ""

    def end(self, *args):
        os._exit(0)

def hello_popup():
    layout=GridLayout(rows=6,padding=10)
    button1=Label(text='Abmelden')
    layout.add_widget((button1))
    button2 = Label(text='Überspringen')
    layout.add_widget((button2))
    button4 = Label(text='Schritt zurück')
    layout.add_widget((button4))
    button5= Label(text='Scan starten')
    layout.add_widget((button5))
    button6 = Label(text='Scan nicht starten')
    layout.add_widget((button6))
    button7 = Button(text='Fenster schließen')
    layout.add_widget((button7))

    popupWindow = Popup(title='Key Words',content=layout,size_hint=(None,None),auto_dismiss=True,size=(Window.width/2.5, Window.width/3))
    popupWindow.open()
    button7.bind(on_release=popupWindow.dismiss)
    return popupWindow



class HelloScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    current = ""

    # Individuelle Anzeige der jeweiligen Fenster.
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()


    def action(self):
        talk_text=" Hallo" + self.current +"Herzlich Willkommen zur Qualitätssicherung. Es freut mich heute mit Ihnen zusammen zu arbeiten. " \
                                           "Bitte stellen Sie das Produkt in den Scanner. Und geben Sie mir Bescheid sobald ich den Scan starten kann."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)


        pos_list = ['starten','starte']
        neg_list = ['nicht','nein','nicht starten','nicht starte']
        listen = True
        res = speech_reco(listen, pos_list, neg_list,self)
        if res == 0:

            popupWindow = hello_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "wait"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                time.sleep(2)
                self.on_enter()
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "wait"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "wait"
        elif res == 2:
            sm.current = "login"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            time.sleep(2)
            self.on_enter()
        elif res == 5:
            sm.current = "wait"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "login"
    def skipBtn(self):
        sm.current = "wait"
    def helpBtn(self):
        hello_popup()


def wait_popup():
    layout=GridLayout(rows=4,padding=10)
    button1=Label(text='Abmelden')
    layout.add_widget((button1))
    button2 = Label(text='Überspringen')
    layout.add_widget((button2))
    button4 = Label(text='Schritt zurück')
    layout.add_widget((button4))
    button5 = Button(text='Fenster schließen')
    layout.add_widget((button5))

    popupWindow = Popup(title='Key Words',content=layout,size_hint=(None,None),auto_dismiss=True,size=(Window.width/2.5, Window.width/3))
    popupWindow.open()
    button5.bind(on_release=popupWindow.dismiss)
    return popupWindow

class WaitScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Gut, dann starte ich jetzt den Scan. Bitte haben Sie einen Augenblick Geduld."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)
        sm.current = "load_one"


    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "hello"
    def skipBtn(self):
        sm.current ="load_one"
    def helpBtn(self):
        wait_popup()





class WaitTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Bitte warten Sie einen Moment während ich den Bagger scanne."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)
        sm.current = "load_two"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "ready_3"
    def skipBtn(self):
        sm.current = "load_two"
    def helpBtn(self):
        wait_popup()

class LoadOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    prozent = ObjectProperty(None)
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bar.value = 0
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        laden = True
        while laden == True:
            if self.bar.value < 1:
                time.sleep(0.1)
                self.bar.value += 0.02
                perc = round(self.bar.value*100)
                self.prozent.text = str(perc)+"%"
            elif self.bar.value >= 1:
                laden = False
                time.sleep(0.5)
                sm.current = "start_work"


class LoadTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bar.value = 0
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        laden = True
        while laden == True:
            if self.bar.value < 1:
                time.sleep(0.1)
                self.bar.value += 0.02
                perc = round(self.bar.value*100)
                self.prozent.text = str(perc)+"%"
            elif self.bar.value >= 1:
                laden = False
                time.sleep(0.5)
                sm.current = "check"

class StartScanScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Kann ich jetzt den Scan starten?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['starten','starte']
        neg_list = ['nicht','nein','nicht starten','nicht starte']
        listen = True
        res = speech_reco(listen, pos_list, neg_list,self)
        if res == 0:
            popupWindow=hello_popup()
            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "wait"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "hello"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                time.sleep(2)
                self.on_enter()
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "wait"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "wait"
        elif res == 2:
            sm.current = "hello"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            time.sleep(2)
            self.on_enter()
        elif res == 5:
            sm.current = "wait"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "hello"
    def skipBtn(self):
        sm.current = "wait"
    def helpBtn(self):

        hello_popup()

def startwork_popup():
    layout=GridLayout(rows=6,padding=10)
    button1=Label(text='Abmelden')
    layout.add_widget((button1))
    button2 = Label(text='Überspringen')
    layout.add_widget((button2))
    button4 = Label(text='Schritt zurück')
    layout.add_widget((button4))
    button5= Label(text='Ja')
    layout.add_widget((button5))
    button6 = Label(text='Nein')
    layout.add_widget((button6))
    button7 = Button(text='Fenster schließen')
    layout.add_widget((button7))

    popupWindow = Popup(title='Key Words',content=layout,size_hint=(None,None),auto_dismiss=True,size=(Window.width/2.5, Window.width/3))
    popupWindow.open()
    button7.bind(on_release=popupWindow.dismiss)
    return popupWindow


class StartWorkScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current

        self.bagger.source = "fehler.jpg"
        self.check_1.active = False
        self.check_2.active = False
        self.check_3.active = False
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Ich habe den Scan abgeschlossen. Bitte entnehmen Sie den Bagger aus dem Scanner, um die Fehler zu beheben. " \
                  "Ich konnte die folgenden Fehler fest stellen. Wollen Sie mit dem Beheben des ersten Fehlers beginnen?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)


        pos_list = ['ja','Ja','beheben']
        neg_list = ['nein','Nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = startwork_popup()

                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "need_help_1"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "wait"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "need_help_1"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "need_help_1"
            elif res == 2:
                sm.current = "wait"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "need_help_1"
        elif modus == "Experte":
            if res == 0:
                popupWindow = startwork_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "experte_1"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "wait"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "experte_1"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "experte_1"
            elif res == 2:
                sm.current = "wait"
            elif res == 3:
                sm.current = "login"
            elif res == 4:

                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "experte_1"


    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "wait"
    def skipBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "need_help_1"
        elif modus == "Experte":
            sm.current = "experte_1"
    def helpBtn(self):
        startwork_popup()


class NeedHelpOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_1_1.gif"
        self.bagger._coreimage.anim_reset(True)
        self.bagger.anim_delay= 0.1
        self.bagger.anim_loop = 1
        self.check_1.active = False
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_1.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Brauchen Sie Hilfe bei der Fehlerbehebung des ersten Fehlers"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['ja','Ja']
        neg_list = ['nein','Nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = startwork_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "error_1"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "start_work"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                sm.current = "experte_1"
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "error_1"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "error_1"
        elif res == 2:
            sm.current = "start_work"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            sm.current = "experte_1"
        elif res == 5:
            sm.current = "error_1"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "start_work"
    def skipBtn(self):
        sm.current = "error_1"
    def helpBtn(self):
        startwork_popup()

def error_popup():
    layout=GridLayout(rows=7,padding=10)
    button1=Label(text='Abmelden')
    layout.add_widget((button1))
    button2 = Label(text='Überspringen')
    layout.add_widget((button2))
    button4 = Label(text='Schritt zurück')
    layout.add_widget((button4))
    button5= Label(text='Fehler behoben')
    layout.add_widget((button5))
    button6 = Label(text='Fehler nicht behoben')
    layout.add_widget((button6))
    button3 = Label(text='Anweisung erneut abspielen')
    layout.add_widget((button3))
    button7 = Button(text='Fenster schließen')
    layout.add_widget((button7))

    popupWindow = Popup(title='Key Words',content=layout,size_hint=(None,None),auto_dismiss=True,size=(Window.width/2.5, Window.width/3))
    popupWindow.open()
    button7.bind(on_release=popupWindow.dismiss)
    return popupWindow

def error_exp_popup():
    layout=GridLayout(rows=7,padding=10)
    button1=Label(text='Abmelden')
    layout.add_widget((button1))
    button2 = Label(text='Überspringen')
    layout.add_widget((button2))
    button4 = Label(text='Schritt zurück')
    layout.add_widget((button4))
    button5= Label(text='Fehler behoben')
    layout.add_widget((button5))
    button6 = Label(text='Fehler nicht behoben')
    layout.add_widget((button6))
    button3 = Label(text='Hilfestellung')
    layout.add_widget((button3))
    button7 = Button(text='Fenster schließen')
    layout.add_widget((button7))

    popupWindow = Popup(title='Key Words',content=layout,size_hint=(None,None),auto_dismiss=True,size=(Window.width/2.5, Window.width/3))
    popupWindow.open()
    button7.bind(on_release=popupWindow.dismiss)
    return popupWindow


class ErrorOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_1.gif"
        self.bagger.anim_delay= 2
        self.check_1.active = False
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_1.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Bitte setzen Sie zunächst die Batteriekassette in der gezeigten Richtung in das Gehäuse und halten Sie diese. " \
                    "Setzen Sie dann zuerst die hintere Seite der Abdeckung ein und drücken sie danach die vordere Seite auf das Gehäuse bis es klickt." \
                    "       Geben Sie mir anschließend Bescheid"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','Behoben','Fertig','fertig']
        neg_list = ['nicht', 'nicht behoben','Anweisung erneut abspielen','abspielen','erneut','nicht fertig']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = error_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "ask_1"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "need_help_1"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_1"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ask_1"
            elif res == 2:
                sm.current = "need_help_1"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "ready_1"
        elif modus == "Experte":
            if res == 0:
                popupWindow = error_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "experte_2"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ask_expert_1"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "experte_2"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "experte_2"
            elif res == 2:
                sm.current = "ask_expert_1"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "experte_2"



    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "need_help_1"
    def skipBtn(self):
        sm.current = "ask_1"
    def helpBtn(self):
        error_popup()

class AskOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)

    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_1.gif"
        self.bagger.anim_delay= 2
        self.check_1.active = False
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_1.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Haben Sie den ersten Fehler behoben?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','Behoben','ja','Ja']
        neg_list = ['nicht', 'nicht behoben','Anweisung erneut abspielen','abspielen','erneut','nein','Nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = error_popup()
            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "ready_1"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "error_1"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                time.sleep(2)
                self.on_enter()
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "ready_1"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "ready_1"
        elif res == 2:
            sm.current = "error_1"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            time.sleep(2)
            self.on_enter()
        elif res == 5:
            sm.current = "ready_1"
    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "error_1"
    def skipBtn(self):
        sm.current = "ready_1"
    def helpBtn(self):
        error_popup()

class ReadyOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)

    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_2_1.gif"
        self.bagger._coreimage.anim_reset(True)
        self.bagger.anim_delay= 0.1
        self.bagger.anim_loop = 1
        self.check_1.active = True
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_2.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Der erste Fehler wurde erfolgreich behoben. Benötigen Sie Hilfe zur Behebung des zweiten Fehlers?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['ja','Ja']
        neg_list = ['nein','Nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = startwork_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "error_2"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "error_1"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                sm.current = "experte_2"
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "error_2"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "error_2"
        elif res == 2:
            sm.current = "error_1"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            sm.current = "experte_2"
        elif res == 5:
            sm.current = "error_2"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "error_1"
    def skipBtn(self):
        sm.current = "error_2"
    def helpBtn(self):
        startwork_popup()




class ErrorTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_2.gif"
        self.bagger.anim_delay= 3
        self.check_1.active = True
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_2.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Bitte öffnen Sie die Klappe auf dem hinteren Aufbau des Baggers." \
                    "Stecken Sie das lose Kabel wie gezeigt in den Steckplatz C der Batterie." \
                    "    Geben Sie mir anschließend Bescheid"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','Behoben','Fertig','fertig']
        neg_list = ['nicht', 'nicht behoben','Anweisung erneut abspielen','abspielen','erneut','nicht fertig']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = error_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "ask_2"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ready_1"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_2"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ask_2"
            elif res == 2:
                sm.current = "ready_1"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "ready_2"
        elif modus == "Experte":
            if res == 0:
                popupWindow = error_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "experte_3"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ask_expert_2"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "experte_3"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "experte_3"
            elif res == 2:
                sm.current = "ask_expert_2"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "experte_3"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "ready_1"
    def skipBtn(self):
        sm.current = "ask_2"
    def helpBtn(self):
        error_popup()

class AskTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_2.gif"
        self.bagger.anim_delay= 2
        self.check_1.active = True
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_2.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Haben Sie den zweiten Fehler behoben?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','Behoben','ja','Ja']
        neg_list = ['nicht', 'nicht behoben','Anweisung erneut abspielen','abspielen','erneut','nein','Nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = error_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "ready_2"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "error_2"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                time.sleep(2)
                self.on_enter()
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "ready_2"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "ready_2"
        elif res == 2:
            sm.current = "error_2"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            time.sleep(2)
            self.on_enter()
        elif res == 5:
            sm.current = "ready_2"
    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "error_2"
    def skipBtn(self):
        sm.current = "ready_2"
    def helpBtn(self):
        error_popup()

class ReadyTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_3_1.gif"
        self.bagger._coreimage.anim_reset(True)
        self.bagger.anim_delay= 0.2
        self.bagger.anim_loop = 1
        self.check_1.active = True
        self.check_2.active = True
        self.check_3.active = False
        self.fehler_3.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Brauchen Sie Hilfe, um den dritten Fehler zu beheben?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['ja','Ja']
        neg_list = ['nein','Nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = startwork_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "error_3"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "error_2"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                sm.current = "experte_3"
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "error_3"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "error_3"
        elif res == 2:
            sm.current = "error_2"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            sm.current = "experte_3"
        elif res == 5:
            sm.current = "error_3"

    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "error_2"
    def skipBtn(self):
        sm.current = "error_3"
    def helpBtn(self):
        startwork_popup()


class ErrorThreeScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_3.gif"
        self.bagger.anim_delay= 3
        self.check_1.active = True
        self.check_2.active = True
        self.check_3.active = False
        self.fehler_3.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Bitte nehmen Sie die gelösten Enden der Ketten und verbinden Sie diese wie gezeigt." \
                    "   Geben Sie mir anschließend Bescheid"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','Behoben','fertig', 'Fertig']
        neg_list = ['nicht', 'nicht behoben','Anweisung erneut abspielen','abspielen','erneut','nicht fertig']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = error_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "ask_3"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ready_2"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_3"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ask_3"
            elif res == 2:
                sm.current = "ready_2"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "ready_3"
        elif modus == "Experte":
            if res == 0:
                popupWindow = error_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "ready_3"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ask_expert_3"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_3"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ready_3"
            elif res == 2:
                sm.current = "ask_expert_3"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "ready_3"


    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "ready_2"
    def skipBtn(self):
        sm.current = "ask_3"
    def helpBtn(self):
        error_popup()

class AskThreeScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_3.gif"
        self.bagger.anim_delay= 2
        self.check_1.active = True
        self.check_2.active = True
        self.check_3.active = False
        self.fehler_3.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text = "Haben Sie den dritten Fehler behoben?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','Behoben','Ja','ja']
        neg_list = ['nicht', 'nicht behoben','Anweisung erneut abspielen','abspielen','erneut','Nein', 'nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = error_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "ready_3"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "error_3"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                time.sleep(2)
                self.on_enter()
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "ready_3"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "ready_3"
        elif res == 2:
            sm.current = "error_3"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            time.sleep(2)
            self.on_enter()
        elif res == 5:
            sm.current = "ready_3"
    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "error_3"
    def skipBtn(self):
        sm.current = "ready_3"
    def helpBtn(self):
        error_popup()

class ReadyThreeScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_3_check.jpg"
        self.check_1.active = True
        self.check_2.active = True
        self.check_3.active = True
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()


    def action(self):
        talk_text="Es wurden alle Fehler erfolgreich behoben. Bitte stellen Sie den Bagger nochmals in den Scanner und geben Sie mir Bescheid sobald ich einen abschließenden Scan starten kann."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['Starte','Starten','starten','starte']
        neg_list = ['nicht','nicht starten','nicht starte']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = hello_popup()

                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "wait_two"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "error_3"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "wait_two"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "wait_two"
            elif res == 2:
                sm.current = "error_3"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()
            elif res == 5:
                sm.current = "wait_two"
        elif modus == "Experte":
            if res == 0:
                popupWindow = hello_popup()

                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)

                if res == 1:
                    sm.current = "wait_two"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "experte_3"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    self.on_enter()
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "wait_two"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "wait_two"
            elif res == 2:
                sm.current = "experte_3"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                time.sleep(2)
                self.on_enter()

            elif res == 5:
                sm.current = "wait_two"

    #Definition der Funktion der Button
    def backBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "error_3"

        elif modus == "expert":
            sm.current = "expert_3"

    def skipBtn(self):
        sm.current = "wait_two"
    def helpBtn(self):
        hello_popup()

def check_popup():
    layout=GridLayout(rows=6,padding=10)
    button1=Label(text='Überspringen')
    layout.add_widget((button1))
    button2 = Label(text='Abmelden')
    layout.add_widget((button2))
    button4 = Label(text='Schritt zurück')
    layout.add_widget((button4))
    button5= Label(text='Produkt funktioniert')
    layout.add_widget((button5))
    button6 = Label(text='Produkt funktioniert nicht')
    layout.add_widget((button6))
    button7 = Button(text='Fenster schließen')
    layout.add_widget((button7))

    popupWindow = Popup(title='Key Words',content=layout,size_hint=(None,None),auto_dismiss=True,size=(Window.width/2.5, Window.width/3))
    popupWindow.open()
    button7.bind(on_release=popupWindow.dismiss)
    return popupWindow


class CheckScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Der Scan ist abgeschlossen. Es wurden alle Fehler erfolgreich behoben." \
                  "Bitte entnehmen Sie den Bagger und überprüfen Sie das Produkt auf die Funktionsfähigkeit mittels der Steuerungs-App"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['funktioniert','Funktioniert','ja']
        neg_list = ['fuktioniert nicht','nicht']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = check_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "bye"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "wait_two"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                time.sleep(2)
                self.on_enter()
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "bye"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "bye"
        elif res == 2:
            sm.current = "wait_two"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            time.sleep(2)
            self.on_enter()
        elif res == 5:
            sm.current = "bye"


    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "wait_two"
    def skipBtn(self):
        sm.current = "bye"
    def helpBtn(self):
        check_popup()


class ByeScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Vielen Dank. Die Qualitätssicherung ist abgeschlossen. Ich habe die Informationen gespeichert. Bitte vergessen Sie nicht sich abzumelden.Bis zum nächsten mal." +self.current
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = []
        neg_list = []
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = wait_popup()

            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "check"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "login"
        elif res == 2:
            sm.current = "check"
        elif res == 3:
            sm.current = "login"
    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "check"
    def skipBtn(self):
        sm.current = "login"
    def helpBtn(self):
        wait_popup()

class ExpertOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_1_mark.png"
        self.check_1.active = False
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_1.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Als erstes müssen sie die Batterie korrekt einsetzen. Sagen Sie mir Bescheid wenn Sie den Fehler behoben haben."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','fertig','Fertig']
        neg_list = ['nicht behoben', 'nicht','hilfestellung','Hilfe','Hilfestellung','hilfe','nicht fertig']

        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = error_exp_popup()

                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)

                if res == 1:
                    sm.current = "ready_1"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "need_help_1"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    sm.current = "ask_expert_1"
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_1"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ready_1"
            elif res == 2:
                sm.current = "need_help_1"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                sm.current = "ask_expert_1"
            elif res == 5:
                sm.current = "ready_1"
        elif modus == "Experte":
            if res == 0:
                popupWindow = error_exp_popup()

                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)

                if res == 1:
                    sm.current = "experte_2"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "start_work"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    sm.current = "ask_expert_1"
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "experte_2"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "experte_2"
            elif res == 2:
                sm.current = "start_work"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                sm.current = "ask_expert_1"
            elif res == 5:
                sm.current = "experte_2"


    #Definition der Funktion der Button
    def backBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "need_help_1"
        elif modus == "Experte":
            sm.current = "start_work"
    def skipBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "ready_1"
        elif modus == "Experte":
            sm.current = "experte_2"
    def helpBtn(self):
        error_exp_popup()

class ExpertTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_2_mark.jpg"
        self.check_1.active = True
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_2.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()
    def action(self):

        talk_text="Befestigen Sie bitte als nächstes das Kabel C der Batterie. Sagen Sie mir Bescheid wenn Sie den Fehler behoben haben."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)


        pos_list = ['behoben','fertig','Fertig']
        neg_list = ['nicht behoben', 'nicht','hilfestellung','Hilfe','Hilfestellung','hilfe','nicht fertig']
        listen = True

        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = error_exp_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "ready_2"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ready_1"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    time.sleep(2)
                    sm.current = "ask_expert_2"
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_2"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ready_2"
            elif res == 2:
                sm.current = "ready_1"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                sm.current = "ask_expert_2"
            elif res == 5:
                sm.current = "ready_2"
        elif modus == "Experte":
            if res == 0:
                popupWindow = error_exp_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)
                if res == 1:
                    sm.current = "experte_3"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "experte_1"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    sm.current = "ask_expert_2"
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "experte_3"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "experte_3"
            elif res == 2:
                sm.current = "experte_1"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                sm.current = "ask_expert_2"
            elif res == 5:
                sm.current = "experte_3"



    #Definition der Funktion der Button
    def backBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "ready_1"
        elif modus == "Experte":
            sm.current = "experte_1"
    def skipBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "ready_2"
        elif modus == "Experte":
            sm.current = "experte_3"
    def helpBtn(self):
        error_exp_popup()

class ExpertThreeScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    check_1 =  ObjectProperty(None)
    check_2 =  ObjectProperty(None)
    check_3 =  ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_3_mark.jpg"
        self.check_1.active = True
        self.check_2.active = True
        self.check_3.active = False
        self.fehler_3.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):

        talk_text="Als letztes müssen Sie den Defekt am Kettenlaufwerk beheben. Sagen Sie mir Bescheid wenn Sie den Fehler behoben haben."
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['behoben','fertig','Fertig']
        neg_list = ['nicht behoben', 'nicht','hilfestellung','Hilfe','Hilfestellung','hilfe','nicht fertig']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            if res == 0:
                popupWindow = error_exp_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)

                if res == 1:
                    sm.current = "ready_3"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "ready_2"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    sm.current = "ask_expert_3"
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_3"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ready_3"
            elif res == 2:
                sm.current = "ready_2"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                sm.current = "ask_expert_3"
            elif res == 5:
                sm.current = "ready_3"
        elif modus == "Experte":
            if res == 0:
                popupWindow = error_exp_popup()
                listen = True
                res = speech_reco(listen, pos_list, neg_list,self)

                if res == 1:
                    sm.current = "ready_3"
                    popupWindow.dismiss()
                elif res == 2:
                    sm.current = "experte_2"
                    popupWindow.dismiss()
                elif res == 3:
                    sm.current = "login"
                    popupWindow.dismiss()
                elif res == 4:
                    sm.current = "ask_expert_3"
                    popupWindow.dismiss()
                elif res == 5:
                    sm.current = "ready_3"
                    popupWindow.dismiss()

            elif res ==1:
                sm.current = "ready_3"
            elif res == 2:
                sm.current = "experte_2"
            elif res == 3:
                sm.current = "login"
            elif res == 4:
                sm.current = "ask_expert_3"
            elif res == 5:
                sm.current = "ready_3"


    #Definition der Funktion der Button
    def backBtn(self):
        password, modus = db.get_user(self.current)
        if modus == "Beginner":
            sm.current = "ready_2"
        elif modus == "Experte":
            sm.current = "experte_2"
    def skipBtn(self):
        sm.current = "ready_3"
    def helpBtn(self):
        error_exp_popup()

class AskExpertOneScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_1_mark.png"
        self.check_1.active = False
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_1.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Brauchen Sie Unterstützung bei der Fehlerbehebung?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)

        pos_list = ['ja']
        neg_list = ['nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = startwork_popup()
            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "error_1"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "experte_1"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                sm.current = "experte_1"
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "error_1"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "error_1"
        elif res == 2:
            sm.current = "experte_1"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            sm.current = "experte_1"
        elif res == 5:
            sm.current = "error_1"


    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "experte_1"
    def skipBtn(self):
        sm.current = "error_2"
    def helpBtn(self):
        sm.current = "main"

class AskExpertTwoScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_2_mark.jpg"
        self.check_1.active = True
        self.check_2.active = False
        self.check_3.active = False
        self.fehler_2.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Brauchen Sie Unterstützung bei der Fehlerbehebung?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)
        pos_list = ['ja']
        neg_list = ['nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = startwork_popup()
            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "error_2"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "experte_2"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                sm.current = "experte_2"
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "error_2"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "error_2"
        elif res == 2:
            sm.current = "experte_2"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            sm.current = "experte_2"
        elif res == 5:
            sm.current = "error_2"
    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "experte_2"
    def skipBtn(self):
        sm.current = "error_2"
    def helpBtn(self):

        wait_popup()

class AskExpertThreeScreen(Screen):
    modus = ObjectProperty(None)
    user = ObjectProperty(None)
    icon = ObjectProperty(None)
    bagger = ObjectProperty(None)
    fehler = ObjectProperty(None)
    fehler_1 = ObjectProperty(None)
    fehler_2 = ObjectProperty(None)
    fehler_3 = ObjectProperty(None)
    werkzeug = ObjectProperty(None)
    current = ""
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.modus.text = "Modus: " + modus
        self.user.text = "Benutzername: " + self.current
        self.bagger.source = "fehler_3_mark.jpg"
        self.check_1.active = True
        self.check_2.active = True
        self.check_3.active = False
        self.fehler_3.color = (0,1,0,1)
        self.icon._coreimage.anim_reset(False)
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        talk_text="Brauchen Sie Unterstützung bei der Fehlerbehebung?"
        say(talk_text,self)
        self.icon._coreimage.anim_reset(False)
        pos_list = ['ja']
        neg_list = ['nein']
        listen = True
        res = speech_reco(listen,pos_list, neg_list,self)
        if res == 0:
            popupWindow = startwork_popup()
            listen = True
            res = speech_reco(listen, pos_list, neg_list,self)
            if res == 1:
                sm.current = "error_3"
                popupWindow.dismiss()
            elif res == 2:
                sm.current = "experte_3"
                popupWindow.dismiss()
            elif res == 3:
                sm.current = "login"
                popupWindow.dismiss()
            elif res == 4:
                sm.current = "experte_3"
                popupWindow.dismiss()
            elif res == 5:
                sm.current = "error_3"
                popupWindow.dismiss()

        elif res ==1:
            sm.current = "error_3"
        elif res == 2:
            sm.current = "experte_3"
        elif res == 3:
            sm.current = "login"
        elif res == 4:
            sm.current = "experte_3"
        elif res == 5:
            sm.current = "error_3"
    #Definition der Funktion der Button
    def backBtn(self):
        sm.current = "experte_3"
    def skipBtn(self):
        sm.current = "error_3"
    def helpBtn(self):

        wait_popup()

class MainWindow(Screen):
    profil = ObjectProperty(None)
    created = ObjectProperty(None)
    user = ObjectProperty(None)

    current = ""

    def logOut(self):
        sm.current = "login"
    # Individuelle Anzeige der jeweiligen Fenster
    def on_enter(self, *args):
        password, modus = db.get_user(self.current)
        self.profil.text = "Leistungsstand: " + modus
        self.user.text = "Benutzername: " + self.current

class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Achtung',
                  content=Label(text='Benutzername oder Password sind falsch?'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def say(text,self):
    tts = gTTS(text=text, lang='de')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    self.icon._coreimage.anim_reset(True)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



def speech_reco(listen, pos_list, neg_list,self):
    next_list = ['Überspringen', 'überspringen','weiter','Weiter']
    logout_list=['Abmelden', 'abmelden']
    help_list = ['Sprachsteuerung','sprachsteuerung','Steuerung','steuerung']
    back_list = ['Schritt', 'zurück']
    sampling_rate = 48000
    data_size = 8192
    recog = spreg.Recognizer()
    with spreg.Microphone(sample_rate = sampling_rate, chunk_size = data_size) as source:
        while listen == True:
            print("bitte sprechen:")
            recog.adjust_for_ambient_noise(source)
            speech = recog.listen(source)
            try:
               text = recog.recognize_google(speech, language = "de-DE")
               print(text)
               res_help = any(ele in text for ele in help_list)
               res_next = any(ele in text for ele in next_list)
               res_back = any(ele in text for ele in back_list)
               res_logout = any(ele in text for ele in logout_list)
               res_pos = any(ele in text for ele in pos_list)
               res_neg = any(ele in text for ele in neg_list)
               if res_help == True:
                   listen = False
                   res = 0
               elif res_next == True:
                   listen = False
                   res = 1
               elif res_back == True:
                   listen = False
                   res = 2
               elif res_logout == True:
                   listen = False
                   res = 3
               elif res_neg == True:
                   listen = False
                   res = 4
               elif res_pos == True:
                   listen = False
                   res = 5
               else:
                   listen = True
                   talk_text = 'Ich habe Sie nicht verstanden. Könnten Sie es bitte noch einmal wiederholen.'
                   say(talk_text,self)
                   self.icon._coreimage.anim_reset(False)

            except spreg.UnknownValueError:
               print('bitte sprechen Sie noch einmal')
            except spreg.RequestError as e:
               print("Request error from Google Speech Recognition service; {}".format(e))

    return res






kv = Builder.load_file("gui.kv")
sm = WindowManager()
db = DataBase("users.txt")

screens = [
    LoginScreen(name="login"),
    MainWindow(name="main"),
    WaitTwoScreen(name="wait_two"),
    HelloScreen(name="hello"),
    StartScanScreen(name="start_scan"),
    WaitScreen(name="wait"),
    StartWorkScreen(name="start_work"),
    NeedHelpOneScreen(name="need_help_1"),
    ErrorOneScreen(name="error_1"),
    AskOneScreen(name="ask_1"),
    ReadyOneScreen(name="ready_1"),
    ErrorTwoScreen(name="error_2"),
    AskTwoScreen(name="ask_2"),
    ReadyTwoScreen(name="ready_2"),
    ErrorThreeScreen(name="error_3"),
    AskThreeScreen(name="ask_3"),
    ReadyThreeScreen(name="ready_3"),
    CheckScreen(name="check"),
    ByeScreen(name="bye"),
    ExpertOneScreen(name="experte_1"),
    ExpertTwoScreen(name="experte_2"),
    ExpertThreeScreen(name="experte_3"),
    AskExpertOneScreen(name="ask_expert_1"),
    AskExpertTwoScreen(name="ask_expert_2"),
    AskExpertThreeScreen(name="ask_expert_3"),
    LoadOneScreen(name="load_one"),
    LoadTwoScreen(name="load_two")
]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
       # Window.bind(on_request_close=self.end)
        return sm


if __name__ == "__main__":
    MyMainApp().run()
