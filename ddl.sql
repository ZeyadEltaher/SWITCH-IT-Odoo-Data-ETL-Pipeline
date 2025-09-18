CREATE TABLE `customers`(
    `id` INT UNSIGNED NOT NULL PRIMARY KEY,
    `first_name` VARCHAR(50),
    `last_name` VARCHAR(50),
    `email` VARCHAR(100),
    `phone` VARCHAR(50),
    `country` VARCHAR(100),
    `city` VARCHAR(100),
    `street` VARCHAR(100),
    `street2` VARCHAR(100),
    `zip_code` VARCHAR(50)
);
CREATE TABLE `orders`(
    `id` INT UNSIGNED NOT NULL PRIMARY KEY,
    `customer_id` INT UNSIGNED NOT NULL,
    `order_date` DATETIME,
    `order_status` VARCHAR(20),
    `sales` INT,
    `delivery_company_id` VARCHAR(20),
    `delivery_status` VARCHAR(20),
    `delivery_sales` INT
);
CREATE TABLE `products`(
    `id` INT UNSIGNED NOT NULL PRIMARY KEY,
    `name` VARCHAR(50)
);