/*
 Navicat Premium Dump SQL

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : cs2_events

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 25/05/2025 17:49:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for map_matches
-- ----------------------------
DROP TABLE IF EXISTS `map_matches`;
CREATE TABLE `map_matches`  (
  `map_match_id` int NOT NULL AUTO_INCREMENT,
  `match_id` int NULL DEFAULT NULL,
  `map_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `map_number` int NULL DEFAULT NULL,
  `team1_score` int NULL DEFAULT NULL,
  `team2_score` int NULL DEFAULT NULL,
  `winner_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`map_match_id`) USING BTREE,
  INDEX `match_id`(`match_id` ASC) USING BTREE,
  INDEX `winner_id`(`winner_id` ASC) USING BTREE,
  CONSTRAINT `map_matches_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `map_matches_ibfk_2` FOREIGN KEY (`winner_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of map_matches
-- ----------------------------
INSERT INTO `map_matches` VALUES (1, 1, 'Inferno', 3, 2, 13, 1);
INSERT INTO `map_matches` VALUES (2, 1, 'Dust2', 1, 16, 12, 2);
INSERT INTO `map_matches` VALUES (3, 1, 'Train', 4, 9, 13, 1);
INSERT INTO `map_matches` VALUES (4, 1, 'Mirage', 2, 13, 10, 2);
INSERT INTO `map_matches` VALUES (18, 1, 'Nuke', 5, 20, 22, 1);

-- ----------------------------
-- Table structure for matches
-- ----------------------------
DROP TABLE IF EXISTS `matches`;
CREATE TABLE `matches`  (
  `match_id` int NOT NULL AUTO_INCREMENT,
  `tournament_id` int NULL DEFAULT NULL,
  `team1_id` int NULL DEFAULT NULL,
  `team2_id` int NULL DEFAULT NULL,
  `match_date` date NULL DEFAULT NULL,
  `match_time` time NULL DEFAULT NULL,
  `format` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `winner_id` int NULL DEFAULT NULL,
  `score_team1` int NULL DEFAULT 0,
  `score_team2` int NULL DEFAULT 0,
  PRIMARY KEY (`match_id`) USING BTREE,
  INDEX `tournament_id`(`tournament_id` ASC) USING BTREE,
  INDEX `team1_id`(`team1_id` ASC) USING BTREE,
  INDEX `team2_id`(`team2_id` ASC) USING BTREE,
  INDEX `winner_id`(`winner_id` ASC) USING BTREE,
  CONSTRAINT `matches_ibfk_1` FOREIGN KEY (`tournament_id`) REFERENCES `tournaments` (`tournament_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`team1_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `matches_ibfk_3` FOREIGN KEY (`team2_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `matches_ibfk_4` FOREIGN KEY (`winner_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of matches
-- ----------------------------
INSERT INTO `matches` VALUES (1, 1, 2, 1, '2025-04-27', '05:00:00', 'BO5', '已结束', 1, 2, 3);

-- ----------------------------
-- Table structure for players
-- ----------------------------
DROP TABLE IF EXISTS `players`;
CREATE TABLE `players`  (
  `player_id` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `real_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `team_id` int NULL DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `role` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`player_id`) USING BTREE,
  UNIQUE INDEX `nickname`(`nickname` ASC) USING BTREE,
  INDEX `team_id`(`team_id` ASC) USING BTREE,
  CONSTRAINT `players_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of players
-- ----------------------------
INSERT INTO `players` VALUES (1, 'apEX', 'Dan Madesclaire', 1, '法国', '指挥');
INSERT INTO `players` VALUES (2, 'ropz', 'Robin Kool', 1, '爱沙尼亚', '步枪手');
INSERT INTO `players` VALUES (3, 'ZywOo', 'Mathieu Herbaut', 1, '法国', '狙击手');
INSERT INTO `players` VALUES (4, 'flameZ', 'Shahar Shushan', 1, '以色列', '步枪手');
INSERT INTO `players` VALUES (5, 'mezii', 'William Merriman', 1, '英国', '步枪手');
INSERT INTO `players` VALUES (6, 'NiKo', 'Nikola Kovač', 2, '波黑', '步枪手');
INSERT INTO `players` VALUES (7, 'Magisk', 'Emil Reif', 2, '丹麦', '步枪手');
INSERT INTO `players` VALUES (8, 'TeSeS', 'René Madsen', 2, '丹麦', '步枪手');
INSERT INTO `players` VALUES (9, 'm0NESY', 'Ilya Osipov', 2, '俄罗斯', '狙击手');
INSERT INTO `players` VALUES (10, 'kyxsan', 'Damjan Stoilkovski', 2, '北马其顿', '指挥');
INSERT INTO `players` VALUES (11, 'bLitz', 'Garidmagnai Byambasuren', 3, '蒙古', '指挥');
INSERT INTO `players` VALUES (12, 'Techno', 'Sodbayar Munkhbold', 3, '蒙古', '步枪手');
INSERT INTO `players` VALUES (13, 'Senzu', 'Azbayar Munkhbold', 3, '蒙古', '步枪手');
INSERT INTO `players` VALUES (14, 'mzinho', 'Ayush Batbold', 3, '蒙古', '步枪手');
INSERT INTO `players` VALUES (15, '910', 'Usukhbayar Banzragch', 3, '蒙古', '狙击手');
INSERT INTO `players` VALUES (16, 'Brollan', 'Ludvig Brolin', 5, '瑞典', '指挥');
INSERT INTO `players` VALUES (17, 'torzsi', 'Ádám Torzsás', 5, '匈牙利', '狙击手');
INSERT INTO `players` VALUES (18, 'Spinx', 'Lotan Giladi', 5, '以色列', '步枪手');
INSERT INTO `players` VALUES (19, 'Jimpphat', 'Jimi Salo', 5, '芬兰', '步枪手');
INSERT INTO `players` VALUES (20, 'xertioN', 'Dorian Berman', 5, '以色列', '步枪手');

-- ----------------------------
-- Table structure for teams
-- ----------------------------
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams`  (
  `team_id` int NOT NULL AUTO_INCREMENT,
  `team_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `logo_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`team_id`) USING BTREE,
  UNIQUE INDEX `team_name`(`team_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teams
-- ----------------------------
INSERT INTO `teams` VALUES (1, 'Vitality', '欧洲', 'https://img-cdn.hltv.org/teamlogo/yeXBldn9w8LZCgdElAenPs.png?ixlib=java-2.1.0&w=100&s=a0731380d1075205aadb30905a49da55', '绰号小蜜蜂');
INSERT INTO `teams` VALUES (2, 'Falcons', '欧洲', 'https://img-cdn.hltv.org/teamlogo/4eJSkDQINNM6Tbs4WvLzkN.png?ixlib=java-2.1.0&w=100&s=01e7f9dd30b34e66f429f43627c2e005', '绰号猎鹰，绿鹰（绿色G2）');
INSERT INTO `teams` VALUES (3, 'The MongolZ', '蒙古', 'https://img-cdn.hltv.org/teamlogo/bRk2sh_tSTO6fq1GLhgcal.png?ixlib=java-2.1.0&w=100&s=1bd99148a19e1e706b543500206901d4', '蒙古队');
INSERT INTO `teams` VALUES (5, 'MOUZ', '欧洲', 'https://img-cdn.hltv.org/teamlogo/IejtXpquZnE8KqYPB1LNKw.svg?ixlib=java-2.1.0&s=7fd33b8def053fbfd8fdbb58e3bdcd3c', '老鼠队');

-- ----------------------------
-- Table structure for tournaments
-- ----------------------------
DROP TABLE IF EXISTS `tournaments`;
CREATE TABLE `tournaments`  (
  `tournament_id` int NOT NULL AUTO_INCREMENT,
  `tournament_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `start_date` date NULL DEFAULT NULL,
  `end_date` date NULL DEFAULT NULL,
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `prize_pool` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`tournament_id`) USING BTREE,
  UNIQUE INDEX `tournament_name`(`tournament_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tournaments
-- ----------------------------
INSERT INTO `tournaments` VALUES (1, 'IEM Melbourne 2025', '2025-04-21', '2025-04-27', '澳大利亚，墨尔本', '$1,000,000', '已结束');

-- ----------------------------
-- View structure for players_by_country
-- ----------------------------
DROP VIEW IF EXISTS `players_by_country`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `players_by_country` AS select `p`.`player_id` AS `player_id`,`p`.`nickname` AS `nickname`,`p`.`country` AS `country`,`t`.`team_name` AS `team_name`,`t`.`country` AS `team_country` from (`players` `p` left join `teams` `t` on((`p`.`team_id` = `t`.`team_id`))) order by `p`.`country`;

-- ----------------------------
-- Procedure structure for update_match_result
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_match_result`;
delimiter ;;
CREATE PROCEDURE `update_match_result`(IN p_match_id INT)
BEGIN
    DECLARE Team1_id INT;
    DECLARE Team2_id INT;
    DECLARE match_format VARCHAR(10);
    DECLARE team1_wins INT;
    DECLARE team2_wins INT;
    DECLARE required_wins INT;
    DECLARE Winner_id INT DEFAULT NULL;
    
    -- 获取比赛信息
    SELECT m.team1_id, m.team2_id, m.format
    INTO team1_id, team2_id, match_format
    FROM matches m
    WHERE m.match_id = p_match_id;
    
    -- 计算每队获胜地图数
    SELECT COUNT(*) INTO team1_wins
    FROM map_matches m
    WHERE match_id = p_match_id AND m.winner_id = Team1_id;
    
    SELECT COUNT(*) INTO team2_wins
    FROM map_matches m
    WHERE match_id = p_match_id AND m.winner_id = Team2_id;
    
    -- 确定需要的获胜地图数
    IF match_format = 'BO1' THEN
        SET required_wins = 1;
    ELSEIF match_format = 'BO3' THEN
        SET required_wins = 2;
    ELSEIF match_format = 'BO5' THEN
        SET required_wins = 3;
    ELSE
        SET required_wins = 1;
    END IF;
    
    -- 确定总获胜者
    IF team1_wins >= required_wins THEN
        SET Winner_id = Team1_id;
    ELSEIF team2_wins >= required_wins THEN
        SET Winner_id = Team2_id;
    END IF;
    
    -- 更新比赛结果
    IF winner_id IS NOT NULL THEN
        UPDATE matches
        SET score_team1 = team1_wins,
            score_team2 = team2_wins,
            winner_id = Winner_id,
            status = '已结束'
        WHERE match_id = p_match_id;
    ELSE
        -- 只更新当前比分
        UPDATE matches
        SET score_team1 = team1_wins,
            score_team2 = team2_wins,
            status = '进行中'
        WHERE match_id = p_match_id;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table map_matches
-- ----------------------------
DROP TRIGGER IF EXISTS `before_map_match_insert`;
delimiter ;;
CREATE TRIGGER `before_map_match_insert` BEFORE INSERT ON `map_matches` FOR EACH ROW BEGIN
    DECLARE match_exists INT;
    DECLARE match_format VARCHAR(10);
    DECLARE max_maps INT;
    DECLARE map_exists INT;
    DECLARE team1 INT;
    DECLARE team2 INT;
    
    SELECT (SELECT COUNT(*) FROM matches WHERE match_id = NEW.match_id),
       (SELECT format FROM matches WHERE match_id = NEW.match_id)
    INTO match_exists, match_format;
    
    -- 根据比赛形式确定最大地图数
    CASE match_format
        WHEN 'BO1' THEN SET max_maps = 1;
        WHEN 'BO3' THEN SET max_maps = 3;
        WHEN 'BO5' THEN SET max_maps = 5;
        ELSE SET max_maps = 1;
    END CASE;
    
    -- 检查地图序号是否超出范围
    IF NEW.map_number <= 0 OR NEW.map_number > max_maps THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '地图序号必须在合理范围内';
    END IF;
    
    -- 检查地图序号是否已存在
    SELECT COUNT(*) INTO map_exists 
    FROM map_matches 
    WHERE match_id = NEW.match_id AND map_number = NEW.map_number;
    
    IF map_exists > 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '该比赛中已存在相同序号的地图';
    END IF;
    
    -- 检查获胜者是否参与了比赛
    IF NEW.winner_id IS NOT NULL THEN
        SELECT team1_id, team2_id INTO team1, team2 
        FROM matches WHERE match_id = NEW.match_id;
        
        IF NEW.winner_id <> team1 AND NEW.winner_id <> team2 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '获胜者必须是参赛队伍之一';
        END IF;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table map_matches
-- ----------------------------
DROP TRIGGER IF EXISTS `after_map_match_insert`;
delimiter ;;
CREATE TRIGGER `after_map_match_insert` AFTER INSERT ON `map_matches` FOR EACH ROW BEGIN
    CALL update_match_result(NEW.match_id);
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table map_matches
-- ----------------------------
DROP TRIGGER IF EXISTS `after_map_match_update`;
delimiter ;;
CREATE TRIGGER `after_map_match_update` AFTER UPDATE ON `map_matches` FOR EACH ROW BEGIN
    IF OLD.winner_id <> NEW.winner_id OR
       (OLD.winner_id IS NULL AND NEW.winner_id IS NOT NULL) OR
       (OLD.winner_id IS NOT NULL AND NEW.winner_id IS NULL) THEN
        CALL update_match_result(NEW.match_id);
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table map_matches
-- ----------------------------
DROP TRIGGER IF EXISTS `after_map_match_delete`;
delimiter ;;
CREATE TRIGGER `after_map_match_delete` AFTER DELETE ON `map_matches` FOR EACH ROW BEGIN
    CALL update_match_result(OLD.match_id);
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table matches
-- ----------------------------
DROP TRIGGER IF EXISTS `before_match_insert`;
delimiter ;;
CREATE TRIGGER `before_match_insert` BEFORE INSERT ON `matches` FOR EACH ROW BEGIN
    DECLARE tournament_exists INT;
    DECLARE team1_exists INT;
    DECLARE team2_exists INT;
    DECLARE t_start_date DATE;
    DECLARE t_end_date DATE;
    
    -- 检查赛事是否存在
    SELECT COUNT(*) INTO tournament_exists FROM tournaments WHERE tournament_id = NEW.tournament_id;
    IF tournament_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '指定的赛事不存在';
    END IF;
    
    -- 检查战队是否存在
    IF NEW.team1_id IS NOT NULL THEN
        SELECT COUNT(*) INTO team1_exists FROM teams WHERE team_id = NEW.team1_id;
        IF team1_exists = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '指定的队伍1不存在';
        END IF;
    END IF;
    
    IF NEW.team2_id IS NOT NULL THEN
        SELECT COUNT(*) INTO team2_exists FROM teams WHERE team_id = NEW.team2_id;
        IF team2_exists = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '指定的队伍2不存在';
        END IF;
    END IF;
    
    -- 检查队伍1和队伍2不是同一支队伍
    IF NEW.team1_id IS NOT NULL AND NEW.team2_id IS NOT NULL AND NEW.team1_id = NEW.team2_id THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '队伍1和队伍2不能是同一支战队';
    END IF;
    
    -- 检查比赛日期在赛事日期范围内
    SELECT start_date, end_date INTO t_start_date, t_end_date 
    FROM tournaments WHERE tournament_id = NEW.tournament_id;
    
    IF NEW.match_date < t_start_date OR NEW.match_date > t_end_date THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '比赛日期必须在赛事日期范围内';
    END IF;
    
    -- 检查比赛形式是否有效
    IF NEW.format NOT IN ('BO1', 'BO3', 'BO5') THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '比赛形式必须是BO1、BO3或BO5';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table matches
-- ----------------------------
DROP TRIGGER IF EXISTS `before_match_update`;
delimiter ;;
CREATE TRIGGER `before_match_update` BEFORE UPDATE ON `matches` FOR EACH ROW BEGIN
    -- 检查获胜者是否参与了比赛
    IF NEW.winner_id IS NOT NULL AND 
       NEW.winner_id <> NEW.team1_id AND 
       NEW.winner_id <> NEW.team2_id THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '获胜者必须是参赛队伍之一';
    END IF;
    
    -- 如果比赛状态设置为"已结束"，检查是否有获胜者
    IF OLD.status <> '已结束' AND NEW.status = '已结束' AND NEW.winner_id IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '已结束的比赛必须指定获胜者';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table players
-- ----------------------------
DROP TRIGGER IF EXISTS `before_player_insert`;
delimiter ;;
CREATE TRIGGER `before_player_insert` BEFORE INSERT ON `players` FOR EACH ROW BEGIN
    DECLARE team_exists INT;
    
    -- 检查战队是否存在（如果指定了战队）
    IF NEW.team_id IS NOT NULL THEN
        SELECT COUNT(*) INTO team_exists FROM teams WHERE team_id = NEW.team_id;
        IF team_exists = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '指定的战队不存在';
        END IF;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table players
-- ----------------------------
DROP TRIGGER IF EXISTS `before_player_update`;
delimiter ;;
CREATE TRIGGER `before_player_update` BEFORE UPDATE ON `players` FOR EACH ROW BEGIN
    DECLARE team_exists INT;
    
    -- 检查战队是否存在（如果指定了战队）
    IF NEW.team_id IS NOT NULL THEN
        SELECT COUNT(*) INTO team_exists FROM teams WHERE team_id = NEW.team_id;
        IF team_exists = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '指定的战队不存在';
        END IF;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tournaments
-- ----------------------------
DROP TRIGGER IF EXISTS `before_tournament_insert`;
delimiter ;;
CREATE TRIGGER `before_tournament_insert` BEFORE INSERT ON `tournaments` FOR EACH ROW BEGIN
    IF NEW.end_date < NEW.start_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '赛事结束日期不能早于开始日期';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tournaments
-- ----------------------------
DROP TRIGGER IF EXISTS `before_tournament_update`;
delimiter ;;
CREATE TRIGGER `before_tournament_update` BEFORE UPDATE ON `tournaments` FOR EACH ROW BEGIN
    DECLARE unfinished_count INT;
    IF NEW.end_date < NEW.start_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '赛事结束日期不能早于开始日期';
    END IF;
    
    IF OLD.status <> NEW.status AND NEW.status = '已结束' THEN
        
        SELECT COUNT(*) INTO unfinished_count 
        FROM matches 
        WHERE tournament_id = NEW.tournament_id AND status <> '已结束';
        
        IF unfinished_count > 0 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '赛事中还有未完成的比赛，无法将状态设为已结束';
        END IF;
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
