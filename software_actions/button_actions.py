from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer
from transpileQSS import loadStyleSheet
from functools import partial
import pymupdf, globals, os, platform, subprocess, threading, shutil, time, pyautogui as pag



# Built in actions
def quitSoftware():
    globals.app.quit()

def minimizeSoftware():
    window = globals.app.activeWindow()
    if window is not None:
        window.showMinimized()


def toggleDialog(dialogID):
    dialog = [dialog for dialog in globals.transpiler.dialogs if dialogID in dialog.attributes.get("id")][0]
    if dialog.widget.isVisible():
        QTimer.singleShot(0, lambda: dialog.widget.reject())
    else:
        QTimer.singleShot(0, lambda: dialog.widget.open())





# Maybe built in?
def loadPDFPage(loaderID, filePath=None, pageNumber=0):
    pdfLoader = globals.transpiler.root.getChildrenBySelector(["loader", loaderID])[0]

    try:
        if pdfLoader is None:
            print(f"PDF loader with ID {loaderID} not found or not initialized")
            return
        if filePath: pdfLoader.doc = pymupdf.open(filePath)

        pageIndex = pdfLoader.currentPage + pageNumber

        if pdfLoader.doc is None: raise ValueError("PDF document not loaded")
        if pageIndex < 0 or pageIndex >= pdfLoader.doc.page_count:
            print(f"Page index out of range {pageIndex} for {pdfLoader.doc.page_count} pages")
            return
        pdfLoader.currentPage = pageIndex
        page = pdfLoader.doc[pageIndex]
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return

    def load():
        pix = page.get_pixmap()
        mode = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, mode)

        pixmap = QPixmap.fromImage(image)

        size = pdfLoader.widget.size()
        if pixmap.height() > pixmap.width(): size *= 2
        scaled_pixmap = pixmap.scaled(
            size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        pdfLoader.widget.setAlignment(Qt.AlignCenter)
        pdfLoader.widget.setPixmap(scaled_pixmap)
        pdfLoader.widget.setFixedSize(scaled_pixmap.size())
    thread = threading.Thread(target=load)
    thread.start()

def loadPDF(viewerID, filePath):
    pdfViewer = globals.transpiler.root.getChildrenBySelector(["box", viewerID])[0]
    pdfViewer.container.layout().setAlignment(Qt.AlignCenter)

    try:
        if pdfViewer is None:
            print(f"PDF viewer with ID {viewerID} not found or not initialized")
            return

        pdfViewer.deleteChildren()

        pdfDoc = pymupdf.open(filePath)
        pageCount = pdfDoc.page_count
        for pageNum in range(pageCount):
            data = {
                "tag": "loader",
                "parent": pdfViewer,
                "attributes": {
                    "id": f"pdf{pageNum}",
                    "class": "pdf_page",
                    "src": f"{filePath}:{pageNum}",
                    "type": "pdf"
                },
                "content": ""
            }
            elem = globals.transpiler.createElement(data)
            elem.parent.children.append(elem)
            elem.load(elem.parent)
        globals.window.style = loadStyleSheet("style.qss")
        globals.window.setStyleSheet(globals.window.style)
        pdfDoc.close()

    except Exception as e:
        print(f"Error loading PDF: {e}")
        return