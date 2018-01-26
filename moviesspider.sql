/*
Navicat MySQL Data Transfer

Source Server         : MySQL
Source Server Version : 50716
Source Host           : localhost:3306
Source Database       : moviesspider

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2018-01-26 19:15:54
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for categroymovietable
-- ----------------------------
DROP TABLE IF EXISTS `categroymovietable`;
CREATE TABLE `categroymovietable` (
  `numid` int(100) NOT NULL AUTO_INCREMENT,
  `categroy` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`numid`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for moviedetailtable
-- ----------------------------
DROP TABLE IF EXISTS `moviedetailtable`;
CREATE TABLE `moviedetailtable` (
  `id` int(100) DEFAULT NULL,
  `director` varchar(100) DEFAULT NULL,
  `keyword` varchar(500) DEFAULT NULL,
  `categroy` varchar(500) DEFAULT NULL,
  `des` varchar(3000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for movieperformertable
-- ----------------------------
DROP TABLE IF EXISTS `movieperformertable`;
CREATE TABLE `movieperformertable` (
  `id` int(100) DEFAULT NULL,
  `performer` varchar(100) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for movietable
-- ----------------------------
DROP TABLE IF EXISTS `movietable`;
CREATE TABLE `movietable` (
  `id` int(100) NOT NULL AUTO_INCREMENT COMMENT '电影的标记',
  `moviename` varchar(100) DEFAULT NULL COMMENT '电影名称',
  `time` varchar(100) DEFAULT NULL COMMENT '电影播放长度',
  `url` varchar(500) DEFAULT NULL COMMENT '电影地址',
  `imagepath` varchar(2000) DEFAULT NULL COMMENT '图片地址',
  `saveimagepath` varchar(500) DEFAULT NULL COMMENT '图片本地保存地址',
  `score` float(10,1) DEFAULT NULL COMMENT '评分',
  `status` int(10) DEFAULT NULL COMMENT '完成状态',
  `source` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15996 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for performerdetailtable
-- ----------------------------
DROP TABLE IF EXISTS `performerdetailtable`;
CREATE TABLE `performerdetailtable` (
  `name` varchar(100) DEFAULT NULL,
  `e_name` varchar(100) DEFAULT NULL,
  `alias` varchar(200) DEFAULT NULL COMMENT '别名',
  `sex` varchar(10) DEFAULT '',
  `bloodtype` varchar(5) DEFAULT NULL,
  `height` varchar(10) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `birthday` varchar(50) DEFAULT NULL,
  `constellation` varchar(500) DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `ResidentialAddress` varchar(100) DEFAULT NULL,
  `school` varchar(200) DEFAULT NULL,
  `BrokerageAgency` varchar(200) DEFAULT NULL,
  `fameyear` varchar(200) DEFAULT NULL COMMENT '成名年代',
  `hobby` varchar(1000) DEFAULT NULL,
  `Occupation` varchar(500) DEFAULT NULL,
  `weight` varchar(500) DEFAULT NULL,
  `image` varchar(1000) DEFAULT NULL,
  `des` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
