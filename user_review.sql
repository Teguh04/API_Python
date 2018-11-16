CREATE database simple_api;
USE simple_api;
CREATE TABLE user_review (
id INT AUTO_INCREMENT,
order_id INT,
product_id INT,
user_id INT,
rating FLOAT,
review VARCHAR(255),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (id));

delimiter //
drop trigger if exists max_num//
create trigger max_num before insert on user_review
for each row 
begin
if new.rating < 1 or new.rating > 5 then
set new.rating = null;
end if;
end//
delimiter ;

USE simple_api;

DROP procedure IF EXISTS spUser;

DELIMITER //
CREATE PROCEDURE spUser (
IN p_order_id INT,
IN p_product_id INT,
IN p_user_id INT,
IN p_rating FLOAT,
IN p_review VARCHAR(255)
)
begin
insert into user_review
(
    order_id,
    product_id,
    user_id,
    rating,
    review
)
values
(
    p_order_id,
    p_product_id,
    p_user_id,
    p_rating,
    p_review
);

end//
DELIMITER ;

USE simple_api;

DROP procedure IF EXISTS spUpdateUser;

DELIMITER //
CREATE PROCEDURE spUpdateUser (
IN p_id INT,
IN p_order_id INT,
IN p_product_id INT,
IN p_user_id INT,
IN p_rating FLOAT,
IN p_review VARCHAR(255)
)
begin

UPDATE user_review SET order_id=p_order_id, product_id=p_product_id, user_id=p_user_id, rating=p_rating, review=p_review WHERE id=p_id;

end//
DELIMITER ;