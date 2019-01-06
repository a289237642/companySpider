/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : newsinfo

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 06/01/2019 15:44:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news`  (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '新闻标识',
  `BTIT` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '标题',
  `CYRS` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '参与人数，注意：原表没有，额外增加的',
  `PLS` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '评论数    注意：原表没有，额外增加的',
  `XWLY` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '新闻来源',
  `ZZLY` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '转载来源',
  `LMLJ` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '栏目路径',
  `BZ` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '编者',
  `CGSJ` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '成稿时间',
  `CJSJ` datetime(0) DEFAULT NULL COMMENT '采集时间',
  `RKSJ` datetime(0) DEFAULT NULL COMMENT '入库时间',
  `YDL` int(11) DEFAULT NULL COMMENT '阅读量',
  `ZZL` int(11) DEFAULT NULL COMMENT '转载量',
  `DJL` int(11) DEFAULT NULL COMMENT '点赞量',
  `ZWWB` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '正文文本',
  `ZWNR` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '正文内容',
  `TJS` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '推荐数  注意：原表没有，额外增加的',
  `YS_URL` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '原始网页链接',
  `CL_URL` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '处理网页链接',
  `TP_URL` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '缩略图片链接',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 80 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
