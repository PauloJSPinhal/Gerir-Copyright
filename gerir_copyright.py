#!/usr/bin/env python3
"""
Gerir copyright - Ferramenta de gestão de autoria para fotografias.
Compatível: Debian 13 / GNOME / GTK3 / exiftool
"""

import sys, os, re, json, subprocess, threading
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GLib, Gdk

IMAGE_EXTS = {'.jpg', '.jpeg', '.heic', '.heif', '.dng', '.cr2', '.cr3'}

def collect_images(paths):
    images = []
    for p in paths:
        p = os.path.abspath(p)
        if os.path.isfile(p) and os.path.splitext(p)[1].lower() in IMAGE_EXTS:
            images.append(p)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in files:
                    if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
                        images.append(os.path.join(root, f))
    return images

def get_metadata_fast(files):
    if not files: return []
    cmd = ['exiftool', '-fast2', '-json', '-Copyright', '-DateTimeOriginal'] + files
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)

def show_message(msg, msg_type, buttons=Gtk.ButtonsType.OK, title="Aviso"):
    dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, msg_type, buttons, msg)
    dlg.set_title(title)
    resp = dlg.run()
    dlg.destroy()
    return resp

def show_main_dialog(def_author, def_year, callback):
    dialog = Gtk.Dialog(title="Definir Autoria", transient_for=None, flags=Gtk.DialogFlags.MODAL)
    dialog.set_default_size(360, 170)
    dialog.set_border_width(16)
    dialog.set_type_hint(Gdk.WindowTypeHint.DIALOG)
    dialog.set_keep_above(True)  # Garante que não fica atrás de outras janelas

    box = dialog.get_content_area()
    box.set_spacing(12)

    grid = Gtk.Grid(row_spacing=10, column_spacing=10)
    grid.attach(Gtk.Label("Autor:", xalign=0), 0, 0, 1, 1)
    entry_author = Gtk.Entry()
    entry_author.set_text(def_author)
    entry_author.set_activates_default(True)
    grid.attach(entry_author, 1, 0, 1, 1)

    grid.attach(Gtk.Label("Ano:", xalign=0), 0, 1, 1, 1)
    entry_year = Gtk.Entry()
    entry_year.set_text(def_year)
    entry_year.set_activates_default(True)
    grid.attach(entry_year, 1, 1, 1, 1)

    box.pack_start(grid, True, True, 0)
    dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
    dialog.add_button("Aplicar", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    def on_response(d, response):
        author = entry_author.get_text().strip()
        year = entry_year.get_text().strip()
        d.destroy()
        callback(response, author, year)

    dialog.connect("response", on_response)
    dialog.show_all()
    dialog.present()  # 🎯 Força a janela para o primeiro plano

def apply_authorship(files, author, year):
    copyright_str = f"(c) {author} ({year})"
    cmd = ['exiftool', '-Copyright=' + copyright_str, '-overwrite_original'] + files
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        subprocess.run(['notify-send', '-i', 'dialog-information', 'Autoria Aplicada', 
                        f'"{copyright_str}" gravado em {len(files)} imagem(ns).'], check=False)
    else:
        show_message(f"Erro ao gravar metadados:\n{res.stderr}", Gtk.MessageType.ERROR, title="Erro")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 gerir_copyright.py <ficheiro1> [ficheiro2] ... [<pasta>]")
        sys.exit(1)

    files = collect_images(sys.argv[1:])
    if not files:
        show_message("Nenhuma imagem válida encontrada.", Gtk.MessageType.INFO, title="Aviso")
        sys.exit(0)

    def worker():
        try:
            meta = get_metadata_fast(files)
            
            authors, years_dt = [], []
            for data in meta:
                cp = data.get('Copyright', '') or ''
                if isinstance(cp, list): cp = cp[0]
                m = re.match(r'\(c\)\s*(.*?)\s*\((\d{4})\)', cp)
                authors.append(m.group(1) if m else None)

                dt = data.get('DateTimeOriginal', '') or ''
                if isinstance(dt, list): dt = dt[0]
                ym = re.search(r'(\d{4})', dt)
                years_dt.append(ym.group(1) if ym else None)

            valid_years = [y for y in years_dt if y is not None]
            if len(valid_years) > 0 and len(set(valid_years)) > 1:
                GLib.idle_add(show_message, "As fotografias selecionadas não são do mesmo ano.\nA operação foi cancelada.", 
                              Gtk.MessageType.WARNING, title="Anos Diferentes")
                return

            def_author = "" if any(a is None for a in authors) else authors[0]
            def_year = valid_years[0] if (valid_years and len(valid_years) == len(years_dt)) else ""

            def on_main_response(response, new_author, new_year):
                if response != Gtk.ResponseType.OK: return
                
                missing = []
                if not new_author: missing.append("Autor")
                if not new_year: missing.append("Ano")
                if missing:
                    show_message(f"Os seguintes campos estão vazios e impedem a validação:\n• {', '.join(missing)}",
                                 Gtk.MessageType.WARNING, title="Validação")
                    return

                existing_authors = set(a for a in authors if a is not None)
                if existing_authors and new_author not in existing_authors:
                    confirm = show_message(f"O autor atual é '{', '.join(existing_authors)}'.\nDeseja alterar para '{new_author}'?",
                                           Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, title="Confirmar Alteração")
                    if confirm != Gtk.ResponseType.YES: return

                apply_authorship(files, new_author, new_year)

            GLib.idle_add(show_main_dialog, def_author, def_year, on_main_response)

        except Exception as e:
            GLib.idle_add(show_message, f"Erro inesperado:\n{e}", Gtk.MessageType.ERROR, title="Erro")

    threading.Thread(target=worker, daemon=True).start()
    Gtk.main()

if __name__ == "__main__":
    main()