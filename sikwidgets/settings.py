from org.sikuli.script.natives import Vision
from sikuli.Sikuli import Settings, setShowActions

DEBUG = False

def debug(status=True):
	global DEBUG
	DEBUG = status
	if DEBUG:
		setShowActions(True)
	else:
		setShowActions(False)
		
IMAGES_PATH = "images"

def mouse_speed_fast():
	Settings.MoveMouseDelay = 0.2

def mouse_speed_med():
	Settings.MoveMouseDelay = 0.5

def mouse_speed_slow():
	Settings.MoveMouseDelay = 0.8

def accuracy_high():
	Vision.setParameter("MinTargetSize", 17)
	Settings.MinSimilarity = 0.98

def accuracy_med():
	Vision.setParameter("MinTargetSize", 12)
	Settings.MinSimilarity = 0.95

def accuracy_low():
	Vision.setParameter("MinTargetSize", 7)
	Settings.MinSimilarity = 0.90

# Defaults
debug(False)
mouse_speed_med()
accuracy_med()