import sys

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

import time


def some_func(param0, param1, callback_funcs=[]):
    total = 100

    for i in range(total):
        time.sleep(0.1)
        if i % 10 == 0 and len(callback_funcs) > 0:
            val = (i / total) * 100
            for func in callback_funcs:
                func(int(val))



class Worker(QObject):
    finished = Signal()
    progress = Signal(int)

    def __init__(self):
        super(Worker, self).__init__()
        self.func = None
        self.args = list()
        self.kwargs = dict()

    def set_workder_func(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """

        """
        def worker_callback(val):
            self.progress.emit(val)

        if not ('callback_funcs' in self.kwargs):
            self.kwargs['callback_funcs'] = []
        self.kwargs['callback_funcs'].append(worker_callback)

        if self.func is not None:
            self.func(*self.args, **self.kwargs)
        self.finished.emit()


class ProgreeThread(object):
    def __init__(self):
        # super(ProgreeThread, self).__init__()
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)

    def add_progress_callback(self, func):
        self.worker.progress.connect(func)

    def set_worker_func(self, func, *args, **kwargs):
        # self.worker.progress.connect(self.reportProgress)
        self.worker.set_workder_func(func, *args, **kwargs)

    def add_finished_callback(self, func):
        self.thread.finished.connect(func)

    def start(self):
        self.thread.start()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        # self.longRunningBtn.clicked.connect(self.runLongTask)
        self.longRunningBtn.clicked.connect(self.runLongTask2)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)
        self.thread_pool = []

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        print('reportProgress', n)
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def runLongTask2(self):
        # def callback_fun(val):
        #     self.reportProgress(val)

        progress = ProgreeThread()
        # protect local-variable destructor
        self.thread_pool.append(progress)
        # self.progress = progress
        progress.add_progress_callback(self.reportProgress)

        def test_callback_func(val):
            print('test_callback_func', val)

        progress.set_worker_func(some_func, 'show', 1, callback_funcs=[test_callback_func])
        # progress.add_progress_callback()
        progress.start()
        print('===============================progress.start()===============================')
        self.longRunningBtn.setEnabled(False)
        print('self.longRunningBtn.setEnabled(False)')

        # self.longRunningBtn.setEnabled()
        progress.add_finished_callback(
            lambda: self.longRunningBtn.setEnabled(True)
        )

        print('self.thread.finished.connect( lambda: self.longRunningBtn.setEnabled(True)')

        progress.add_finished_callback(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

        print('        self.thread.finished.connect(\
                lambda: self.stepLabel.setText("Long-Running Step: 0")\
            )')

        progress.add_finished_callback(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )
        progress.add_finished_callback(
            lambda: self.thread_pool.remove(progress)
        )

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        print('thread init and connect')
        # Step 6: Start the thread
        self.thread.start()
        print('thread-start')

        # Final resets
        self.longRunningBtn.setEnabled(False)
        print('self.longRunningBtn.setEnabled(False)')

        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )

        print('self.thread.finished.connect( lambda: self.longRunningBtn.setEnabled(True)')

        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

        print('        self.thread.finished.connect(\
            lambda: self.stepLabel.setText("Long-Running Step: 0")\
        )')
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
