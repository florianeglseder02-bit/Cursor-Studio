import ctypes, json, os, sys, tempfile
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

BASE = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
ASSETS = BASE / 'assets'
ITEMS = json.loads((ASSETS / 'cursors.json').read_text(encoding='utf-8'))

class CursorStudio:
    def __init__(self, root):
        self.root = root
        root.title('Cursor Studio')
        root.geometry('980x760')
        root.minsize(760, 620)
        root.configure(bg='#0b1020')
        self.selected = ITEMS[0]
        self.size = tk.IntVar(value=72)
        self.filter = tk.StringVar(value='Alle')
        self.photos = {}
        self._style()
        self._build()
        self._select(self.selected)

    def _style(self):
        s=ttk.Style(); s.theme_use('clam')
        s.configure('TCombobox', fieldbackground='#18213a', background='#18213a', foreground='white')
        s.configure('Horizontal.TScale', background='#121a2e', troughcolor='#273552')

    def _build(self):
        header=tk.Frame(self.root,bg='#0b1020'); header.pack(fill='x',padx=26,pady=(22,12))
        tk.Label(header,text='CURSOR STUDIO',font=('Segoe UI',11,'bold'),fg='#9c8cff',bg='#0b1020').pack(anchor='w')
        tk.Label(header,text='Dein Cursor. Dein Style.',font=('Segoe UI',27,'bold'),fg='white',bg='#0b1020').pack(anchor='w',pady=(3,0))
        tk.Label(header,text='Wähle ein Design, passe die Größe an und übernimm es für Windows.',font=('Segoe UI',10),fg='#a8b2cc',bg='#0b1020').pack(anchor='w',pady=(4,0))
        body=tk.Frame(self.root,bg='#0b1020'); body.pack(fill='both',expand=True,padx=26,pady=12)
        left=tk.Frame(body,bg='#121a2e',highlightbackground='#263453',highlightthickness=1); left.pack(side='left',fill='both',expand=True,padx=(0,14))
        bar=tk.Frame(left,bg='#121a2e'); bar.pack(fill='x',padx=16,pady=14)
        tk.Label(bar,text='DESIGNS',font=('Segoe UI',10,'bold'),fg='white',bg='#121a2e').pack(side='left')
        cb=ttk.Combobox(bar,textvariable=self.filter,values=['Alle','Bunte Cursor','Galaktische Cursor'],state='readonly',width=19); cb.pack(side='right'); cb.bind('<<ComboboxSelected>>',lambda e:self._populate())
        self.canvas=tk.Canvas(left,bg='#0e1629',highlightthickness=0)
        self.scroll=ttk.Scrollbar(left,orient='vertical',command=self.canvas.yview)
        self.grid=tk.Frame(self.canvas,bg='#0e1629')
        self.grid.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0),window=self.grid,anchor='nw')
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side='left',fill='both',expand=True,padx=(12,0),pady=(0,12)); self.scroll.pack(side='right',fill='y',pady=(0,12),padx=(0,8))
        right=tk.Frame(body,bg='#121a2e',width=280,highlightbackground='#263453',highlightthickness=1); right.pack(side='right',fill='y'); right.pack_propagate(False)
        tk.Label(right,text='VORSCHAU',font=('Segoe UI',10,'bold'),fg='white',bg='#121a2e').pack(anchor='w',padx=18,pady=(18,8))
        self.preview=tk.Label(right,bg='#0e1629',text='',width=18,height=9); self.preview.pack(fill='x',padx=16)
        self.name=tk.Label(right,text='',font=('Segoe UI',11,'bold'),fg='white',bg='#121a2e',wraplength=230); self.name.pack(pady=(12,18))
        tk.Label(right,text='GRÖSSE',font=('Segoe UI',9,'bold'),fg='#a8b2cc',bg='#121a2e').pack(anchor='w',padx=18)
        scale=ttk.Scale(right,from_=32,to=128,orient='horizontal',variable=self.size,command=lambda v:self._preview()); scale.pack(fill='x',padx=18,pady=9)
        self.size_label=tk.Label(right,text='72 px',font=('Segoe UI',10,'bold'),fg='#9c8cff',bg='#121a2e'); self.size_label.pack(anchor='e',padx=18)
        tk.Button(right,text='Auf Windows anwenden',command=self._apply,bg='#7865f5',fg='white',activebackground='#8e7eff',activeforeground='white',relief='flat',font=('Segoe UI',10,'bold'),pady=12,cursor='hand2').pack(fill='x',padx=16,pady=(25,8))
        tk.Button(right,text='Windows-Standard wiederherstellen',command=self._reset,bg='#202c45',fg='#dce4f8',activebackground='#2b3a59',activeforeground='white',relief='flat',font=('Segoe UI',9),pady=10,cursor='hand2').pack(fill='x',padx=16)
        tk.Label(right,text='Änderungen gelten systemweit.\nZum Zurücksetzen Windows-Standard nutzen.',font=('Segoe UI',8),fg='#8390ad',bg='#121a2e',wraplength=240,justify='center').pack(side='bottom',pady=16)
        self._populate()

    def _populate(self):
        for w in self.grid.winfo_children(): w.destroy()
        visible=[x for x in ITEMS if self.filter.get()=='Alle' or x['group']==self.filter.get()]
        for i,item in enumerate(visible):
            im=Image.open(ASSETS/item['file']).convert('RGBA'); im.thumbnail((86,86))
            photo=ImageTk.PhotoImage(im); self.photos[item['id']]=photo
            selected=item['id']==self.selected['id']
            b=tk.Button(self.grid,image=photo,text=item['name'].split()[-1],compound='top',command=lambda x=item:self._select(x),bg='#27365a' if selected else '#17233c',fg='white',activebackground='#34466e',activeforeground='white',relief='flat',bd=0,font=('Segoe UI',8),width=112,height=122,cursor='hand2')
            b.grid(row=i//3,column=i%3,padx=5,pady=5,sticky='nsew')
        for c in range(3): self.grid.grid_columnconfigure(c,weight=1)

    def _select(self,item):
        self.selected=item; self.name.config(text=item['name']); self._preview(); self._populate()

    def _preview(self):
        if not hasattr(self,'preview'): return
        px=max(32,int(self.size.get())); self.size_label.config(text=f'{px} px')
        im=Image.open(ASSETS/self.selected['file']).convert('RGBA'); im.thumbnail((px,px),Image.Resampling.LANCZOS)
        bg=Image.new('RGBA',(180,180),(14,22,41,255)); bg.alpha_composite(im,((180-im.width)//2,(180-im.height)//2))
        self.preview_img=ImageTk.PhotoImage(bg); self.preview.config(image=self.preview_img)

    def _make_cur(self, png, out, size):
        im=Image.open(png).convert('RGBA'); im.thumbnail((size,size),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(size,size),(0,0,0,0)); canvas.alpha_composite(im,((size-im.width)//2,(size-im.height)//2))
        import io, struct
        data=io.BytesIO(); canvas.save(data,format='PNG'); payload=data.getvalue()
        # CUR directory entry: hotspot at the upper-left tip area.
        hx=max(1,int(size*.16)); hy=max(1,int(size*.16))
        header=struct.pack('<HHH',0,2,1)
        entry=struct.pack('<BBBBHHII',size if size<256 else 0,size if size<256 else 0,0,0,hx,hy,len(payload),22)
        Path(out).write_bytes(header+entry+payload)

    def _apply(self):
        if sys.platform!='win32':
            messagebox.showerror('Windows erforderlich','Das Anwenden des System-Cursors funktioniert nur unter Windows.'); return
        try:
            size=max(32,int(self.size.get()))
            temp=Path(tempfile.gettempdir())/'cursor_studio_custom.cur'
            self._make_cur(ASSETS/self.selected['file'],temp,size)
            user32=ctypes.WinDLL('user32',use_last_error=True)
            user32.LoadImageW.restype=ctypes.c_void_p
            user32.LoadImageW.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_uint,ctypes.c_int,ctypes.c_int,ctypes.c_uint]
            user32.SetSystemCursor.argtypes=[ctypes.c_void_p,ctypes.c_uint]
            user32.SetSystemCursor.restype=ctypes.c_bool
            IMAGE_CURSOR=2; LR_LOADFROMFILE=0x10; OCR_NORMAL=32512
            h=user32.LoadImageW(None,str(temp),IMAGE_CURSOR,0,0,LR_LOADFROMFILE)
            if not h: raise ctypes.WinError(ctypes.get_last_error())
            if not user32.SetSystemCursor(h,OCR_NORMAL): raise ctypes.WinError(ctypes.get_last_error())
            messagebox.showinfo('Cursor geändert',f'{self.selected["name"]} wurde als Windows-Zeiger übernommen.\nGröße: {size} px')
        except Exception as e: messagebox.showerror('Fehler beim Anwenden',str(e))

    def _reset(self):
        if sys.platform!='win32':
            messagebox.showerror('Windows erforderlich','Das Zurücksetzen funktioniert nur unter Windows.'); return
        SPI_SETCURSORS=0x57
        user32=ctypes.WinDLL('user32',use_last_error=True)
        user32.SystemParametersInfoW.argtypes=[ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint]
        user32.SystemParametersInfoW.restype=ctypes.c_bool
        ok=user32.SystemParametersInfoW(SPI_SETCURSORS,0,None,0)
        if ok: messagebox.showinfo('Zurückgesetzt','Die Windows-Standardcursor wurden wiederhergestellt.')
        else: messagebox.showerror('Fehler','Windows konnte die Standardcursor nicht wiederherstellen.')

if __name__=='__main__':
    if sys.platform!='win32':
        print('Cursor Studio ist für Windows gedacht.');
    root=tk.Tk(); app=CursorStudio(root); root.mainloop()
