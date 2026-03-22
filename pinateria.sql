-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 22-03-2026 a las 21:19:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pinateria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `precio`, `stock`) VALUES
(1, 'Pelota de fútbol', 15.50, 20),
(2, 'Muñeca Barbie', 25.00, 15),
(3, 'Carrito de juguete', 12.00, 30),
(4, 'Rompecabezas 1000 piezas', 18.75, 10),
(5, 'Lego set básico', 40.00, 25),
(6, 'Pelota de baloncesto', 20.00, 10),
(7, 'Aros de hula hoop', 8.50, 40),
(8, 'Patineta', 35.00, 8),
(9, 'Peluche oso', 10.00, 50),
(10, 'Libro infantil', 7.50, 60),
(11, 'Set de pinturas', 12.50, 20),
(12, 'Carrito teledirigido', 30.00, 12),
(13, 'Rompecabezas 500 piezas', 12.00, 18),
(14, 'Muñeco de acción', 15.00, 25),
(15, 'Bicicleta infantil', 80.00, 5),
(16, 'Set de instrumentos musicales', 25.00, 10),
(17, 'Cubo Rubik', 5.00, 30),
(18, 'Avión de juguete', 20.00, 15),
(19, 'Pista de autos', 35.00, 12),
(20, 'Set de plastilina', 8.00, 40),
(21, 'Disfraz de superhéroe', 20.00, 8),
(22, 'Rompecabezas 200 piezas', 5.00, 25),
(23, 'Pelota de voleibol', 18.00, 15),
(24, 'Muñeca bebé', 22.00, 10),
(25, 'Tren de juguete', 30.00, 5),
(26, 'Set de construcción magnético', 45.00, 7),
(27, 'Puzzle 3D', 25.00, 10),
(28, 'Coche de carreras', 18.00, 12),
(29, 'Set de dibujo', 15.00, 20),
(30, 'Pelota de tenis', 10.00, 25),
(31, 'velas #3', 4.00, 1),
(32, 'vela #4', 5.00, 1),
(33, 'vela #5', 5.00, 1),
(34, 'vela #6', 5.00, 1),
(35, 'velas #7', 4.00, 1),
(36, 'flores azules', 24.00, 1),
(37, 'rasas amarillas', 20.00, 1),
(38, 'girasoles ', 10.00, 1),
(39, 'caja musical', 5.00, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `password`) VALUES
(1, 'Luis Admin', 'admin@gmail.com', '1234'),
(2, 'smal', 'smal@usuario', '1234');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
