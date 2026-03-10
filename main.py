import json
import math
import os
import calendar
from datetime import datetime, date, timedelta

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

ARCHIVO = "horas_servicio_ashlee.json"
NOMBRE_ALUMNA = ""
NOMBRE_CORTO = "Ashlee"


KV = """
#:import dp kivy.metrics.dp

<SoftCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(14)
    spacing: dp(8)
    size_hint_y: None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [22, 22, 22, 22]

<TitleText@Label>:
    color: .10, .22, .40, 1
    bold: True
    font_size: "20sp"
    size_hint_y: None
    height: self.texture_size[1]

<SubTitleText@Label>:
    color: .10, .22, .40, 1
    bold: True
    font_size: "16sp"
    size_hint_y: None
    height: self.texture_size[1]

<MutedText@Label>:
    color: .35, .40, .48, 1
    font_size: "13sp"
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None

<StatValue@Label>:
    color: .08, .16, .27, 1
    bold: True
    font_size: "22sp"
    size_hint_y: None
    height: self.texture_size[1]

<PrimaryBtn@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    bold: True
    size_hint_y: None
    height: dp(46)
    canvas.before:
        Color:
            rgba: .16, .43, .89, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16, 16, 16, 16]

<SecondaryBtn@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: .14, .22, .36, 1
    bold: True
    size_hint_y: None
    height: dp(44)
    canvas.before:
        Color:
            rgba: .91, .95, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16, 16, 16, 16]

<DayCellButton>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: self.fg_color
    bold: self.is_selected
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [14, 14, 14, 14]
        Color:
            rgba: self.dot_color
        Ellipse:
            size: dp(6), dp(6)
            pos: self.center_x - dp(3), self.y + dp(4)

BoxLayout:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: .94, .96, .99, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(68)
        padding: dp(12), dp(10)
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: .06, .16, .29, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Button:
            text: "Menú"
            size_hint_x: None
            width: dp(84)
            background_normal: ""
            background_down: ""
            background_color: 0, 0, 0, 0
            color: 1, 1, 1, 1
            bold: True
            canvas.before:
                Color:
                    rgba: .20, .32, .50, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [16, 16, 16, 16]
            on_release: app.open_menu()

        Label:
            text: "Servicio Social"
            color: 1, 1, 1, 1
            bold: True
            font_size: "20sp"
            halign: "left"
            valign: "middle"
            text_size: self.size

        Label:
            text: app.nombre_corto
            color: .86, .91, 1, 1
            bold: True
            font_size: "16sp"
            size_hint_x: None
            width: dp(90)
            halign: "right"
            valign: "middle"
            text_size: self.size

    ScrollView:
        do_scroll_x: False

        BoxLayout:
            id: main_box
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(10)

            SoftCard:
                spacing: dp(6)

                TitleText:
                    text: "Control de horas"

                MutedText:
                    text: app.nombre_alumna
                    bold: True

            SoftCard:
                spacing: dp(12)

                BoxLayout:
                    size_hint_y: None
                    height: dp(180)
                    spacing: dp(12)

                    ProgressRing:
                        id: ring
                        size_hint: None, None
                        size: dp(170), dp(170)

                    BoxLayout:
                        orientation: "vertical"
                        spacing: dp(6)

                        SubTitleText:
                            text: "Resumen"

                        MutedText:
                            text: "Objetivo total"
                        StatValue:
                            id: lbl_obj
                            text: "0.00 h"

                        MutedText:
                            text: "Acumulado"
                        StatValue:
                            id: lbl_acu
                            text: "0.00 h"

                        MutedText:
                            text: "Faltan"
                        StatValue:
                            id: lbl_fal
                            text: "0.00 h"

                MutedText:
                    id: lbl_jornadas
                    text: "Jornadas de 8h: 0.00"

                MutedText:
                    id: lbl_prom
                    text: "Promedio reciente: 0.00 h"

                MutedText:
                    id: lbl_est
                    text: "Fecha estimada de término: Sin datos suficientes"

            SoftCard:
                spacing: dp(10)

                BoxLayout:
                    size_hint_y: None
                    height: dp(34)

                    SubTitleText:
                        id: lbl_mes
                        text: "Calendario"

                    Button:
                        text: "<"
                        size_hint_x: None
                        width: dp(42)
                        background_normal: ""
                        background_color: 0, 0, 0, 0
                        color: .15, .22, .35, 1
                        bold: True
                        on_release: app.prev_month()

                    Button:
                        text: ">"
                        size_hint_x: None
                        width: dp(42)
                        background_normal: ""
                        background_color: 0, 0, 0, 0
                        color: .15, .22, .35, 1
                        bold: True
                        on_release: app.next_month()

                MutedText:
                    id: lbl_fecha_sel
                    text: "Fecha seleccionada: --/--/----"

                GridLayout:
                    id: cal_head
                    cols: 7
                    spacing: dp(6)
                    size_hint_y: None
                    height: dp(30)

                GridLayout:
                    id: cal_grid
                    cols: 7
                    spacing: dp(6)
                    size_hint_y: None
                    height: self.minimum_height

            SoftCard:
                spacing: dp(10)

                SubTitleText:
                    text: "Registrar horas del día"

                MutedText:
                    text: "Horas trabajadas"

                ModernInput:
                    id: txt_horas
                    hint_text: "Ejemplo: 4.5"

                MutedText:
                    text: "Nota opcional"

                ModernInput:
                    id: txt_nota
                    hint_text: "Ejemplo: Actividades administrativas"

                BoxLayout:
                    size_hint_y: None
                    height: dp(46)
                    spacing: dp(8)

                    PrimaryBtn:
                        text: "Guardar"
                        on_release: app.save_daily()

                    SecondaryBtn:
                        text: "Limpiar"
                        on_release: app.clear_form()

            SoftCard:
                spacing: dp(10)

                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(10)

                    SubTitleText:
                        text: "Registros recientes"
                        size_hint_x: 1
                        text_size: self.size
                        halign: "left"
                        valign: "middle"

                    SecondaryBtn:
                        text: "Ver resumen mensual"
                        size_hint_x: None
                        width: dp(170)
                        on_release: app.open_month_summary()

                BoxLayout:
                    id: recent_box
                    orientation: "vertical"
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height
"""


