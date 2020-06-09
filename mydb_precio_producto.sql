-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.19

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

--
-- Table structure for table `precio_producto`
--

DROP TABLE IF EXISTS `precio_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `precio_producto` (
  `idProducto` varchar(16) NOT NULL,
  `fecha` date NOT NULL,
  `precioCosto` int NOT NULL,
  `precioVenta` int NOT NULL,
  PRIMARY KEY (`idProducto`,`fecha`),
  CONSTRAINT `idProducto` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idproducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `precio_producto`
--

LOCK TABLES `precio_producto` WRITE;
/*!40000 ALTER TABLE `precio_producto` DISABLE KEYS */;
INSERT INTO `precio_producto` VALUES ('4005808307326','2018-12-20',990,1290),('4005900528230','2018-12-20',700,990),('4005900528230','2019-01-06',800,1000),('4007817362020','2018-12-20',1500,2390),('4902505322723','2018-12-20',2500,3100),('4902505341618','2019-01-07',600,400),('4902505375132','2018-12-20',2500,3000),('7597','2018-12-22',490,690),('7597','2019-05-28',490,990),('7702018951185','2018-12-20',1000,1990),('78002456','2018-12-01',500,800),('78002456','2018-12-20',490,790),('78002456','2019-01-03',550,850),('7801620852955','2019-01-06',600,850),('7802175455806','2018-12-25',200,250),('7807210650079','2018-12-20',390,690),('7807265973352','2019-01-03',990,1290),('884938152419','2018-12-20',9990,14990),('9786073206037','2019-03-23',50000,70000),('9786076224441','2019-03-23',15000,18000),('9786076224946','2019-03-23',10000,13000),('9786076225950','2019-03-23',5000,7000),('9786076226612','2019-01-07',1,1),('9786076226612','2019-05-29',100,1),('9786076229446','2019-03-23',5000,7000),('9786076229446','2019-05-29',100,7000),('9786077071655','2019-04-10',100,200),('9789873832048','2019-03-23',15000,20000),('9789873832048','2019-05-29',100,20000);
/*!40000 ALTER TABLE `precio_producto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-06 23:56:36
