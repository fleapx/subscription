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
) CHARACTER SET UTF8;

CREATE TABLE email_log
(
  id             INT(10) AUTO_INCREMENT
    PRIMARY KEY,
  from_mail      VARCHAR(250) NULL,
  to_mail        VARCHAR(250) NULL,
  user_id        INT(10)      NULL,
  send_timestamp VARCHAR(25)  NULL,
  context        MEDIUMTEXT   NULL,
  weibo_count    INT(12)      NULL
) CHARACTER SET UTF8;