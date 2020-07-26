from cover import initCoverPage

from pylash.core import init, addChild
from pylash.loaders import LoadManage
from pylash.events import MouseEvent
from pylash.ui import LoadingSample1, Button

import os

def main():
    loadList = []
    for root, dirs, files in os.walk("./res/images/"):
        for filename in files:
            if filename.split(".")[1] == "png":
                loadList.append({"name":filename.split(".")[0], "path": root+filename})

    for root, dirs, files in os.walk("./res/"):
        for filename in files:
            if filename.split(".")[1] == "wav":
                loadList.append({"name":filename.split(".")[0], "path": root+filename})

    loadingLayer = LoadingSample1()
    addChild(loadingLayer)

    def next(result):
        loadingLayer.remove()
        initCoverPage(result)

    
    LoadManage.load(loadList, loadingLayer.setProgress, next)

init(250, "Greedy Snake", 520, 640, main)
