from .utils import *
import time


class ProcessManager:
    MAX = 10
    ID = 0
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
    def access_window(name, func_name, *args):
        name = "[%s]" % name
        for i, win in enumerate(ProcessManager.windows()):
            if win.get_title()[:len(name)] == name:
                if win.state in (WStates.ACTIVE, WStates.NOT_RESPONDING):
                    win.state = WStates.ACTIVE
                ProcessManager.set_as_toplevel(i)
                if hasattr(win, func_name):
                    return getattr(win, func_name)(*args)
                return -1
        return -1

    @staticmethod
    def session():
        return ProcessManager.instance._current_session

    @staticmethod
    def set_session(name):
        ProcessManager.instance._current_session = name

    @staticmethod
    def execution_datas():
        return ProcessManager.instance._execution_datas

    @staticmethod
    def update_process(process):
        if process.state not in (WStates.UNACTIVE, WStates.NOT_RESPONDING):
            start = time.time()
            process.update()
            try:
                ProcessManager.instance._execution_datas[process.id]['exc_times'].append((time.time() - start) * 1000)
            except Exception:
                process.state = WStates.NOT_RESPONDING
                print(process.get_title(), "a planté")
        else:
            ProcessManager.instance._execution_datas[process.id]['draw_times'].append(0.0)
        if len(ProcessManager.instance._execution_datas[process.id]['exc_times']) > ProcessManager.MAX:
            ProcessManager.instance._execution_datas[process.id]['exc_times'] = \
                ProcessManager.instance._execution_datas[process.id]['exc_times'][::-1][:ProcessManager.MAX][::-1]

    @staticmethod
    def draw_process(process, *args):
        if process.state not in (WStates.UNACTIVE, WStates.NOT_RESPONDING):
            start = time.time()
            process.draw(*args)
            try:
                ProcessManager.instance._execution_datas[process.id]['draw_times'].append((time.time() - start) * 1000)
            except Exception:
                process.state = WStates.NOT_RESPONDING
                print(process.get_title(), "a planté")
        else:
            ProcessManager.instance._execution_datas[process.id]['draw_times'].append(0.0)
        if len(ProcessManager.instance._execution_datas[process.id]['draw_times']) > ProcessManager.MAX:
            ProcessManager.instance._execution_datas[process.id]['draw_times'] = \
                ProcessManager.instance._execution_datas[process.id]['draw_times'][::-1][:ProcessManager.MAX][::-1]

    @staticmethod
    def remove_process(i):
        ProcessManager.windows()[i].state = WStates.UNACTIVE

    @staticmethod
    def set_as_toplevel(i):
        ProcessManager.instance._windows[0:0] = [ProcessManager.instance._windows.pop(i)]
        ProcessManager.windows()[0].state = WStates.ACTIVE

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
        i.id = ProcessManager.ID
        ProcessManager.instance._execution_datas[i.id] = {
            'exc_times': [],
            'draw_times': []
        }
        ProcessManager.ID += 1

    @staticmethod
    def init_windows_with(*args):
        for i, window in enumerate(ProcessManager.windows()):
            ProcessManager.windows()[i] = window(*args)
            ProcessManager.windows()[i].id = ProcessManager.ID
            ProcessManager.instance._execution_datas[ProcessManager.windows()[i].id] = {
                'exc_times': [],
                'draw_times': []
            }
            ProcessManager.ID += 1

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
