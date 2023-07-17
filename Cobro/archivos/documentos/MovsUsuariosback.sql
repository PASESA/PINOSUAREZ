-- MySQL dump 10.19  Distrib 10.3.29-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: Parqueadero1
-- ------------------------------------------------------
-- Server version	10.3.29-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `MovsUsuarios`
--

DROP TABLE IF EXISTS `MovsUsuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MovsUsuarios` (
  `Id_movs` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Idusuario` int(10) unsigned NOT NULL,
  `usuario` varchar(25) NOT NULL,
  `inicio` datetime DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `turno` int(11) DEFAULT NULL,
  `comentarios` varchar(255) DEFAULT NULL,
  `CierreCorte` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Id_movs`),
  KEY `Idusuario` (`Idusuario`),
  CONSTRAINT `MovsUsuarios_ibfk_1` FOREIGN KEY (`Idusuario`) REFERENCES `Usuarios` (`Id_usuario`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MovsUsuarios`
--

LOCK TABLES `MovsUsuarios` WRITE;
/*!40000 ALTER TABLE `MovsUsuarios` DISABLE KEYS */;
INSERT INTO `MovsUsuarios` VALUES (1,1,'AG','2022-08-27 02:28:41','Aurelio Guarneros Ruiz',3,NULL,'2022-08-27 03:50:39.'),(2,1,'AG','2022-08-27 03:32:30','Aurelio Guarneros Ruiz',1,NULL,'No aplica'),(3,1,'AG','2022-08-27 03:50:25','Aurelio Guarneros Ruiz',1,NULL,'No aplica'),(4,1,'AG','2022-08-27 03:55:53','Aurelio Guarneros Ruiz',1,NULL,'2022-08-27 03:56:59.'),(5,1,'AG','2022-08-27 04:07:16','Aurelio Guarneros Ruiz',1,NULL,'2022-08-27 04:07:24.');
/*!40000 ALTER TABLE `MovsUsuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-27  5:03:44
