import sys
from vidCapReco import main
from listen import listen
from bot import bot1
from threading import *

main()
t1 = Thread(target = bot1)
t1.start()
