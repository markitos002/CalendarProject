import sys
from datetime import date, timedelta
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except Exception:
    tk = None  # type: ignore

# Excel
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# Optional PDF
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    REPORTLAB_OK = True
except Exception:
    REPORTLAB_OK = False

# Optional Holidays (for Colombia)
def _fallback_colombia_holidays_2025() -> Dict[date, str]:
    """Minimal fallback for 2025 Colombian holidays that affect Aug–Dec period.

    This covers Monday-observed holidays within the semester window.
    """
    return {
        date(2025, 8, 18): "Asunción de la Virgen (festivo)",
        date(2025, 10, 13): "Día de la Raza (festivo)",
        date(2025, 11, 3): "Día de Todos los Santos (festivo)",
        date(2025, 11, 17): "Independencia de Cartagena (festivo)",
        date(2025, 12, 8): "Inmaculada Concepción (festivo)",
    }


def get_colombia_holidays(start: date, end: date) -> Dict[date, str]:
    """Return a dict of holiday_date -> holiday_name for Colombia within range.

    Tries the 'holidays' package; falls back to a minimal 2025 set.
    """
    try:
        import holidays  # type: ignore

        co = holidays.country_holidays("CO", years={start.year, end.year})
        out: Dict[date, str] = {}
        d = start
        while d <= end:
            if d in co:
                out[d] = str(co.get(d))
            d += timedelta(days=1)
        return out
    except Exception:
        fallback = _fallback_colombia_holidays_2025()
        return {k: v for k, v in fallback.items() if start <= k <= end}


SPANISH_MONTHS = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


@dataclass
class WeekDates:
    semana: int
    lunes: date
    martes: date
    miercoles: date


def compute_weeks(start_monday: date, weeks: int = 18) -> List[WeekDates]:
    if start_monday.weekday() != 0:
        raise ValueError("La fecha de inicio debe ser un lunes")
    out: List[WeekDates] = []
    for i in range(weeks):
        mon = start_monday + timedelta(weeks=i)
        out.append(WeekDates(semana=i + 1, lunes=mon, martes=mon + timedelta(days=1), miercoles=mon + timedelta(days=2)))
    return out


def build_excel(
    out_path: str,
    title: str,
    subtitle: str,
    week_dates: List[WeekDates],
    entries: Dict[int, Tuple[str, str, str, str]],
    holidays_map: Dict[date, str],
) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Calendario"

    # Styles
    header_font = Font(bold=True, size=14)
    sub_font = Font(bold=False, size=12)
    week_header_font = Font(bold=True, size=12)
    thin = Side(border_style="thin", color="000000")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)
    align_center = Alignment(horizontal="center", vertical="center")
    align_wrap = Alignment(wrap_text=True, vertical="top")
    holiday_fill = PatternFill("solid", fgColor="F2F2F2")
    session_fill = PatternFill("solid", fgColor="E2F0D9")

    # Title
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=6)
    ws.cell(row=1, column=1, value=title).font = header_font
    ws.cell(row=1, column=1).alignment = align_center

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)
    ws.cell(row=2, column=1, value=subtitle).font = sub_font
    ws.cell(row=2, column=1).alignment = align_center

    row = 4
    # Column widths
    widths = [22, 22, 22, 22, 1, 1]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    for wd in week_dates:
        month_name = SPANISH_MONTHS[wd.lunes.month]
        # Week header
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
        ws.cell(row=row, column=1, value=f"SEMANA {wd.semana} {month_name}").font = week_header_font
        ws.cell(row=row, column=1).alignment = align_center
        row += 1

        # Day headers
        headers = [
            f"Lunes {wd.lunes.strftime('%d/%m')}",
            f"Martes {wd.martes.strftime('%d/%m')}",
            f"Miércoles 1 {wd.miercoles.strftime('%d/%m')}",
            f"Miércoles 2 {wd.miercoles.strftime('%d/%m')}",
        ]
        for col, h in enumerate(headers, start=1):
            c = ws.cell(row=row, column=col, value=h)
            c.font = Font(bold=True)
            c.alignment = align_center
            c.border = border
        row += 1

        # Content row
        mon_txt, tue_txt, wed1_txt, wed2_txt = entries.get(wd.semana, ("", "", "", ""))

        for col, (d, txt) in enumerate(
            [
                (wd.lunes, mon_txt),
                (wd.martes, tue_txt),
                (wd.miercoles, wed1_txt),
                (wd.miercoles, wed2_txt),
            ],
            start=1,
        ):
            cell = ws.cell(row=row, column=col)
            is_holiday = d in holidays_map
            if is_holiday:
                cell.value = f"Festivo: {holidays_map[d]}\nNo hay clase"
                cell.fill = holiday_fill
            else:
                cell.value = txt
                if txt:
                    cell.fill = session_fill
            cell.alignment = align_wrap
            cell.border = border
        row += 2  # leave a blank row between weeks

    wb.save(out_path)


