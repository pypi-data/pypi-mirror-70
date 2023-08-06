# hspace_widget.py
#
# This file is part of scqubits.
#
#    Copyright (c) 2019, Jens Koch and Peter Groszkowski
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import functools

import numpy as np

try:
    import ipywidgets
except ImportError:
    _HAS_IPYWIDGETS = False
else:
    _HAS_IPYWIDGETS = True

try:
    from IPython.display import display
except ImportError:
    _HAS_IPYTHON = False
else:
    _HAS_IPYTHON = True

import scqubits
from scqubits.ui.qubit_widget import _HAS_IPYWIDGETS, _HAS_IPYTHON
from scqubits.utils import misc as utils


class HilbertSpaceUi:
    """Class for setup and display of the ipywidget used for creation of a HilbertSpace object."""
    @utils.Required(ipywidgets=_HAS_IPYWIDGETS)
    def __init__(self):
        """Set up all widget GUI elements and class attributes."""
        self.error_output = None
        self.interact_current_index = 0
        self.interact_max_index = 0
        self.subsys_list = []
        self.interact_list = [self.empty_interaction_term()]

        label = ipywidgets.Label(value='HilbertSpace subsys_list')
        self.subsys_widget = ipywidgets.Textarea(placeholder='object name 1\nobject name 2\n...\n(existing  objects)')
        self.subsys_box = ipywidgets.VBox([label, self.subsys_widget])

        self.interact_new_button = ipywidgets.Button(description='New', layout=ipywidgets.Layout(width='80px'))
        self.interact_del_button = ipywidgets.Button(icon='fa-remove', layout=ipywidgets.Layout(width='30px'))
        self.interact_right_button = ipywidgets.Button(icon='arrow-right', layout=ipywidgets.Layout(width='30px'))
        self.interact_left_button = ipywidgets.Button(icon='arrow-left', layout=ipywidgets.Layout(width='30px'))
        self.interact_buttons = ipywidgets.HBox([self.interact_new_button, self.interact_left_button,
                                                 self.interact_right_button, self.interact_del_button])

        self.op1_widget = ipywidgets.Text(description='op1', placeholder='e.g., <object>.n_operator()')
        self.op2_widget = ipywidgets.Text(description='op2', placeholder='e.g., <object>.creation_operator()')
        self.op1subsys_widget = ipywidgets.Text(description='subsys1')
        self.op2subsys_widget = ipywidgets.Text(description='subsys2')
        self.g_widget = ipywidgets.FloatText(description='g_strength')
        self.addhc_widget = ipywidgets.Dropdown(description='add_hc', options=['False', 'True'])

        self.interact_box = ipywidgets.VBox([
            self.interact_buttons,
            self.op1subsys_widget,
            self.op1_widget,
            self.op2subsys_widget,
            self.op2_widget,
            self.g_widget,
            self.addhc_widget
        ])

        self.interact_new_button.on_click(self.new_interaction_term)
        self.interact_del_button.on_click(self.del_interaction_term)
        self.interact_left_button.on_click(self.previous_interaction_term)
        self.interact_right_button.on_click(self.next_interaction_term)

        self.tab_nest = ipywidgets.widgets.Tab()
        self.tab_nest.children = [self.subsys_box, self.interact_box]
        self.tab_nest.set_title(0, 'Subsystems')
        self.tab_nest.set_title(1, 'Interactions')

        # run button is connected externally, see use in create_hilbertspace_widget below
        self.run_button = ipywidgets.Button(description='Finish')

        self.ui = ipywidgets.VBox([self.tab_nest, self.run_button])

    def finish(self, callback_func, *args, **kwargs):
        subsystem_list = self.validated_subsys_list()
        if subsystem_list is False:
            return None
        interaction_list = self.validated_interact_list()
        if interaction_list is False:
            return None

        callback_func(subsystem_list, interaction_list)

    def set_err_output(self, out):
        self.error_output = out

    def set_data(self, **kwargs):
        self.set_subsys_list(kwargs.pop('subsys_list'))
        self.set_interact_term(**kwargs)

    def set_subsys_list(self, str_list):
        self.subsys_list = str_list.split('\n')
        while '' in self.subsys_list:
            self.subsys_list.remove('')

    def set_interact_term(self, **kwargs):
        self.interact_list[self.interact_current_index] = kwargs

    def new_interaction_term(self, *args):
        self.interact_max_index += 1
        self.interact_current_index = self.interact_max_index
        self.interact_list.append(self.empty_interaction_term())
        self.interact_index_change()

    def del_interaction_term(self, *args):
        if len(self.interact_list) == 1:
            self.interact_list[0] = self.empty_interaction_term()
        else:
            del self.interact_list[self.interact_current_index]
        if self.interact_max_index > 0:
            self.interact_max_index -= 1
        if self.interact_current_index > 0:
            self.interact_current_index -= 1
        self.interact_index_change()

    def next_interaction_term(self, *args):
        if self.interact_current_index < self.interact_max_index:
            self.interact_current_index += 1
            self.interact_index_change()

    def previous_interaction_term(self, *args):
        if self.interact_current_index > 0:
            self.interact_current_index -= 1
            self.interact_index_change()

    def interact_index_change(self, *args):
        interact_params = self.interact_list[self.interact_current_index]
        self.op1_widget.value = interact_params['op1']
        self.op1subsys_widget.value = interact_params['subsys1']
        self.op2_widget.value = interact_params['op2']
        self.op2subsys_widget.value = interact_params['subsys2']
        self.g_widget.value = interact_params['g_strength']
        self.addhc_widget.value = interact_params['add_hc']

    @staticmethod
    def empty_interaction_term():
        return {
            'op1': '',
            'subsys1': '',
            'op2': '',
            'subsys2': '',
            'g_strength': 0.0,
            'add_hc': 'False'
        }

    def widgets_dict(self):
        return {
            'subsys_list': self.subsys_widget,
            'op1': self.op1_widget,
            'subsys1': self.op1subsys_widget,
            'op2': self.op2_widget,
            'subsys2': self.op2subsys_widget,
            'g_strength': self.g_widget,
            'add_hc': self.addhc_widget
        }

    def validated_subsys_list(self):
        import importlib
        main = importlib.import_module('__main__')
        import scqubits.core.qubit_base as base

        self.error_output.clear_output()

        subsys_list = []
        for subsys_name in self.subsys_list:
            try:
                instance = getattr(main, subsys_name)
                subsys_list.append(instance)
            except AttributeError:
                with self.error_output:
                    print("Error: name '{}' is not defined.".format(subsys_name))
                return False
            if not isinstance(instance, scqubits.core.qubit_base.QuantumSystem):
                with self.error_output:
                    print("Type mismatch: object '{}' is not a qubit or oscillator.".format(subsys_name))
                return False
        return subsys_list

    def validated_interact_list(self):
        import importlib
        main = importlib.import_module('__main__')

        self.error_output.clear_output()

        interaction_list = []
        for interaction_term in self.interact_list:
            if interaction_term == self.empty_interaction_term():
                continue
            for param_name in ['subsys1', 'subsys2']:
                if interaction_term[param_name] not in self.subsys_list:
                    with self.error_output:
                        print("Error: subsystem operator '{}' is not consistent "
                              "with HilbertSpace subsys_list.".format(interaction_term[param_name]))
                    return False
            for param_name in ['op1', 'op2']:
                operator_str = interaction_term[param_name]
                try:
                    instance = eval(operator_str, main.__dict__)
                except (NameError, SyntaxError):
                    with self.error_output:
                        print("Error: {} '{}' is not defined or has a syntax error.".format(param_name, operator_str))
                    return False
                if not isinstance(instance, np.ndarray):
                    with self.error_output:
                        print("Type mismatch: '{}' is not a valid operator.".format(operator_str))
                    return False
            interaction_list.append(scqubits.InteractionTerm(g_strength=interaction_term['g_strength'],
                                                             op1=eval(interaction_term['op1'], main.__dict__),
                                                             subsys1=eval(interaction_term['subsys1'], main.__dict__),
                                                             op2=eval(interaction_term['op2'], main.__dict__),
                                                             subsys2=eval(interaction_term['subsys2'], main.__dict__),
                                                             add_hc=(interaction_term['add_hc'] == 'True')))
        return interaction_list


@utils.Required(ipywidgets=_HAS_IPYWIDGETS, IPython=_HAS_IPYTHON)
def create_hilbertspace_widget(callback_func):
    """
    Display ipywidgets interface for creating a HilbertSpace object. Typically, this function will be called by
    `HilbertSpace.create()``.


    Parameters
    ----------
    callback_func: function
        Function that receives the subsystem and interaction data from the widget. Typically, this is
        ``HilbertSpace.__init__()``
    """
    ui_view = HilbertSpaceUi()

    out = ipywidgets.interactive_output(
        ui_view.set_data,
        ui_view.widgets_dict()
    )
    finish_func = functools.partial(ui_view.finish, callback_func)
    ui_view.run_button.on_click(finish_func)

    ui_view.set_err_output(out)
    display(ui_view.ui, out)
