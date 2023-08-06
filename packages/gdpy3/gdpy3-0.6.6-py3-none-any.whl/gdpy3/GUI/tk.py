# -*- coding: utf-8 -*-

# Copyright (c) 2020 shmilee

import os
import time
import numpy
import tempfile
import getpass
import tkinter
import screeninfo
from tkinter import ttk, simpledialog, filedialog, messagebox
from tkinter.constants import *
from distutils.version import LooseVersion

from ..__about__ import __data_path__, __icon_name__, __gversion__
from ..glogger import getGLogger
from ..processors import get_processor, Processor_Names

__all__ = ['GTkApp']
log = getGLogger('G')


class GTkApp(object):
    '''
    GUI(Graphical User Interface) made by tkinter.
    '''
    recent = os.path.join(
        tempfile.gettempdir(), 'gdpy3-%s-recent' % getpass.getuser())

    def __init__(self, path=None, ask_sftp=False):
        '''
        Parameters
        ----------
        path: str
            case path, default ''
        ask_sftp: bool
            if no path given, ask for a sftp(not local) path, default False
        '''
        root = tkinter.Tk(className='gdpy3-gui')
        img = tkinter.PhotoImage(file=os.path.join(
            __data_path__, 'icon', '%s.gif' % __icon_name__))
        root.tk.call('wm', 'iconphoto', root._w, "-default", img)
        root.protocol("WM_DELETE_WINDOW", self.close_app)
        style = ttk.Style()
        font = ('Microsoft YaHei', 10)
        width = 0
        style.configure('.', font=font)
        main = ttk.Frame(root, relief=RIDGE, borderwidth=2)
        main.pack(fill=BOTH, expand=1)
        log.debug('Main frame packed.')
        # 1
        w_frame_proc = ttk.Labelframe(main, text='1. Processor:', width=width)
        w_str_path = tkinter.StringVar(value='')  # default path ''
        w_str_path.trace("w", self.save_case_path)
        w_entry_path = ttk.Entry(
            w_frame_proc, font=font, textvariable=w_str_path)
        w_entry_path.grid(in_=w_frame_proc, row=0, column=0, padx=5, pady=5,
                          sticky=W+E)
        w_path = ttk.Button(
            w_frame_proc, text='Path', width=0, command=self.ask_case_path)
        w_path.grid(in_=w_frame_proc, row=0, column=1, padx=5, pady=5)
        w_str_proc = tkinter.StringVar()
        w_select_proc = ttk.Combobox(
            w_frame_proc, values=Processor_Names, font=font,
            textvariable=w_str_proc, state='readonly')
        w_str_proc.set(Processor_Names[0])
        w_select_proc.grid(in_=w_frame_proc, row=1, column=0, padx=5, pady=5)
        w_pick = ttk.Button(
            w_frame_proc, text="Pick", width=0, command=self.after_pick)
        w_pick.grid(in_=w_frame_proc, row=1, column=1, padx=5, pady=5)
        w_frame_proc.grid(row=0, column=0, padx=10, pady=5, sticky=W+E)
        # 2
        w_frame_fig = ttk.Labelframe(main, text='2. Figure:', width=width)
        w_str_filter = tkinter.StringVar(value='^.*/.*$')
        w_entry_filter = ttk.Entry(
            w_frame_fig, font=font, textvariable=w_str_filter)
        w_entry_filter.grid(in_=w_frame_fig, row=0, column=0, padx=5, pady=5)
        w_filter = ttk.Button(
            w_frame_fig, text='Filter', width=0, command=self.after_filter)
        w_filter.grid(in_=w_frame_fig, row=0, column=1, padx=5, pady=5)
        w_list_fig = tkinter.Variable(value=[])
        w_listbox_fig = tkinter.Listbox(
            w_frame_fig, selectmode=SINGLE, exportselection=0, font=font,
            listvariable=w_list_fig, state='normal')
        w_scrollbar_fig = ttk.Scrollbar(
            w_frame_fig, orient="vertical", command=w_listbox_fig.yview)
        w_listbox_fig.config(yscrollcommand=w_scrollbar_fig.set)
        w_listbox_fig.grid(in_=w_frame_fig, row=1, columnspan=2,
                           sticky=W+E, padx=5, pady=5)
        w_scrollbar_fig.grid(in_=w_frame_fig, row=1, column=1,
                             sticky=E+N+S, padx=5, pady=5)
        w_frame_fig.grid(row=1, column=0, padx=10, pady=5, sticky=W+E)
        # 3
        w_frame_panel = ttk.Labelframe(main, text='3. Panel:', width=width)
        # 3 - VerticalScrolledFrame
        w_kw_out_frame = ttk.Frame(w_frame_panel)
        w_kw_scrollbar = ttk.Scrollbar(w_kw_out_frame, orient=VERTICAL)
        w_kw_scrollbar.pack(fill=Y, side=RIGHT, expand=0)
        w_kw_canvas = tkinter.Canvas(
            w_kw_out_frame, bd=0, highlightthickness=0,
            yscrollcommand=w_kw_scrollbar.set, width=0, height=160)
        w_kw_canvas.pack(side=LEFT, fill=BOTH, anchor=W, expand=1)
        w_kw_scrollbar.config(command=w_kw_canvas.yview)
        w_kw_canvas.xview_moveto(0)
        w_kw_canvas.yview_moveto(0)
        w_kw_in_frame = ttk.Frame(w_kw_canvas)
        w_kw_canvas.create_window(0, 0, window=w_kw_in_frame, anchor=NW)

        def _configure_canvas_interiorframe(event):
            w_kw_canvas.update_idletasks()
            w_kw_canvas.configure(scrollregion=w_kw_canvas.bbox("all"))
        w_kw_in_frame.bind('<Configure>', _configure_canvas_interiorframe)

        def _on_mousewheel(event):
            number = 0
            # Linux wheel event: event.delta = 0, event.num = 4 or 5
            # Windows wheel event: event.delta = -120 or 120 ?
            if event.num == 5 or event.delta == -120:
                number = 1  # down
            if event.num == 4 or event.delta == 120:
                number = -1  # up
            log.debug('Wheel event: num %d, delta %d -> %d'
                      % (event.num, event.delta, number))
            w_kw_canvas.yview_scroll(number, "units")
        w_kw_canvas.bind("<MouseWheel>", _on_mousewheel)
        w_kw_canvas.bind("<Button-4>", _on_mousewheel)
        w_kw_canvas.bind("<Button-5>", _on_mousewheel)
        w_kw_in_frame.bind("<MouseWheel>", _on_mousewheel)
        w_kw_in_frame.bind("<Button-4>", _on_mousewheel)
        w_kw_in_frame.bind("<Button-5>", _on_mousewheel)
        w_kw_out_frame.pack(in_=w_frame_panel, side=TOP,
                            expand=1, fill=X, padx=5, pady=5)
        w_plot = ttk.Button(
            w_frame_panel, text='Plot', width=8, command=self.after_plot)
        w_plot.pack(in_=w_frame_panel, side=BOTTOM, anchor=E, padx=5, pady=5)
        w_frame_panel.grid(row=2, column=0, padx=10, pady=5, sticky=W+E)
        # 4 - bottom
        version_text = "Version %s" % __gversion__
        w_info = tkinter.Label(
            main, relief=RIDGE, borderwidth=1, anchor=CENTER,
            font=(font[0], 8), text="%s\t© %s shmilee\t" % (
                                    version_text, time.strftime('%Y')))
        w_info.grid(row=3, column=0, sticky=W+E)
        log.debug('Main frame filled.')
        # X - for share
        self.root = root
        try:
            monitors = screeninfo.get_monitors()
            monitor = sorted(monitors, key=lambda m: m.width, reverse=True)[0]
        except Exception:
            log.debug('No active monitors found!')
            monitor = None
        self.monitor = monitor
        self.center(root)
        self.img = img
        self.processor_name = w_str_proc
        self.figlabel_filter = w_str_filter
        self.figlabels = w_list_fig
        self.figlistbox = w_listbox_fig
        self.figkwframe = w_kw_in_frame
        self.pathlabel = w_str_path
        self.ask_sftp = ask_sftp
        # cache processor instances, key (type(processor).__name__, self.path)
        self.cache_processors = {}
        self.processor = None
        # cache all figure kwargs widgets of different processors
        # key [processor.name-processor.saltstr][figlabel]
        self.cache_figkwslib = {}
        self.figkws = {}  # kwargs widgets mapped in panel
        # cache all plotted figure windows of different processors
        # key of window: [processor.name-processor.saltstr][accfiglabel]
        self.cache_figwindows = {}
        self.next_figwindow_index = 0
        # X - events
        w_select_proc.bind("<<ComboboxSelected>>", self.after_processor_name)
        w_entry_filter.bind("<Return>", self.after_filter)
        w_listbox_fig.bind("<<ListboxSelect>>", self.after_figlabel)
        # X - start
        if path:
            self.path = path
            self.save_case_path()
        else:
            if self.ask_sftp:
                self.ask_case_path(N=2)
            else:
                self.ask_case_path(N=1)
        self.root.title('gdpy3 - %s' % self.path)
        if monitor:
            log.info('Start Tk mainloop on monitor %s.' % monitor.name)
        else:
            log.info('Start Tk mainloop.')
        self.root.mainloop()

    def close_app(self):
        # close and destroy all fig windows
        for key in self.cache_figwindows.keys():
            log.debug('Destroy figure windows of %s' % key)
            for n, w in self.cache_figwindows[key].items():
                log.debug('Destroy window: %s' % n)
                w.destroy()
        # close root window
        log.debug('Destroy root window.')
        self.root.destroy()
        log.info('Quit, bye!')
        self.root.quit()

    def _get_path(self):
        return self.pathlabel.get()

    def _set_path(self, path):
        self.pathlabel.set(path)

    path = property(_get_path, _set_path)

    def center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        if self.monitor:
            x = self.monitor.x + (self.monitor.width // 2) - (width // 2)
            y = self.monitor.y + (self.monitor.height // 2) - (height // 2)
        else:
            x = (win.winfo_screenwidth() // 2) - (width // 2)
            y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def ask_case_path(self, N=1):
        if self.ask_sftp:
            for _ in range(N):
                path = simpledialog.askstring(
                    "Input sftp path",
                    "Directory in SSH server, format: "
                    "'sftp://username@host[:port]##remote/path'",
                    initialvalue='sftp://',
                    parent=self.root)
                if path:
                    self.path = path
                    return
        else:
            initialdir = None
            if os.path.isfile(self.recent):
                # read, get valid recent initialdir
                try:
                    with open(self.recent, 'r', encoding='utf-8') as rf:
                        old_dir = os.path.dirname(rf.readline())
                        for _ in range(N * 2):
                            if os.path.isdir(old_dir):
                                initialdir = old_dir
                                break
                            else:
                                old_dir = os.path.dirname(old_dir)
                except Exception:
                    log.debug('Error of getting initialdir.', exc_info=1)
            for _ in range(N):
                path = filedialog.askopenfilename(
                    parent=self.root, initialdir=initialdir)
                if path:
                    self.path = path
                    self.save_case_path()
                    return

    def save_case_path(self, *args):
        if self.path and not self.path.startswith('sftp://'):
            try:
                with open(self.recent, 'w', encoding='utf-8') as rf:
                    rf.write(self.path)
            except Exception:
                log.debug('Error of saving recent path.', exc_info=1)

    def reset_panel(self):
        for n, w in self.figkws.items():
            w.grid_forget()
            w.pack_forget()
            w.place_forget()
        self.figkws = {}

    def close_figwindows(self, processor):
        key = '%s-%s' % (processor.name, processor.saltstr)
        if key in self.cache_figwindows:
            log.debug('Hide figure windows of %s' % key)
            for n, w in self.cache_figwindows[key].items():
                log.debug('Hide window: %s' % n)
                w.wm_withdraw()

    def after_pick(self):
        if self.processor_name.get():
            gdpcls = get_processor(name=self.processor_name.get())
            if self.path.startswith('sftp://'):
                def _passwd_CALLBACK(prompt):
                    return simpledialog.askstring(
                        "Input Password", prompt, show='*', parent=self.root)
                from ..getpasswd import GetPasswd
                GetPasswd.CALLBACK = _passwd_CALLBACK
            if self.path.endswith(gdpcls.saltname):
                self.path = self.path[:-len(gdpcls.saltname)]
            # close and hide old fig windows
            if self.processor:
                self.close_figwindows(self.processor)
            key = (gdpcls.__name__, self.path)
            if key in self.cache_processors:
                gdp = self.cache_processors[key]
            else:
                gdp = gdpcls(self.path)
            self.root.title('gdpy3 - %s' % self.path)
            if gdp.pckloader:
                log.debug('Set processor for %s' % self.path)
                self.processor = gdp
                if key not in self.cache_processors:
                    self.cache_processors[key] = gdp
                self.figlabel_filter.set('^.*/.*$')
                self.figlabels.set(gdp.availablelabels)
                self.figlistbox.selection_clear(0, END)
                # reset panel, hide kw widgets
                self.reset_panel()
            else:
                messagebox.showerror(message='Failed to get processor!')
        else:
            messagebox.showwarning(message='Select processor first!')

    def after_filter(self, *args):
        if self.processor:
            self.figlabels.set(self.processor.refind(
                self.figlabel_filter.get()))
            self.figlistbox.selection_clear(0, END)
            # reset panel
            self.reset_panel()
        else:
            messagebox.showwarning(message='Pick processor first!')

    def after_plot(self):
        if not self.figlistbox.curselection():
            messagebox.showwarning(message='Select a figure first!')
            return
        if not self.processor.visplter.name.startswith('mpl::'):
            messagebox.showerror(message='%s not supported with Tk!'
                                 % self.processor.plotter.name)
            return
        figlabel = self.figlabels.get()[self.figlistbox.curselection()[0]]
        figkwargs = {k: v.value for k, v in self.figkws.items()}
        log.debug('Collect figkwargs: %s' % figkwargs)
        accfiglabel = self.processor.visplt(figlabel, show=False, **figkwargs)
        if accfiglabel in self.processor.visplter.figures:
            figure = self.processor.visplter.get_figure(accfiglabel)
        else:
            messagebox.showerror(message='Failed to get figure object!')
            return
        key = '%s-%s' % (self.processor.name, self.processor.saltstr)
        if key not in self.cache_figwindows:
            self.cache_figwindows[key] = {}
        if accfiglabel in self.cache_figwindows[key]:
            log.debug('Raise old figure window.')
            self.cache_figwindows[key][accfiglabel].wm_deiconify()
        else:
            log.debug('Get new figure window.')
            index = self.next_figwindow_index
            self.next_figwindow_index += 1
            self.cache_figwindows[key][accfiglabel] = MplFigWindow(
                figure, accfiglabel, index, self, class_='gdpy3-gui')

    def after_processor_name(self, event):
        self.figlabel_filter.set('^.*/.*$')
        self.figlabels.set([])
        self.figlistbox.selection_clear(0, END)
        # reset panel
        self.reset_panel()
        # close fig windows
        if self.processor:
            self.close_figwindows(self.processor)

    def get_figkws_widgets(self, options):
        controls = {}
        for k, v in options.items():
            if v['widget'] in (
                    'IntSlider', 'FloatSlider',
                    'IntRangeSlider', 'FloatRangeSlider'):
                # width = 8 if v['widget'].startswith('Float') else 0
                controls[k] = LabeledSpinBoxs(
                    self.figkwframe,
                    v['description'],
                    v['rangee'],
                    v['value'],
                    state='readonly', width=0)
            elif v['widget'] in ('Dropdown', 'SelectMultiple'):
                controls[k] = LabeledListbox(
                    self.figkwframe,
                    v['description'],
                    v['options'],
                    v['value'],
                    width=0, height=0)
            elif v['widget'] in ('Checkbox',):
                controls[k] = Checkbox(
                    self.figkwframe,
                    v['description'],
                    v['value'])
            else:
                pass
        return controls

    def after_figlabel(self, event):
        if self.figlistbox.curselection():
            figlabel = self.figlabels.get()[self.figlistbox.curselection()[0]]
            # update panel
            self.reset_panel()
            key = '%s-%s' % (self.processor.name, self.processor.saltstr)
            if key not in self.cache_figkwslib:
                self.cache_figkwslib[key] = {}
            if figlabel in self.cache_figkwslib[key]:
                log.debug("Use old widgets")
                self.figkws = self.cache_figkwslib[key][figlabel]
            else:
                log.debug("Gen new widgets")
                result = self.processor.export(figlabel, what='options')
                options = dict(**result['digoptions'], **result['visoptions'])
                if options:
                    self.figkws = self.get_figkws_widgets(options)
                else:
                    self.figkws = {}
                self.cache_figkwslib[key][figlabel] = self.figkws
            for n, w in self.figkws.items():
                w.pack(anchor=W, padx=5, pady=5)


class LabeledSpinBoxs(ttk.Frame):
    '''
    Spinbox widgets with a Label widget indicating their description.

    Parameters
    ----------
    desc: str
        description
    rangee: tuple
        (from_, to, step)
    init_val: one or more int or float numbers
        initial value, num or [num1, num2, ...]
        If N>1 numbers given, N Spinboxs will be generated.
    cnf, kw: options for Spinbox
    '''

    def __init__(self, master, desc, rangee, init_val=None, cnf={}, **kw):
        super(LabeledSpinBoxs, self).__init__(master, borderwidth=1)
        self.label = ttk.Label(self, text=desc)
        from_, to, step = rangee
        for _k in ['from_', 'to', 'textvariable']:
            _ignore = kw.pop(_k, None)
        if init_val is None:
            init_val = from_
        if isinstance(init_val, (int, float, numpy.number)):
            init_val = [init_val]
        self.variables = []
        self.spinboxs = []
        for i_val in init_val:
            if (isinstance(step, (int, numpy.integer))
                    and isinstance(i_val, (int, numpy.integer))):
                self.variables.append(tkinter.IntVar(self))
            elif (isinstance(step, (float, numpy.floating))
                    and isinstance(i_val, (float, numpy.floating))):
                self.variables.append(tkinter.DoubleVar(self))
            else:
                log.error('type error: var %s, step %s ' %
                          (type(i_val), type(step)))
                raise ValueError("Only int, float number supported!")
            self.variables[-1].set(i_val)
            self.spinboxs.append(tkinter.Spinbox(
                self, cnf=cnf,
                from_=from_, to=to, increment=step,
                textvariable=self.variables[-1], **kw))
        # arrange in line
        self.label.pack(side=LEFT, padx=2)
        for sb in self.spinboxs:
            sb.pack(side=LEFT, padx=2)

    @property
    def value(self):
        if len(self.variables) == 1:
            return self.variables[0].get()
        else:
            return [v.get() for v in self.variables]


class LabeledListbox(ttk.Frame):
    '''
    A Listbox widget with a Label widget indicating its description.

    Parameters
    ----------
    desc: str
        description
    items: list
        items to select
    init_val: initial value, default None
        If init_val is list, selectmode of Listbox will be MULTIPLE,
        otherwise, SINGLE.
    cnf, kw: options for Listbox
    '''

    def __init__(self, master, desc, items, init_val=None, cnf={}, **kw):
        super(LabeledListbox, self).__init__(master, borderwidth=1)
        self.label = ttk.Label(self, text=desc)
        self.label.pack(side=LEFT, anchor=NW, padx=2)
        self._variable = tkinter.Variable(self, value=items)
        for _k in ['listvariable', 'exportselection', 'selectmode']:
            _ignore = kw.pop(_k, None)
        if isinstance(init_val, list):
            self._selectmode = MULTIPLE
        else:
            self._selectmode = SINGLE
        self.listbox = tkinter.Listbox(
            self, cnf={}, listvariable=self._variable,
            exportselection=0, selectmode=self._selectmode, **kw)
        self.listbox.selection_clear(0, END)
        if init_val:
            if not isinstance(init_val, list):
                init_val = [init_val]
            for i_val in init_val:
                if i_val in items:
                    self.listbox.selection_set(items.index(i_val))
        self.listbox.pack(side=LEFT, padx=2)

    @property
    def value(self):
        items = self._variable.get()
        selection = self.listbox.curselection()
        if self._selectmode == MULTIPLE:
            return [items[i] for i in selection]
        else:
            return items[selection[0]]


class Checkbox(ttk.Checkbutton):
    '''Ttk Checkbutton widget, add w.value support.'''

    def __init__(self, master, desc, init_val=False, **kw):
        self._variable = tkinter.BooleanVar(master, value=init_val)
        for _k in ['offvalue', 'onvalue', 'text', 'variable']:
            _ignore = kw.pop(_k, None)
        super(Checkbox, self).__init__(
            master, offvalue=False, onvalue=True,
            text=desc, variable=self._variable, **kw)

    @property
    def value(self):
        return self._variable.get()


class MplFigWindow(tkinter.Toplevel):
    '''Embed a Matplotlib figure to Tkinter GUI.'''

    def __init__(self, fig, figlabel, index, app, cnf={}, **kw):
        super(MplFigWindow, self).__init__(master=app.root, cnf=cnf, **kw)
        self.title('%s - %d - %s' % (figlabel, index, app.path))
        self.protocol("WM_DELETE_WINDOW", self.wm_withdraw)

        import matplotlib
        # matplotlib.use('TkAgg', warn=False, force=True)
        import matplotlib.backends.backend_tkagg as tkagg
        if LooseVersion(matplotlib.__version__) <= LooseVersion('2.1.2'):
            log.debug('Recommand matplotlib>=2.2.0')
            tkagg.NavigationToolbar2Tk = tkagg.NavigationToolbar2TkAgg

        self.figure_label = figlabel
        self.figure_backend = tkagg
        self.figure_canvas = None
        self.figure_toolbar = None
        self.figure_update(fig)
        self.left_right(app.monitor, right=index % 2)

    def left_right(self, monitor, right=1):
        if monitor:
            width = int(0.45 * monitor.width)
            height = int(0.8 * monitor.height)
            x = monitor.x + int(0.05 * monitor.width) + right * width
            y = monitor.y + int(0.1 * monitor.height)
        else:
            width = int(0.45 * self.winfo_screenwidth())
            height = int(0.8 * self.winfo_screenheight())
            x = int(0.05 * self.winfo_screenwidth()) + right * width
            y = int(0.1 * self.winfo_screenheight())
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def figure_on_key_event(self, event):
        from matplotlib.backend_bases import key_press_handler
        key_press_handler(event, self.figure_canvas, self.figure_toolbar)

    def figure_update(self, fig):
        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()
        if self.figure_toolbar:
            self.figure_toolbar.destroy()
        if fig:
            canvas = self.figure_backend.FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            toolbar = self.figure_backend.NavigationToolbar2Tk(canvas, self)
            toolbar.update()
            canvas.mpl_connect('key_press_event', self.figure_on_key_event)
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            # toolbar.pack()
            self.figure_canvas = canvas
            self.figure_toolbar = toolbar

            # monkey patch default filename
            # see: FigureCanvasBase.get_default_filename()
            #      FigureCanvasBase.get_window_title()
            label = self.figure_label.replace('/', '-').replace(':', '_')
            tstr = time.strftime('%Y%m%d')
            canvas.get_window_title = lambda: '%s-%s' % (label, tstr)
        else:
            self.figure_canvas = None
            self.figure_toolbar = None