def build_pdf(
    out_path: str,
    title: str,
    subtitle: str,
    week_dates: List[WeekDates],
    entries: Dict[int, Tuple[str, str, str, str]],
    holidays_map: Dict[date, str],
) -> None:
    if not REPORTLAB_OK:
        raise RuntimeError("ReportLab no está instalado. Instálalo para exportar a PDF.")

    doc = SimpleDocTemplate(out_path, pagesize=landscape(A4), rightMargin=18, leftMargin=18, topMargin=24, bottomMargin=24)
    styles = getSampleStyleSheet()
    parts: List = []
    parts.append(Paragraph(title, styles["Title"]))
    parts.append(Paragraph(subtitle, styles["Normal"]))
    parts.append(Spacer(1, 10))

    for wd in week_dates:
        month_name = SPANISH_MONTHS[wd.lunes.month]
        parts.append(Paragraph(f"SEMANA {wd.semana} {month_name}", styles["Heading2"]))

        data = [
            [
                f"Lunes {wd.lunes.strftime('%d/%m')}",
                f"Martes {wd.martes.strftime('%d/%m')}",
                f"Miércoles 1 {wd.miercoles.strftime('%d/%m')}",
                f"Miércoles 2 {wd.miercoles.strftime('%d/%m')}",
            ]
        ]

        mon_txt, tue_txt, wed1_txt, wed2_txt = entries.get(wd.semana, ("", "", "", ""))

        def cell_text(d: date, txt: str) -> str:
            if d in holidays_map:
                return f"Festivo: {holidays_map[d]}\nNo hay clase"
            return txt

        data.append([
            cell_text(wd.lunes, mon_txt),
            cell_text(wd.martes, tue_txt),
            cell_text(wd.miercoles, wed1_txt),
            cell_text(wd.miercoles, wed2_txt),
        ])

        t = Table(data, colWidths=[200, 200, 200, 200])
        t.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ])
        )
        # Shade holiday cells
        holidays_cols = []
        if wd.lunes in holidays_map:
            holidays_cols.append(0)
        if wd.martes in holidays_map:
            holidays_cols.append(1)
        if wd.miercoles in holidays_map:
            holidays_cols.extend([2, 3])
        for c in holidays_cols:
            t.setStyle(TableStyle([("BACKGROUND", (c, 1), (c, 1), colors.whitesmoke)]))

        parts.append(t)
        parts.append(Spacer(1, 6))

    doc.build(parts)


