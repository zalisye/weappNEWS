/*
Navicat MySQL Data Transfer

Source Server         : 123.206.13.98_3306
Source Server Version : 50636
Source Host           : 123.206.13.98:3306
Source Database       : news

Target Server Type    : MYSQL
Target Server Version : 50636
File Encoding         : 65001

Date: 2017-06-10 23:09:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for data
-- ----------------------------
DROP TABLE IF EXISTS `data`;
CREATE TABLE `data` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` text COLLATE utf8_bin NOT NULL,
  `Abstract` text COLLATE utf8_bin NOT NULL,
  `Context` longtext COLLATE utf8_bin NOT NULL,
  `Imagepath` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `Audiopath` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `School` varchar(255) COLLATE utf8_bin NOT NULL,
  `Time_stamp` date NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3341 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
