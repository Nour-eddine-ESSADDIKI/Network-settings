from sys import stdout

from PyQt5 import QtCore
from PyQt5.uic.properties import QtGui
from PyQt5.uic.uiparser import QtWidgets
from mainform import *
import subprocess,re
import scapy.all
from ping_form import Ui_Form1
import os
import pyperclip
from netaddr import IPAddress
import ipaddress


class Controllers:

    def showmainwindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btnpingfr.clicked.connect(self.showpingform)
        self.ui.btnlaunch.clicked.connect(self.cardsnames)
        self.ui.btnaffich.clicked.connect(self.afficher)
        self.ui.btnrenew.clicked.connect(self.renew)
        self.ui.btnrelease.clicked.connect(self.release)
        self.ui.btnexit.setIcon(QtGui.QIcon("icons/delete.svg"))
        self.window.show()

    def showpingform(self):
        self.window1 = QtWidgets.QWidget()
        self.ui1 = Ui_Form1()
        self.ui1.setupUi(self.window1)
        self.window1.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui1.btnpingexe.clicked.connect(self.pingg)
        self.ui1.exitpingform.setIcon(QtGui.QIcon("icons/delete.svg"))
        self.ui1.backmainwindow.setIcon(QtGui.QIcon("icons/return-arrow.svg"))
        self.ui1.backmainwindow.clicked.connect(self.window.show)
        self.ui1.backmainwindow.clicked.connect(self.window1.hide)
        self.window1.show()
        self.window.hide()
        #self.ui1.exitpingform.clicked.connect(self.window.show)
        self.ui1.exitpingform.clicked.connect(self.window1.close)

    def pingg(self):

        host = self.ui1.lineEdit.text()

        command = subprocess.Popen(["ping", host],stdout=subprocess.PIPE,universal_newlines=True).communicate()[0]
        #print(command)
        # if command.poll() == 0:
        #     reponse = "yes"
        # else:
        #     reponse = "no"
        #
        # print(reponse)

        if "TTL" in command:
            reponse="yes"
        else:
            reponse="no"

        if reponse == "yes":
            try:
                self.ui1.textoutping.setPlainText(
                    "Il ya de la Connexion Entre Votre Machine Et la station :" + host)
            except:
                pass

        else:

            try:
                    self.ui1.textoutping.setPlainText("Il n'ya pas d'une Connexion Avec la station :" + host)


                    QtWidgets.QMessageBox.critical(self.window, 'Erreur',
                      'Veuiller verifier que l\'adresse vous avez taper est correct ou verifier votre connexion internet',
                                                   QtWidgets.QMessageBox.Ok)

            except:
                pass




    def cardsnames(self):
        interfacees = []
        a = scapy.all.get_windows_if_list()
        for i in range(len(a)):
            var = a[i].get('name')
            interfacees.append(var)
        for i in interfacees:
            self.ui.comboBox.addItem(i)


    def afficher(self):

        itrfce = str(self.ui.comboBox.currentText())
        try:
            b = os.system("ipconfig /all | clip")
            a = pyperclip.paste()
            a = str(a)
            lis = []
            carte = []
            for line in a.split("\n"):
                lis.append(line)
            for i in range(len(lis)):
                if itrfce in lis[i]:
                    index = i
                    break
            for i in lis:
                if "Carte" in i:
                    if "Description" not in i:
                        carte.append(i)
            for i in range(len(lis)):
                if itrfce in lis[i]:
                    index = i
                    break
            for i in range(len(carte)):
                if itrfce in carte[i]:
                    next_card = carte[i + 1]
                    break
            for i in range(len(lis)):
                if next_card in lis[i]:
                    next_ind = i
                    break
            for i in range(len(lis)):
                if i >= index and i <= next_ind:
                    if "Adresse IPv4" in lis[i]:
                        lineeipv4 = lis[i]
                        #print(lineeipv4)
                        break
            for i in range(len(lis)):
                if i >= index and i <= next_ind:
                    if "Masque de sous-réseau" in lis[i]:
                        linemask = lis[i]
                        # print(linemask)
                        break
            for i in range(len(lis)):
                if i >= index and i <= next_ind:
                    if "Passerelle par défaut" in lis[i]:
                        linepasserelle = lis[i]
                        break
            for i in range(len(lis)):
                if i >= index and i <= next_ind:
                    if "DHCP activé" in lis[i]:
                        lineedhcp = lis[i]
                        break
            for i in range(len(lis)):
                if i >= index and i <= next_ind:
                    if "Serveurs DNS" in lis[i]:
                        lineedns = lis[i]
                        break

        except:
            pass

        try:
            try:
                pv4_add = re.search("([0-9]{1,3}\.*){4}", lineeipv4).group(0)
                if pv4_add.isspace():
                    self.ui.lineipv4.setText("None")
                self.ui.lineipv4.setText(str(pv4_add))
            except:
                self.ui.lineipv4.setText("None")

            try:
                masque = linemask.partition(":")[2]
                if masque.isspace():
                    self.ui.linemasquee.setText("None")
                else:
                    self.ui.linemasquee.setText(str(masque))
            except:
                self.ui.linemasquee.setText("None")

            try:
                passerlle = linepasserelle.partition(":")[2]
                if passerlle.isspace():
                    self.ui.linegateway.setText("None")
                else:
                    self.ui.linegateway.setText(str(passerlle))
            except:
                self.ui.linegateway.setText("None")

            try:
                dns = lineedns.partition(":")[2]
                if dns.isspace():
                    self.ui.linedns.setText("None")
                else:
                    self.ui.linedns.setText(dns)
            except:
                self.ui.linedns.setText("None")

            try:
                dhcp = lineedhcp.partition(":")[2]
                if dhcp.isspace():
                    self.ui.linedhcp.setText("None")
                else:
                    self.ui.linedhcp.setText(dhcp)
            except:
                self.linedhcp.setText("None")

        except:
            pass

        try:
            masque_cidr = IPAddress(masque.strip()).netmask_bits()
            masque_cidr = str(masque_cidr)
            this_host = pv4_add + '/' + masque_cidr
            addr_reseau = ipaddress.ip_network(this_host.strip(), strict=False)
            self.ui.lineaddreseau.setText(str(addr_reseau))
        except:
            self.ui.lineaddreseau.setText("None")

    def release(self):
        try:
            subprocess.call(["ipconfig", "/release"], shell=True)
            QtWidgets.QMessageBox.information(self.window, 'ATTENTION','vous avez libéré votre addresse IP.',QtWidgets.QMessageBox.Ok)
        except:
            pass

    def renew(self):
        try:
            subprocess.call(["ipconfig", "/renew"], shell=True)
            QtWidgets.QMessageBox.information(self.window, 'ATTENTION', 'vous avez demendé une adresse IP.',QtWidgets.QMessageBox.Ok)

        except:
            pass






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    controller = Controllers()
    controller.showmainwindow()
    sys.exit(app.exec_())
