# app.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import model
import ctypes
#告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#获取屏幕的缩放因子
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)


class CS2EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CS2赛事管理系统")
        self.root.geometry("1200x800")
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各功能页面
        self.create_teams_page()
        self.create_players_page()
        self.create_tournaments_page()
        self.create_matches_page()
        
        # 初始化状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="导入数据", command=self.import_data)
        file_menu.add_command(label="导出数据", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 数据管理菜单
        data_menu = tk.Menu(menubar, tearoff=0)
        data_menu.add_command(label="战队管理", command=lambda: self.notebook.select(0))
        data_menu.add_command(label="选手管理", command=lambda: self.notebook.select(1))
        data_menu.add_command(label="赛事管理", command=lambda: self.notebook.select(2))
        data_menu.add_command(label="比赛管理", command=lambda: self.notebook.select(3))
        menubar.add_cascade(label="数据管理", menu=data_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_teams_page(self):
        teams_frame = ttk.Frame(self.notebook)
        self.notebook.add(teams_frame, text="战队管理")
        
        # 创建分栏布局
        paned = ttk.PanedWindow(teams_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧战队列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 搜索框
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.team_search_var = tk.StringVar()
        self.team_search_entry = ttk.Entry(search_frame, textvariable=self.team_search_var)
        self.team_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_teams).pack(side=tk.LEFT, padx=5)
        
        # 战队列表
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树状表格
        self.teams_tree = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set)
        self.teams_tree["columns"] = ("team_id", "team_name", "country")
        self.teams_tree.column("#0", width=0, stretch=tk.NO)
        self.teams_tree.column("team_id", width=50, anchor=tk.CENTER)
        self.teams_tree.column("team_name", width=150)
        self.teams_tree.column("country", width=100, anchor=tk.CENTER)
        
        self.teams_tree.heading("#0", text="")
        self.teams_tree.heading("team_id", text="ID")
        self.teams_tree.heading("team_name", text="战队名称")
        self.teams_tree.heading("country", text="国家/地区")
        
        self.teams_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.teams_tree.yview)
        
        # 绑定选择事件
        self.teams_tree.bind("<<TreeviewSelect>>", self.on_team_select)
        
        # 按钮框架
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="添加", command=self.add_team).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑", command=self.edit_team).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除", command=self.delete_team).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_teams).pack(side=tk.LEFT, padx=5)
        
        # 右侧详细信息
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # 添加战队详细信息表单
        self.team_detail_frame = ttk.LabelFrame(right_frame, text="战队详细信息")
        self.team_detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建详细信息表单
        form_grid = ttk.Frame(self.team_detail_frame)
        form_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 战队ID
        ttk.Label(form_grid, text="战队ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.team_id_var = tk.StringVar()
        self.team_id_entry = ttk.Entry(form_grid, textvariable=self.team_id_var, state="readonly")
        self.team_id_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 战队名称
        ttk.Label(form_grid, text="战队名称:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.team_name_var = tk.StringVar()
        self.team_name_entry = ttk.Entry(form_grid, textvariable=self.team_name_var, state="readonly")
        self.team_name_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 国家/地区
        ttk.Label(form_grid, text="国家/地区:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.team_country_var = tk.StringVar()
        self.team_country_entry = ttk.Entry(form_grid, textvariable=self.team_country_var, state="readonly")
        self.team_country_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Logo URL
        ttk.Label(form_grid, text="Logo URL:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.team_logo_var = tk.StringVar()
        self.team_logo_entry = ttk.Entry(form_grid, textvariable=self.team_logo_var, state="readonly")
        self.team_logo_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 简介
        ttk.Label(form_grid, text="简介:").grid(row=4, column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        self.team_desc_text = tk.Text(form_grid, height=6, width=40, state="disabled")
        self.team_desc_text.grid(row=4, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # 选手列表
        ttk.Label(form_grid, text="队员:").grid(row=5, column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        
        # 创建队员列表框架
        players_frame = ttk.Frame(form_grid)
        players_frame.grid(row=5, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # 队员列表滚动条
        player_scrollbar = ttk.Scrollbar(players_frame)
        player_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 队员列表显示
        self.players_listbox = tk.Listbox(players_frame, height=6, yscrollcommand=player_scrollbar.set)
        self.players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        player_scrollbar.config(command=self.players_listbox.yview)
        
        # 设置列宽度
        form_grid.columnconfigure(1, weight=1)
        
        # 加载战队数据
        self.refresh_teams()
    
    def create_players_page(self):
        players_frame = ttk.Frame(self.notebook)
        self.notebook.add(players_frame, text="选手管理")
        
        # 创建分栏布局
        paned = ttk.PanedWindow(players_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧选手列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 搜索框
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.player_search_var = tk.StringVar()
        self.player_search_entry = ttk.Entry(search_frame, textvariable=self.player_search_var)
        self.player_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_players).pack(side=tk.LEFT, padx=5)
        
        # 选手列表
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树状表格
        self.players_tree = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set)
        self.players_tree["columns"] = ("player_id", "nickname", "team_name", "country")
        self.players_tree.column("#0", width=0, stretch=tk.NO)
        self.players_tree.column("player_id", width=50, anchor=tk.CENTER)
        self.players_tree.column("nickname", width=120)
        self.players_tree.column("team_name", width=120)
        self.players_tree.column("country", width=100, anchor=tk.CENTER)
        
        self.players_tree.heading("#0", text="")
        self.players_tree.heading("player_id", text="ID")
        self.players_tree.heading("nickname", text="游戏ID")
        self.players_tree.heading("team_name", text="所属战队")
        self.players_tree.heading("country", text="国家/地区")
        
        self.players_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.players_tree.yview)
        
        # 绑定选择事件
        self.players_tree.bind("<<TreeviewSelect>>", self.on_player_select)
        
        # 按钮框架
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="添加", command=self.add_player).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑", command=self.edit_player).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除", command=self.delete_player).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_players).pack(side=tk.LEFT, padx=5)
        
        # 右侧详细信息
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # 添加选手详细信息表单
        self.player_detail_frame = ttk.LabelFrame(right_frame, text="选手详细信息")
        self.player_detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建详细信息表单
        form_grid = ttk.Frame(self.player_detail_frame)
        form_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 选手ID
        ttk.Label(form_grid, text="选手ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_id_var = tk.StringVar()
        self.player_id_entry = ttk.Entry(form_grid, textvariable=self.player_id_var, state="readonly")
        self.player_id_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 游戏ID
        ttk.Label(form_grid, text="游戏ID:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_nickname_var = tk.StringVar()
        self.player_nickname_entry = ttk.Entry(form_grid, textvariable=self.player_nickname_var, state="readonly")
        self.player_nickname_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 真实姓名
        ttk.Label(form_grid, text="真实姓名:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_realname_var = tk.StringVar()
        self.player_realname_entry = ttk.Entry(form_grid, textvariable=self.player_realname_var, state="readonly")
        self.player_realname_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 所属战队
        ttk.Label(form_grid, text="所属战队:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_team_var = tk.StringVar()
        self.player_team_entry = ttk.Entry(form_grid, textvariable=self.player_team_var, state="readonly")
        self.player_team_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 国家/地区
        ttk.Label(form_grid, text="国家/地区:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_country_var = tk.StringVar()
        self.player_country_entry = ttk.Entry(form_grid, textvariable=self.player_country_var, state="readonly")
        self.player_country_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 游戏角色
        ttk.Label(form_grid, text="游戏角色:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.player_role_var = tk.StringVar()
        self.player_role_entry = ttk.Entry(form_grid, textvariable=self.player_role_var, state="readonly")
        self.player_role_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_grid.columnconfigure(1, weight=1)
        
        # 加载选手数据
        self.refresh_players()
    
    def create_tournaments_page(self):
        tournaments_frame = ttk.Frame(self.notebook)
        self.notebook.add(tournaments_frame, text="赛事管理")
        
        # 创建分栏布局
        paned = ttk.PanedWindow(tournaments_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧赛事列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 搜索框
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.tournament_search_var = tk.StringVar()
        self.tournament_search_entry = ttk.Entry(search_frame, textvariable=self.tournament_search_var)
        self.tournament_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_tournaments).pack(side=tk.LEFT, padx=5)
        
        # 赛事列表
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树状表格
        self.tournaments_tree = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set)
        self.tournaments_tree["columns"] = ("tournament_id", "tournament_name", "dates", "status")
        self.tournaments_tree.column("#0", width=0, stretch=tk.NO)
        self.tournaments_tree.column("tournament_id", width=50, anchor=tk.CENTER)
        self.tournaments_tree.column("tournament_name", width=200)
        self.tournaments_tree.column("dates", width=150, anchor=tk.CENTER)
        self.tournaments_tree.column("status", width=80, anchor=tk.CENTER)
        
        self.tournaments_tree.heading("#0", text="")
        self.tournaments_tree.heading("tournament_id", text="ID")
        self.tournaments_tree.heading("tournament_name", text="赛事名称")
        self.tournaments_tree.heading("dates", text="日期")
        self.tournaments_tree.heading("status", text="状态")
        
        self.tournaments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tournaments_tree.yview)
        
        # 绑定选择事件
        self.tournaments_tree.bind("<<TreeviewSelect>>", self.on_tournament_select)
        
        # 按钮框架
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="添加", command=self.add_tournament).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑", command=self.edit_tournament).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除", command=self.delete_tournament).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_tournaments).pack(side=tk.LEFT, padx=5)
        
        # 右侧详细信息
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # 添加赛事详细信息表单
        self.tournament_detail_frame = ttk.LabelFrame(right_frame, text="赛事详细信息")
        self.tournament_detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建详细信息表单
        form_grid = ttk.Frame(self.tournament_detail_frame)
        form_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 赛事ID
        ttk.Label(form_grid, text="赛事ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_id_var = tk.StringVar()
        self.tournament_id_entry = ttk.Entry(form_grid, textvariable=self.tournament_id_var, state="readonly")
        self.tournament_id_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 赛事名称
        ttk.Label(form_grid, text="赛事名称:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_name_var = tk.StringVar()
        self.tournament_name_entry = ttk.Entry(form_grid, textvariable=self.tournament_name_var, state="readonly")
        self.tournament_name_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 开始日期
        ttk.Label(form_grid, text="开始日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_start_var = tk.StringVar()
        self.tournament_start_entry = ttk.Entry(form_grid, textvariable=self.tournament_start_var, state="readonly")
        self.tournament_start_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 结束日期
        ttk.Label(form_grid, text="结束日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_end_var = tk.StringVar()
        self.tournament_end_entry = ttk.Entry(form_grid, textvariable=self.tournament_end_var, state="readonly")
        self.tournament_end_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 举办地点
        ttk.Label(form_grid, text="举办地点:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_location_var = tk.StringVar()
        self.tournament_location_entry = ttk.Entry(form_grid, textvariable=self.tournament_location_var, state="readonly")
        self.tournament_location_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 奖金池
        ttk.Label(form_grid, text="奖金池:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_prize_var = tk.StringVar()
        self.tournament_prize_entry = ttk.Entry(form_grid, textvariable=self.tournament_prize_var, state="readonly")
        self.tournament_prize_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 状态
        ttk.Label(form_grid, text="状态:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.tournament_status_var = tk.StringVar()
        self.tournament_status_entry = ttk.Entry(form_grid, textvariable=self.tournament_status_var, state="readonly")
        self.tournament_status_entry.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛列表标签
        ttk.Label(form_grid, text="比赛列表:").grid(row=7, column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        
        # 比赛列表框架
        matches_frame = ttk.Frame(form_grid)
        matches_frame.grid(row=7, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # 比赛列表滚动条
        matches_scrollbar = ttk.Scrollbar(matches_frame)
        matches_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 比赛列表树视图
        self.tournament_matches_tree = ttk.Treeview(matches_frame, height=6, yscrollcommand=matches_scrollbar.set)
        self.tournament_matches_tree["columns"] = ("match_id", "teams", "date", "result")
        self.tournament_matches_tree.column("#0", width=0, stretch=tk.NO)
        self.tournament_matches_tree.column("match_id", width=50, anchor=tk.CENTER)
        self.tournament_matches_tree.column("teams", width=180)
        self.tournament_matches_tree.column("date", width=90, anchor=tk.CENTER)
        self.tournament_matches_tree.column("result", width=80, anchor=tk.CENTER)
        
        self.tournament_matches_tree.heading("#0", text="")
        self.tournament_matches_tree.heading("match_id", text="ID")
        self.tournament_matches_tree.heading("teams", text="对阵")
        self.tournament_matches_tree.heading("date", text="日期")
        self.tournament_matches_tree.heading("result", text="比分")
        
        self.tournament_matches_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        matches_scrollbar.config(command=self.tournament_matches_tree.yview)
        
        # 设置列宽度
        form_grid.columnconfigure(1, weight=1)
        
        # 加载赛事数据
        self.refresh_tournaments()
    
    def create_matches_page(self):
        matches_frame = ttk.Frame(self.notebook)
        self.notebook.add(matches_frame, text="比赛管理")
        
        # 创建分栏布局
        paned = ttk.PanedWindow(matches_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧比赛列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 搜索和筛选框架
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 搜索框
        ttk.Label(search_frame, text="搜索:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_search_var = tk.StringVar()
        self.match_search_entry = ttk.Entry(search_frame, textvariable=self.match_search_var)
        self.match_search_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 赛事筛选
        ttk.Label(search_frame, text="赛事:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_tournament_var = tk.StringVar()
        self.match_tournament_combobox = ttk.Combobox(search_frame, textvariable=self.match_tournament_var, width=28)
        self.match_tournament_combobox.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 战队筛选
        ttk.Label(search_frame, text="战队:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_team_var = tk.StringVar()
        self.match_team_combobox = ttk.Combobox(search_frame, textvariable=self.match_team_var, width=28)
        self.match_team_combobox.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 状态筛选
        ttk.Label(search_frame, text="状态:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_status_var = tk.StringVar()
        self.match_status_combobox = ttk.Combobox(search_frame, textvariable=self.match_status_var, width=28)
        self.match_status_combobox['values'] = ["全部", "未开始", "进行中", "已结束"]
        self.match_status_combobox.current(0)
        self.match_status_combobox.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 搜索按钮
        ttk.Button(search_frame, text="搜索", command=self.search_matches).grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # 设置列宽度
        search_frame.columnconfigure(1, weight=1)
        
        # 比赛列表
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树状表格
        self.matches_tree = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set)
        self.matches_tree["columns"] = ("match_id", "tournament", "teams", "date", "status")
        self.matches_tree.column("#0", width=0, stretch=tk.NO)
        self.matches_tree.column("match_id", width=50, anchor=tk.CENTER)
        self.matches_tree.column("tournament", width=100)
        self.matches_tree.column("teams", width=150)
        self.matches_tree.column("date", width=100, anchor=tk.CENTER)
        self.matches_tree.column("status", width=80, anchor=tk.CENTER)
        
        self.matches_tree.heading("#0", text="")
        self.matches_tree.heading("match_id", text="ID")
        self.matches_tree.heading("tournament", text="赛事")
        self.matches_tree.heading("teams", text="对阵")
        self.matches_tree.heading("date", text="日期")
        self.matches_tree.heading("status", text="状态")
        
        self.matches_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.matches_tree.yview)
        
        # 绑定选择事件
        self.matches_tree.bind("<<TreeviewSelect>>", self.on_match_select)
        
        # 按钮框架
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="添加", command=self.add_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑", command=self.edit_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除", command=self.delete_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_matches).pack(side=tk.LEFT, padx=5)
        
        # 右侧详细信息
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # 添加比赛详细信息表单
        self.match_detail_frame = ttk.LabelFrame(right_frame, text="比赛详细信息")
        self.match_detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建详细信息表单
        form_grid = ttk.Frame(self.match_detail_frame)
        form_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 比赛ID
        ttk.Label(form_grid, text="比赛ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_id_var = tk.StringVar()
        self.match_id_entry = ttk.Entry(form_grid, textvariable=self.match_id_var, state="readonly")
        self.match_id_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 所属赛事
        ttk.Label(form_grid, text="所属赛事:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_tournament_name_var = tk.StringVar()
        self.match_tournament_name_entry = ttk.Entry(form_grid, textvariable=self.match_tournament_name_var, state="readonly")
        self.match_tournament_name_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍1
        ttk.Label(form_grid, text="队伍1:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_team1_var = tk.StringVar()
        self.match_team1_entry = ttk.Entry(form_grid, textvariable=self.match_team1_var, state="readonly")
        self.match_team1_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍2
        ttk.Label(form_grid, text="队伍2:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_team2_var = tk.StringVar()
        self.match_team2_entry = ttk.Entry(form_grid, textvariable=self.match_team2_var, state="readonly")
        self.match_team2_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛日期
        ttk.Label(form_grid, text="比赛日期:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_date_var = tk.StringVar()
        self.match_date_entry = ttk.Entry(form_grid, textvariable=self.match_date_var, state="readonly")
        self.match_date_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛时间
        ttk.Label(form_grid, text="比赛时间:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_time_var = tk.StringVar()
        self.match_time_entry = ttk.Entry(form_grid, textvariable=self.match_time_var, state="readonly")
        self.match_time_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛形式
        ttk.Label(form_grid, text="比赛形式:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_format_var = tk.StringVar()
        self.match_format_entry = ttk.Entry(form_grid, textvariable=self.match_format_var, state="readonly")
        self.match_format_entry.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛状态
        ttk.Label(form_grid, text="比赛状态:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_status_display_var = tk.StringVar()
        self.match_status_display_entry = ttk.Entry(form_grid, textvariable=self.match_status_display_var, state="readonly")
        self.match_status_display_entry.grid(row=7, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛结果
        ttk.Label(form_grid, text="比赛结果:").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.match_result_var = tk.StringVar()
        self.match_result_entry = ttk.Entry(form_grid, textvariable=self.match_result_var, state="readonly")
        self.match_result_entry.grid(row=8, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 地图比赛标签
        ttk.Label(form_grid, text="地图比赛:").grid(row=9, column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        
        # 地图比赛框架
        maps_frame = ttk.Frame(form_grid)
        maps_frame.grid(row=9, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # 地图比赛滚动条
        maps_scrollbar = ttk.Scrollbar(maps_frame)
        maps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 地图比赛列表
        self.map_matches_tree = ttk.Treeview(maps_frame, height=6, yscrollcommand=maps_scrollbar.set)
        self.map_matches_tree["columns"] = ("map_match_id", "map_name", "map_number", "score", "winner")
        self.map_matches_tree.column("#0", width=0, stretch=tk.NO)
        self.map_matches_tree.column("map_match_id", width=50, anchor=tk.CENTER)
        self.map_matches_tree.column("map_name", width=100)
        self.map_matches_tree.column("map_number", width=50, anchor=tk.CENTER)
        self.map_matches_tree.column("score", width=80, anchor=tk.CENTER)
        self.map_matches_tree.column("winner", width=100)
        
        self.map_matches_tree.heading("#0", text="")
        self.map_matches_tree.heading("map_match_id", text="ID")
        self.map_matches_tree.heading("map_name", text="地图")
        self.map_matches_tree.heading("map_number", text="序号")
        self.map_matches_tree.heading("score", text="比分")
        self.map_matches_tree.heading("winner", text="获胜方")
        
        self.map_matches_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        maps_scrollbar.config(command=self.map_matches_tree.yview)
        
        # 地图比赛操作按钮
        map_buttons_frame = ttk.Frame(form_grid)
        map_buttons_frame.grid(row=10, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(map_buttons_frame, text="添加地图", command=self.add_map_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(map_buttons_frame, text="编辑地图", command=self.edit_map_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(map_buttons_frame, text="删除地图", command=self.delete_map_match).pack(side=tk.LEFT, padx=5)
        
        # 设置列宽度
        form_grid.columnconfigure(1, weight=1)
        
        # 加载比赛数据和筛选选项
        self.load_filter_options()
        self.refresh_matches()
    
    # 战队相关方法
    def search_teams(self):
        keyword = self.team_search_var.get()
        if keyword:
            teams = model.Team.search(keyword)
        else:
            teams = model.Team.get_all()
        self.update_teams_tree(teams)
    
    def refresh_teams(self):
        teams = model.Team.get_all()
        self.update_teams_tree(teams)
    
    def update_teams_tree(self, teams):
        # 清空树
        for item in self.teams_tree.get_children():
            self.teams_tree.delete(item)
        
        # 添加数据
        for team in teams:
            self.teams_tree.insert("", tk.END, values=(team.team_id, team.team_name, team.country))
    
    def add_team(self):
        """添加新战队的对话框"""
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加战队")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 战队名称
        ttk.Label(form_frame, text="战队名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 国家/地区
        ttk.Label(form_frame, text="国家/地区:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        country_var = tk.StringVar()
        country_entry = ttk.Entry(form_frame, textvariable=country_var, width=30)
        country_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Logo URL
        ttk.Label(form_frame, text="Logo URL:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        logo_var = tk.StringVar()
        logo_entry = ttk.Entry(form_frame, textvariable=logo_var, width=30)
        logo_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 简介
        ttk.Label(form_frame, text="简介:").grid(row=3, column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        desc_text = tk.Text(form_frame, height=6, width=30)
        desc_text.grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_team():
            # 获取表单数据
            team_name = name_var.get().strip()
            country = country_var.get().strip()
            logo_url = logo_var.get().strip()
            description = desc_text.get(1.0, tk.END).strip()
            
            # 验证数据
            if not team_name:
                messagebox.showwarning("警告", "战队名称不能为空")
                return
            
            # 创建新战队对象
            team = model.Team(
                team_name=team_name,
                country=country if country else None,
                logo_url=logo_url if logo_url else None,
                description=description if description else None
            )
            
            # 保存到数据库
            try:
                success = team.save()
                if success:
                    messagebox.showinfo("成功", f"战队 '{team_name}' 添加成功！")
                    dialog.destroy()
                    self.refresh_teams()  # 刷新战队列表
                else:
                    messagebox.showerror("错误", "保存战队信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加战队时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_team).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        name_entry.focus_set()
    
    def edit_team(self):
        """编辑战队信息的对话框"""
        # 检查是否有选中的战队
        selected_items = self.teams_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要编辑的战队")
            return
            
        # 获取选中行的战队ID
        item = selected_items[0]
        team_id = self.teams_tree.item(item, "values")[0]
        
        # 获取战队对象
        team = model.Team.get_by_id(team_id)
        if not team:
            messagebox.showerror("错误", "找不到指定的战队")
            return
        
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑战队 - {team.team_name}")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 战队名称
        ttk.Label(form_frame, text="战队名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar(value=team.team_name)
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 国家/地区
        ttk.Label(form_frame, text="国家/地区:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        country_var = tk.StringVar(value=team.country if team.country else "")
        country_entry = ttk.Entry(form_frame, textvariable=country_var, width=30)
        country_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Logo URL
        ttk.Label(form_frame, text="Logo URL:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        logo_var = tk.StringVar(value=team.logo_url if team.logo_url else "")
        logo_entry = ttk.Entry(form_frame, textvariable=logo_var, width=30)
        logo_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 简介
        ttk.Label(form_frame, text="简介:").grid(row=3, column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        desc_text = tk.Text(form_frame, height=6, width=30)
        if team.description:
            desc_text.insert(tk.END, team.description)
        desc_text.grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_team():
            # 获取表单数据
            team_name = name_var.get().strip()
            country = country_var.get().strip()
            logo_url = logo_var.get().strip()
            description = desc_text.get(1.0, tk.END).strip()
            
            # 验证数据
            if not team_name:
                messagebox.showwarning("警告", "战队名称不能为空")
                return
            
            # 更新战队对象
            team.team_name = team_name
            team.country = country if country else None
            team.logo_url = logo_url if logo_url else None
            team.description = description if description else None
            
            # 保存到数据库
            try:
                success = team.save()
                if success:
                    messagebox.showinfo("成功", f"战队 '{team_name}' 更新成功！")
                    dialog.destroy()
                    self.refresh_teams()  # 刷新战队列表
                    self.on_team_select(None)  # 刷新详情显示
                else:
                    messagebox.showerror("错误", "保存战队信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新战队时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_team).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        name_entry.focus_set()
    
    def delete_team(self):
        """删除选中的战队"""
        selected_items = self.teams_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的战队")
            return
        
        # 获取选中行的战队ID和名称
        item = selected_items[0]
        team_values = self.teams_tree.item(item, "values")
        team_id = team_values[0]
        team_name = team_values[1]
        
        # 确认删除
        confirm = messagebox.askyesno(
            "确认删除", 
            f"确定要删除战队 '{team_name}' 吗？\n\n"
            "这将同时处理与该战队相关的所有数据，包括选手关联和比赛记录。\n"
            "此操作不可恢复！"
        )
        
        if not confirm:
            return
        
        # 获取战队对象
        team = model.Team.get_by_id(team_id)
        if not team:
            messagebox.showerror("错误", "找不到指定的战队")
            return
        
        # 使用事务删除战队及相关数据
        self.status_var.set("正在删除战队数据...")
        self.root.update()  # 更新界面
        
        success, message = team.delete_with_transaction()
        
        if success:
            messagebox.showinfo("成功", message)
            self.refresh_teams()  # 刷新战队列表
        else:
            messagebox.showerror("删除失败", message)
        
        self.status_var.set("就绪")
    
    # 其他方法实现
    def import_data(self):
        # 实现数据导入功能
        pass
    
    def export_data(self):
        # 实现数据导出功能
        pass
    
    def show_help(self):
        # 显示帮助信息
        messagebox.showinfo("使用说明", "CS2赛事管理系统使用说明...\n\n本系统用于管理CS2电竞赛事、战队、选手和比赛数据。")
    
    def show_about(self):
        # 显示关于信息
        messagebox.showinfo("关于", "CS2赛事管理系统 v1.0\n\n一个用于管理CS2赛事信息的系统")

    def on_team_select(self, event):
        """当在树状图中选择一个战队时显示详细信息"""
        selected_items = self.teams_tree.selection()
        if not selected_items:
            return
            
        # 获取选中行的战队ID
        item = selected_items[0]
        team_id = self.teams_tree.item(item, "values")[0]
        
        # 获取战队详情
        team = model.Team.get_by_id(team_id)
        if not team:
            messagebox.showerror("错误", "无法获取战队信息")
            return
        
        # 更新表单显示战队信息
        self.team_id_var.set(team.team_id)
        self.team_name_var.set(team.team_name)
        self.team_country_var.set(team.country if team.country else "")
        self.team_logo_var.set(team.logo_url if team.logo_url else "")
        
        # 更新简介
        self.team_desc_text.config(state="normal")
        self.team_desc_text.delete(1.0, tk.END)
        if team.description:
            self.team_desc_text.insert(tk.END, team.description)
        self.team_desc_text.config(state="disabled")
        
        # 加载战队成员
        self.players_listbox.delete(0, tk.END)
        players = model.Player.get_by_team(team.team_id)
        if players:
            for player in players:
                display_text = f"{player.nickname} ({player.real_name})" if player.real_name else player.nickname
                self.players_listbox.insert(tk.END, display_text)
        else:
            self.players_listbox.insert(tk.END, "暂无队员信息")

    # 选手相关方法
    def search_players(self):
        keyword = self.player_search_var.get()
        if keyword:
            players = model.Player.search(keyword)
        else:
            players = model.Player.get_all()
        self.update_players_tree(players)
    
    def refresh_players(self):
        players = model.Player.get_all()
        self.update_players_tree(players)
    
    def update_players_tree(self, players):
        # 清空树
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)
        
        # 添加数据
        for player in players:
            # 获取战队名称（如果有）
            team_name = ""
            if player.team_id:
                team = model.Team.get_by_id(player.team_id)
                if team:
                    team_name = team.team_name
            
            self.players_tree.insert("", tk.END, values=(
                player.player_id, 
                player.nickname, 
                team_name, 
                player.country if player.country else ""
            ))
    
    def on_player_select(self, event):
        """当在树状图中选择一个选手时显示详细信息"""
        selected_items = self.players_tree.selection()
        if not selected_items:
            # 如果没有选中项，清空详情显示
            self.player_id_var.set("")
            self.player_nickname_var.set("")
            self.player_realname_var.set("")
            self.player_team_var.set("")
            self.player_country_var.set("")
            self.player_role_var.set("")
            return
            
        # 获取选中行的选手ID
        item = selected_items[0]
        player_id = self.players_tree.item(item, "values")[0]
        
        # 获取选手详情
        player = model.Player.get_by_id(player_id)
        if not player:
            messagebox.showerror("错误", "无法获取选手信息")
            return
        
        # 更新表单显示选手信息
        self.player_id_var.set(player.player_id)
        self.player_nickname_var.set(player.nickname)
        self.player_realname_var.set(player.real_name if player.real_name else "")
        self.player_country_var.set(player.country if player.country else "")
        self.player_role_var.set(player.role if player.role else "")
        
        # 获取并显示战队信息
        team_name = "无战队"
        if player.team_id:
            team = model.Team.get_by_id(player.team_id)
            if team:
                team_name = team.team_name
        
        self.player_team_var.set(team_name)
    
    def add_player(self):
        """添加新选手的对话框"""
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加选手")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 游戏ID
        ttk.Label(form_frame, text="游戏ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        nickname_var = tk.StringVar()
        nickname_entry = ttk.Entry(form_frame, textvariable=nickname_var, width=30)
        nickname_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 真实姓名
        ttk.Label(form_frame, text="真实姓名:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        realname_var = tk.StringVar()
        realname_entry = ttk.Entry(form_frame, textvariable=realname_var, width=30)
        realname_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 所属战队
        ttk.Label(form_frame, text="所属战队:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        team_id_var = tk.StringVar()
        team_combobox = ttk.Combobox(form_frame, textvariable=team_id_var, width=28)
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_options = [("", "无战队")]  # 添加无战队选项
        if teams:
            for team in teams:
                team_options.append((str(team.team_id), team.team_name))
        
        team_combobox['values'] = [option[1] for option in team_options]
        team_combobox.current(0)  # 默认选择第一个
        team_combobox.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 国家/地区
        ttk.Label(form_frame, text="国家/地区:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        country_var = tk.StringVar()
        country_entry = ttk.Entry(form_frame, textvariable=country_var, width=30)
        country_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 游戏角色
        ttk.Label(form_frame, text="游戏角色:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        role_var = tk.StringVar()
        role_combobox = ttk.Combobox(form_frame, textvariable=role_var, width=28)
        role_combobox['values'] = ["步枪手", "狙击手", "指挥"]
        role_combobox.current(0)
        role_combobox.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_player():
            # 获取表单数据
            nickname = nickname_var.get().strip()
            real_name = realname_var.get().strip()
            country = country_var.get().strip()
            role = role_var.get().strip()
            
            # 获取选择的战队ID
            selected_team_name = team_combobox.get()
            team_id = None
            for option in team_options:
                if option[1] == selected_team_name and option[0]:
                    team_id = int(option[0])
                    break
            
            # 验证数据
            if not nickname:
                messagebox.showwarning("警告", "游戏ID不能为空")
                return
            
            # 创建新选手对象
            player = model.Player(
                nickname=nickname,
                real_name=real_name if real_name else None,
                team_id=team_id,
                country=country if country else None,
                role=role if role else None
            )
            
            # 保存到数据库
            try:
                success = player.save()
                if success:
                    messagebox.showinfo("成功", f"选手 '{nickname}' 添加成功！")
                    dialog.destroy()
                    self.refresh_players()  # 刷新选手列表
                else:
                    messagebox.showerror("错误", "保存选手信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加选手时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_player).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        nickname_entry.focus_set()
    
    def edit_player(self):
        """编辑选手信息的对话框"""
        # 检查是否有选中的选手
        selected_items = self.players_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要编辑的选手")
            return
            
        # 获取选中行的选手ID
        item = selected_items[0]
        player_id = self.players_tree.item(item, "values")[0]
        
        # 获取选手对象
        player = model.Player.get_by_id(player_id)
        if not player:
            messagebox.showerror("错误", "找不到指定的选手")
            return
        
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑选手 - {player.nickname}")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 游戏ID
        ttk.Label(form_frame, text="游戏ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        nickname_var = tk.StringVar(value=player.nickname)
        nickname_entry = ttk.Entry(form_frame, textvariable=nickname_var, width=30)
        nickname_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 真实姓名
        ttk.Label(form_frame, text="真实姓名:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        realname_var = tk.StringVar(value=player.real_name if player.real_name else "")
        realname_entry = ttk.Entry(form_frame, textvariable=realname_var, width=30)
        realname_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 所属战队
        ttk.Label(form_frame, text="所属战队:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        team_id_var = tk.StringVar()
        team_combobox = ttk.Combobox(form_frame, textvariable=team_id_var, width=28)
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_options = [("", "无战队")]  # 添加无战队选项
        if teams:
            for team in teams:
                team_options.append((str(team.team_id), team.team_name))
        
        team_combobox['values'] = [option[1] for option in team_options]
        
        # 设置当前选手的战队
        current_index = 0  # 默认为"无战队"
        if player.team_id:
            for i, option in enumerate(team_options):
                if option[0] and int(option[0]) == player.team_id:
                    current_index = i
                    break
        
        team_combobox.current(current_index)
        team_combobox.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 国家/地区
        ttk.Label(form_frame, text="国家/地区:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        country_var = tk.StringVar(value=player.country if player.country else "")
        country_entry = ttk.Entry(form_frame, textvariable=country_var, width=30)
        country_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 游戏角色
        ttk.Label(form_frame, text="游戏角色:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        role_var = tk.StringVar(value=player.role if player.role else "")
        role_combobox = ttk.Combobox(form_frame, textvariable=role_var, width=28)
        role_combobox['values'] = ["步枪手", "狙击手", "指挥"]
        
        # 设置当前角色
        if player.role and player.role in role_combobox['values']:
            role_combobox.set(player.role)
        else:
            role_combobox.current(0)
            
        role_combobox.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_player():
            # 获取表单数据
            nickname = nickname_var.get().strip()
            real_name = realname_var.get().strip()
            country = country_var.get().strip()
            role = role_var.get().strip()
            
            # 获取选择的战队ID
            selected_team_name = team_combobox.get()
            team_id = None
            for option in team_options:
                if option[1] == selected_team_name and option[0]:
                    team_id = int(option[0])
                    break
            
            # 验证数据
            if not nickname:
                messagebox.showwarning("警告", "游戏ID不能为空")
                return
            
            # 更新选手对象
            player.nickname = nickname
            player.real_name = real_name if real_name else None
            player.team_id = team_id
            player.country = country if country else None
            player.role = role if role else None
            
            # 保存到数据库
            try:
                success = player.save()
                if success:
                    messagebox.showinfo("成功", f"选手 '{nickname}' 更新成功！")
                    dialog.destroy()
                    self.refresh_players()  # 刷新选手列表
                    self.on_player_select(None)  # 刷新详情显示
                else:
                    messagebox.showerror("错误", "保存选手信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新选手时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_player).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        nickname_entry.focus_set()
    
    def delete_player(self):
        """删除选中的选手"""
        selected_items = self.players_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的选手")
            return
        
        # 获取选中行的选手ID和名称
        item = selected_items[0]
        player_values = self.players_tree.item(item, "values")
        player_id = player_values[0]
        player_nickname = player_values[1]
        
        # 确认删除
        confirm = messagebox.askyesno(
            "确认删除", 
            f"确定要删除选手 '{player_nickname}' 吗？\n此操作不可恢复！"
        )
        
        if not confirm:
            return
        
        # 获取选手对象
        player = model.Player.get_by_id(player_id)
        if not player:
            messagebox.showerror("错误", "找不到指定的选手")
            return
        
        # 删除选手
        try:
            success = player.delete()
            if success:
                messagebox.showinfo("成功", f"选手 '{player_nickname}' 已成功删除！")
                self.refresh_players()  # 刷新选手列表
            else:
                messagebox.showerror("删除失败", "无法删除选手数据")
        except Exception as e:
            messagebox.showerror("错误", f"删除选手时出错: {str(e)}")

    def search_tournaments(self):
        keyword = self.tournament_search_var.get()
        if keyword:
            tournaments = model.Tournament.search(keyword)
        else:
            tournaments = model.Tournament.get_all()
        self.update_tournaments_tree(tournaments)
    
    def refresh_tournaments(self):
        tournaments = model.Tournament.get_all()
        self.update_tournaments_tree(tournaments)
    
    def update_tournaments_tree(self, tournaments):
        # 清空树
        for item in self.tournaments_tree.get_children():
            self.tournaments_tree.delete(item)
        
        # 添加数据
        for tournament in tournaments:
            self.tournaments_tree.insert("", tk.END, values=(
                tournament.tournament_id, 
                tournament.tournament_name, 
                f"{tournament.start_date} - {tournament.end_date}", 
                tournament.status
            ))
    
    def on_tournament_select(self, event):
        """当在树状图中选择一个赛事时显示详细信息"""
        selected_items = self.tournaments_tree.selection()
        if not selected_items:
            # 如果没有选中项，清空详情显示
            self.tournament_id_var.set("")
            self.tournament_name_var.set("")
            self.tournament_start_var.set("")
            self.tournament_end_var.set("")
            self.tournament_location_var.set("")
            self.tournament_prize_var.set("")
            self.tournament_status_var.set("")
            # 清空比赛列表
            for item in self.tournament_matches_tree.get_children():
                self.tournament_matches_tree.delete(item)
            return
            
        # 获取选中行的赛事ID
        item = selected_items[0]
        tournament_id = self.tournaments_tree.item(item, "values")[0]
        
        # 获取赛事详情
        tournament = model.Tournament.get_by_id(tournament_id)
        if not tournament:
            messagebox.showerror("错误", "无法获取赛事信息")
            return
        
        # 更新表单显示赛事信息
        self.tournament_id_var.set(tournament.tournament_id)
        self.tournament_name_var.set(tournament.tournament_name)
        self.tournament_start_var.set(tournament.start_date)
        self.tournament_end_var.set(tournament.end_date)
        self.tournament_location_var.set(tournament.location if tournament.location else "")
        self.tournament_prize_var.set(tournament.prize_pool if tournament.prize_pool else "")
        self.tournament_status_var.set(tournament.status if tournament.status else "")
        
        # 加载赛事的比赛
        self.load_tournament_matches(tournament.tournament_id)
    
    def load_tournament_matches(self, tournament_id):
        """加载赛事的比赛列表"""
        # 清空比赛列表
        for item in self.tournament_matches_tree.get_children():
            self.tournament_matches_tree.delete(item)
        
        # 获取比赛列表
        matches = model.Match.get_by_tournament(tournament_id)
        
        if not matches:
            self.tournament_matches_tree.insert("", tk.END, values=("", "暂无比赛信息", "", ""))
            return
        
        # 添加比赛数据
        for match in matches:
            # 获取队伍名称
            team1_name = "待定"
            team2_name = "待定"
            
            if match.team1_id:
                team1 = model.Team.get_by_id(match.team1_id)
                if team1:
                    team1_name = team1.team_name
            
            if match.team2_id:
                team2 = model.Team.get_by_id(match.team2_id)
                if team2:
                    team2_name = team2.team_name
            
            # 获取比赛结果
            result = "未进行"
            if match.status == "已结束":
                result = f"{match.score_team1}:{match.score_team2}"
            
            teams_display = f"{team1_name} vs {team2_name}"
            
            self.tournament_matches_tree.insert("", tk.END, values=(
                match.match_id,
                teams_display,
                match.match_date,
                result
            ))
    
    def add_tournament(self):
        """添加新赛事的对话框"""
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加赛事")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 赛事名称
        ttk.Label(form_frame, text="赛事名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 开始日期
        ttk.Label(form_frame, text="开始日期:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        start_var = tk.StringVar()
        start_entry = ttk.Entry(form_frame, textvariable=start_var, width=30)
        start_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # 结束日期
        ttk.Label(form_frame, text="结束日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        end_var = tk.StringVar()
        end_entry = ttk.Entry(form_frame, textvariable=end_var, width=30)
        end_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # 举办地点
        ttk.Label(form_frame, text="举办地点:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        location_var = tk.StringVar()
        location_entry = ttk.Entry(form_frame, textvariable=location_var, width=30)
        location_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 奖金池
        ttk.Label(form_frame, text="奖金池:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        prize_var = tk.StringVar()
        prize_entry = ttk.Entry(form_frame, textvariable=prize_var, width=30)
        prize_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 状态
        ttk.Label(form_frame, text="状态:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(form_frame, textvariable=status_var, width=28)
        status_combobox['values'] = ["未开始", "进行中", "已结束"]
        status_combobox.current(0)
        status_combobox.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_tournament():
            # 获取表单数据
            tournament_name = name_var.get().strip()
            start_date = start_var.get().strip()
            end_date = end_var.get().strip()
            location = location_var.get().strip()
            prize_pool = prize_var.get().strip()
            status = status_var.get()
            
            # 验证数据
            if not tournament_name:
                messagebox.showwarning("警告", "赛事名称不能为空")
                return
            
            if not start_date or not end_date:
                messagebox.showwarning("警告", "赛事日期不能为空")
                return
            
            # 创建新赛事对象
            tournament = model.Tournament(
                tournament_name=tournament_name,
                start_date=start_date,
                end_date=end_date,
                location=location if location else None,
                prize_pool=prize_pool if prize_pool else None,
                status=status
            )
            
            # 保存到数据库
            try:
                success = tournament.save()
                if success:
                    messagebox.showinfo("成功", f"赛事 '{tournament_name}' 添加成功！")
                    dialog.destroy()
                    self.refresh_tournaments()  # 刷新赛事列表
                else:
                    messagebox.showerror("错误", "保存赛事信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加赛事时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_tournament).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        name_entry.focus_set()
    
    def edit_tournament(self):
        """编辑赛事信息的对话框"""
        # 检查是否有选中的赛事
        selected_items = self.tournaments_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要编辑的赛事")
            return
            
        # 获取选中行的赛事ID
        item = selected_items[0]
        tournament_id = self.tournaments_tree.item(item, "values")[0]
        
        # 获取赛事对象
        tournament = model.Tournament.get_by_id(tournament_id)
        if not tournament:
            messagebox.showerror("错误", "找不到指定的赛事")
            return
        
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑赛事 - {tournament.tournament_name}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 赛事名称
        ttk.Label(form_frame, text="赛事名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar(value=tournament.tournament_name)
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 开始日期
        ttk.Label(form_frame, text="开始日期:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        start_var = tk.StringVar(value=tournament.start_date)
        start_entry = ttk.Entry(form_frame, textvariable=start_var, width=30)
        start_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # 结束日期
        ttk.Label(form_frame, text="结束日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        end_var = tk.StringVar(value=tournament.end_date)
        end_entry = ttk.Entry(form_frame, textvariable=end_var, width=30)
        end_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # 举办地点
        ttk.Label(form_frame, text="举办地点:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        location_var = tk.StringVar(value=tournament.location if tournament.location else "")
        location_entry = ttk.Entry(form_frame, textvariable=location_var, width=30)
        location_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 奖金池
        ttk.Label(form_frame, text="奖金池:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        prize_var = tk.StringVar(value=tournament.prize_pool if tournament.prize_pool else "")
        prize_entry = ttk.Entry(form_frame, textvariable=prize_var, width=30)
        prize_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 状态
        ttk.Label(form_frame, text="状态:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        status_var = tk.StringVar(value=tournament.status if tournament.status else "未开始")
        status_combobox = ttk.Combobox(form_frame, textvariable=status_var, width=28)
        status_combobox['values'] = ["未开始", "进行中", "已结束"]
        
        # 设置当前状态
        if tournament.status and tournament.status in status_combobox['values']:
            status_combobox.set(tournament.status)
        else:
            status_combobox.current(0)
            
        status_combobox.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_tournament():
            # 获取表单数据
            tournament_name = name_var.get().strip()
            start_date = start_var.get().strip()
            end_date = end_var.get().strip()
            location = location_var.get().strip()
            prize_pool = prize_var.get().strip()
            status = status_var.get()
            
            # 验证数据
            if not tournament_name:
                messagebox.showwarning("警告", "赛事名称不能为空")
                return
            
            if not start_date or not end_date:
                messagebox.showwarning("警告", "赛事日期不能为空")
                return
            
            # 更新赛事对象
            tournament.tournament_name = tournament_name
            tournament.start_date = start_date
            tournament.end_date = end_date
            tournament.location = location if location else None
            tournament.prize_pool = prize_pool if prize_pool else None
            tournament.status = status
            
            # 保存到数据库
            try:
                success = tournament.save()
                if success:
                    messagebox.showinfo("成功", f"赛事 '{tournament_name}' 更新成功！")
                    dialog.destroy()
                    self.refresh_tournaments()  # 刷新赛事列表
                    self.on_tournament_select(None)  # 刷新详情显示
                else:
                    messagebox.showerror("错误", "保存赛事信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新赛事时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_tournament).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        name_entry.focus_set()
    
    def delete_tournament(self):
        """删除选中的赛事"""
        selected_items = self.tournaments_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的赛事")
            return
        
        # 获取选中行的赛事ID和名称
        item = selected_items[0]
        tournament_values = self.tournaments_tree.item(item, "values")
        tournament_id = tournament_values[0]
        tournament_name = tournament_values[1]
        
        # 确认删除
        confirm = messagebox.askyesno(
            "确认删除", 
            f"确定要删除赛事 '{tournament_name}' 吗？\n\n"
            "这将同时删除该赛事的所有比赛记录。\n"
            "此操作不可恢复！"
        )
        
        if not confirm:
            return
        
        # 获取赛事对象
        tournament = model.Tournament.get_by_id(tournament_id)
        if not tournament:
            messagebox.showerror("错误", "找不到指定的赛事")
            return
        
        # 删除赛事
        try:
            success = tournament.delete()
            if success:
                messagebox.showinfo("成功", f"赛事 '{tournament_name}' 已成功删除！")
                self.refresh_tournaments()  # 刷新赛事列表
            else:
                messagebox.showerror("删除失败", "无法删除赛事数据")
        except Exception as e:
            messagebox.showerror("错误", f"删除赛事时出错: {str(e)}")

    def search_matches(self):
        keyword = self.match_search_var.get()
        tournament_id = self.match_tournament_var.get()
        team_id = self.match_team_var.get()
        status = self.match_status_var.get()
        matches = model.Match.search(keyword, tournament_id, team_id, status)
        self.update_matches_tree(matches)
    
    def refresh_matches(self):
        matches = model.Match.get_all()
        self.update_matches_tree(matches)
    
    def update_matches_tree(self, matches):
        # 清空树
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
        
        # 添加数据
        for match in matches:
            self.matches_tree.insert("", tk.END, values=(
                match.match_id,
                match.tournament.tournament_name,
                f"{match.team1.team_name} vs {match.team2.team_name}",
                match.match_date,
                match.status
            ))
    
    def on_match_select(self, event):
        """当在树状图中选择一个比赛时显示详细信息"""
        selected_items = self.matches_tree.selection()
        if not selected_items:
            return
        
        # 获取选中行的比赛ID
        item = selected_items[0]
        match_id = self.matches_tree.item(item, "values")[0]
        
        # 获取比赛详情
        match = model.Match.get_by_id(match_id)
        if not match:
            messagebox.showerror("错误", "无法获取比赛信息")
            return
        
        # 更新表单显示比赛信息
        self.match_id_var.set(match.match_id)
        self.match_tournament_name_var.set(match.tournament.tournament_name)
        self.match_team1_var.set(match.team1.team_name)
        self.match_team2_var.set(match.team2.team_name)
        self.match_date_var.set(match.match_date)
        self.match_time_var.set(match.match_time)
        self.match_format_var.set(match.format)
        self.match_status_display_var.set(match.status)
        self.match_result_var.set(f"{match.score_team1}:{match.score_team2}")
        
        # 加载比赛的地图
        self.load_match_maps(match.match_id)
    
    def load_match_maps(self, match_id):
        """加载比赛的地图"""
        # 清空地图列表
        for item in self.map_matches_tree.get_children():
            self.map_matches_tree.delete(item)
        
        # 获取地图列表
        maps = model.Map.get_by_match(match_id)
        
        if not maps:
            self.map_matches_tree.insert("", tk.END, values=("", "暂无地图信息", "", "", ""))
            return
        
        # 添加地图数据
        for map in maps:
            self.map_matches_tree.insert("", tk.END, values=(
                map.map_match_id,
                map.map_name,
                map.map_number,
                map.score,
                map.winner.team_name
            ))
    
    def add_match(self):
        """添加新比赛的对话框"""
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加比赛")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 所属赛事
        ttk.Label(form_frame, text="所属赛事:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tournament_id_var = tk.StringVar()
        tournament_combobox = ttk.Combobox(form_frame, textvariable=tournament_id_var, width=28)
        
        # 获取所有赛事
        tournaments = model.Tournament.get_all()
        tournament_options = [("", "无赛事")]  # 添加无赛事选项
        if tournaments:
            for tournament in tournaments:
                tournament_options.append((str(tournament.tournament_id), tournament.tournament_name))
        
        tournament_combobox['values'] = [option[1] for option in tournament_options]
        tournament_combobox.current(0)  # 默认选择第一个
        tournament_combobox.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍1
        ttk.Label(form_frame, text="队伍1:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        team1_id_var = tk.StringVar()
        team1_combobox = ttk.Combobox(form_frame, textvariable=team1_id_var, width=28)
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_options = [("", "无战队")]  # 添加无战队选项
        if teams:
            for team in teams:
                team_options.append((str(team.team_id), team.team_name))
        
        team1_combobox['values'] = [option[1] for option in team_options]
        team1_combobox.current(0)  # 默认选择第一个
        team1_combobox.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍2
        ttk.Label(form_frame, text="队伍2:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        team2_id_var = tk.StringVar()
        team2_combobox = ttk.Combobox(form_frame, textvariable=team2_id_var, width=28)
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_options = [("", "无战队")]  # 添加无战队选项
        if teams:
            for team in teams:
                team_options.append((str(team.team_id), team.team_name))
        
        team2_combobox['values'] = [option[1] for option in team_options]
        team2_combobox.current(0)  # 默认选择第一个
        team2_combobox.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛日期
        ttk.Label(form_frame, text="比赛日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        date_var = tk.StringVar()
        date_entry = ttk.Entry(form_frame, textvariable=date_var, width=30)
        date_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=3, column=2, sticky=tk.W, padx=5)
        
        # 比赛时间
        ttk.Label(form_frame, text="比赛时间:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(form_frame, textvariable=time_var, width=30)
        time_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(HH:MM)").grid(row=4, column=2, sticky=tk.W, padx=5)
        
        # 比赛形式
        ttk.Label(form_frame, text="比赛形式:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        format_var = tk.StringVar()
        format_entry = ttk.Entry(form_frame, textvariable=format_var, width=30)
        format_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛状态
        ttk.Label(form_frame, text="比赛状态:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(form_frame, textvariable=status_var, width=28)
        status_combobox['values'] = ["未开始", "进行中", "已结束"]
        status_combobox.current(0)
        status_combobox.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_match():
            # 获取表单数据
            tournament_id = tournament_combobox.get()
            team1_id = team1_combobox.get()
            team2_id = team2_combobox.get()
            date = date_var.get().strip()
            time = time_var.get().strip()
            format = format_var.get().strip()
            status = status_var.get()
            
            # 验证数据
            if not tournament_id or not team1_id or not team2_id:
                messagebox.showwarning("警告", "赛事、队伍1或队伍2不能为空")
                return
            
            if not date or not time:
                messagebox.showwarning("警告", "比赛日期和时间不能为空")
                return
            
            if not format:
                messagebox.showwarning("警告", "比赛形式不能为空")
                return
            
            # 创建新比赛对象
            match = model.Match(
                tournament_id=tournament_id,
                team1_id=team1_id,
                team2_id=team2_id,
                match_date=date,
                match_time=time,
                format=format,
                status=status
            )
            
            # 保存到数据库
            try:
                success = match.save()
                if success:
                    messagebox.showinfo("成功", f"比赛 '{tournament_id} vs {team1_id} vs {team2_id}' 添加成功！")
                    dialog.destroy()
                    self.refresh_matches()  # 刷新比赛列表
                else:
                    messagebox.showerror("错误", "保存比赛信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加比赛时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_match).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        tournament_combobox.focus_set()
    
    def edit_match(self):
        """编辑比赛信息的对话框"""
        # 检查是否有选中的比赛
        selected_items = self.matches_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要编辑的比赛")
            return
        
        # 获取选中行的比赛ID
        item = selected_items[0]
        match_id = self.matches_tree.item(item, "values")[0]
        
        # 获取比赛详情
        match = model.Match.get_by_id(match_id)
        if not match:
            messagebox.showerror("错误", "找不到指定的比赛")
            return
        
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑比赛 - {match.tournament.tournament_name} vs {match.team1.team_name} vs {match.team2.team_name}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 所属赛事
        ttk.Label(form_frame, text="所属赛事:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tournament_id_var = tk.StringVar(value=match.tournament.tournament_id)
        tournament_combobox = ttk.Combobox(form_frame, textvariable=tournament_id_var, width=28)
        
        # 获取所有赛事
        tournaments = model.Tournament.get_all()
        tournament_options = [("", "无赛事")]  # 添加无赛事选项
        if tournaments:
            for tournament in tournaments:
                tournament_options.append((str(tournament.tournament_id), tournament.tournament_name))
        
        tournament_combobox['values'] = [option[1] for option in tournament_options]
        
        # 设置当前比赛的赛事
        current_index = 0  # 默认为"无赛事"
        if match.tournament:
            for i, option in enumerate(tournament_options):
                if option[0] and int(option[0]) == match.tournament.tournament_id:
                    current_index = i
                    break
        
        tournament_combobox.current(current_index)
        tournament_combobox.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍1
        ttk.Label(form_frame, text="队伍1:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        team1_id_var = tk.StringVar(value=match.team1.team_id)
        team1_combobox = ttk.Combobox(form_frame, textvariable=team1_id_var, width=28)
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_options = [("", "无战队")]  # 添加无战队选项
        if teams:
            for team in teams:
                team_options.append((str(team.team_id), team.team_name))
        
        team1_combobox['values'] = [option[1] for option in team_options]
        
        # 设置当前比赛的队伍1
        current_index = 0  # 默认为"无战队"
        if match.team1:
            for i, option in enumerate(team_options):
                if option[0] and int(option[0]) == match.team1.team_id:
                    current_index = i
                    break
        
        team1_combobox.current(current_index)
        team1_combobox.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍2
        ttk.Label(form_frame, text="队伍2:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        team2_id_var = tk.StringVar(value=match.team2.team_id)
        team2_combobox = ttk.Combobox(form_frame, textvariable=team2_id_var, width=28)
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_options = [("", "无战队")]  # 添加无战队选项
        if teams:
            for team in teams:
                team_options.append((str(team.team_id), team.team_name))
        
        team2_combobox['values'] = [option[1] for option in team_options]
        
        # 设置当前比赛的队伍2
        current_index = 0  # 默认为"无战队"
        if match.team2:
            for i, option in enumerate(team_options):
                if option[0] and int(option[0]) == match.team2.team_id:
                    current_index = i
                    break
        
        team2_combobox.current(current_index)
        team2_combobox.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛日期
        ttk.Label(form_frame, text="比赛日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        date_var = tk.StringVar(value=match.match_date)
        date_entry = ttk.Entry(form_frame, textvariable=date_var, width=30)
        date_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=3, column=2, sticky=tk.W, padx=5)
        
        # 比赛时间
        ttk.Label(form_frame, text="比赛时间:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        time_var = tk.StringVar(value=match.match_time)
        time_entry = ttk.Entry(form_frame, textvariable=time_var, width=30)
        time_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(form_frame, text="(HH:MM)").grid(row=4, column=2, sticky=tk.W, padx=5)
        
        # 比赛形式
        ttk.Label(form_frame, text="比赛形式:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        format_var = tk.StringVar(value=match.format)
        format_entry = ttk.Entry(form_frame, textvariable=format_var, width=30)
        format_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛状态
        ttk.Label(form_frame, text="比赛状态:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        status_var = tk.StringVar(value=match.status)
        status_combobox = ttk.Combobox(form_frame, textvariable=status_var, width=28)
        status_combobox['values'] = ["未开始", "进行中", "已结束"]
        
        # 设置当前比赛的状态
        if match.status and match.status in status_combobox['values']:
            status_combobox.set(match.status)
        else:
            status_combobox.current(0)
            
        status_combobox.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_match():
            # 获取表单数据
            tournament_id = tournament_combobox.get()
            team1_id = team1_combobox.get()
            team2_id = team2_combobox.get()
            date = date_var.get().strip()
            time = time_var.get().strip()
            format = format_var.get().strip()
            status = status_var.get()
            
            # 验证数据
            if not tournament_id or not team1_id or not team2_id:
                messagebox.showwarning("警告", "赛事、队伍1或队伍2不能为空")
                return
            
            if not date or not time:
                messagebox.showwarning("警告", "比赛日期和时间不能为空")
                return
            
            if not format:
                messagebox.showwarning("警告", "比赛形式不能为空")
                return
            
            # 更新比赛对象
            match.tournament_id = tournament_id
            match.team1_id = team1_id
            match.team2_id = team2_id
            match.match_date = date
            match.match_time = time
            match.format = format
            match.status = status
            
            # 保存到数据库
            try:
                success = match.save()
                if success:
                    messagebox.showinfo("成功", f"比赛 '{tournament_id} vs {team1_id} vs {team2_id}' 更新成功！")
                    dialog.destroy()
                    self.refresh_matches()  # 刷新比赛列表
                    self.on_match_select(None)  # 刷新详情显示
                else:
                    messagebox.showerror("错误", "保存比赛信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新比赛时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_match).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        tournament_combobox.focus_set()
    
    def delete_match(self):
        """删除选中的比赛"""
        selected_items = self.matches_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的比赛")
            return
        
        # 获取选中行的比赛ID和名称
        item = selected_items[0]
        match_values = self.matches_tree.item(item, "values")
        match_id = match_values[0]
        tournament_name = match_values[1]
        team1_name = match_values[2]
        team2_name = match_values[3]
        
        # 确认删除
        confirm = messagebox.askyesno(
            "确认删除", 
            f"确定要删除比赛 '{tournament_name} vs {team1_name} vs {team2_name}' 吗？\n\n"
            "这将同时删除该比赛的所有地图记录。\n"
            "此操作不可恢复！"
        )
        
        if not confirm:
            return
        
        # 获取比赛对象
        match = model.Match.get_by_id(match_id)
        if not match:
            messagebox.showerror("错误", "找不到指定的比赛")
            return
        
        # 删除比赛
        try:
            success = match.delete()
            if success:
                messagebox.showinfo("成功", f"比赛 '{tournament_name} vs {team1_name} vs {team2_name}' 已成功删除！")
                self.refresh_matches()  # 刷新比赛列表
            else:
                messagebox.showerror("删除失败", "无法删除比赛数据")
        except Exception as e:
            messagebox.showerror("错误", f"删除比赛时出错: {str(e)}")
    
    def add_map_match(self):
        """添加新地图的对话框"""
        # 检查是否有选中的比赛
        selected_items = self.matches_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择一个比赛")
            return

        # 获取选中行的比赛ID
        item = selected_items[0]
        match_id = self.matches_tree.item(item, "values")[0]

        # 获取比赛详情
        match = model.Match.get_by_id(match_id)
        if not match:
            messagebox.showerror("错误", "找不到指定的比赛")
            return

        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加地图")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 地图名称
        ttk.Label(form_frame, text="地图名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 地图编号
        ttk.Label(form_frame, text="地图编号:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        number_var = tk.StringVar()
        number_entry = ttk.Entry(form_frame, textvariable=number_var, width=30)
        number_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛ID
        ttk.Label(form_frame, text="比赛ID:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        match_id_var = tk.StringVar(value=match.match_id)
        match_id_entry = ttk.Entry(form_frame, textvariable=match_id_var, state="readonly")
        match_id_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 所属赛事
        ttk.Label(form_frame, text="所属赛事:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        tournament_name_var = tk.StringVar(value=match.tournament.tournament_name)
        tournament_name_entry = ttk.Entry(form_frame, textvariable=tournament_name_var, state="readonly")
        tournament_name_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍1
        ttk.Label(form_frame, text="队伍1:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        team1_name_var = tk.StringVar(value=match.team1.team_name)
        team1_name_entry = ttk.Entry(form_frame, textvariable=team1_name_var, state="readonly")
        team1_name_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍2
        ttk.Label(form_frame, text="队伍2:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        team2_name_var = tk.StringVar(value=match.team2.team_name)
        team2_name_entry = ttk.Entry(form_frame, textvariable=team2_name_var, state="readonly")
        team2_name_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛结果
        ttk.Label(form_frame, text="比赛结果:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        result_var = tk.StringVar()
        result_entry = ttk.Entry(form_frame, textvariable=result_var, width=30)
        result_entry.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 获胜方
        ttk.Label(form_frame, text="获胜方:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        winner_var = tk.StringVar()
        winner_entry = ttk.Entry(form_frame, textvariable=winner_var, width=30)
        winner_entry.grid(row=7, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_map():
            # 获取表单数据
            name = name_var.get().strip()
            number = number_var.get().strip()
            match_id = match_id_var.get()
            tournament_name = tournament_name_var.get()
            team1_name = team1_name_var.get()
            team2_name = team2_name_var.get()
            team1_score, team2_score = result_var.get().strip().split(':')
            winner_id = winner_var.get()

            # 验证数据
            if not name:
                messagebox.showwarning("警告", "地图名称不能为空")
                return
            
            if not number:
                messagebox.showwarning("警告", "地图编号不能为空")
                return
            
            if not team1_score or not team2_score:
                messagebox.showwarning("警告", "队伍1或队伍2得分不能为空")
                return
            
            if not winner_id:
                messagebox.showwarning("警告", "获胜方不能为空")
                return
            
            # 创建新地图对象
            map = model.Map(
                map_name=name,
                map_number=number,
                match_id=match_id,
                team1_score=team1_score,
                team2_score=team2_score,
                winner_id=winner_id
            )
            
            # 保存到数据库
            try:
                success = map.save()
                if success:
                    messagebox.showinfo("成功", f"地图 '{name}' 添加成功！")
                    dialog.destroy()
                    self.refresh_matches()  # 刷新比赛列表
                else:
                    messagebox.showerror("错误", "保存地图信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加地图时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_map).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        name_entry.focus_set()
    
    def edit_map_match(self):
        """编辑地图的对话框"""
        # 检查是否有选中的地图
        selected_items = self.map_matches_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要编辑的地图")
            return
        
        # 获取选中行的地图ID
        item = selected_items[0]
        map_match_id = self.map_matches_tree.item(item, "values")[0]
        
        # 获取地图详情
        map = model.Map.get_by_id(map_match_id)
        if not map:
            messagebox.showerror("错误", "找不到指定的地图")
            return
        
        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑地图 - {map.map_name}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 地图名称
        ttk.Label(form_frame, text="地图名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar(value=map.map_name)
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 地图编号
        ttk.Label(form_frame, text="地图编号:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        number_var = tk.StringVar(value=map.map_number)
        number_entry = ttk.Entry(form_frame, textvariable=number_var, width=30)
        number_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛ID
        ttk.Label(form_frame, text="比赛ID:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        match_id_var = tk.StringVar(value=map.match.match_id)
        match_id_entry = ttk.Entry(form_frame, textvariable=match_id_var, state="readonly")
        match_id_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 所属赛事
        ttk.Label(form_frame, text="所属赛事:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        tournament_name_var = tk.StringVar(value=map.tournament.tournament_name)
        tournament_name_entry = ttk.Entry(form_frame, textvariable=tournament_name_var, state="readonly")
        tournament_name_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍1
        ttk.Label(form_frame, text="队伍1:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        team1_name_var = tk.StringVar(value=map.team1.team_name)
        team1_name_entry = ttk.Entry(form_frame, textvariable=team1_name_var, state="readonly")
        team1_name_entry.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 队伍2
        ttk.Label(form_frame, text="队伍2:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        team2_name_var = tk.StringVar(value=map.team2.team_name)
        team2_name_entry = ttk.Entry(form_frame, textvariable=team2_name_var, state="readonly")
        team2_name_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 比赛结果
        ttk.Label(form_frame, text="比赛结果:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        result_var = tk.StringVar(value=map.result)
        result_entry = ttk.Entry(form_frame, textvariable=result_var, width=30)
        result_entry.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 获胜方
        ttk.Label(form_frame, text="获胜方:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        winner_var = tk.StringVar(value=map.winner.team_name)
        winner_entry = ttk.Entry(form_frame, textvariable=winner_var, width=30)
        winner_entry.grid(row=7, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # 设置列宽度
        form_frame.columnconfigure(1, weight=1)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮回调函数
        def save_map():
            # 获取表单数据
            name = name_var.get().strip()
            number = number_var.get().strip()
            match_id = match_id_var.get()
            tournament_name = tournament_name_var.get()
            team1_name = team1_name_var.get()
            team2_name = team2_name_var.get()
            result = result_var.get().strip()
            winner = winner_var.get()
            
            # 验证数据
            if not name:
                messagebox.showwarning("警告", "地图名称不能为空")
                return
            
            if not number:
                messagebox.showwarning("警告", "地图编号不能为空")
                return
            
            if not match_id:
                messagebox.showwarning("警告", "比赛ID不能为空")
                return
            
            if not tournament_name:
                messagebox.showwarning("警告", "赛事名称不能为空")
                return
            
            if not team1_name or not team2_name:
                messagebox.showwarning("警告", "队伍1或队伍2不能为空")
                return
            
            if not result:
                messagebox.showwarning("警告", "比赛结果不能为空")
                return
            
            # 更新地图对象
            map.map_name = name
            map.map_number = number
            map.match_id = match_id
            map.tournament_name = tournament_name
            map.team1_name = team1_name
            map.team2_name = team2_name
            map.result = result
            map.winner = winner
            
            # 保存到数据库
            try:
                success = map.save()
                if success:
                    messagebox.showinfo("成功", f"地图 '{name}' 更新成功！")
                    dialog.destroy()
                    self.refresh_matches()  # 刷新比赛列表
                    self.on_match_select(None)  # 刷新详情显示
                else:
                    messagebox.showerror("错误", "保存地图信息失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新地图时出错: {str(e)}")
        
        ttk.Button(button_frame, text="保存", command=save_map).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置初始焦点
        name_entry.focus_set()
    
    def delete_map_match(self):
        """删除选中的地图"""
        selected_items = self.map_matches_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的地图")
            return
        
        # 获取选中行的地图ID
        item = selected_items[0]
        map_match_id = self.map_matches_tree.item(item, "values")[0]
        
        # 获取地图详情
        map = model.Map.get_by_id(map_match_id)
        if not map:
            messagebox.showerror("错误", "找不到指定的地图")
            return
        
        # 确认删除
        confirm = messagebox.askyesno(
            "确认删除", 
            f"确定要删除地图 '{map.map_name}' 吗？\n此操作不可恢复！"
        )
        
        if not confirm:
            return
        
        # 删除地图
        try:
            success = map.delete()
            if success:
                messagebox.showinfo("成功", f"地图 '{map.map_name}' 已成功删除！")
                self.refresh_matches()  # 刷新比赛列表
            else:
                messagebox.showerror("删除失败", "无法删除地图数据")
        except Exception as e:
            messagebox.showerror("错误", f"删除地图时出错: {str(e)}")
    
    def load_filter_options(self):
        # 获取所有赛事
        tournaments = model.Tournament.get_all()
        tournament_names = [tournament.tournament_name for tournament in tournaments] if tournaments else []
        
        # 获取所有战队
        teams = model.Team.get_all()
        team_names = [team.team_name for team in teams] if teams else []
        
        # 设置筛选选项
        self.match_tournament_combobox['values'] = tournament_names
        self.match_team_combobox['values'] = team_names
        self.match_status_combobox['values'] = ["全部", "未开始", "进行中", "已结束"]
    
    def on_match_select(self, event):
        """当在树状图中选择一个比赛时显示详细信息"""
        selected_items = self.matches_tree.selection()
        if not selected_items:
            return
        
        # 获取选中行的比赛ID
        item = selected_items[0]
        match_id = self.matches_tree.item(item, "values")[0]
        
        # 获取比赛详情
        match = model.Match.get_by_id(match_id)
        if not match:
            messagebox.showerror("错误", "无法获取比赛信息")
            return
        
        # 更新表单显示比赛信息
        self.match_id_var.set(match.match_id)
        self.match_tournament_name_var.set(match.tournament.tournament_name)
        self.match_team1_var.set(match.team1.team_name)
        self.match_team2_var.set(match.team2.team_name)
        self.match_date_var.set(match.match_date)
        self.match_time_var.set(match.match_time)
        self.match_format_var.set(match.format)
        self.match_status_display_var.set(match.status)
        self.match_result_var.set(f"{match.score_team1}:{match.score_team2}")
        
        # 加载比赛的地图
        self.load_match_maps(match.match_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = CS2EventApp(root)
    root.tk.call('tk', 'scaling', ScaleFactor/75)
    root.mainloop()