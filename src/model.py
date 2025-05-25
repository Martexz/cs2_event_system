# models.py
from db_connector import DatabaseConnector

class Team:
    """战队模型类，处理与teams表相关的操作"""
    
    def __init__(self, team_id=None, team_name=None, country=None, logo_url=None, description=None):
        """初始化战队对象"""
        self.team_id = team_id
        self.team_name = team_name
        self.country = country
        self.logo_url = logo_url
        self.description = description
        self.db = DatabaseConnector()
    
    def save(self):
        """保存或更新战队信息"""
        if self.team_id:
            # 更新现有战队
            query = """
            UPDATE teams 
            SET team_name = %s, country = %s, logo_url = %s, description = %s
            WHERE team_id = %s
            """
            params = (self.team_name, self.country, self.logo_url, self.description, self.team_id)
            result = self.db.execute_update(query, params)
            self.db.disconnect()
            return result > 0
        else:
            # 创建新战队
            query = """
            INSERT INTO teams (team_name, country, logo_url, description)
            VALUES (%s, %s, %s, %s)
            """
            params = (self.team_name, self.country, self.logo_url, self.description)
            self.team_id = self.db.execute_insert(query, params)
            self.db.disconnect()
            return self.team_id is not None
    
    def delete(self):
        """删除战队"""
        if not self.team_id:
            return False
        
        query = "DELETE FROM teams WHERE team_id = %s"
        result = self.db.execute_update(query, (self.team_id,))
        self.db.disconnect()
        return result > 0
    
    @staticmethod
    def get_by_id(team_id):
        """通过ID获取战队信息"""
        db = DatabaseConnector()
        query = "SELECT * FROM teams WHERE team_id = %s"
        rows = db.execute_query(query, (team_id,))
        db.disconnect()
        
        if not rows:
            return None
        
        team_data = rows[0]
        return Team(
            team_id=team_data['team_id'],
            team_name=team_data['team_name'],
            country=team_data['country'],
            logo_url=team_data['logo_url'],
            description=team_data['description']
        )
    
    @staticmethod
    def get_all():
        """获取所有战队列表"""
        db = DatabaseConnector()
        query = "SELECT * FROM teams ORDER BY team_name"
        rows = db.execute_query(query)
        db.disconnect()
        
        teams = []
        if rows:
            for row in rows:
                teams.append(Team(
                    team_id=row['team_id'],
                    team_name=row['team_name'],
                    country=row['country'],
                    logo_url=row['logo_url'],
                    description=row['description']
                ))
        
        return teams
    
    @staticmethod
    def search(keyword):
        """搜索战队"""
        db = DatabaseConnector()
        query = """
        SELECT * FROM teams 
        WHERE team_name LIKE %s OR country LIKE %s OR description LIKE %s
        ORDER BY team_name
        """
        search_param = f"%{keyword}%"
        rows = db.execute_query(query, (search_param, search_param, search_param))
        db.disconnect()
        
        teams = []
        if rows:
            for row in rows:
                teams.append(Team(
                    team_id=row['team_id'],
                    team_name=row['team_name'],
                    country=row['country'],
                    logo_url=row['logo_url'],
                    description=row['description']
                ))
        
        return teams

    def delete_with_transaction(self):
        """使用事务删除战队及其相关数据"""
        if not self.team_id:
            return False, "战队ID不能为空"
        
        db = DatabaseConnector()
        success = False
        message = ""
        
        try:
            # 开始事务
            if not db.begin_transaction():
                return False, "无法开始事务"
            
            # 1. 查询并处理关联的选手
            query_players = "SELECT player_id FROM players WHERE team_id = %s"
            player_rows = db.execute_query(query_players, (self.team_id,))
            
            player_ids = []
            if player_rows:
                player_ids = [row['player_id'] for row in player_rows]
                update_players = "UPDATE players SET team_id = NULL WHERE team_id = %s"
                db.execute_update(update_players, (self.team_id,))
            
            # 2. 查询并处理相关的地图比赛
            # 首先查找所有涉及此战队的比赛
            query_matches = """
            SELECT match_id FROM matches 
            WHERE team1_id = %s OR team2_id = %s OR winner_id = %s
            """
            match_rows = db.execute_query(query_matches, (self.team_id, self.team_id, self.team_id))
            
            match_ids = []
            if match_rows:
                match_ids = [row['match_id'] for row in match_rows]
                
                # 对于每个比赛，先删除关联的地图比赛
                for match_id in match_ids:
                    delete_map_matches = "DELETE FROM map_matches WHERE match_id = %s"
                    db.execute_update(delete_map_matches, (match_id,))
                
                # 然后删除比赛本身
                delete_matches = "DELETE FROM matches WHERE match_id IN ({})".format(
                    ','.join(['%s'] * len(match_ids)))
                db.execute_update(delete_matches, match_ids)
            
            # 3. 记录日志（如果有日志表）
            try:
                log_query = """
                INSERT INTO system_logs (action, table_affected, record_id, action_time, details)
                VALUES (%s, %s, %s, NOW(), %s)
                """
                details = f"删除战队: {self.team_name}，相关数据已处理: {len(player_ids)}名选手, {len(match_ids)}场比赛"
                db.execute_insert(log_query, ("删除", "teams", self.team_id, details))
            except Exception as e:
                # 日志记录失败不应影响主要操作
                print(f"记录日志时出错: {e}")
            
            # 4. 最后删除战队本身
            delete_query = "DELETE FROM teams WHERE team_id = %s"
            result = db.execute_update(delete_query, (self.team_id,))
            
            # 提交事务
            if db.commit():
                success = True
                message = f"战队 '{self.team_name}' 及其相关数据已成功删除"
            else:
                message = "提交事务失败"
                success = False
        
        except Exception as e:
            # 出现任何错误，回滚事务
            db.rollback()
            message = f"删除战队时出错: {str(e)}"
            success = False
        finally:
            # 关闭数据库连接
            db.disconnect()
        
        return success, message


