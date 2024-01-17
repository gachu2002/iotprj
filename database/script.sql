drop database ARMS;
create database ARMS;
use ARMS;

create table users (username varchar(255), password varchar(255), first_name varchar(255), Last_name varchar(255), email varchar(255), phone_number varchar(255), last_login datetime, api_key varchar(255));
show tables;
select * from users;
alter table users add unique (username);
alter table users add unique (username, api_key);
alter table users add primary key (username, api_key);
truncate users;
insert into users (username, password, first_name, last_name, email, phone_number, last_login, api_key) values ('amansingh', 'password here', 'Aman', 'Singh', 'singhaman11415@gmail.com', '8770262013', now(), 'abhikuchnhihai');
insert into users (username, password, first_name, last_name, email, phone_number, last_login, api_key) values ('nguyen', 'Love123bgbg@', 'Ahell', 'boye', 'nguyen@gmail.com', '8770262013', now(), 'sddasdsadas');
select * from users;

create table devices (deviceID varchar(255), username varchar(255), device_type varchar(255), device_value varchar(255),  register ENUM('yes', 'no'), foreign key (username) references users(username), primary key (deviceID, username));
insert into devices (deviceID, username, device_type, device_value, register) values ('1281', 'amansingh', 'sensor', '50 60','yes');
insert into devices (deviceID, username, device_type, device_value, register) values ('1283', 'amansingh', 'sensor', '20 30','yes');
insert into devices (deviceID, username, device_type, device_value, register) values ('1220', 'amansingh', 'sensor','20 30','yes');
insert into devices (deviceID, username, device_type, device_value, register) values ('1250', 'amansingh', 'sensor','40 30','no');
insert into devices (deviceID, username, device_type, device_value, register) values ('1002', 'amansingh', 'led', 'on','yes');
insert into devices (deviceID, username, device_type, device_value, register) values ('1402', 'amansingh', 'led', 'off','yes');
select * from devices;

create table statistics (record_id int auto_increment, deviceID varchar(255), temp int, humid int, record_time datetime, foreign key (deviceID) references devices(deviceID), primary key(record_id));

drop table users;
drop table devices;
drop table statistics;
