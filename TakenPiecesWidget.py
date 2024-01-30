from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


class TakenPiecesWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 54)
        self.setScene(self.scene)

    def show_taken_pieces(self, pieces):
        for i in range(len(pieces)):
            svg = QGraphicsSvgItem(pieces[i].texture)
            svg.setScale(0.5)
            svg.setPos(i*36, 0)
            self.scene.addItem(svg)

    def clear(self):
        self.scene.clear()