class Player:
    """选手模型类，处理与players表相关的操作"""
    
    def __init__(self, player_id=None, nickname=None, real_name=None, team_id=None, 
                 country=None, role=None):
        """初始化选手对象"""
        self.player_id = player_id
        self.nickname = nickname
        self.real_name = real_name
        self.team_id = team_id
        self.country = country
        self.role = role
        self.db = DatabaseConnector()
    
    def save(self):
        """保存或更新选手信息"""
        if self.player_id:
            # 更新现有选手
            query = """
            UPDATE players 
            SET nickname = %s, real_name = %s, team_id = %s, country = %s, role = %s
            WHERE player_id = %s
            """
            params = (self.nickname, self.real_name, self.team_id, self.country, 
                      self.role, self.player_id)
            result = self.db.execute_update(query, params)
            self.db.disconnect()
            return result > 0
        else:
            # 创建新选手
            query = """
            INSERT INTO players (nickname, real_name, team_id, country, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.nickname, self.real_name, self.team_id, self.country, self.role)
            self.player_id = self.db.execute_insert(query, params)
            self.db.disconnect()
            return self.player_id is not None
    
    def delete(self):
        """删除选手"""
        if not self.player_id:
            return False
        
        query = "DELETE FROM players WHERE player_id = %s"
        result = self.db.execute_update(query, (self.player_id,))
        self.db.disconnect()
        return result > 0
    
    @staticmethod
    def get_by_id(player_id):
        """通过ID获取选手信息"""
        db = DatabaseConnector()
        query = "SELECT * FROM players WHERE player_id = %s"
        rows = db.execute_query(query, (player_id,))
        db.disconnect()
        
        if not rows:
            return None
        
        player_data = rows[0]
        return Player(
            player_id=player_data['player_id'],
            nickname=player_data['nickname'],
            real_name=player_data['real_name'],
            team_id=player_data['team_id'],
            country=player_data['country'],
            role=player_data['role']
        )
    
    @staticmethod
    def get_all():
        """获取所有选手列表"""
        db = DatabaseConnector()
        query = "SELECT * FROM players ORDER BY nickname"
        rows = db.execute_query(query)
        db.disconnect()
        
        players = []
        if rows:
            for row in rows:
                players.append(Player(
                    player_id=row['player_id'],
                    nickname=row['nickname'],
                    real_name=row['real_name'],
                    team_id=row['team_id'],
                    country=row['country'],
                    role=row['role']
                ))
        
        return players
    
    @staticmethod
    def get_by_team(team_id):
        """获取指定战队的所有选手"""
        db = DatabaseConnector()
        query = "SELECT * FROM players WHERE team_id = %s ORDER BY nickname"
        rows = db.execute_query(query, (team_id,))
        db.disconnect()
        
        players = []
        if rows:
            for row in rows:
                players.append(Player(
                    player_id=row['player_id'],
                    nickname=row['nickname'],
                    real_name=row['real_name'],
                    team_id=row['team_id'],
                    country=row['country'],
                    role=row['role']
                ))
        
        return players
    
    @staticmethod
    def search(keyword):
        """搜索选手"""
        db = DatabaseConnector()
        query = """
        SELECT * FROM players 
        WHERE nickname LIKE %s OR real_name LIKE %s OR country LIKE %s
        ORDER BY nickname
        """
        search_param = f"%{keyword}%"
        rows = db.execute_query(query, (search_param, search_param, search_param))
        db.disconnect()
        
        players = []
        if rows:
            for row in rows:
                players.append(Player(
                    player_id=row['player_id'],
                    nickname=row['nickname'],
                    real_name=row['real_name'],
                    team_id=row['team_id'],
                    country=row['country'],
                    role=row['role']
                ))
        
        return players

    @staticmethod
    def get_by_country():
        """从视图players_by_country中获取按国家分组的选手信息"""
        db = DatabaseConnector()
        query = "SELECT player_id, nickname, country, team_name, team_country FROM players_by_country"
        rows = db.execute_query(query)
        db.disconnect()
        
        players = []
        if rows:
            for row in rows:
                players.append({
                    'player_id': row['player_id'],
                    'nickname': row['nickname'],
                    'country': row['country'],
                    'team_name': row['team_name'],
                    'team_country': row['team_country']
                })
        
        return players


class Tournament:
    """赛事模型类，处理与tournaments表相关的操作"""
    
    def __init__(self, tournament_id=None, tournament_name=None, start_date=None, 
                 end_date=None, location=None, prize_pool=None, status=None):
        """初始化赛事对象"""
        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.prize_pool = prize_pool
        self.status = status
        self.db = DatabaseConnector()
    
    def save(self):
        """保存或更新赛事信息"""
        if self.tournament_id:
            # 更新现有赛事
            query = """
            UPDATE tournaments 
            SET tournament_name = %s, start_date = %s, end_date = %s, 
                location = %s, prize_pool = %s, status = %s
            WHERE tournament_id = %s
            """
            params = (self.tournament_name, self.start_date, self.end_date,
                      self.location, self.prize_pool, self.status, self.tournament_id)
            result = self.db.execute_update(query, params)
            self.db.disconnect()
            return result > 0
        else:
            # 创建新赛事
            query = """
            INSERT INTO tournaments 
            (tournament_name, start_date, end_date, location, prize_pool, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.tournament_name, self.start_date, self.end_date,
                      self.location, self.prize_pool, self.status)
            self.tournament_id = self.db.execute_insert(query, params)
            self.db.disconnect()
            return self.tournament_id is not None
    
    def delete(self):
        """删除赛事"""
        if not self.tournament_id:
            return False
        
        query = "DELETE FROM tournaments WHERE tournament_id = %s"
        result = self.db.execute_update(query, (self.tournament_id,))
        self.db.disconnect()
        return result > 0
    
    @staticmethod
    def get_by_id(tournament_id):
        """通过ID获取赛事信息"""
        db = DatabaseConnector()
        query = "SELECT * FROM tournaments WHERE tournament_id = %s"
        rows = db.execute_query(query, (tournament_id,))
        db.disconnect()
        
        if not rows:
            return None
        
        tournament_data = rows[0]
        return Tournament(
            tournament_id=tournament_data['tournament_id'],
            tournament_name=tournament_data['tournament_name'],
            start_date=tournament_data['start_date'],
            end_date=tournament_data['end_date'],
            location=tournament_data['location'],
            prize_pool=tournament_data['prize_pool'],
            status=tournament_data['status']
        )
    
    @staticmethod
    def get_all():
        """获取所有赛事列表"""
        db = DatabaseConnector()
        query = "SELECT * FROM tournaments ORDER BY start_date DESC"
        rows = db.execute_query(query)
        db.disconnect()
        
        tournaments = []
        if rows:
            for row in rows:
                tournaments.append(Tournament(
                    tournament_id=row['tournament_id'],
                    tournament_name=row['tournament_name'],
                    start_date=row['start_date'],
                    end_date=row['end_date'],
                    location=row['location'],
                    prize_pool=row['prize_pool'],
                    status=row['status']
                ))
        
        return tournaments
    
    @staticmethod
    def get_active_tournaments():
        """获取所有进行中的赛事"""
        db = DatabaseConnector()
        query = "SELECT * FROM tournaments WHERE status = '进行中' ORDER BY start_date"
        rows = db.execute_query(query)
        db.disconnect()
        
        tournaments = []
        if rows:
            for row in rows:
                tournaments.append(Tournament(
                    tournament_id=row['tournament_id'],
                    tournament_name=row['tournament_name'],
                    start_date=row['start_date'],
                    end_date=row['end_date'],
                    location=row['location'],
                    prize_pool=row['prize_pool'],
                    status=row['status']
                ))
        
        return tournaments
    
    @staticmethod
    def search(keyword):
        """搜索赛事"""
        db = DatabaseConnector()
        query = """
        SELECT * FROM tournaments 
        WHERE tournament_name LIKE %s OR location LIKE %s
        ORDER BY start_date DESC
        """
        search_param = f"%{keyword}%"
        rows = db.execute_query(query, (search_param, search_param))
        db.disconnect()
        
        tournaments = []
        if rows:
            for row in rows:
                tournaments.append(Tournament(
                    tournament_id=row['tournament_id'],
                    tournament_name=row['tournament_name'],
                    start_date=row['start_date'],
                    end_date=row['end_date'],
                    location=row['location'],
                    prize_pool=row['prize_pool'],
                    status=row['status']
                ))
        
        return tournaments


