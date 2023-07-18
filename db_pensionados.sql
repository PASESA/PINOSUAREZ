-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 17-07-2023 a las 22:46:03
-- Versión del servidor: 10.4.22-MariaDB
-- Versión de PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `movimientospens` (
  `Id_movs` int(10) UNSIGNED NOT NULL,
  `Idcliente` int(10) UNSIGNED NOT NULL,
  `num_tarjeta` int(11) NOT NULL,
  `Entrada` datetime DEFAULT NULL,
  `Salida` datetime DEFAULT NULL,
  `TiempoTotal` varchar(255) DEFAULT NULL,
  `Estatus` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagospens`
--

CREATE TABLE `pagospens` (
  `Id_pago` int(10) UNSIGNED NOT NULL,
  `Idcliente` int(10) UNSIGNED NOT NULL,
  `num_tarjeta` int(11) NOT NULL,
  `Fecha_pago` datetime DEFAULT NULL,
  `Fecha_vigencia` datetime DEFAULT NULL,
  `Mensualidad` varchar(255) DEFAULT NULL,
  `Monto` float DEFAULT NULL,
  `TipoPago` enum('Transferencia','Efectivo') NOT NULL DEFAULT 'Transferencia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Estructura de tabla para la tabla `pensionados`
--

CREATE TABLE `pensionados` (
  `Id_cliente` int(10) UNSIGNED NOT NULL,
  `Num_tarjeta` int(11) NOT NULL,
  `Nom_cliente` varchar(255) DEFAULT NULL,
  `Apell1_cliente` varchar(255) DEFAULT NULL,
  `Apell2_cliente` varchar(255) DEFAULT NULL,
  `Fecha_alta` datetime DEFAULT NULL,
  `Telefono1` varchar(25) DEFAULT NULL,
  `Telefono2` varchar(25) DEFAULT NULL,
  `Ciudad` varchar(255) DEFAULT NULL,
  `Colonia` varchar(255) DEFAULT NULL,
  `CP` varchar(8) DEFAULT NULL,
  `Calle_num` varchar(255) DEFAULT NULL,
  `Placas` varchar(50) DEFAULT NULL,
  `Modelo_auto` varchar(50) DEFAULT NULL,
  `Color_auto` varchar(20) DEFAULT NULL,
  `Vigencia` varchar(20) DEFAULT NULL,
  `Fecha_vigencia` datetime DEFAULT NULL,
  `Monto` int(15) DEFAULT NULL,
  `Estatus` varchar(20) DEFAULT NULL,
  `Cortesia` varchar(20) DEFAULT NULL,
  `Tolerancia` varchar(20) DEFAULT NULL,
  `Ult_Cambio` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indices de la tabla `movimientospens`
--
ALTER TABLE `movimientospens`
  ADD PRIMARY KEY (`Id_movs`),
  ADD KEY `Idcliente` (`Idcliente`);

--
-- Indices de la tabla `pagospens`
--
ALTER TABLE `pagospens`
  ADD PRIMARY KEY (`Id_pago`),
  ADD KEY `Idcliente` (`Idcliente`);

--
-- Indices de la tabla `pensionados`
--
ALTER TABLE `pensionados`
  ADD PRIMARY KEY (`Id_cliente`);

--
ALTER TABLE `movimientospens`
  ADD CONSTRAINT `MovimientosPens_ibfk_1` FOREIGN KEY (`Idcliente`) REFERENCES `pensionados` (`Id_cliente`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `pagospens`
--
ALTER TABLE `pagospens`
  ADD CONSTRAINT `PagosPens_ibfk_1` FOREIGN KEY (`Idcliente`) REFERENCES `pensionados` (`Id_cliente`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
