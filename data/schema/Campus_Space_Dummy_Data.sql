BEGIN TRANSACTION;
CREATE TABLE blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE, -- e.g. Block-25
    code VARCHAR(10) NOT NULL UNIQUE   -- e.g. B25
);
INSERT INTO "blocks" VALUES(1,'Block-25','B25');
INSERT INTO "blocks" VALUES(2,'Block-26','B26');
INSERT INTO "blocks" VALUES(3,'Block-27','B27');
INSERT INTO "blocks" VALUES(4,'Block-28','B28');
CREATE TABLE canteen_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    canteen_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    check_out_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Active' CHECK(status IN ('Active', 'Checked Out', 'Expired')),
    FOREIGN KEY (canteen_id) REFERENCES canteens(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE canteens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER NOT NULL UNIQUE,
    floor_id INTEGER NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE, -- e.g. B25C
    capacity INTEGER NOT NULL CHECK(capacity BETWEEN 100 AND 200),
    qr_code_identifier VARCHAR(100) NOT NULL UNIQUE,
    default_visit_duration_min INTEGER DEFAULT 20,
    FOREIGN KEY (block_id) REFERENCES blocks(id) ON DELETE CASCADE,
    FOREIGN KEY (floor_id) REFERENCES floors(id) ON DELETE CASCADE
);
INSERT INTO "canteens" VALUES(1,1,6,'B25 Main Canteen','B25C',120,'QR_B25C_FLOOR6',20);
INSERT INTO "canteens" VALUES(2,2,14,'B26 Main Canteen','B26C',150,'QR_B26C_FLOOR6',20);
INSERT INTO "canteens" VALUES(3,3,22,'B27 Main Canteen','B27C',180,'QR_B27C_FLOOR6',20);
INSERT INTO "canteens" VALUES(4,4,30,'B28 Main Canteen','B28C',140,'QR_B28C_FLOOR6',20);
CREATE TABLE classroom_verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reported_status VARCHAR(30) NOT NULL CHECK(reported_status IN ('Reported Available', 'Reported Occupied', 'Restricted')),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floor_id INTEGER NOT NULL,
    room_number VARCHAR(20) NOT NULL, -- e.g. B25-101
    capacity INTEGER DEFAULT 60 CHECK(capacity = 60),
    student_sockets INTEGER DEFAULT 60 CHECK(student_sockets = 60),
    faculty_sockets INTEGER DEFAULT 2 CHECK(faculty_sockets = 2),
    ac_count INTEGER DEFAULT 2 CHECK(ac_count = 2),
    is_quiet_zone BOOLEAN DEFAULT 1,
    FOREIGN KEY (floor_id) REFERENCES floors(id) ON DELETE CASCADE,
    UNIQUE(floor_id, room_number)
);
INSERT INTO "classrooms" VALUES(1,1,'B25-101',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(2,1,'B25-102',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(3,1,'B25-103',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(4,1,'B25-104',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(5,1,'B25-105',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(6,1,'B25-106',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(7,1,'B25-107',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(8,1,'B25-108',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(9,1,'B25-109',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(10,1,'B25-110',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(11,2,'B25-201',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(12,2,'B25-202',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(13,2,'B25-203',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(14,2,'B25-204',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(15,2,'B25-205',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(16,2,'B25-206',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(17,2,'B25-207',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(18,2,'B25-208',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(19,2,'B25-209',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(20,2,'B25-210',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(21,3,'B25-301',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(22,3,'B25-302',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(23,3,'B25-303',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(24,3,'B25-304',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(25,3,'B25-305',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(26,3,'B25-306',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(27,3,'B25-307',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(28,3,'B25-308',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(29,3,'B25-309',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(30,3,'B25-310',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(31,4,'B25-401',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(32,4,'B25-402',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(33,4,'B25-403',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(34,4,'B25-404',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(35,4,'B25-405',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(36,4,'B25-406',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(37,4,'B25-407',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(38,4,'B25-408',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(39,4,'B25-409',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(40,4,'B25-410',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(41,5,'B25-501',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(42,5,'B25-502',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(43,5,'B25-503',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(44,5,'B25-504',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(45,5,'B25-505',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(46,5,'B25-506',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(47,5,'B25-507',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(48,5,'B25-508',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(49,5,'B25-509',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(50,5,'B25-510',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(51,6,'B25-601',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(52,6,'B25-602',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(53,6,'B25-603',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(54,6,'B25-604',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(55,6,'B25-605',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(56,6,'B25-606',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(57,6,'B25-607',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(58,6,'B25-608',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(59,6,'B25-609',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(60,6,'B25-610',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(61,7,'B25-701',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(62,7,'B25-702',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(63,7,'B25-703',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(64,7,'B25-704',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(65,7,'B25-705',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(66,7,'B25-706',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(67,7,'B25-707',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(68,7,'B25-708',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(69,7,'B25-709',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(70,7,'B25-710',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(71,8,'B25-801',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(72,8,'B25-802',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(73,8,'B25-803',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(74,8,'B25-804',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(75,8,'B25-805',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(76,8,'B25-806',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(77,8,'B25-807',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(78,8,'B25-808',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(79,8,'B25-809',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(80,8,'B25-810',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(81,9,'B26-101',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(82,9,'B26-102',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(83,9,'B26-103',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(84,9,'B26-104',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(85,9,'B26-105',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(86,9,'B26-106',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(87,9,'B26-107',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(88,9,'B26-108',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(89,9,'B26-109',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(90,9,'B26-110',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(91,10,'B26-201',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(92,10,'B26-202',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(93,10,'B26-203',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(94,10,'B26-204',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(95,10,'B26-205',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(96,10,'B26-206',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(97,10,'B26-207',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(98,10,'B26-208',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(99,10,'B26-209',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(100,10,'B26-210',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(101,11,'B26-301',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(102,11,'B26-302',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(103,11,'B26-303',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(104,11,'B26-304',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(105,11,'B26-305',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(106,11,'B26-306',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(107,11,'B26-307',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(108,11,'B26-308',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(109,11,'B26-309',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(110,11,'B26-310',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(111,12,'B26-401',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(112,12,'B26-402',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(113,12,'B26-403',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(114,12,'B26-404',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(115,12,'B26-405',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(116,12,'B26-406',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(117,12,'B26-407',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(118,12,'B26-408',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(119,12,'B26-409',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(120,12,'B26-410',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(121,13,'B26-501',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(122,13,'B26-502',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(123,13,'B26-503',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(124,13,'B26-504',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(125,13,'B26-505',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(126,13,'B26-506',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(127,13,'B26-507',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(128,13,'B26-508',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(129,13,'B26-509',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(130,13,'B26-510',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(131,14,'B26-601',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(132,14,'B26-602',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(133,14,'B26-603',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(134,14,'B26-604',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(135,14,'B26-605',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(136,14,'B26-606',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(137,14,'B26-607',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(138,14,'B26-608',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(139,14,'B26-609',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(140,14,'B26-610',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(141,15,'B26-701',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(142,15,'B26-702',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(143,15,'B26-703',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(144,15,'B26-704',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(145,15,'B26-705',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(146,15,'B26-706',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(147,15,'B26-707',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(148,15,'B26-708',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(149,15,'B26-709',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(150,15,'B26-710',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(151,16,'B26-801',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(152,16,'B26-802',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(153,16,'B26-803',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(154,16,'B26-804',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(155,16,'B26-805',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(156,16,'B26-806',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(157,16,'B26-807',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(158,16,'B26-808',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(159,16,'B26-809',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(160,16,'B26-810',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(161,17,'B27-101',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(162,17,'B27-102',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(163,17,'B27-103',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(164,17,'B27-104',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(165,17,'B27-105',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(166,17,'B27-106',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(167,17,'B27-107',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(168,17,'B27-108',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(169,17,'B27-109',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(170,17,'B27-110',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(171,18,'B27-201',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(172,18,'B27-202',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(173,18,'B27-203',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(174,18,'B27-204',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(175,18,'B27-205',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(176,18,'B27-206',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(177,18,'B27-207',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(178,18,'B27-208',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(179,18,'B27-209',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(180,18,'B27-210',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(181,19,'B27-301',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(182,19,'B27-302',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(183,19,'B27-303',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(184,19,'B27-304',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(185,19,'B27-305',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(186,19,'B27-306',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(187,19,'B27-307',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(188,19,'B27-308',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(189,19,'B27-309',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(190,19,'B27-310',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(191,20,'B27-401',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(192,20,'B27-402',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(193,20,'B27-403',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(194,20,'B27-404',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(195,20,'B27-405',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(196,20,'B27-406',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(197,20,'B27-407',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(198,20,'B27-408',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(199,20,'B27-409',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(200,20,'B27-410',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(201,21,'B27-501',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(202,21,'B27-502',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(203,21,'B27-503',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(204,21,'B27-504',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(205,21,'B27-505',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(206,21,'B27-506',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(207,21,'B27-507',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(208,21,'B27-508',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(209,21,'B27-509',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(210,21,'B27-510',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(211,22,'B27-601',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(212,22,'B27-602',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(213,22,'B27-603',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(214,22,'B27-604',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(215,22,'B27-605',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(216,22,'B27-606',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(217,22,'B27-607',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(218,22,'B27-608',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(219,22,'B27-609',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(220,22,'B27-610',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(221,23,'B27-701',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(222,23,'B27-702',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(223,23,'B27-703',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(224,23,'B27-704',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(225,23,'B27-705',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(226,23,'B27-706',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(227,23,'B27-707',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(228,23,'B27-708',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(229,23,'B27-709',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(230,23,'B27-710',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(231,24,'B27-801',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(232,24,'B27-802',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(233,24,'B27-803',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(234,24,'B27-804',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(235,24,'B27-805',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(236,24,'B27-806',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(237,24,'B27-807',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(238,24,'B27-808',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(239,24,'B27-809',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(240,24,'B27-810',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(241,25,'B28-101',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(242,25,'B28-102',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(243,25,'B28-103',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(244,25,'B28-104',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(245,25,'B28-105',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(246,25,'B28-106',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(247,25,'B28-107',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(248,25,'B28-108',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(249,25,'B28-109',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(250,25,'B28-110',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(251,26,'B28-201',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(252,26,'B28-202',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(253,26,'B28-203',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(254,26,'B28-204',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(255,26,'B28-205',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(256,26,'B28-206',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(257,26,'B28-207',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(258,26,'B28-208',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(259,26,'B28-209',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(260,26,'B28-210',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(261,27,'B28-301',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(262,27,'B28-302',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(263,27,'B28-303',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(264,27,'B28-304',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(265,27,'B28-305',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(266,27,'B28-306',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(267,27,'B28-307',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(268,27,'B28-308',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(269,27,'B28-309',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(270,27,'B28-310',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(271,28,'B28-401',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(272,28,'B28-402',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(273,28,'B28-403',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(274,28,'B28-404',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(275,28,'B28-405',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(276,28,'B28-406',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(277,28,'B28-407',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(278,28,'B28-408',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(279,28,'B28-409',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(280,28,'B28-410',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(281,29,'B28-501',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(282,29,'B28-502',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(283,29,'B28-503',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(284,29,'B28-504',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(285,29,'B28-505',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(286,29,'B28-506',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(287,29,'B28-507',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(288,29,'B28-508',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(289,29,'B28-509',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(290,29,'B28-510',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(291,30,'B28-601',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(292,30,'B28-602',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(293,30,'B28-603',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(294,30,'B28-604',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(295,30,'B28-605',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(296,30,'B28-606',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(297,30,'B28-607',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(298,30,'B28-608',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(299,30,'B28-609',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(300,30,'B28-610',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(301,31,'B28-701',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(302,31,'B28-702',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(303,31,'B28-703',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(304,31,'B28-704',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(305,31,'B28-705',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(306,31,'B28-706',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(307,31,'B28-707',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(308,31,'B28-708',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(309,31,'B28-709',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(310,31,'B28-710',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(311,32,'B28-801',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(312,32,'B28-802',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(313,32,'B28-803',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(314,32,'B28-804',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(315,32,'B28-805',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(316,32,'B28-806',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(317,32,'B28-807',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(318,32,'B28-808',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(319,32,'B28-809',60,60,2,2,1);
INSERT INTO "classrooms" VALUES(320,32,'B28-810',60,60,2,2,1);
CREATE TABLE fault_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id VARCHAR(20) UNIQUE NOT NULL,
    classroom_id INTEGER,
    canteen_id INTEGER,
    reported_by_user_id INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL, -- AC, Socket, Fan, Projector, etc.
    description TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'Submitted' CHECK(status IN ('Submitted', 'In Progress', 'Completed', 'Escalated to Higher Authority')),
    is_urgent BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to_user_id INTEGER,
    is_escalated BOOLEAN DEFAULT 0, -- Set to 1 if not resolved within 7 days
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE,
    FOREIGN KEY (canteen_id) REFERENCES canteens(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_by_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id) ON DELETE SET NULL
);
INSERT INTO "fault_reports" VALUES(1,'TICK-1001',1,NULL,7,'AC Socket','Student socket #12 sparking','In Progress',0,'2026-10-23 17:42:33','2026-10-25 17:42:33',4,0);
INSERT INTO "fault_reports" VALUES(2,'TICK-1002',15,NULL,8,'AC Unit','AC unit cooling not effective in B25-205','Escalated to Higher Authority',0,'2026-10-16 17:42:33','2026-10-25 17:42:33',5,1);
CREATE TABLE floors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER NOT NULL,
    floor_number INTEGER NOT NULL CHECK(floor_number BETWEEN 1 AND 8),
    has_alleyway_access BOOLEAN NOT NULL, -- True for floors 1-5, False for 6, 7, 8
    FOREIGN KEY (block_id) REFERENCES blocks(id) ON DELETE CASCADE,
    UNIQUE(block_id, floor_number)
);
INSERT INTO "floors" VALUES(1,1,1,1);
INSERT INTO "floors" VALUES(2,1,2,1);
INSERT INTO "floors" VALUES(3,1,3,1);
INSERT INTO "floors" VALUES(4,1,4,1);
INSERT INTO "floors" VALUES(5,1,5,1);
INSERT INTO "floors" VALUES(6,1,6,0);
INSERT INTO "floors" VALUES(7,1,7,0);
INSERT INTO "floors" VALUES(8,1,8,0);
INSERT INTO "floors" VALUES(9,2,1,1);
INSERT INTO "floors" VALUES(10,2,2,1);
INSERT INTO "floors" VALUES(11,2,3,1);
INSERT INTO "floors" VALUES(12,2,4,1);
INSERT INTO "floors" VALUES(13,2,5,1);
INSERT INTO "floors" VALUES(14,2,6,0);
INSERT INTO "floors" VALUES(15,2,7,0);
INSERT INTO "floors" VALUES(16,2,8,0);
INSERT INTO "floors" VALUES(17,3,1,1);
INSERT INTO "floors" VALUES(18,3,2,1);
INSERT INTO "floors" VALUES(19,3,3,1);
INSERT INTO "floors" VALUES(20,3,4,1);
INSERT INTO "floors" VALUES(21,3,5,1);
INSERT INTO "floors" VALUES(22,3,6,0);
INSERT INTO "floors" VALUES(23,3,7,0);
INSERT INTO "floors" VALUES(24,3,8,0);
INSERT INTO "floors" VALUES(25,4,1,1);
INSERT INTO "floors" VALUES(26,4,2,1);
INSERT INTO "floors" VALUES(27,4,3,1);
INSERT INTO "floors" VALUES(28,4,4,1);
INSERT INTO "floors" VALUES(29,4,5,1);
INSERT INTO "floors" VALUES(30,4,6,0);
INSERT INTO "floors" VALUES(31,4,7,0);
INSERT INTO "floors" VALUES(32,4,8,0);
CREATE TABLE timetable_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classroom_id INTEGER NOT NULL,
    subject_name VARCHAR(100), -- Subjects can differ across classes
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_break_slot BOOLEAN DEFAULT 0, -- Synchronized 1-hr break windows
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id) ON DELETE CASCADE
);
INSERT INTO "timetable_entries" VALUES(1,1,'Data Structures','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(2,1,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(3,2,'Database Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(4,2,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(5,3,'Computer Networks','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(6,3,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(7,4,'Operating Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(8,4,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(9,5,'Software Engineering','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(10,5,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(11,6,'Data Structures','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(12,6,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(13,7,'Database Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(14,7,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(15,8,'Computer Networks','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(16,8,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(17,9,'Operating Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(18,9,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(19,10,'Software Engineering','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(20,10,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(21,11,'Data Structures','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(22,11,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(23,12,'Database Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(24,12,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(25,13,'Computer Networks','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(26,13,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(27,14,'Operating Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(28,14,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(29,15,'Software Engineering','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(30,15,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(31,16,'Data Structures','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(32,16,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(33,17,'Database Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(34,17,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(35,18,'Computer Networks','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(36,18,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(37,19,'Operating Systems','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(38,19,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
INSERT INTO "timetable_entries" VALUES(39,20,'Software Engineering','Monday','10:00:00','12:00:00',0);
INSERT INTO "timetable_entries" VALUES(40,20,'Common Lunch & Study Break','Monday','12:00:00','13:00:00',1);
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('admin', 'maintenance', 'student')),
    escalation_authority BOOLEAN DEFAULT 0
);
INSERT INTO "users" VALUES(1,'Karan Kr.','karan@campusspace.edu','admin',1);
INSERT INTO "users" VALUES(2,'Aniket','aniket@campusspace.edu','admin',1);
INSERT INTO "users" VALUES(3,'Shreyansh','shreyansh@campusspace.edu','admin',1);
INSERT INTO "users" VALUES(4,'Rajesh Kumar','rajesh.maint@campusspace.edu','maintenance',0);
INSERT INTO "users" VALUES(5,'Suresh Verma','suresh.maint@campusspace.edu','maintenance',0);
INSERT INTO "users" VALUES(6,'Amit Patel','amit.maint@campusspace.edu','maintenance',0);
INSERT INTO "users" VALUES(7,'Rohan Sharma','rohan@student.campusspace.edu','student',0);
INSERT INTO "users" VALUES(8,'Priya Singh','priya@student.campusspace.edu','student',0);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('users',8);
INSERT INTO "sqlite_sequence" VALUES('blocks',4);
INSERT INTO "sqlite_sequence" VALUES('floors',32);
INSERT INTO "sqlite_sequence" VALUES('classrooms',320);
INSERT INTO "sqlite_sequence" VALUES('canteens',4);
INSERT INTO "sqlite_sequence" VALUES('timetable_entries',40);
INSERT INTO "sqlite_sequence" VALUES('fault_reports',2);
COMMIT;