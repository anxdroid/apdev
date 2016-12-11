-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dic 11, 2016 alle 00:59
-- Versione del server: 5.5.53-0+deb8u1
-- PHP Version: 5.6.27-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `apdb`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `events`
--
-- Creazione: Dic 10, 2016 alle 20:13
--

DROP TABLE IF EXISTS `events`;
CREATE TABLE IF NOT EXISTS `events` (
`id` int(10) unsigned NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `category` varchar(200) NOT NULL,
  `cmd` varchar(200) NOT NULL,
  `value` varchar(200) NOT NULL,
  `source` varchar(15) NOT NULL,
  `params` text
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `events`
--

INSERT INTO `events` (`id`, `timestamp`, `category`, `cmd`, `value`, `source`, `params`) VALUES
(5, '2016-12-10 20:07:44', 'SRV', 'START', '2315', '192.168.1.3', '{"pid": "2315"}'),
(24, '2016-12-10 20:22:08', 'SRV', 'START', '2450', '192.168.1.3', '{"pid": "2450"}'),
(26, '2016-12-10 20:22:30', 'SRV', 'START', '2455', '192.168.1.3', '{"pid": "2455"}'),
(27, '2016-12-10 20:22:30', 'SRV', 'STOP', '2455', '192.168.1.3', '{"pid": "2455"}'),
(28, '2016-12-10 20:25:10', 'SRV', 'START', '2476', '192.168.1.3', '{"pid": "2476"}'),
(29, '2016-12-10 20:25:11', 'SRV', 'STOP', '2476', '192.168.1.3', '{"pid": "2476"}'),
(30, '2016-12-10 20:30:36', 'SRV', 'START', '2523', '192.168.1.3', '{"pid": "2523"}'),
(31, '2016-12-10 20:30:54', 'SRV', 'STOP', '2523', '192.168.1.3', '{"pid": "2523"}'),
(32, '2016-12-10 20:33:12', 'SRV', 'START', '2545', '192.168.1.3', '{"pid": "2545"}'),
(33, '2016-12-10 20:33:20', 'SRV', 'STOP', '2545', '192.168.1.3', '{"pid": "2545"}'),
(34, '2016-12-10 20:33:52', 'SRV', 'START', '2554', '192.168.1.3', '{"pid": "2554"}'),
(35, '2016-12-10 20:33:53', 'SRV', 'STOP', '2554', '192.168.1.3', '{"pid": "2554"}'),
(36, '2016-12-10 20:34:04', 'SRV', 'START', '2561', '192.168.1.3', '{"pid": "2561"}'),
(37, '2016-12-10 20:34:04', 'SRV', 'STOP', '2561', '192.168.1.3', '{"pid": "2561"}'),
(38, '2016-12-10 20:34:14', 'SRV', 'START', '2571', '192.168.1.3', '{"pid": "2571"}'),
(39, '2016-12-10 20:34:14', 'SRV', 'STOP', '2571', '192.168.1.3', '{"pid": "2571"}'),
(40, '2016-12-10 20:35:21', 'SRV', 'START', '2579', '192.168.1.3', '{"pid": "2579"}'),
(41, '2016-12-10 20:35:26', 'SRV', 'STOP', '2579', '192.168.1.3', '{"pid": "2579"}'),
(42, '2016-12-10 20:39:58', 'SRV', 'START', '2612', '192.168.1.3', '{"pid": "2612"}'),
(43, '2016-12-10 20:40:06', 'SRV', 'STOP', '2612', '192.168.1.3', '{"pid": "2612"}'),
(44, '2016-12-10 20:40:58', 'SRV', 'START', '2623', '192.168.1.3', '{"pid": "2623"}'),
(45, '2016-12-10 20:40:58', 'SRV', 'STOP', '2623', '192.168.1.3', '{"pid": "2623"}'),
(46, '2016-12-10 20:43:22', 'SRV', 'START', '2642', '192.168.1.3', '{"pid": "2642"}'),
(47, '2016-12-10 20:44:45', 'SRV', 'START', '2655', '192.168.1.3', '{"pid": "2655"}'),
(48, '2016-12-10 20:45:11', 'SRV', 'START', '2665', '192.168.1.3', '{"pid": "2665"}'),
(49, '2016-12-10 20:45:18', 'SRV', 'START', '2669', '192.168.1.3', '{"pid": "2669"}'),
(50, '2016-12-10 20:45:49', 'SRV', 'START', '2677', '192.168.1.3', '{"pid": "2677"}'),
(51, '2016-12-10 20:46:01', 'SRV', 'START', '2680', '192.168.1.3', '{"pid": "2680"}'),
(52, '2016-12-10 20:46:08', 'SRV', 'STOP', '2680', '192.168.1.3', '{"pid": "2680"}'),
(53, '2016-12-10 20:47:20', 'SRV', 'START', '2693', '192.168.1.3', '{"pid": "2693"}'),
(54, '2016-12-10 20:47:27', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52008], "pid": "2693", "thread": "<Process(Process-1, initial)>"}'),
(55, '2016-12-10 20:47:40', 'SRV', 'STOP', '2693', '192.168.1.3', '{"pid": "2693"}'),
(56, '2016-12-10 20:49:32', 'SRV', 'START', '2716', '192.168.1.3', '{"pid": "2716"}'),
(57, '2016-12-10 20:49:40', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52010], "pid": "2716", "thread": "<Process(Process-1, initial)>"}'),
(58, '2016-12-10 20:53:04', 'SRV', 'STOP', '2716', '192.168.1.3', '{"pid": "2716"}'),
(59, '2016-12-10 21:05:00', 'SRV', 'START', '2835', '192.168.1.3', '{"pid": "2835"}'),
(60, '2016-12-10 21:05:24', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52016], "pid": "2835", "thread": "<Process(Process-1, initial)>"}'),
(61, '2016-12-10 21:05:41', 'SRV', 'STOP', '2835', '192.168.1.3', '{"pid": "2835"}'),
(62, '2016-12-10 21:06:36', 'SRV', 'START', '2860', '192.168.1.3', '{"pid": "2860"}'),
(63, '2016-12-10 21:10:32', 'SRV', 'START', '2884', '192.168.1.3', '{"pid": "2884"}'),
(64, '2016-12-10 21:10:38', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52022], "pid": "2884", "thread": "<Process(Process-1, initial)>"}'),
(65, '2016-12-10 21:10:51', 'SRV', 'STOP', '2884', '192.168.1.3', '{"pid": "2884"}'),
(66, '2016-12-10 21:12:44', 'SRV', 'START', '2904', '192.168.1.3', '{"pid": "2904"}'),
(67, '2016-12-10 21:12:50', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52024], "pid": "2904", "thread": "<Process(Process-1, initial)>"}'),
(68, '2016-12-10 21:14:29', 'SRV', 'STOP', '2904', '192.168.1.3', '{"pid": "2904"}'),
(69, '2016-12-10 21:14:52', 'SRV', 'START', '2921', '192.168.1.3', '{"pid": "2921"}'),
(70, '2016-12-10 21:15:14', 'SRV', 'START', '2925', '192.168.1.3', '{"pid": "2925"}'),
(71, '2016-12-10 21:16:14', 'SRV', 'START', '2937', '192.168.1.3', '{"pid": "2937"}'),
(72, '2016-12-10 21:16:19', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52026], "pid": "2937", "thread": "<Process(Process-1, initial)>"}'),
(73, '2016-12-10 21:17:20', 'SRV', 'STOP', '2937', '192.168.1.3', '{"pid": "2937"}'),
(74, '2016-12-10 21:17:21', 'SRV', 'START', '2948', '192.168.1.3', '{"pid": "2948"}'),
(75, '2016-12-10 21:17:53', 'SRV', 'START', '2951', '192.168.1.3', '{"pid": "2951"}'),
(76, '2016-12-10 21:18:41', 'SRV', 'START', '2959', '192.168.1.3', '{"pid": "2959"}'),
(77, '2016-12-10 21:18:47', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52028], "pid": "2959", "thread": "<Process(Process-1, initial)>"}'),
(78, '2016-12-10 21:18:52', 'CMDSRV', 'AUTH', 'anto', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52028], "retval": "Get out !", "AUTH": false}'),
(79, '2016-12-10 21:19:03', 'CMDSRV', 'AUTH', 'anto', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52028], "retval": "Get out !", "AUTH": false}'),
(80, '2016-12-10 21:21:23', 'CMDSRV', 'AUTH', 'anto', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52028], "retval": "Get out !", "AUTH": false}'),
(81, '2016-12-10 21:21:31', 'SRV', 'STOP', '2959', '192.168.1.3', '{"pid": "2959"}'),
(82, '2016-12-10 21:26:27', 'SRV', 'START', '3028', '192.168.1.3', '{"pid": "3028"}'),
(83, '2016-12-10 21:26:55', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52044], "pid": "3028", "thread": "<Process(Process-1, initial)>"}'),
(84, '2016-12-10 21:27:09', 'SRV', 'STOP', '3028', '192.168.1.3', '{"pid": "3028"}'),
(85, '2016-12-10 21:27:39', 'SRV', 'START', '3052', '192.168.1.3', '{"pid": "3052"}'),
(86, '2016-12-10 21:29:23', 'SRV', 'START', '3068', '192.168.1.3', '{"pid": "3068"}'),
(87, '2016-12-10 21:29:24', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52046], "pid": "3068", "thread": "<Process(Process-1, initial)>"}'),
(89, '2016-12-10 21:36:05', 'SRV', 'START', '3132', '192.168.1.3', '{"pid": "3132"}'),
(90, '2016-12-10 21:36:44', 'SRV', 'START', '3136', '192.168.1.3', '{"pid": "3136"}'),
(91, '2016-12-10 21:37:40', 'SRV', 'START', '3148', '192.168.1.3', '{"pid": "3148"}'),
(92, '2016-12-10 21:38:41', 'SRV', 'START', '3156', '192.168.1.3', '{"pid": "3156"}'),
(93, '2016-12-10 21:39:30', 'SRV', 'START', '3182', '192.168.1.3', '{"pid": "3182"}'),
(94, '2016-12-10 21:40:03', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52052], "pid": "3182", "thread": "<Process(Process-1, initial)>"}'),
(95, '2016-12-10 21:40:16', 'SRV', 'STOP', '3182', '192.168.1.3', '{"pid": "3182"}'),
(96, '2016-12-10 21:41:38', 'SRV', 'START', '3219', '192.168.1.3', '{"pid": "3219"}'),
(97, '2016-12-10 21:41:42', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52054], "pid": "3219", "thread": "<Process(Process-1, initial)>"}'),
(98, '2016-12-10 21:41:54', 'SRV', 'STOP', '3219', '192.168.1.3', '{"pid": "3219"}'),
(99, '2016-12-10 21:42:23', 'SRV', 'START', '3232', '192.168.1.3', '{"pid": "3232"}'),
(100, '2016-12-10 21:42:26', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52056], "pid": "3232", "thread": "<Process(Process-1, initial)>"}'),
(101, '2016-12-10 21:42:35', 'SRV', 'STOP', '3232', '192.168.1.3', '{"pid": "3232"}'),
(102, '2016-12-10 21:43:16', 'SRV', 'START', '3244', '192.168.1.3', '{"pid": "3244"}'),
(103, '2016-12-10 21:43:18', 'CMDSRV', 'CONNECTION', '<Process(Process-1, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "pid": "3244", "thread": "<Process(Process-1, initial)>"}'),
(104, '2016-12-10 21:43:21', 'CMDSRV', 'AUTH', 'a', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "retval": "Get out !", "AUTH": false}'),
(105, '2016-12-10 21:43:29', 'CMDSRV', 'AUTH', 'anto_resistor', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "retval": "Get out !", "AUTH": false}'),
(106, '2016-12-10 21:43:36', 'CMDSRV', 'AUTH', 'anto', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "retval": "Welcome !", "AUTH": true}'),
(107, '2016-12-10 21:44:08', 'CMDSRV', 'HETER', 'a', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "retval": "Unknown command !", "AUTH": true}'),
(108, '2016-12-10 21:44:14', 'CMDSRV', 'HATERS', 'OFF', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "retval": "Unknown command !", "AUTH": true}'),
(109, '2016-12-10 21:44:25', 'CMDSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52058], "retval": "GPIO 18 HIGH", "AUTH": true}'),
(110, '2016-12-10 21:49:23', 'SRV', 'STOP', '3244', '192.168.1.3', '{"pid": "3244"}'),
(111, '2016-12-10 21:49:24', 'SRV', 'START', '3292', '192.168.1.3', '{"pid": "3292"}'),
(112, '2016-12-10 21:50:25', 'SRV', 'START', '3301', '192.168.1.3', '{"pid": "3301"}'),
(113, '2016-12-10 21:51:23', 'SRV', 'START', '3311', '192.168.1.3', '{"pid": "3311"}'),
(114, '2016-12-10 21:51:28', 'SRV', 'STOP', '3311', '192.168.1.3', '{"pid": "3311"}'),
(115, '2016-12-10 21:52:20', 'SRV', 'START', '3324', '192.168.1.3', '{"pid": "3324"}'),
(116, '2016-12-10 21:52:44', 'SRV', 'STOP', '3324', '192.168.1.3', '{"pid": "3324"}'),
(117, '2016-12-10 21:52:45', 'SRV', 'START', '3330', '192.168.1.3', '{"pid": "3330"}'),
(118, '2016-12-10 21:53:23', 'CMDSRV', 'CONNECTION', '<Process(Process-2, initial)>', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52064], "pid": "3330", "thread": "<Process(Process-2, initial)>"}'),
(119, '2016-12-10 21:53:30', 'CMDSRV', 'AUTH', 'anto', '192.168.1.3', '{"clientaddr": ["127.0.0.1", 52064], "retval": "Welcome !", "AUTH": true}'),
(120, '2016-12-10 21:58:12', 'SRV', 'STOP', '3330', '192.168.1.3', '{"pid": "3330"}'),
(121, '2016-12-10 21:59:38', 'SRV', 'START', '3523', '192.168.1.3', '{"pid": "3523"}'),
(122, '2016-12-10 21:59:38', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 1, "AUTH": true}'),
(123, '2016-12-10 22:02:41', 'SRV', 'STOP', '3523', '192.168.1.3', '{"pid": "3523"}'),
(124, '2016-12-10 22:02:49', 'SRV', 'START', '3549', '192.168.1.3', '{"pid": "3549"}'),
(125, '2016-12-10 22:02:49', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 2, "AUTH": true}'),
(126, '2016-12-10 22:02:56', 'SRV', 'STOP', '3549', '192.168.1.3', '{"pid": "3549"}'),
(127, '2016-12-10 22:03:32', 'SRV', 'START', '3561', '192.168.1.3', '{"pid": "3561"}'),
(128, '2016-12-10 22:06:57', 'SRV', 'STOP', '3561', '192.168.1.3', '{"pid": "3561"}'),
(129, '2016-12-10 22:06:58', 'SRV', 'START', '3589', '192.168.1.3', '{"pid": "3589"}'),
(130, '2016-12-10 22:06:58', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 3, "AUTH": true}'),
(131, '2016-12-10 22:07:55', 'SRV', 'STOP', '3589', '192.168.1.3', '{"pid": "3589"}'),
(132, '2016-12-10 22:07:58', 'SRV', 'START', '3601', '192.168.1.3', '{"pid": "3601"}'),
(133, '2016-12-10 22:08:40', 'SRV', 'STOP', '3601', '192.168.1.3', '{"pid": "3601"}'),
(134, '2016-12-10 22:09:44', 'SRV', 'START', '3618', '192.168.1.3', '{"pid": "3618"}'),
(135, '2016-12-10 22:10:17', 'SRV', 'STOP', '3618', '192.168.1.3', '{"pid": "3618"}'),
(136, '2016-12-10 22:10:24', 'SRV', 'START', '3630', '192.168.1.3', '{"pid": "3630"}'),
(137, '2016-12-10 22:10:25', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 4, "AUTH": true}'),
(138, '2016-12-10 22:11:15', 'SRV', 'STOP', '3630', '192.168.1.3', '{"pid": "3630"}'),
(139, '2016-12-10 22:16:53', 'SRV', 'START', '3686', '192.168.1.3', '{"pid": "3686"}'),
(140, '2016-12-10 22:16:59', 'SRV', 'STOP', '3686', '192.168.1.3', '{"pid": "3686"}'),
(141, '2016-12-10 22:17:30', 'SRV', 'START', '3694', '192.168.1.3', '{"pid": "3694"}'),
(142, '2016-12-10 22:17:37', 'SRV', 'STOP', '3694', '192.168.1.3', '{"pid": "3694"}'),
(143, '2016-12-10 22:19:21', 'SRV', 'START', '3712', '192.168.1.3', '{"pid": "3712"}'),
(144, '2016-12-10 22:19:21', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 5, "AUTH": true}'),
(145, '2016-12-10 22:19:48', 'SRV', 'STOP', '3712', '192.168.1.3', '{"pid": "3712"}'),
(146, '2016-12-10 22:20:35', 'SRV', 'START', '3728', '192.168.1.3', '{"pid": "3728"}'),
(147, '2016-12-10 22:20:35', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 6, "AUTH": true}'),
(148, '2016-12-10 22:20:54', 'SRV', 'STOP', '3728', '192.168.1.3', '{"pid": "3728"}'),
(149, '2016-12-10 22:24:32', 'SRV', 'START', '3755', '192.168.1.3', '{"pid": "3755"}'),
(150, '2016-12-10 22:24:36', 'SRV', 'STOP', '3755', '192.168.1.3', '{"pid": "3755"}'),
(151, '2016-12-10 22:29:02', 'SRV', 'START', '3787', '192.168.1.3', '{"pid": "3787"}'),
(152, '2016-12-10 22:30:13', 'SRV', 'STOP', '3787', '192.168.1.3', '{"pid": "3787"}'),
(153, '2016-12-10 22:32:07', 'SRV', 'START', '3816', '192.168.1.3', '{"pid": "3816"}'),
(154, '2016-12-10 22:32:07', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 7, "AUTH": true}'),
(155, '2016-12-10 22:32:31', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 8, "AUTH": true}'),
(156, '2016-12-10 22:33:07', 'SRV', 'STOP', '3816', '192.168.1.3', '{"pid": "3816"}'),
(157, '2016-12-10 22:53:22', 'SRV', 'START', '3979', '192.168.1.3', '{"pid": "3979"}'),
(158, '2016-12-10 22:53:47', 'SRV', 'START', '3989', '192.168.1.3', '{"pid": "3989"}'),
(159, '2016-12-10 22:53:54', 'SRV', 'STOP', '3989', '192.168.1.3', '{"pid": "3989"}'),
(160, '2016-12-10 22:56:29', 'SRV', 'START', '4014', '192.168.1.3', '{"pid": "4014"}'),
(161, '2016-12-10 22:58:57', 'SRV', 'STOP', '4014', '192.168.1.3', '{"pid": "4014"}'),
(162, '2016-12-10 23:06:49', 'SRV', 'START', '4106', '192.168.1.3', '{"pid": "4106"}'),
(163, '2016-12-10 23:06:52', 'SRV', 'STOP', '4106', '192.168.1.3', '{"pid": "4106"}'),
(164, '2016-12-10 23:07:32', 'SRV', 'START', '4118', '192.168.1.3', '{"pid": "4118"}'),
(165, '2016-12-10 23:07:50', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": null, "retval": "GPIO 18 HIGH", "job_id": 1, "AUTH": true}'),
(166, '2016-12-10 23:08:07', 'SRV', 'STOP', '4118', '192.168.1.3', '{"pid": "4118"}'),
(167, '2016-12-10 23:09:27', 'SRV', 'START', '4134', '192.168.1.3', '{"pid": "4134"}'),
(168, '2016-12-10 23:09:31', 'SRV', 'STOP', '4134', '192.168.1.3', '{"pid": "4134"}'),
(169, '2016-12-10 23:10:55', 'SRV', 'START', '4151', '192.168.1.3', '{"pid": "4151"}'),
(170, '2016-12-10 23:10:59', 'SRV', 'STOP', '4151', '192.168.1.3', '{"pid": "4151"}'),
(171, '2016-12-10 23:14:44', 'SRV', 'START', '4184', '192.168.1.3', '{"pid": "4184"}'),
(172, '2016-12-10 23:15:34', 'SRV', 'STOP', '4184', '192.168.1.3', '{"pid": "4184"}'),
(173, '2016-12-10 23:17:25', 'SRV', 'START', '4208', '192.168.1.3', '{"pid": "4208"}'),
(174, '2016-12-10 23:17:29', 'SRV', 'STOP', '4208', '192.168.1.3', '{"pid": "4208"}'),
(175, '2016-12-10 23:18:09', 'SRV', 'START', '4220', '192.168.1.3', '{"pid": "4220"}'),
(176, '2016-12-10 23:18:13', 'SRV', 'STOP', '4220', '192.168.1.3', '{"pid": "4220"}'),
(177, '2016-12-10 23:19:21', 'SRV', 'START', '4234', '192.168.1.3', '{"pid": "4234"}'),
(178, '2016-12-10 23:19:22', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": null, "retval": "GPIO 18 HIGH", "job_id": 1, "AUTH": true}'),
(179, '2016-12-10 23:19:35', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": null, "retval": "GPIO 18 HIGH", "job_id": 1, "AUTH": true}'),
(180, '2016-12-10 23:19:53', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": null, "retval": "GPIO 18 HIGH", "job_id": 1, "AUTH": true}'),
(181, '2016-12-10 23:20:04', 'SRV', 'STOP', '4234', '192.168.1.3', '{"pid": "4234"}'),
(182, '2016-12-10 23:20:08', 'SRV', 'START', '4245', '192.168.1.3', '{"pid": "4245"}'),
(183, '2016-12-10 23:20:27', 'SRV', 'STOP', '4245', '192.168.1.3', '{"pid": "4245"}'),
(184, '2016-12-10 23:21:26', 'SRV', 'START', '4263', '192.168.1.3', '{"pid": "4263"}'),
(185, '2016-12-10 23:21:26', 'TRGSRV', 'HEATERS', 'OFF', '127.0.0.1', 'Trigger id: 1'),
(186, '2016-12-10 23:22:42', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 1, "AUTH": true}'),
(187, '2016-12-10 23:23:42', 'SRV', 'STOP', '4263', '192.168.1.3', '{"pid": "4263"}'),
(188, '2016-12-10 23:24:33', 'SRV', 'START', '4288', '192.168.1.3', '{"pid": "4288"}'),
(189, '2016-12-10 23:24:33', 'JOBSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"clientaddr": "", "retval": "GPIO 18 HIGH", "job_id": 9, "AUTH": true}'),
(190, '2016-12-10 23:24:55', 'TRGSRV', 'HEATERS', 'OFF', '127.0.0.1', 'Trigger id: 1'),
(191, '2016-12-10 23:25:21', 'TRGSRV', 'HEATERS', 'OFF', '127.0.0.1', 'Trigger id: 1'),
(192, '2016-12-10 23:27:01', 'SRV', 'STOP', '4288', '192.168.1.3', '{"pid": "4288"}'),
(193, '2016-12-10 23:27:09', 'SRV', 'START', '4311', '192.168.1.3', '{"pid": "4311"}'),
(194, '2016-12-10 23:28:29', 'SRV', 'STOP', '4311', '192.168.1.3', '{"pid": "4311"}'),
(195, '2016-12-10 23:31:32', 'SRV', 'START', '4350', '192.168.1.3', '{"pid": "4350"}'),
(196, '2016-12-10 23:32:54', 'TRGSRV', 'HEATERS', 'OFF', '127.0.0.1', 'Trigger id: 1'),
(197, '2016-12-10 23:36:31', 'SRV', 'STOP', '4350', '192.168.1.3', '{"pid": "4350"}'),
(198, '2016-12-10 23:36:34', 'SRV', 'START', '4390', '192.168.1.3', '{"pid": "4390"}'),
(199, '2016-12-10 23:36:55', 'SRV', 'STOP', '4390', '192.168.1.3', '{"pid": "4390"}'),
(200, '2016-12-10 23:36:59', 'SRV', 'START', '4398', '192.168.1.3', '{"pid": "4398"}'),
(201, '2016-12-10 23:37:51', 'TRIGGERSRV', 'HEATERS', 'OFF', '192.168.1.3', '{"retval": "GPIO 18 HIGH", "AUTH": true, "trigger_id": 1}'),
(202, '2016-12-10 23:38:40', 'SRV', 'STOP', '4398', '192.168.1.3', '{"pid": "4398"}'),
(203, '2016-12-10 23:48:51', 'SRV', 'START', '4500', '192.168.1.3', '{"pid": "4500"}'),
(204, '2016-12-10 23:48:54', 'SRV', 'STOP', '4500', '192.168.1.3', '{"pid": "4500"}'),
(205, '2016-12-10 23:49:37', 'SRV', 'START', '4510', '192.168.1.3', '{"pid": "4510"}'),
(206, '2016-12-10 23:52:31', 'SRV', 'STOP', '4510', '192.168.1.3', '{"pid": "4510"}');

-- --------------------------------------------------------

--
-- Struttura della tabella `jobs`
--
-- Creazione: Dic 10, 2016 alle 21:58
--

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE IF NOT EXISTS `jobs` (
`id` int(10) unsigned NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cmd` varchar(250) NOT NULL,
  `status` int(3) NOT NULL DEFAULT '0',
  `ip` varchar(15) NOT NULL,
  `started` timestamp NULL DEFAULT NULL,
  `ended` timestamp NULL DEFAULT NULL,
  `source` varchar(15) NOT NULL DEFAULT '127.0.0.1'
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `jobs`
--

INSERT INTO `jobs` (`id`, `timestamp`, `cmd`, `status`, `ip`, `started`, `ended`, `source`) VALUES
(1, '2016-12-10 23:36:36', 'HEATERS:OFF', 1, '', '2016-12-10 23:36:36', '2016-12-10 23:22:42', '127.0.0.1'),
(2, '2016-12-10 22:02:49', 'HEATERS:OFF', 2, '', '2016-12-10 22:02:49', '2016-12-10 22:02:49', '127.0.0.1'),
(3, '2016-12-10 22:06:58', 'HEATERS:OFF', 2, '', '2016-12-10 22:06:58', '2016-12-10 22:06:58', '127.0.0.1'),
(4, '2016-12-10 22:10:25', 'HEATERS:OFF', 2, '', '2016-12-10 22:10:25', '2016-12-10 22:10:25', '127.0.0.1'),
(5, '2016-12-10 22:19:21', 'HEATERS:OFF', 2, '', '2016-12-10 22:19:21', '2016-12-10 22:19:21', '127.0.0.1'),
(6, '2016-12-10 22:20:35', 'HEATERS:OFF', 2, '', '2016-12-10 22:20:35', '2016-12-10 22:20:35', '127.0.0.1'),
(7, '2016-12-10 22:32:07', 'HEATERS:OFF', 2, '', '2016-12-10 22:32:07', '2016-12-10 22:32:07', '127.0.0.1'),
(8, '2016-12-10 22:32:31', 'HEATERS:OFF', 2, '', '2016-12-10 22:32:31', '2016-12-10 22:32:31', '127.0.0.1'),
(9, '2016-12-10 23:24:33', 'HEATERS:OFF', 2, '', '2016-12-10 23:24:33', '2016-12-10 23:24:33', '127.0.0.1');

-- --------------------------------------------------------

--
-- Struttura della tabella `sensors`
--
-- Creazione: Dic 10, 2016 alle 23:32
--

DROP TABLE IF EXISTS `sensors`;
CREATE TABLE IF NOT EXISTS `sensors` (
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `value` decimal(6,3) NOT NULL,
  `source` varchar(250) NOT NULL DEFAULT 'TEMP_SALOTTO',
  `unit` varchar(50) DEFAULT '&deg;'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `sensors`
--

INSERT INTO `sensors` (`timestamp`, `value`, `source`, `unit`) VALUES
('2016-12-10 18:23:50', 19.700, 'TEMP_DISIMPEGNO', '&deg;'),
('2016-12-10 18:23:50', 45.200, 'UMID_DISIMPEGNO', '%'),
('2016-12-10 18:24:21', 20.000, 'TEMP_SALOTTO', '&deg;'),
('2016-12-10 18:24:29', 0.400, 'TEMP_DISIMPEGNO', '&deg;'),
('2016-12-10 18:24:29', 38.800, 'UMID_DISIMPEGNO', '%'),
('2016-12-10 18:25:01', 19.600, 'TEMP_DISIMPEGNO', '&deg;'),
('2016-12-10 18:25:01', 45.300, 'UMID_DISIMPEGNO', '%'),
('2016-12-10 23:32:27', 20.000, 'TEMP_SALOTTO', '&deg;'),
('2016-12-10 23:37:36', 20.000, 'TEMP_SALOTTO', '&deg;'),
('2016-12-10 23:49:38', 19.187, 'TEMP_SALOTTO', '&deg;'),
('2016-12-10 23:49:59', 9.100, 'TEMP_DISIMPEGNO', '&deg;'),
('2016-12-10 23:50:30', 19.187, 'TEMP_SALOTTO', '&deg;'),
('2016-12-10 23:51:01', 18.300, 'TEMP_DISIMPEGNO', '&deg;'),
('2016-12-10 23:51:01', 47.200, 'UMID_DISIMPEGNO', '%'),
('2016-12-10 23:51:32', 19.250, 'TEMP_SALOTTO', '&deg;'),
('2016-12-10 23:51:40', 18.300, 'TEMP_DISIMPEGNO', '&deg;'),
('2016-12-10 23:51:40', 47.200, 'UMID_DISIMPEGNO', '%'),
('2016-12-10 23:52:11', 19.187, 'TEMP_SALOTTO', '&deg;');

-- --------------------------------------------------------

--
-- Struttura della tabella `thresholds`
--
-- Creazione: Dic 10, 2016 alle 15:29
--

DROP TABLE IF EXISTS `thresholds`;
CREATE TABLE IF NOT EXISTS `thresholds` (
`id` int(10) unsigned NOT NULL,
  `source` text NOT NULL,
  `min` decimal(6,3) NOT NULL,
  `max` decimal(6,3) NOT NULL,
  `active` int(3) unsigned NOT NULL DEFAULT '1'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `thresholds`
--

INSERT INTO `thresholds` (`id`, `source`, `min`, `max`, `active`) VALUES
(1, 'TEMP_SALOTTO', 20.000, 21.000, 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `triggers`
--
-- Creazione: Dic 10, 2016 alle 15:33
--

DROP TABLE IF EXISTS `triggers`;
CREATE TABLE IF NOT EXISTS `triggers` (
`id` int(10) unsigned NOT NULL,
  `expression` text NOT NULL,
  `cmd` varchar(250) NOT NULL,
  `active` int(3) unsigned NOT NULL,
  `last_triggered` timestamp NULL DEFAULT NULL,
  `last_result` int(3) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `triggers`
--

INSERT INTO `triggers` (`id`, `expression`, `cmd`, `active`, `last_triggered`, `last_result`) VALUES
(1, '1', 'HEATERS:OFF', 1, '2016-12-10 23:37:51', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--
-- Creazione: Dic 10, 2016 alle 15:36
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
`id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `group` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `realm` varchar(100) DEFAULT 'apdom'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `group`, `timestamp`, `realm`) VALUES
(1, 'anto', '$apr1$rg04ZUqm$x/8a5EBCbyAhvKciRRNLX.', 'admin', '2016-12-10 21:21:13', 'apdom');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `events`
--
ALTER TABLE `events`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sensors`
--
ALTER TABLE `sensors`
 ADD PRIMARY KEY (`timestamp`,`value`);

--
-- Indexes for table `thresholds`
--
ALTER TABLE `thresholds`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `triggers`
--
ALTER TABLE `triggers`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=207;
--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `thresholds`
--
ALTER TABLE `thresholds`
MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `triggers`
--
ALTER TABLE `triggers`
MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
