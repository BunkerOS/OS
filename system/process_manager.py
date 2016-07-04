from .utils import *
import time


class ProcessManager:
    MAX = 10
    instance = None

    def __init__(self):
        if not ProcessManager.instance or ProcessManager.instance != self:
            ProcessManager.instance = self
        self._windows = []
        self._adding_order = []
        self._clock = pygame.time.Clock()
        self._execution_datas = {}
        self._current_session = "NONE"

    @staticmethod
    def set_session(name):
        ProcessManager.instance._current_session = name

    @staticmethod
    def execution_datas():
        return ProcessManager.instance._execution_datas

    @staticmethod
    def update_process(process):
        if process.state != WStates.UNACTIVE:
            start = time.time()
            process.update()
            ProcessManager.instance._execution_datas[process.get_title()]['exc_times'].append((time.time() - start) * 1000)
        else:
            ProcessManager.instance._execution_datas[process.get_title()]['draw_times'].append(0.0)
        if len(ProcessManager.instance._execution_datas[process.get_title()]['exc_times']) > ProcessManager.MAX:
            ProcessManager.instance._execution_datas[process.get_title()]['exc_times'] = \
                ProcessManager.instance._execution_datas[process.get_title()]['exc_times'][::-1][:ProcessManager.MAX][::-1]

    @staticmethod
    def draw_process(process, *args):
        if process.state != WStates.UNACTIVE:
            start = time.time()
            process.draw(*args)
            ProcessManager.instance._execution_datas[process.get_title()]['draw_times'].append((time.time() - start) * 1000)
        else:
            ProcessManager.instance._execution_datas[process.get_title()]['draw_times'].append(0.0)
        if len(ProcessManager.instance._execution_datas[process.get_title()]['draw_times']) > ProcessManager.MAX:
            ProcessManager.instance._execution_datas[process.get_title()]['draw_times'] = \
                ProcessManager.instance._execution_datas[process.get_title()]['draw_times'][::-1][:ProcessManager.MAX][::-1]

    @staticmethod
    def remove_process(i):
        ProcessManager.instance._windows.pop(i)

    @staticmethod
    def set_as_toplevel(i):
        ProcessManager.instance._windows[0:0] = [ProcessManager.instance._windows.pop(i)]
        ProcessManager.windows()[0].state = WStates.ACTIVE

    @staticmethod
    def kill_process(i):
        ProcessManager.instance._windows.pop(i)

    @staticmethod
    def get_first_active():
        for win in ProcessManager.windows():
            if win.state == WStates.ACTIVE:
                return win
        return None

    @staticmethod
    def clock():
        return ProcessManager.instance._clock

    @staticmethod
    def windows():
        return ProcessManager.instance._windows

    @staticmethod
    def windows_ordered_by_date():
        return ProcessManager.instance._adding_order

    @staticmethod
    def add_windows(*news):
        for new in news:
            ProcessManager.windows().append(new)
            ProcessManager.windows_ordered_by_date().append(new)

    @staticmethod
    def get_sizeof_window(index):
        if 0 <= index < len(ProcessManager.windows()):
            return ProcessManager.windows().__sizeof__()
        raise IndexError("Can not acces window at '%i'" % index)

    @staticmethod
    def add_window_and_init(window, *args):
        i = window(*args)
        ProcessManager.windows().append(i)
        ProcessManager.instance._execution_datas[i.get_title()] = {
            'exc_times': [],
            'draw_times': []
        }

    @staticmethod
    def init_windows_with(*args):
        for i, window in enumerate(ProcessManager.windows()):
            ProcessManager.windows()[i] = window(*args)
            ProcessManager.instance._execution_datas[ProcessManager.windows()[i].get_title()] = {
                'exc_times': [],
                'draw_times': []
            }

    @staticmethod
    def reoder_ifalive():
        alives = []
        not_alives = []
        for w in ProcessManager.windows():
            if w.alive():
                alives.append(w)
            else:
                not_alives.append(w)
        ProcessManager.instance._windows = alives + not_alives
