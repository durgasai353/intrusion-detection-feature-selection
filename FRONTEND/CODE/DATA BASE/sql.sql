/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - analysis
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`analysis` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `analysis`;

/*Table structure for table `intursion` */

DROP TABLE IF EXISTS `intursion`;

CREATE TABLE `intursion` (
  `s.no` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`s.no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `intursion` */

insert  into `intursion`(`s.no`,`name`,`email`,`password`,`phone`) values (1,'hello','hello@gmail.com','123','7894561230');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
