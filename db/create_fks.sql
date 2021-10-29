ALTER TABLE `localized_twitter`.`tweet` 
ADD CONSTRAINT `user_fk`
  FOREIGN KEY (`userid`)
  REFERENCES `localized_twitter`.`user` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;