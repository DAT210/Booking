-- MySQL dump 10.13  Distrib 5.7.21, for Win64 (x86_64)
--
-- Host: localhost    Database: bookingdb
-- ------------------------------------------------------
-- Server version	5.7.21-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booking_info`
--

CREATE SCHEMA IF NOT EXISTS `bookingdb` ;
USE `bookingdb` ;

DROP TABLE IF EXISTS `booking_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booking_info` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `additional_info` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`bid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking_info`
--

LOCK TABLES `booking_info` WRITE;
/*!40000 ALTER TABLE `booking_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `booking_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `period`
--

DROP TABLE IF EXISTS `period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period` (
  `name` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `period`
--

LOCK TABLES `period` WRITE;
/*!40000 ALTER TABLE `period` DISABLE KEYS */;
INSERT INTO `period` VALUES ('breakfast','Breakfast'),('dinner','Dinner'),('lunch','Lunch');
/*!40000 ALTER TABLE `period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rest_book`
--

DROP TABLE IF EXISTS `rest_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rest_book` (
  `rid` int(11) NOT NULL,
  `bid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `timeid` int(11) DEFAULT NULL,
  PRIMARY KEY (`rid`,`bid`,`tid`),
  KEY `bid` (`bid`),
  KEY `tid` (`tid`),
  KEY `timeid` (`timeid`),
  CONSTRAINT `rest_book_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `restaurant` (`rid`),
  CONSTRAINT `rest_book_ibfk_2` FOREIGN KEY (`bid`) REFERENCES `booking_info` (`bid`),
  CONSTRAINT `rest_book_ibfk_3` FOREIGN KEY (`timeid`) REFERENCES `time_period` (`timeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rest_book`
--

LOCK TABLES `rest_book` WRITE;
/*!40000 ALTER TABLE `rest_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `rest_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurant` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `street` varchar(50) DEFAULT NULL,
  `latitude` varchar(15) DEFAULT NULL,
  `longitude` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`rid`),
  KEY `zip` (`zip`),
  CONSTRAINT `restaurant_ibfk_1` FOREIGN KEY (`zip`) REFERENCES `zip_city` (`zip`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (1,'Royale Stavanger','90010000',4005,'Kongsgårdbakken 1','5.730274','58.970052'),(2,'Mexico Randaberg','90020000',4070,'Tungenesveien 2','5.617925','59.000448'),(3,'Famoso Sandnes','90030000',4306,'Julie Eges Gate 6','5.739098','58.850582');
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_period`
--

DROP TABLE IF EXISTS `time_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time_period` (
  `timeid` int(11) NOT NULL,
  `time` time NOT NULL,
  `period` varchar(50) NOT NULL,
  PRIMARY KEY (`timeid`),
  KEY `period` (`period`),
  CONSTRAINT `time_period_ibfk_1` FOREIGN KEY (`period`) REFERENCES `period` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_period`
--

LOCK TABLES `time_period` WRITE;
/*!40000 ALTER TABLE `time_period` DISABLE KEYS */;
INSERT INTO `time_period` VALUES (1,'09:00:00','breakfast'),(2,'09:30:00','breakfast'),(3,'10:00:00','breakfast'),(4,'10:30:00','breakfast'),(5,'12:00:00','lunch'),(6,'12:30:00','lunch'),(7,'13:00:00','lunch'),(8,'13:30:00','lunch'),(9,'14:00:00','lunch'),(10,'14:30:00','lunch'),(11,'15:00:00','lunch'),(12,'17:00:00','dinner'),(13,'17:30:00','dinner'),(14,'18:00:00','dinner'),(15,'18:30:00','dinner'),(16,'19:00:00','dinner'),(17,'19:30:00','dinner'),(18,'20:00:00','dinner'),(19,'20:30:00','dinner'),(20,'21:00:00','dinner');
/*!40000 ALTER TABLE `time_period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zip_city`
--

DROP TABLE IF EXISTS `zip_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zip_city` (
  `zip` int(11) NOT NULL,
  `city` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`zip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zip_city`
--

LOCK TABLES `zip_city` WRITE;
/*!40000 ALTER TABLE `zip_city` DISABLE KEYS */;
INSERT INTO `zip_city` VALUES (4005,'Stavanger'),(4010,'Stavanger'),(4070,'Randaberg'),(4306,'Sandnes');
/*!40000 ALTER TABLE `zip_city` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-02 12:43:14