class CalendarGUI:
    def __init__(self, root: tk.Tk, start: date = date(2025, 8, 18), weeks: int = 18) -> None:  # type: ignore[name-defined]
        self.root = root
        self.root.title("Generador de Calendario de Clases")
        self.start = start
        self.weeks = weeks
        self.week_dates = compute_weeks(start, weeks)
        self.end = self.week_dates[-1].miercoles
        self.holidays = get_colombia_holidays(self.start, self.end)

        # Top fields
        top = ttk.Frame(root)
        top.pack(fill=tk.X, padx=10, pady=(10, 4))

        ttk.Label(top, text="Título (curso)").grid(row=0, column=0, sticky=tk.W)
        self.var_title = tk.StringVar(value="Fundamentos de Ciencias Básicas - 2025 - B")
        ttk.Entry(top, width=60, textvariable=self.var_title).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(top, text="Subtítulo (opcional)").grid(row=1, column=0, sticky=tk.W)
        self.var_sub = tk.StringVar(value=f"Desde {self.start.strftime('%d/%m/%Y')} por {self.weeks} semanas")
        ttk.Entry(top, width=60, textvariable=self.var_sub).grid(row=1, column=1, sticky=tk.W)

        # Scrollable frame for weeks
        container = ttk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas = tk.Canvas(container, height=480)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)
        self.scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Headers
        header = ttk.Frame(self.scroll_frame)
        header.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(header, text="Semana", width=8).grid(row=0, column=0)
        ttk.Label(header, text="Lunes", width=28).grid(row=0, column=1)
        ttk.Label(header, text="Martes", width=28).grid(row=0, column=2)
        ttk.Label(header, text="Miércoles (Sesión 1)", width=28).grid(row=0, column=3)
        ttk.Label(header, text="Miércoles (Sesión 2)", width=28).grid(row=0, column=4)

        # Store widgets for each semana; avoid direct tk.Text type hints for compatibility
        self.inputs: Dict[int, Tuple[Any, Any, Any, Any]] = {}

        for i, wd in enumerate(self.week_dates, start=1):
            row_idx = i
            frm = ttk.Frame(self.scroll_frame)
            frm.grid(row=row_idx, column=0, sticky=tk.W, pady=2)

            holiday_mon = wd.lunes in self.holidays
            holiday_tue = wd.martes in self.holidays
            holiday_wed = wd.miercoles in self.holidays

            semana_lbl = f"{wd.semana} ({wd.lunes.strftime('%d/%m')} - {wd.miercoles.strftime('%d/%m')})"
            ttk.Label(frm, text=semana_lbl, width=12).grid(row=0, column=0, padx=(0, 6))

            def mk_text(parent, col, day: date, is_holiday: bool) -> Any:
                t = tk.Text(parent, width=28, height=3, wrap="word")
                t.grid(row=0, column=col, padx=3)
                if is_holiday:
                    t.insert("1.0", f"Festivo: {self.holidays[day]}\nNo hay clase")
                    t.config(state=tk.DISABLED)
                return t

            txt_mon = mk_text(frm, 1, wd.lunes, holiday_mon)
            txt_tue = mk_text(frm, 2, wd.martes, holiday_tue)
            txt_w1 = mk_text(frm, 3, wd.miercoles, holiday_wed)
            txt_w2 = mk_text(frm, 4, wd.miercoles, holiday_wed)
            self.inputs[wd.semana] = (txt_mon, txt_tue, txt_w1, txt_w2)

        # Action buttons
        actions = ttk.Frame(root)
        actions.pack(fill=tk.X, padx=10, pady=(0, 12))
        ttk.Button(actions, text="Exportar a Excel (.xlsx)", command=self.export_excel).pack(side=tk.LEFT)
        ttk.Button(actions, text="Exportar a PDF (.pdf)", command=self.export_pdf).pack(side=tk.LEFT, padx=10)

        # Holidays notice
        info = ttk.Label(root, text=f"Festivos detectados: {', '.join(d.strftime('%d/%m') for d in sorted(self.holidays.keys()))}")
        info.pack(padx=10, pady=(0, 10))

    def _collect_entries(self) -> Dict[int, Tuple[str, str, str, str]]:
        out: Dict[int, Tuple[str, str, str, str]] = {}
        for semana, (m, t, w1, w2) in self.inputs.items():
            def get_text(txt: Any) -> str:
                if str(txt["state"]) == "disabled":
                    return ""
                return txt.get("1.0", "end").strip()

            out[semana] = (get_text(m), get_text(t), get_text(w1), get_text(w2))
        return out

    def export_excel(self) -> None:
        title = self.var_title.get().strip() or "Calendario de sesiones"
        subtitle = self.var_sub.get().strip()
        path = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
        )
        if not path:
            return
        try:
            build_excel(path, title, subtitle, self.week_dates, self._collect_entries(), self.holidays)
            messagebox.showinfo("Listo", f"Archivo Excel generado:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el Excel.\n{e}")

    def export_pdf(self) -> None:
        title = self.var_title.get().strip() or "Calendario de sesiones"
        subtitle = self.var_sub.get().strip()
        path = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
        )
        if not path:
            return
        try:
            build_pdf(path, title, subtitle, self.week_dates, self._collect_entries(), self.holidays)
            messagebox.showinfo("Listo", f"Archivo PDF generado:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF.\n{e}")


def run_gui() -> int:
    if tk is None:
        print("tkinter no está disponible en este entorno.")
        return 2
    root = tk.Tk()
    CalendarGUI(root)
    root.mainloop()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    # For now, always launch GUI; future: add CLI flags
    return run_gui()


if __name__ == "__main__":
    sys.exit(main())
