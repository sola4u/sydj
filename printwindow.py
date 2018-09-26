
#/usr/bin/env python
#coding: utf-8

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets
from address import *
from calendar import *
from login import *
import address_dic


class PrintWindow(QWidget):

    def __init__(self,id):
        super(PrintWindow, self).__init__()