def cargar_datos():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("objetivo_horas", 0.0)
                data.setdefault("registros", [])
                return data
        except Exception:
            pass
    return {"objetivo_horas": 0.0, "registros": []}


def guardar_datos(data):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fmt_horas(v):
    return f"{float(v):.2f}"


def parse_horas(txt):
    txt = (txt or "").strip().replace(",", ".")
    if not txt:
        raise ValueError("Vacío")
    val = float(txt)
    if val < 0:
        raise ValueError("Negativo")
    return round(val, 2)


def total_horas(data):
    return round(sum(float(r["horas"]) for r in data["registros"]), 2)


def ordenar_registros(data):
    data["registros"].sort(key=lambda r: (r["fecha"], 0 if r.get("es_inicial", False) else 1), reverse=True)


def promedio_reciente(data, ultimos_dias=30):
    hoy = date.today()
    desde = hoy - timedelta(days=ultimos_dias - 1)
    vals = []
    for r in data["registros"]:
        if r.get("es_inicial", False):
            continue
        f = datetime.strptime(r["fecha"], "%Y-%m-%d").date()
        if desde <= f <= hoy and float(r["horas"]) > 0:
            vals.append(float(r["horas"]))
    if not vals:
        return 0.0
    return round(sum(vals) / len(vals), 2)


def fecha_estimada(data):
    objetivo = float(data.get("objetivo_horas", 0) or 0)
    acumulado = total_horas(data)
    faltan = max(0.0, objetivo - acumulado)
    if faltan <= 0:
        return "Ya terminó"
    prom = promedio_reciente(data, 30)
    if prom <= 0:
        return "Sin datos suficientes"
    dias = math.ceil(faltan / prom)
    return (date.today() + timedelta(days=dias)).strftime("%d/%m/%Y")


def resumen_mensual(data):
    res = {}
    for r in data["registros"]:
        f = datetime.strptime(r["fecha"], "%Y-%m-%d").date()
        clave = f"{f.year:04d}-{f.month:02d}"
        res[clave] = res.get(clave, 0.0) + float(r["horas"])
    return dict(sorted(res.items()))


