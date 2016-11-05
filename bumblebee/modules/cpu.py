import bumblebee.module
import psutil

def usage():
    return "cpu"

def notes():
    return "Warning is at 70%, Critical at 80%."

def description():
    return "Displays CPU utilization across all CPUs."

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._perc = psutil.cpu_percent(percpu=False)

        output.add_callback(module=self.instance(), button=1, cmd="gnome-system-monitor")

    def widgets(self):
        self._perc = psutil.cpu_percent(percpu=False)
        return bumblebee.output.Widget(self, "{:05.02f}%".format(self._perc))

    def warning(self, widget):
        return self._perc > self._config.parameter("warning", 70)

    def critical(self, widget):
        return self._perc > self._config.parameter("critical", 80)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
