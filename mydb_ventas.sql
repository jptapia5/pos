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
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `idVenta` int NOT NULL,
  `montoVenta` int DEFAULT NULL,
  `folioBoleta` int DEFAULT NULL,
  `fechaVenta` date DEFAULT NULL,
  `idMedioPago` int DEFAULT NULL,
  `idCliente` int DEFAULT NULL,
  `idUsuario` int DEFAULT NULL,
  PRIMARY KEY (`idVenta`),
  KEY `mediopago_venta` (`idMedioPago`),
  KEY `cliente_venta` (`idCliente`),
  KEY `usuario_venta` (`idUsuario`),
  CONSTRAINT `cliente_venta` FOREIGN KEY (`idCliente`) REFERENCES `clientes` (`idCliente`),
  CONSTRAINT `mediopago_venta` FOREIGN KEY (`idMedioPago`) REFERENCES `medio_de_pago` (`idmediopago`),
  CONSTRAINT `usuario_venta` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (0,0,0,'0000-00-00',0,0,1000),(1,20000,12,'2019-05-27',2,1,1001),(2,7000,111,'2019-05-27',2,1,1000),(3,70000,112,'2019-05-27',2,1,1000),(4,7201,0,'2019-12-15',0,NULL,1000),(5,7201,0,'2019-12-15',0,NULL,1000),(6,7201,113,'2019-12-15',1,NULL,1000),(7,7201,0,'2019-12-15',0,NULL,1000),(8,7201,114,'2019-12-15',1,NULL,1000),(9,1,0,'2019-12-16',0,NULL,1000),(10,2,115,'2019-12-16',1,NULL,1000),(11,2,0,'2019-12-16',0,NULL,1000),(12,3,116,'2019-12-16',1,NULL,1000),(13,200,0,'2019-12-16',0,NULL,1000),(14,200,117,'2019-12-16',1,NULL,1000),(15,200,0,'2019-12-16',0,NULL,1000),(16,1000,118,'2019-12-16',1,NULL,1000),(17,14000,119,'2019-12-16',1,NULL,1000),(18,7000,120,'2019-12-16',1,NULL,1000),(19,7000,121,'2019-12-16',1,NULL,1000),(20,7000,122,'2019-12-16',1,NULL,1000),(21,7000,123,'2019-12-16',1,NULL,1000),(22,7000,124,'2019-12-16',1,NULL,1000),(23,90000,126,'2020-04-02',1,NULL,1000);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-06 23:56:38
