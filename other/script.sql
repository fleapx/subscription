CREATE DATABASE weibotrace;
USE weibotrace;
CREATE TABLE traced_uid
(
  id         INT AUTO_INCREMENT
    PRIMARY KEY,
  uid        VARCHAR(20)     NOT NULL,
  comment    VARCHAR(120)    NULL,
  user_id    VARCHAR(20)     NOT NULL,
  user_email VARCHAR(120)    NOT NULL,
  status     INT DEFAULT '0' NOT NULL
  COMMENT '0为正常订阅，1为暂停'
)