def iso_a_ddmmyyyy(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d/%m/%Y")


def ddmmyyyy_a_iso(txt):
    return datetime.strptime(txt, "%d/%m/%Y").strftime("%Y-%m-%d")


class ProgressRing(Widget):
    progress = NumericProperty(0.0)
    center_text = StringProperty("0%")
    sub_text = StringProperty("avance")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw, progress=self.redraw,
                  center_text=self.redraw, sub_text=self.redraw)

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            size = min(self.width, self.height)
            thickness = dp(11)
            pad = dp(10)
            w = size - pad * 2

            Color(0.90, 0.93, 0.98, 1)
            Line(circle=(self.center_x, self.center_y, w / 2), width=thickness)

            Color(0.16, 0.43, 0.89, 1)
            Line(circle=(self.center_x, self.center_y, w / 2, 90, 90 + 360 * self.progress), width=thickness)

            Color(1, 1, 1, 1)
            Ellipse(
                pos=(self.center_x - (w - thickness * 2.4) / 2, self.center_y - (w - thickness * 2.4) / 2),
                size=(w - thickness * 2.4, w - thickness * 2.4)
            )

        self.canvas.after.clear()
        with self.canvas.after:
            from kivy.core.text import Label as CoreLabel

            lbl = CoreLabel(text=self.center_text, font_size=dp(26), bold=True)
            lbl.refresh()
            tex = lbl.texture
            Color(0.10, 0.18, 0.30, 1)
            Rectangle(
                texture=tex,
                pos=(self.center_x - tex.size[0] / 2, self.center_y - dp(6)),
                size=tex.size
            )

            lbl2 = CoreLabel(text=self.sub_text, font_size=dp(12))
            lbl2.refresh()
            tex2 = lbl2.texture
            Color(0.45, 0.50, 0.58, 1)
            Rectangle(
                texture=tex2,
                pos=(self.center_x - tex2.size[0] / 2, self.center_y - dp(28)),
                size=tex2.size
            )


class ModernInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(54)
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = (0.08, 0.10, 0.16, 1)
        self.hint_text_color = (0.78, 0.81, 0.87, 1)
        self.cursor_color = (0.16, 0.43, 0.89, 1)
        self.font_size = "17sp"
        self.padding = [dp(14), dp(14), dp(14), dp(14)]
        self.bind(pos=self._redraw, size=self._redraw, focus=self._redraw)
        Clock.schedule_once(lambda dt: self._redraw(), 0)

    def _redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.focus:
                Color(0.98, 0.99, 1, 1)
            else:
                Color(0.96, 0.97, 0.99, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[14, 14, 14, 14])

            if self.focus:
                Color(0.16, 0.43, 0.89, 1)
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 14), width=1.6)
            else:
                Color(0.84, 0.88, 0.94, 1)
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 14), width=1)


class DayCellButton(Button):
    iso_date = StringProperty("")
    bg_color = ListProperty([0.97, 0.98, 1, 1])
    fg_color = ListProperty([0.12, 0.12, 0.12, 1])
    dot_color = ListProperty([0, 0, 0, 0])
    is_selected = BooleanProperty(False)


