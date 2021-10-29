CREATE TABLE `user` (
  `id` bigint NOT NULL,
  `name` varchar(45) NOT NULL,
  `screen_name` varchar(45) NOT NULL,
  `location` varchar(45) NOT NULL,
  `followers_count` varchar(45) NOT NULL,
  `created_at` datetime NOT NULL,
  `statuses_count` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tweet` (
  `id` bigint NOT NULL,
  `userid` bigint NOT NULL,
  `created_at` datetime NOT NULL,
  `text` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`userid`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
