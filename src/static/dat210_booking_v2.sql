-- MySQL dump 10.13  Distrib 5.7.21, for Win64 (x86_64)
--
-- Host: localhost    Database: DAT210_booking
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

DROP TABLE IF EXISTS `booking_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booking_info` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `rid` int(11) DEFAULT NULL,
  `additional_info` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`bid`),
  KEY `cid` (`cid`),
  KEY `fk_rid` (`rid`),
  CONSTRAINT `booking_info_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer` (`cid`),
  CONSTRAINT `fk_rid` FOREIGN KEY (`rid`) REFERENCES `rest_book` (`rid`)
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
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `street` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `zip` (`zip`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`zip`) REFERENCES `zip_city` (`zip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
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
  `date` datetime DEFAULT NULL,
  `for_hours` int(11) DEFAULT NULL,
  PRIMARY KEY (`rid`,`bid`,`tid`),
  KEY `bid` (`bid`),
  KEY `tid` (`tid`),
  CONSTRAINT `rest_book_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `restaurant` (`rid`),
  CONSTRAINT `rest_book_ibfk_2` FOREIGN KEY (`bid`) REFERENCES `booking_info` (`bid`)
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

-- Dump completed on 2018-10-15 20:53:34