class RecentRow(BoxLayout):
    def __init__(self, idx, title, subtitle, on_press, on_delete, can_delete=True, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(96),
            padding=dp(10),
            spacing=dp(10),
            **kwargs
        )
        self.idx = idx

        with self.canvas.before:
            Color(0.97, 0.98, 1, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[18, 18, 18, 18])
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        info = BoxLayout(
            orientation="vertical",
            spacing=dp(4),
            size_hint_x=1,
            padding=(0, dp(2), 0, dp(2))
        )

        lbl1 = Label(
            text=title,
            color=(0.10, 0.18, 0.30, 1),
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(34),
            font_size="16sp"
        )
        lbl1.bind(size=lambda i, v: setattr(i, "text_size", v))

        lbl2 = Label(
            text=subtitle,
            color=(0.42, 0.48, 0.56, 1),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(38),
            font_size="14sp"
        )
        lbl2.bind(size=lambda i, v: setattr(i, "text_size", v))

        info.add_widget(lbl1)
        info.add_widget(lbl2)

        btn_main = Button(
            text="",
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            size_hint_x=1
        )
        btn_main.bind(on_release=lambda *_: on_press(idx))

        left_wrap = BoxLayout(size_hint_x=1)
        left_wrap.add_widget(info)
        left_wrap.add_widget(btn_main)

        btn_delete = Button(
            text="Borrar",
            size_hint=(None, None),
            size=(dp(78), dp(38)),
            background_normal="",
            background_down="",
            background_color=(0.95, 0.89, 0.89, 1),
            color=(0.75, 0.16, 0.20, 1),
            bold=True,
            font_size="13sp",
            disabled=not can_delete,
            opacity=1 if can_delete else 0.35
        )
        btn_delete.bind(on_release=lambda *_: on_delete(idx))

        right_wrap = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(84),
            padding=(0, dp(18), 0, dp(18))
        )
        right_wrap.add_widget(btn_delete)

        self.add_widget(left_wrap)
        self.add_widget(right_wrap)

    def _upd_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class SimplePopup(ModalView):
    def __init__(self, title, content_widget, buttons, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.92, None)
        self.height = dp(420)
        self.auto_dismiss = True

        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[24, 24, 24, 24])
        root.bind(pos=self._upd_bg, size=self._upd_bg)

        lbl = Label(
            text=title,
            color=(0.10, 0.18, 0.30, 1),
            bold=True,
            font_size="18sp",
            size_hint_y=None,
            height=dp(34),
            halign="left",
            valign="middle"
        )
        lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        root.add_widget(lbl)
        root.add_widget(content_widget)

        if buttons:
            bbar = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
            for b in buttons:
                btn = Button(
                    text=b["text"],
                    background_normal="",
                    background_down="",
                    background_color=b.get("bg", (.91, .95, 1, 1)),
                    color=b.get("fg", (.15, .22, .35, 1)),
                    bold=True
                )
                btn.bind(on_release=b["callback"])
                bbar.add_widget(btn)
            root.add_widget(bbar)

        self.add_widget(root)

    def _upd_bg(self, widget, *args):
        self.bg.pos = widget.pos
        self.bg.size = widget.size