class Match:
    """比赛模型类，处理与matches表相关的操作"""
    
    def __init__(self, match_id=None, tournament_id=None, team1_id=None, team2_id=None,
                 match_date=None, match_time=None, format=None, status=None, winner_id=None,
                 score_team1=0, score_team2=0):
        """初始化比赛对象"""
        self.match_id = match_id
        self.tournament_id = tournament_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.match_date = match_date
        self.match_time = match_time
        self.format = format
        self.status = status
        self.winner_id = winner_id
        self.score_team1 = score_team1
        self.score_team2 = score_team2
        self.db = DatabaseConnector()
    
    def save(self):
        """保存或更新比赛信息"""
        try:
            # 获取赛事ID
            if isinstance(self.tournament_id, str):
                self.tournament_id = Match.get_tournament_id_by_name(self.tournament_id)
                if not self.tournament_id:
                    print("错误: 无法找到指定的赛事名称对应的ID")
                    return False

            # 获取队伍1 ID
            if isinstance(self.team1_id, str):
                self.team1_id = Match.get_team_id_by_name(self.team1_id)
                if not self.team1_id:
                    print("错误: 无法找到指定的队伍1名称对应的ID")
                    return False

            # 获取队伍2 ID
            if isinstance(self.team2_id, str):
                self.team2_id = Match.get_team_id_by_name(self.team2_id)
                if not self.team2_id:
                    print("错误: 无法找到指定的队伍2名称对应的ID")
                    return False

            if self.match_id:
                # 更新现有比赛
                query = """
                UPDATE matches 
                SET tournament_id = %s, team1_id = %s, team2_id = %s, match_date = %s,
                    match_time = %s, format = %s, status = %s, winner_id = %s,
                    score_team1 = %s, score_team2 = %s
                WHERE match_id = %s
                """
                params = (self.tournament_id, self.team1_id, self.team2_id, self.match_date,
                          self.match_time, self.format, self.status, self.winner_id,
                          self.score_team1, self.score_team2, self.match_id)
                result = self.db.execute_update(query, params)
                self.db.disconnect()
                return result > 0
            else:
                # 创建新比赛
                query = """
                INSERT INTO matches 
                (tournament_id, team1_id, team2_id, match_date, match_time, format, status, winner_id,
                 score_team1, score_team2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (self.tournament_id, self.team1_id, self.team2_id, self.match_date,
                          self.match_time, self.format, self.status, self.winner_id,
                          self.score_team1, self.score_team2)
                self.match_id = self.db.execute_insert(query, params)
                self.db.disconnect()
                return self.match_id is not None
        except Exception as e:
            print(f"保存比赛信息时出错: {e}")
            return False
    
    def delete(self):
        """删除比赛"""
        if not self.match_id:
            return False
        
        query = "DELETE FROM matches WHERE match_id = %s"
        result = self.db.execute_update(query, (self.match_id,))
        self.db.disconnect()
        return result > 0
    
    @staticmethod
    def get_by_id(match_id):
        """通过ID获取比赛信息"""
        db = DatabaseConnector()
        query = "SELECT * FROM matches WHERE match_id = %s"
        rows = db.execute_query(query, (match_id,))
        db.disconnect()
        
        if not rows:
            return None
        
        match_data = rows[0]
        return Match(
            match_id=match_data['match_id'],
            tournament_id=match_data['tournament_id'],
            team1_id=match_data['team1_id'],
            team2_id=match_data['team2_id'],
            match_date=match_data['match_date'],
            match_time=match_data['match_time'],
            format=match_data['format'],
            status=match_data['status'],
            winner_id=match_data['winner_id'],
            score_team1=match_data['score_team1'],
            score_team2=match_data['score_team2']
        )
    
    @staticmethod
    def get_all():
        """获取所有比赛列表"""
        db = DatabaseConnector()
        query = "SELECT * FROM matches ORDER BY match_date DESC, match_time DESC"
        rows = db.execute_query(query)
        db.disconnect()
        
        matches = []
        if rows:
            for row in rows:
                matches.append(Match(
                    match_id=row['match_id'],
                    tournament_id=row['tournament_id'],
                    team1_id=row['team1_id'],
                    team2_id=row['team2_id'],
                    match_date=row['match_date'],
                    match_time=row['match_time'],
                    format=row['format'],
                    status=row['status'],
                    winner_id=row['winner_id'],
                    score_team1=row['score_team1'],
                    score_team2=row['score_team2']
                ))
        
        return matches
    
    @staticmethod
    def get_by_tournament(tournament_id):
        """获取特定赛事的所有比赛"""
        db = DatabaseConnector()
        query = """
        SELECT * FROM matches 
        WHERE tournament_id = %s 
        ORDER BY match_date, match_time
        """
        rows = db.execute_query(query, (tournament_id,))
        db.disconnect()
        
        matches = []
        if rows:
            for row in rows:
                matches.append(Match(
                    match_id=row['match_id'],
                    tournament_id=row['tournament_id'],
                    team1_id=row['team1_id'],
                    team2_id=row['team2_id'],
                    match_date=row['match_date'],
                    match_time=row['match_time'],
                    format=row['format'],
                    status=row['status'],
                    winner_id=row['winner_id'],
                    score_team1=row['score_team1'],
                    score_team2=row['score_team2']
                ))
        
        return matches
    
    @staticmethod
    def get_by_team(team_id):
        """获取特定战队参与的所有比赛"""
        db = DatabaseConnector()
        query = """
        SELECT * FROM matches 
        WHERE team1_id = %s OR team2_id = %s 
        ORDER BY match_date DESC, match_time DESC
        """
        rows = db.execute_query(query, (team_id, team_id))
        db.disconnect()
        
        matches = []
        if rows:
            for row in rows:
                matches.append(Match(
                    match_id=row['match_id'],
                    tournament_id=row['tournament_id'],
                    team1_id=row['team1_id'],
                    team2_id=row['team2_id'],
                    match_date=row['match_date'],
                    match_time=row['match_time'],
                    format=row['format'],
                    status=row['status'],
                    winner_id=row['winner_id'],
                    score_team1=row['score_team1'],
                    score_team2=row['score_team2']
                ))
        
        return matches

    @staticmethod
    def search(keyword=None, tournament_id=None, team_id=None, status=None):
        """搜索比赛，支持按关键词、赛事ID、战队ID和状态进行筛选"""
        db = DatabaseConnector()
        
        # 构建基本查询
        query = "SELECT * FROM matches WHERE 1=1"
        params = []
        
        # 添加关键词筛选（匹配赛事名称）
        if keyword and keyword.strip():
            # 先通过关键词查找赛事ID
            tournament_query = "SELECT tournament_id FROM tournaments WHERE tournament_name LIKE %s"
            tournament_ids = db.execute_query(tournament_query, (f"%{keyword.strip()}%",))
            
            if tournament_ids:
                tournament_id_list = [row['tournament_id'] for row in tournament_ids]
                # 使用IN操作符匹配赛事ID
                query += f" AND tournament_id IN ({','.join(['%s'] * len(tournament_id_list))})"
                params.extend(tournament_id_list)
        
        # 添加赛事ID筛选
        if tournament_id and tournament_id != "全部" and tournament_id != "":
            if isinstance(tournament_id, str) and tournament_id.isdigit():
                tournament_id = int(tournament_id)
            if isinstance(tournament_id, int):
                query += " AND tournament_id = %s"
                params.append(tournament_id)
        
        # 添加战队ID筛选
        if team_id and team_id != "全部" and team_id != "":
            if isinstance(team_id, str) and team_id.isdigit():
                team_id = int(team_id)
            if isinstance(team_id, int):
                query += " AND (team1_id = %s OR team2_id = %s)"
                params.extend([team_id, team_id])
        
        # 添加状态筛选
        if status and status != "全部" and status != "":
            query += " AND status = %s"
            params.append(status)
        
        # 按日期和时间排序
        query += " ORDER BY match_date DESC, match_time DESC"
        
        # 执行查询
        rows = db.execute_query(query, tuple(params) if params else None)
        db.disconnect()
        
        matches = []
        if rows:
            for row in rows:
                matches.append(Match(
                    match_id=row['match_id'],
                    tournament_id=row['tournament_id'],
                    team1_id=row['team1_id'],
                    team2_id=row['team2_id'],
                    match_date=row['match_date'],
                    match_time=row['match_time'],
                    format=row['format'],
                    status=row['status'],
                    winner_id=row['winner_id'],
                    score_team1=row['score_team1'],
                    score_team2=row['score_team2']
                ))
        
        return matches

    @property
    def team1(self):
        """获取队伍1对象"""
        if not hasattr(self, '_team1') and self.team1_id:
            self._team1 = Team.get_by_id(self.team1_id)
        return getattr(self, '_team1', None)
    
    @property
    def team2(self):
        """获取队伍2对象"""
        if not hasattr(self, '_team2') and self.team2_id:
            self._team2 = Team.get_by_id(self.team2_id)
        return getattr(self, '_team2', None)
    
    @property
    def tournament(self):
        """获取赛事对象"""
        if not hasattr(self, '_tournament') and self.tournament_id:
            self._tournament = Tournament.get_by_id(self.tournament_id)
        return getattr(self, '_tournament', None)
    
    @property
    def winner(self):
        """获取获胜者对象"""
        if not hasattr(self, '_winner') and self.winner_id:
            self._winner = Team.get_by_id(self.winner_id)
        return getattr(self, '_winner', None)

    @staticmethod
    def get_tournament_id_by_name(tournament_name):
        """通过赛事名称获取赛事ID"""
        db = DatabaseConnector()
        query = "SELECT tournament_id FROM tournaments WHERE tournament_name = %s"
        rows = db.execute_query(query, (tournament_name,))
        db.disconnect()
        
        if not rows:
            return None
        
        return rows[0]['tournament_id']

    @staticmethod
    def get_team_id_by_name(team_name):
        """通过队伍名称获取队伍ID"""
        db = DatabaseConnector()
        query = "SELECT team_id FROM teams WHERE team_name = %s"
        rows = db.execute_query(query, (team_name,))
        db.disconnect()
        
        if not rows:
            return None
        
        return rows[0]['team_id']


class MapMatch:
    """地图比赛模型类，处理与map_matches表相关的操作"""
    
    def __init__(self, map_match_id=None, match_id=None, map_name=None, map_number=None,
                 team1_score=None, team2_score=None, winner_id=None):
        """初始化地图比赛对象"""
        self.map_match_id = map_match_id
        self.match_id = match_id
        self.map_name = map_name
        self.map_number = map_number
        self.team1_score = team1_score
        self.team2_score = team2_score
        self.winner_id = winner_id
        self.db = DatabaseConnector()
    
    def save(self):
        """保存或更新地图比赛信息"""
        if self.map_match_id:
            # 更新现有地图比赛
            query = """
            UPDATE map_matches 
            SET match_id = %s, map_name = %s, map_number = %s,
                team1_score = %s, team2_score = %s, winner_id = %s
            WHERE map_match_id = %s
            """
            params = (self.match_id, self.map_name, self.map_number,
                      self.team1_score, self.team2_score, self.winner_id, self.map_match_id)
            result = self.db.execute_update(query, params)
            self.db.disconnect()
            return result > 0
        else:
            # 创建新地图比赛
            query = """
            INSERT INTO map_matches 
            (match_id, map_name, map_number, team1_score, team2_score, winner_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.match_id, self.map_name, self.map_number,
                      self.team1_score, self.team2_score, self.winner_id)
            self.map_match_id = self.db.execute_insert(query, params)
            self.db.disconnect()
            return self.map_match_id is not None
    
    def delete(self):
        """删除地图比赛"""
        if not self.map_match_id:
            return False
        
        query = "DELETE FROM map_matches WHERE map_match_id = %s"
        result = self.db.execute_update(query, (self.map_match_id,))
        self.db.disconnect()
        return result > 0
    
    @staticmethod
    def get_by_id(map_match_id):
        """通过ID获取地图比赛信息"""
        db = DatabaseConnector()
        query = "SELECT * FROM map_matches WHERE map_match_id = %s"
        rows = db.execute_query(query, (map_match_id,))
        db.disconnect()
        
        if not rows:
            return None
        
        map_match_data = rows[0]
        return MapMatch(
            map_match_id=map_match_data['map_match_id'],
            match_id=map_match_data['match_id'],
            map_name=map_match_data['map_name'],
            map_number=map_match_data['map_number'],
            team1_score=map_match_data['team1_score'],
            team2_score=map_match_data['team2_score'],
            winner_id=map_match_data['winner_id']
        )
    
    @property
    def match(self):
        """获取关联的比赛对象"""
        if not hasattr(self, '_match') and self.match_id:
            self._match = Match.get_by_id(self.match_id)
        return getattr(self, '_match', None)
    
    @property
    def team1(self):
        """获取队伍1对象"""
        match = self.match
        if match:
            return match.team1
        return None
    
    @property
    def team2(self):
        """获取队伍2对象"""
        match = self.match
        if match:
            return match.team2
        return None
    
    @property
    def tournament(self):
        """获取赛事对象"""
        match = self.match
        if match:
            return match.tournament
        return None
    
    @property
    def score(self):
        """获取比分字符串"""
        if hasattr(self, 'team1_score') and hasattr(self, 'team2_score'):
            return f"{self.team1_score}:{self.team2_score}"
        return None
    
    @property
    def winner(self):
        """获取获胜者对象"""
        if not hasattr(self, '_winner') and self.winner_id:
            self._winner = Team.get_by_id(self.winner_id)
        return getattr(self, '_winner', None)
    
    @staticmethod
    def get_by_match(match_id):
        """获取特定比赛的所有地图比赛，按地图顺序排序"""
        db = DatabaseConnector()
        query = "SELECT * FROM map_matches WHERE match_id = %s ORDER BY map_number"
        rows = db.execute_query(query, (match_id,))
        db.disconnect()
        
        map_matches = []
        if rows:
            for row in rows:
                map_matches.append(MapMatch(
                    map_match_id=row['map_match_id'],
                    match_id=row['match_id'],
                    map_name=row['map_name'],
                    map_number=row['map_number'],
                    team1_score=row['team1_score'],
                    team2_score=row['team2_score'],
                    winner_id=row['winner_id']
                ))
        
        return map_matches

# 为了UI中使用方便，创建一个Map类别名
Map = MapMatch