CREATE DATABASE subscription default character set utf8;
USE subscription;
CREATE TABLE weibo_subscription (
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  uid VARCHAR(20) NOT NULL ,
  comment VARCHAR(120) DEFAULT NULL ,
  status int(11) NOT NULL DEFAULT '0' COMMENT '0为正常订阅，1为暂停',
  add_time DATETIME DEFAULT now() NOT NULL
);

CREATE TABLE weixin_subscription(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  wechat_num VARCHAR(25) NOT NULL ,
  comment VARCHAR(120) DEFAULT NULL ,
  status int(11) NOT NULL DEFAULT '0' COMMENT '0为正常订阅，1为暂停',
  add_time DATETIME DEFAULT now() NOT NULL
);