class ServicioSocialApp(App):
    nombre_alumna = StringProperty(NOMBRE_ALUMNA)
    nombre_corto = StringProperty(NOMBRE_CORTO)

    def build(self):
        self.title = "Servicio Social"
        self.data = cargar_datos()
        self.edit_idx = None
        self.selected_idx = None

        hoy = date.today()
        self.sel_iso = hoy.strftime("%Y-%m-%d")
        self.cal_year = hoy.year
        self.cal_month = hoy.month

        self.root = Builder.load_string(KV)
        Clock.schedule_once(lambda dt: self.refresh_all(), 0)
        return self.root

    def refresh_all(self):
        self.update_summary()
        self.build_calendar()
        self.build_recent()

    def update_summary(self):
        objetivo = float(self.data.get("objetivo_horas", 0) or 0)
        acumulado = total_horas(self.data)
        faltan = max(0.0, objetivo - acumulado)
        jornadas = faltan / 8 if faltan > 0 else 0.0
        prom = promedio_reciente(self.data, 30)
        est = fecha_estimada(self.data)

        self.root.ids.lbl_obj.text = f"{fmt_horas(objetivo)} h"
        self.root.ids.lbl_acu.text = f"{fmt_horas(acumulado)} h"
        self.root.ids.lbl_fal.text = f"{fmt_horas(faltan)} h"
        self.root.ids.lbl_jornadas.text = f"Jornadas de 8h: {fmt_horas(jornadas)}"
        self.root.ids.lbl_prom.text = f"Promedio reciente: {fmt_horas(prom)} h"
        self.root.ids.lbl_est.text = f"Fecha estimada de término: {est}"

        progreso = 0 if objetivo <= 0 else min(1.0, acumulado / objetivo)
        self.root.ids.ring.progress = progreso
        self.root.ids.ring.center_text = f"{int(round(progreso * 100))}%"
        self.root.ids.ring.sub_text = "avance"

    def _dias_con_registros(self):
        m = {}
        for r in self.data["registros"]:
            m[r["fecha"]] = m.get(r["fecha"], 0.0) + float(r["horas"])
        return m

    def build_calendar(self):
        self.root.ids.cal_head.clear_widgets()
        self.root.ids.cal_grid.clear_widgets()

        meses_es = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.root.ids.lbl_mes.text = f"{meses_es[self.cal_month]} {self.cal_year}"
        self.root.ids.lbl_fecha_sel.text = f"Fecha seleccionada: {iso_a_ddmmyyyy(self.sel_iso)}"

        for d in ["L", "M", "M", "J", "V", "S", "D"]:
            lbl = Label(text=d, color=(0.35, 0.40, 0.48, 1), bold=True)
            self.root.ids.cal_head.add_widget(lbl)

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdatescalendar(self.cal_year, self.cal_month)
        regs = self._dias_con_registros()
        hoy_iso = date.today().strftime("%Y-%m-%d")

        for week in weeks:
            for d in week:
                iso = d.strftime("%Y-%m-%d")
                btn = DayCellButton(text=str(d.day), iso_date=iso, size_hint_y=None, height=dp(46))

                esta_mes = (d.month == self.cal_month)
                seleccionado = (iso == self.sel_iso)
                es_hoy = (iso == hoy_iso)
                tiene = iso in regs

                if seleccionado:
                    btn.bg_color = [0.16, 0.43, 0.89, 1]
                    btn.fg_color = [1, 1, 1, 1]
                    btn.dot_color = [1, 1, 1, 1] if tiene else [0, 0, 0, 0]
                    btn.is_selected = True
                elif es_hoy:
                    btn.bg_color = [0.84, 0.91, 1, 1]
                    btn.fg_color = [0.08, 0.16, 0.27, 1]
                    btn.dot_color = [0.16, 0.43, 0.89, 1] if tiene else [0, 0, 0, 0]
                elif esta_mes:
                    btn.bg_color = [0.97, 0.98, 1, 1]
                    btn.fg_color = [0.12, 0.12, 0.12, 1]
                    btn.dot_color = [0.16, 0.43, 0.89, 1] if tiene else [0, 0, 0, 0]
                else:
                    btn.bg_color = [0.94, 0.94, 0.94, 1]
                    btn.fg_color = [0.60, 0.60, 0.60, 1]
                    btn.dot_color = [0.70, 0.70, 0.70, 1] if tiene else [0, 0, 0, 0]

                btn.bind(on_release=self.select_day)
                self.root.ids.cal_grid.add_widget(btn)

    def select_day(self, btn):
        self.sel_iso = btn.iso_date
        f = datetime.strptime(self.sel_iso, "%Y-%m-%d").date()
        self.cal_year = f.year
        self.cal_month = f.month
        self.build_calendar()

    def prev_month(self):
        if self.cal_month == 1:
            self.cal_month = 12
            self.cal_year -= 1
        else:
            self.cal_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.cal_month == 12:
            self.cal_month = 1
            self.cal_year += 1
        else:
            self.cal_month += 1
        self.build_calendar()

    def build_recent(self):
        ordenar_registros(self.data)
        box = self.root.ids.recent_box
        box.clear_widgets()

        if not self.data["registros"]:
            lbl = Label(
                text="No hay registros todavía.",
                color=(0.42, 0.48, 0.56, 1),
                size_hint_y=None,
                height=dp(36)
            )
            box.add_widget(lbl)
            return

        for idx, r in enumerate(self.data["registros"][:20]):
            tipo = "Carga inicial" if r.get("es_inicial", False) else "Registro diario"
            nota = r.get("nota", "").strip()
            title = f"{iso_a_ddmmyyyy(r['fecha'])}  •  {fmt_horas(r['horas'])} h"
            subtitle = tipo if not nota else f"{tipo}\\n{nota}"
            row = RecentRow(
                idx,
                title,
                subtitle,
                self.on_recent_press,
                self.delete_row,
                can_delete=not r.get("es_inicial", False)
            )
            box.add_widget(row)

    def on_recent_press(self, idx):
        self.selected_idx = idx
        reg = self.data["registros"][idx]

        if reg.get("es_inicial", False):
            self.show_info("Ese registro es carga inicial. Se edita desde el menú.")
            return

        self.edit_idx = idx
        self.sel_iso = reg["fecha"]
        f = datetime.strptime(self.sel_iso, "%Y-%m-%d").date()
        self.cal_year = f.year
        self.cal_month = f.month
        self.root.ids.txt_horas.text = fmt_horas(reg["horas"])
        self.root.ids.txt_nota.text = reg.get("nota", "")
        self.build_calendar()

    def clear_form(self):
        self.edit_idx = None
        self.root.ids.txt_horas.text = ""
        self.root.ids.txt_nota.text = ""

        hoy = date.today()
        self.sel_iso = hoy.strftime("%Y-%m-%d")
        self.cal_year = hoy.year
        self.cal_month = hoy.month
        self.build_calendar()

    def save_daily(self):
        txt_horas = self.root.ids.txt_horas.text.strip()
        if not txt_horas:
            self.show_error("Escribe las horas trabajadas.")
            return

        try:
            horas = parse_horas(txt_horas)
        except Exception:
            self.show_error("Ingresa horas válidas.")
            return

        nota = self.root.ids.txt_nota.text.strip()

        if self.edit_idx is None:
            self.data["registros"].append({
                "fecha": self.sel_iso,
                "horas": horas,
                "nota": nota,
                "es_inicial": False
            })
            msg = "Registro guardado."
        else:
            reg = self.data["registros"][self.edit_idx]
            reg["fecha"] = self.sel_iso
            reg["horas"] = horas
            reg["nota"] = nota
            reg["es_inicial"] = False
            msg = "Registro actualizado."

        guardar_datos(self.data)
        self.clear_form()
        self.refresh_all()
        self.show_info(msg)

    def delete_row(self, idx, *_):
        if idx is None or idx >= len(self.data["registros"]):
            self.show_error("No encontré el registro.")
            return

        reg = self.data["registros"][idx]

        if reg.get("es_inicial", False):
            self.show_error("La carga inicial no se elimina desde aquí.")
            return

        fecha_txt = iso_a_ddmmyyyy(reg["fecha"])

        def do_delete(*args):
            popup.dismiss()
            self.data["registros"].pop(idx)
            guardar_datos(self.data)
            self.selected_idx = None
            self.edit_idx = None
            self.clear_form()
            self.refresh_all()
            self.show_info(f"Registro eliminado: {fecha_txt}")

        content = BoxLayout(orientation="vertical", spacing=dp(10))
        lab = Label(text=f"¿Eliminar el registro del {fecha_txt}?", color=(0.15, 0.22, 0.35, 1))
        content.add_widget(lab)

        popup = SimplePopup(
            "Eliminar registro",
            content,
            [
                {"text": "Cancelar", "callback": lambda x: popup.dismiss()},
                {"text": "Eliminar", "callback": do_delete, "bg": (.16, .43, .89, 1), "fg": (1, 1, 1, 1)},
            ],
        )
        popup.open()

    def open_menu(self):
        content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        btn1 = Button(text="Establecer objetivo total", background_normal="", background_down="", background_color=(.91, .95, 1, 1), color=(.15, .22, .35, 1), bold=True, size_hint_y=None, height=dp(50))
        btn2 = Button(text="Captura inicial acumulada", background_normal="", background_down="", background_color=(.91, .95, 1, 1), color=(.15, .22, .35, 1), bold=True, size_hint_y=None, height=dp(50))
        btn3 = Button(text="Cerrar", background_normal="", background_down="", background_color=(.16, .43, .89, 1), color=(1, 1, 1, 1), bold=True, size_hint_y=None, height=dp(50))

        content.add_widget(btn1)
        content.add_widget(btn2)
        content.add_widget(btn3)

        popup = SimplePopup("Menú principal", content, [])
        popup.height = dp(320)

        btn1.bind(on_release=lambda x: (popup.dismiss(), self.open_goal_popup()))
        btn2.bind(on_release=lambda x: (popup.dismiss(), self.open_initial_popup()))
        btn3.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    def open_goal_popup(self):
        box = BoxLayout(orientation="vertical", spacing=dp(8))
        inp = ModernInput(
            text=fmt_horas(self.data.get("objetivo_horas", 0) or 0),
            hint_text="Objetivo total de horas"
        )
        box.add_widget(inp)

        def save_goal(*args):
            try:
                self.data["objetivo_horas"] = parse_horas(inp.text)
            except Exception:
                self.show_error("Objetivo inválido.")
                return
            guardar_datos(self.data)
            popup.dismiss()
            self.refresh_all()
            self.show_info("Objetivo guardado.")

        popup = SimplePopup(
            "Objetivo total",
            box,
            [
                {"text": "Cancelar", "callback": lambda x: popup.dismiss()},
                {"text": "Guardar", "callback": save_goal, "bg": (.16, .43, .89, 1), "fg": (1, 1, 1, 1)},
            ]
        )
        popup.height = dp(240)
        popup.open()

    def open_initial_popup(self):
        box = BoxLayout(orientation="vertical", spacing=dp(8))
        inp_fecha = ModernInput(text=iso_a_ddmmyyyy(self.sel_iso), hint_text="Fecha corte DD/MM/AAAA")
        inp_horas = ModernInput(hint_text="Horas acumuladas")
        inp_nota = ModernInput(text="Carga inicial acumulada", hint_text="Nota")
        box.add_widget(inp_fecha)
        box.add_widget(inp_horas)
        box.add_widget(inp_nota)

        def save_initial(*args):
            try:
                fecha_iso = ddmmyyyy_a_iso(inp_fecha.text.strip())
                horas = parse_horas(inp_horas.text)
                nota = inp_nota.text.strip() or "Carga inicial acumulada"
            except Exception:
                self.show_error("Datos inválidos en carga inicial.")
                return

            self.data["registros"] = [r for r in self.data["registros"] if not r.get("es_inicial", False)]
            self.data["registros"].append({
                "fecha": fecha_iso,
                "horas": horas,
                "nota": nota,
                "es_inicial": True
            })
            guardar_datos(self.data)
            popup.dismiss()
            self.refresh_all()
            self.show_info("Carga inicial guardada.")

        popup = SimplePopup(
            "Captura inicial acumulada",
            box,
            [
                {"text": "Cancelar", "callback": lambda x: popup.dismiss()},
                {"text": "Guardar", "callback": save_initial, "bg": (.16, .43, .89, 1), "fg": (1, 1, 1, 1)},
            ]
        )
        popup.height = dp(340)
        popup.open()

    def open_month_summary(self):
        res = resumen_mensual(self.data)
        texto = ""
        if not res:
            texto = "No hay registros todavía."
        else:
            for k, horas in res.items():
                anio, mes = k.split("-")
                texto += f"{mes}/{anio}: {fmt_horas(horas)} h\\n"
            texto += "\\n"
            objetivo = float(self.data.get("objetivo_horas", 0) or 0)
            acumulado = total_horas(self.data)
            faltan = max(0.0, objetivo - acumulado)
            texto += f"TOTAL: {fmt_horas(acumulado)} h\\n"
            texto += f"FALTAN: {fmt_horas(faltan)} h\\n"
            texto += f"JORNADAS DE 8H: {fmt_horas(faltan / 8 if faltan > 0 else 0)}\\n"
            texto += f"FECHA ESTIMADA: {fecha_estimada(self.data)}"

        box = ScrollView()
        lab = Label(
            text=texto,
            color=(0.15, 0.22, 0.35, 1),
            size_hint_y=None,
            halign="left",
            valign="top",
            padding=(dp(8), dp(8))
        )
        lab.bind(width=lambda i, v: setattr(i, "text_size", (v - dp(16), None)))
        lab.bind(texture_size=lambda i, v: setattr(i, "height", v[1] + dp(20)))
        box.add_widget(lab)

        popup = SimplePopup(
            "Resumen por mes",
            box,
            [{"text": "Cerrar", "callback": lambda x: popup.dismiss(), "bg": (.16, .43, .89, 1), "fg": (1, 1, 1, 1)}]
        )
        popup.height = dp(500)
        popup.open()

    def show_error(self, msg):
        self._simple_msg("Error", msg)

    def show_info(self, msg):
        self._simple_msg("Listo", msg)

    def _simple_msg(self, title, text):
        box = BoxLayout()
        box.add_widget(Label(text=text, color=(0.15, 0.22, 0.35, 1)))
        popup = SimplePopup(
            title,
            box,
            [{"text": "OK", "callback": lambda x: popup.dismiss(), "bg": (.16, .43, .89, 1), "fg": (1, 1, 1, 1)}]
        )
        popup.height = dp(220)
        popup.open()


if __name__ == "__main__":
    ServicioSocialApp().run()