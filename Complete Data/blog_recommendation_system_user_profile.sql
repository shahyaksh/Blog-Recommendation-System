-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: blog-recommedation-system.cu9zz7jlsnla.ap-south-1.rds.amazonaws.com    Database: blog_recommendation_system
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profile` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(40) DEFAULT NULL,
  `user_email` varchar(80) DEFAULT NULL,
  `user_pic` text,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile`
--

LOCK TABLES `user_profile` WRITE;
/*!40000 ALTER TABLE `user_profile` DISABLE KEYS */;
INSERT INTO `user_profile` VALUES (10,'Yaksh@178','yakshshah170802@gmail.com','71ac684267d38b00e8cae14e2ce7c5f0avatar image.png'),(11,'Yaksh@123','20IT404@bvmengineering.ac.in','default_profile_pic.jpg'),(13,'MDA','manndesai03@gmail.com','1e5edf6ec504ba4eavatar image.png'),(14,'ruchib_0810','ruchishingala2771@gmail.com','default_profile_pic.jpg'),(15,' vatsalshah','vatsal.shah@bvmengineering.ac.in','62253359349e87616.jpg'),(16,'Yash','capcool81@gmail.com','default_profile_pic.jpg'),(17,'Ajay','capcool79@gmail.com','default_profile_pic.jpg'),(18,'gfgbvm22','geeksforgeeksbvm@bvmengineering.ac.in','default_profile_pic.jpg'),(19,'Mann','desaimn2003@gmail.com','default_profile_pic.jpg'),(20,'Neelam@22','whitefeather2211@gmail.com','default_profile_pic.jpg'),(21,'mann','20it405@bvmengineering.ac.in','default_profile_pic.jpg'),(22,'Yaksh178','no.reply.yakshblog@gmail.com','default_profile_pic.jpg'),(23,'Yaksh@178','mnd180203@gmail.com','default_profile_pic.jpg');
/*!40000 ALTER TABLE `user_profile` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-11 10:37:09
