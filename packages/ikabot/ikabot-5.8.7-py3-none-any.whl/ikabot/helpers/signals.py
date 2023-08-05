#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import gettext
from ikabot.config import *
from ikabot.helpers.botComm import *

t = gettext.translation('signals', 
                        localedir, 
                        languages=idiomas,
                        fallback=True)
_ = t.gettext

def do_nothing(signal, frame):
	pass

def deactivate_sigint():
	signal.signal(signal.SIGHUP, do_nothing)
	signal.signal(signal.SIGINT, do_nothing)

def create_handler(s):
	def _handler(signum, frame):
		raise Exception(_('Señal recibida número {:d}').format(signum))
	return _handler

def setSignalsHandlers(s):
	signals = [signal.SIGQUIT, signal.SIGABRT, signal.SIGTERM]
	for sgn in signals:
		signal.signal(sgn, create_handler(s))

def setInfoSignal(s, info): # el proceso explica su funcion por stdout
	info = _('información del proceso {}:\n{}').format(os.getpid(), info)
	def _sendInfo(signum, frame):
		sendToBot(s, info)
	signal.signal(signal.SIGUSR1, _sendInfo) # kill -SIGUSR1 pid
