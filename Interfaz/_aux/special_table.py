# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:57:52 2023

@author: Spect
"""


from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QTableView
from PyQt5.QtCore import Qt, QModelIndex

class ReorderableTable(QTableWidget):
    def __init__(self):
        super().__init__(5, 3)  # 5 rows and 3 columns

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setDragDropMode(QTableWidget.InternalMove)
        # self.setDragDropMode(QTableWidget.DragDrop)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.setDragDropOverwriteMode(False)

        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"Row {row}, Col {col}")
                self.setItem(row, col, item)
                
            
    def dropEvent(self, event):
        if event.source() == self and (event.dropAction() == Qt.MoveAction or self.dragDropMode() == QAbstractItemView.InternalMove):
            success, row, col, topIndex = self.dropOn(event)
            if success:             
                selRows = self.getSelectedRowsFast()                        

                top = selRows[0]
                # print 'top is %d'%top
                dropRow = row
                if dropRow == -1:
                    dropRow = self.rowCount()
                # print 'dropRow is %d'%dropRow
                offset = dropRow - top
                # print 'offset is %d'%offset

                for i, row in enumerate(selRows):
                    r = row + offset
                    if r > self.rowCount() or r < 0:
                        r = 0
                    self.insertRow(r)
                    # print 'inserting row at %d'%r


                selRows = self.getSelectedRowsFast()
                # print 'selected rows: %s'%selRows

                top = selRows[0]
                # print 'top is %d'%top
                offset = dropRow - top                
                # print 'offset is %d'%offset
                for i, row in enumerate(selRows):
                    r = row + offset
                    if r > self.rowCount() or r < 0:
                        r = 0

                    for j in range(self.columnCount()):
                        # print 'source is (%d, %d)'%(row, j)
                        # print 'item text: %s'%self.item(row,j).text()
                        source = QTableWidgetItem(self.item(row, j))
                        # print 'dest is (%d, %d)'%(r,j)
                        self.setItem(r, j, source)

                # Why does this NOT need to be here?
                # for row in reversed(selRows):
                    # self.removeRow(row)

                event.accept()

        else:
            QTableView.dropEvent(event)                

    def getSelectedRowsFast(self):
        selRows = []
        for item in self.selectedItems():
            if item.row() not in selRows:
                selRows.append(item.row())
        return selRows

    def droppingOnItself(self, event, index):
        dropAction = event.dropAction()

        if self.dragDropMode() == QAbstractItemView.InternalMove:
            dropAction = Qt.MoveAction

        if event.source() == self and event.possibleActions() & Qt.MoveAction and dropAction == Qt.MoveAction:
            selectedIndexes = self.selectedIndexes()
            child = index
            while child.isValid() and child != self.rootIndex():
                if child in selectedIndexes:
                    return True
                child = child.parent()

        return False

    def dropOn(self, event):
        if event.isAccepted():
            return False, None, None, None

        index = QModelIndex()
        row = -1
        col = -1

        if self.viewport().rect().contains(event.pos()):
            index = self.indexAt(event.pos())
            if not index.isValid() or not self.visualRect(index).contains(event.pos()):
                index = self.rootIndex()

        if self.model().supportedDropActions() & event.dropAction():
            if index != self.rootIndex():
                dropIndicatorPosition = self.position(event.pos(), self.visualRect(index), index)

                if dropIndicatorPosition == QAbstractItemView.AboveItem:
                    row = index.row()
                    col = index.column()
                    # index = index.parent()
                elif dropIndicatorPosition == QAbstractItemView.BelowItem:
                    row = index.row() + 1
                    col = index.column()
                    # index = index.parent()
                else:
                    row = index.row()
                    col = index.column()

            if not self.droppingOnItself(event, index):
                # print 'row is %d'%row
                # print 'col is %d'%col
                return True, row, col, index

        return False, None, None, None

    def position(self, pos, rect, index):
        r = QAbstractItemView.OnViewport
        margin = 2
        if pos.y() - rect.top() < margin:
            r = QAbstractItemView.AboveItem
        elif rect.bottom() - pos.y() < margin:
            r = QAbstractItemView.BelowItem 
        elif rect.contains(pos, True):
            r = QAbstractItemView.OnItem

        if r == QAbstractItemView.OnItem and not (self.model().flags(index) & Qt.ItemIsDropEnabled):
            r = QAbstractItemView.AboveItem if pos.y() < rect.center().y() else QAbstractItemView.BelowItem

        return r


