import os
import sys
import configparser

import h5py
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt


class Pogger():
    def __init__(self, pogger_path=None, verbose=False):
        self._is_verbose = verbose
        self._path = pogger_path
        self._initialise_context()
        self._initialise_paths()
        self._initialise_printer()
        self._initialise_h5()
        self._initialise_figures()

        if self._is_verbose:
            print("Logging initialised")

    def _initialise_paths(self):
        # Read user config file to get archive path
        if self._path is None:
            self._config_path_dir = os.path.expanduser("~")
            self._config_path_dir += "/.config/pogger/"
            if not os.path.exists(self._config_path_dir):
                os.makedirs(self._config_path_dir)
            self._config_path = self._config_path_dir + "pogger.conf"
            if os.path.exists(self._config_path):
                config = configparser.ConfigParser()
                config.read(self._config_path)
                if "path" in config:
                    if "archive" in config["path"]:
                        self._path = \
                            os.path.expanduser(config["path"]["archive"])
                        if self._path[-1] != "/":
                            self._path += "/"

        # If config isn't there, then set a default path
        if self._path is None:
            self._path = os.path.expanduser("~")
            self._path += "/pogger_archives/"

        # Script name
        self._python_name = __name__
        self._path += self._python_name + "/"

        # Timestamp
        self._datetime = dt.datetime.now()
        self._datetime_string = dt.datetime.strftime(
            self._datetime,
            "%Y-%m-%dT%H-%M-%S"
        )
        self._datetime_path = dt.datetime.strftime(
            self._datetime,
            "%Y/%m/%d/%H-%M-%S/"
        )
        self._path_dir = self._path + self._datetime_path
        self._path_full = self._path_dir \
            + self._datetime_string + "_" + self._python_name
        if not os.path.exists(self._path_dir):
            os.makedirs(self._path_dir)

    def record(self, result_names, result_units=None):
        def write_result(result, result_name, result_unit=None):
            if result is None:
                return
            elif type(result) is tuple:
                for result_index, result_value in enumerate(result):
                    result_name_value = result_name[result_index]
                    if result_unit is None:
                        result_unit_value = None
                    else:
                        result_unit_value = result_unit[result_index]

                    write_result(
                        result_value,
                        result_name_value,
                        result_unit_value
                    )
            elif isinstance(result, np.ndarray):
                self.write_array(result_name, result, result_unit)
            else:
                self.write_value(result_name, result, result_unit)

        def wrapper(function: callable):
            def wrapped(*arguments, **keyword_arguments):
                try:
                    results = function(*arguments, **keyword_arguments)
                except Exception as exception:
                    results = None
                    raise exception
                finally:
                    write_result(results, result_names, result_units)

                    figure_numbers = plt.get_fignums()
                    figure_labels = plt.get_figlabels()
                    for figure_number, figure_label in \
                            zip(figure_numbers, figure_labels):
                        if figure_number not in self._plotted_figures:
                            plt.figure(figure_number)
                            plt.savefig(
                                self._figure_path
                                + self.get_context().replace("/", "_")
                                + "_" + figure_label + ".png")
                            plt.savefig(
                                self._figure_path
                                + self.get_context().replace("/", "_")
                                + "_" + figure_label + ".pdf")
                            self._plotted_figures.append(figure_number)
                            if self._is_verbose:
                                print(
                                    "Figure written to",
                                    self.get_context().replace("/", "_")
                                    + "_" + figure_label)
                return results
            return wrapped
        return wrapper

    def _initialise_figures(self):
        self._figure_path_dir = self._path_dir + "figures/"
        if not os.path.exists(self._figure_path_dir):
            os.makedirs(self._figure_path_dir)
        self._figure_path = self._figure_path_dir \
            + self._datetime_string + "_" + self._python_name + "_"

        self._plotted_figures = []

    def _initialise_h5(self):
        self._path_h5 = self._path_full + ".h5"
        with h5py.File(self._path_h5, "w"):
            pass

    def _initialise_context(self):
        self.set_context()

    def _initialise_printer(self):
        self._normal_out = sys.stdout
        self._normal_error_out = sys.stderr
        self._log_out_path = self._path_full + ".log"
        self._printer = Printer(self._normal_out, self._log_out_path)
        sys.stdout = self._printer
        sys.stderr = self._printer

    def set_context(self, context=None):
        if context is None:
            self._context = ""
        self._context = context

    def get_context(self):
        return self._context

    def write_array(self, path, array, units=None):
        path_full = "data/" + self._context + "/" + path
        path_split = path_full.split("/")
        with h5py.File(self._path_h5, "a") as file_h5:
            path_dir = ""
            for dir_index in range(1, len(path_split) - 1):
                path_dir += path_split[dir_index] + "/"
                file_h5.require_group(path_dir[:-1])

            file_h5[path_full] = array
            if units is not None:
                file_h5[path_full].attrs["_units"] = units
        if self._is_verbose:
            print("Array written to hdf5 path", path_full)

    def write_value(self, path, value, units=None):
        path_full = "data/" + self._context + "/" + path
        path_split = path_full.split("/")
        with h5py.File(self._path_h5, "a") as file_h5:
            path_dir = ""
            for dir_index in range(0, len(path_split) - 1):
                path_dir += path_split[dir_index] + "/"
                file_h5.require_group(path_dir[:-1])
            file_h5[path_dir].attrs[path_split[-1]] = value
            if units is not None:
                file_h5[path_dir].attrs[path_split[-1] + "_units"] = units
        if self._is_verbose:
            print("Value written to hdf5 path", path_full)


class Printer:
    def __init__(self, normal_out, log_out_path: str):
        self._normal_out = normal_out
        self._log_out_path = log_out_path
        with open(self._log_out_path, "w"):
            pass

    def write(self, *arguments, **keyword_arguments):
        self._normal_out.write(*arguments, **keyword_arguments)
        with open(self._log_out_path, "a") as log_file:
            log_file.write(*arguments, **keyword_arguments)

    def flush(self, *arguments, **keyword_arguments):
        self._normal_out.flush(*arguments, **keyword_arguments)
        with open(self._log_out_path, "a") as log_file:
            log_file.flush(*arguments, **keyword_arguments)
