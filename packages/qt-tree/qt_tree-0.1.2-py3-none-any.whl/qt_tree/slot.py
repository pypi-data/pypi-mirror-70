from PySide2 import QtCore, QtGui, QtWidgets
from . import util


class SlotItem(QtWidgets.QGraphicsItem):
    def __init__(self, parent, slot_type):
        super().__init__(parent)

        # Status.
        self.setAcceptHoverEvents(True)

        # Storage.
        self.slotType = slot_type

        # Style.
        self._createStyle(parent)

        self.pen = QtGui.QPen()
        self.pen.setStyle(QtCore.Qt.SolidLine)

        self.setFlag(SlotItem.ItemStacksBehindParent)

        # Connections storage.
        self.connected_slots = list()
        self.newConnection = None
        self.connections = list()
        if slot_type == 'parent':
            self.maxConnections = 1
        elif slot_type == 'child':
            self.maxConnections = -1
        else:
            raise RuntimeError

    def accepts(self, slot_item):
        # no child on child or parent on parent
        hasChildItem = 'child' in [self.slotType, slot_item.slotType]
        hasParentItem = 'parent' in [self.slotType, slot_item.slotType]
        if not (hasChildItem and hasParentItem):
            return False

        # no self connection
        if self.parentItem() == slot_item.parentItem():
            return False

        # no more than maxConnections
        if self.maxConnections > 0 and len(self.connected_slots) >= self.maxConnections:
            return False

        # no loop
        if self.__check_no_loop(slot_item):
            return False

        # otherwize, all fine.
        return True

    def __check_no_loop(self, slot_item):
        if self.slotType == 'child':
            parent = self.parentItem().data
        elif self.slotType == 'parent':
            child = self.parentItem().data

        if slot_item.slotType == 'child':
            parent = slot_item.parentItem().data
        elif slot_item.slotType == 'parent':
            child = slot_item.parentItem().data

        return any(ancestor is child
                   for ancestor in parent.iter_path_reverse())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.newConnection = ConnectionItem(self.center(),
                                                self.mapToScene(event.pos()),
                                                self,
                                                None)

            self.connections.append(self.newConnection)
            self.scene().addItem(self.newConnection)

            view = self.scene().views()[0]
            view.drawingConnection = True
            view.sourceSlot = self
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        from .node import NodeItem

        view = self.scene().views()[0]
        config = view.config
        if view.drawingConnection:
            mbb = util._createPointerBoundingBox(pointerPos=event.scenePos().toPoint(),
                                                 bbSize=config['mouse_bounding_box'])

            # Get nodes in pointer's bounding box.
            targets = self.scene().items(mbb)

            if any(isinstance(target, NodeItem) for target in targets):
                if self.parentItem() not in targets:
                    for target in targets:
                        if isinstance(target, NodeItem):
                            view.currentHoveredNode = target
            else:
                view.currentHoveredNode = None

            # Set connection's end point.
            self.newConnection.target_point = self.mapToScene(event.pos())
            self.newConnection.updatePath()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        view = self.scene().views()[0]
        if event.button() == QtCore.Qt.LeftButton:
            view.drawingConnection = False

            target = self.scene().itemAt(event.scenePos().toPoint(), QtGui.QTransform())

            if not isinstance(target, SlotItem):
                self.newConnection._remove()
                super().mouseReleaseEvent(event)
                return

            if target.accepts(self):
                self.newConnection.target = target
                self.newConnection.source = self
                self.newConnection.target_point = target.center()
                self.newConnection.source_point = self.center()

                # Perform the ConnectionItem.
                self.connect(target, self.newConnection)
                target.connect(self, self.newConnection)

                self.newConnection.updatePath()
            else:
                self.newConnection._remove()
        else:
            super().mouseReleaseEvent(event)

        view.currentHoveredNode = None

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)

        view = self.scene().views()[0]
        config = view.config
        if view.drawingConnection:
            if self.parentItem() == view.currentHoveredNode:
                painter.setBrush(
                    QtGui.QColor(*config['connection']
                                 ['color']['non_connectable'])
                )
                if self.slotType != view.sourceSlot.slotType:
                    if not view.sourceSlot.__check_no_loop(self):
                        _penValid = QtGui.QPen()
                        _penValid.setStyle(QtCore.Qt.SolidLine)
                        _penValid.setWidth(2)
                        _penValid.setColor(QtGui.QColor(255, 255, 255, 255))
                        painter.setPen(_penValid)
                        painter.setBrush(self.brush)

        painter.drawEllipse(self.boundingRectForPaint())

    def center(self):
        rect = self.boundingRect()
        center = QtCore.QPointF(rect.x() + rect.width() * 0.5,
                                rect.y() + rect.height() * 0.5)

        return self.mapToScene(center)

    def _createStyle(self, parent):
        config = parent.scene().views()[0].config
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor(*config['slot']['color']['main']))

    def boundingRect(self):
        width = height = self.parentItem().baseWidth / 2.0
        x = (self.parentItem().baseWidth - width) / 2.
        y = - height / 2.0
        if self.slotType == 'child':
            y += self.parentItem().height
        rect = QtCore.QRectF(QtCore.QRect(x, y, width, height))
        return rect

    def boundingRectForPaint(self):
        width = height = self.parentItem().baseWidth / 10.0
        x = (self.parentItem().baseWidth - width) / 2.
        y = - height / 2.0
        if self.slotType == 'child':
            y += self.parentItem().height
        rect = QtCore.QRectF(QtCore.QRect(x, y, width, height))
        return rect

    def connect(self, slot_item, connection):
        scene = self.scene()
        view = scene.views()[0]

        if self.maxConnections > 0 and len(self.connected_slots) >= self.maxConnections:
            # Already connected.
            self.connections[self.maxConnections - 1]._remove()

        # Populate connection.
        if slot_item.slotType == 'parent':
            connection.parentSlotItem = slot_item
            connection.childNode = slot_item.parentItem()
            connection.childSlotItem = self
            connection.parentNode = self.parentItem()
        else:
            connection.childSlotItem = slot_item
            connection.parentNode = slot_item.parentItem()
            connection.parentSlotItem = self
            connection.childNode = self.parentItem()

        # Add slot to connected slots.
        if slot_item not in self.connected_slots:
            self.connected_slots.append(slot_item)

        # Add connection.
        if connection not in self.connections:
            self.connections.append(connection)

        # Connect data
        child = connection.childNode
        parent = connection.parentNode
        if child is not None and parent is not None:
            child = child.data
            parent = parent.data
            child.parent = parent
            if scene.root != parent.root:
                scene.root = parent.root
                view.signal_RootUpdated.emit(parent.root)

        # Emit signal.
        view.signal_Connected.emit(
            connection.childNode, connection.parentNode
        )

    def disconnect(self, connection):
        view = self.scene().views()[0]

        # Remove slot from connected slots
        if self.slotType == 'parent':
            slot_item = connection.childSlotItem
        else:
            slot_item = connection.parentSlotItem

        if slot_item in self.connected_slots:
            self.connected_slots.remove(slot_item)

        # Remove connections
        self.connections.remove(connection)

        # Disconnect data
        child = connection.childNode
        parent = connection.parentNode
        if child is not None and parent is not None:
            child.data.parent = None

        # Emit signal.
        view.signal_Disconnected.emit(
            connection.childNode, connection.parentNode
        )


class ConnectionItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, source_point, target_point, source, target):
        super().__init__()

        self.setZValue(1)

        # Storage.
        self.parentNode = None
        self.childNode = None

        self.source_point = source_point
        self.target_point = target_point
        self.source = source
        self.target = target

        self.childSlotItem = None
        self.parentSlotItem = None

        self.movable_point = None

        self.data = tuple()

        # Methods.
        self._createStyle()

    def _createStyle(self):
        config = self.source.scene().views()[0].config
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

        self._pen = QtGui.QPen(
            QtGui.QColor(*config['connection']['color']['main'])
        )
        self._pen.setWidth(config['connection']['width'])

    def mousePressEvent(self, event):
        view = self.scene().views()[0]

        for item in view.scene().items():
            if isinstance(item, ConnectionItem):
                item.setZValue(0)

        view.drawingConnection = True

        d_to_target = (event.pos() - self.target_point).manhattanLength()
        d_to_source = (event.pos() - self.source_point).manhattanLength()
        if d_to_target < d_to_source:
            self.target_point = event.pos()
            self.movable_point = 'target_point'
            self.target.disconnect(self)
            self.target = None
            view.sourceSlot = self.source
        else:
            self.source_point = event.pos()
            self.movable_point = 'source_point'
            self.source.disconnect(self)
            self.source = None
            view.sourceSlot = self.target

        self.updatePath()

    def mouseMoveEvent(self, event):
        from .node import NodeItem
        view = self.scene().views()[0]
        config = view.config

        mbb = util._createPointerBoundingBox(pointerPos=event.scenePos().toPoint(),
                                             bbSize=config['mouse_bounding_box'])

        # Get nodes in pointer's bounding box.
        targets = self.scene().items(mbb)

        if any(isinstance(target, NodeItem) for target in targets):

            if view.sourceSlot.parentItem() not in targets:
                for target in targets:
                    if isinstance(target, NodeItem):
                        view.currentHoveredNode = target
        else:
            view.currentHoveredNode = None

        if self.movable_point == 'target_point':
            self.target_point = event.pos()
        else:
            self.source_point = event.pos()

        self.updatePath()

    def mouseReleaseEvent(self, event):
        view = self.scene().views()[0]
        view.drawingConnection = False

        slot = self.scene().itemAt(event.scenePos().toPoint(), QtGui.QTransform())

        if not isinstance(slot, SlotItem):
            self._remove()
            self.updatePath()
            super().mouseReleaseEvent(event)
            return

        if self.movable_point == 'target_point':
            if slot.accepts(self.source):
                self.target = slot
                self.target_point = slot.center()
                slot_child = self.source
                slot_parent = self.target
                slot_parent.connect(slot_child, self)
                self.updatePath()
            else:
                self._remove()

        else:
            if slot.accepts(self.target):
                self.source = slot
                self.source_point = slot.center()
                slot_parent = self.target
                slot_child = self.source
                slot_child.connect(slot_parent, self)
                self.updatePath()
            else:
                self._remove()

    def _remove(self):
        if self.source is not None:
            self.source.disconnect(self)
        if self.target is not None:
            self.target.disconnect(self)

        scene = self.scene()
        scene.removeItem(self)
        scene.update()

    def updatePath(self):
        self.setPen(self._pen)

        path = QtGui.QPainterPath()
        path.moveTo(self.source_point)
        dx = (self.target_point.x() - self.source_point.x()) * 0.5
        dy = self.target_point.y() - self.source_point.y()
        ctrl1 = QtCore.QPointF(self.source_point.x() + dx,
                               self.source_point.y() + dy * 0)
        ctrl2 = QtCore.QPointF(self.source_point.x() + dx,
                               self.source_point.y() + dy * 1)
        path.cubicTo(ctrl1, ctrl2, self.target_point)

        self.setPath(path)
