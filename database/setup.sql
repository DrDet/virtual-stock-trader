begin;

CREATE DATABASE vstrader_users;
USE vstrader_users;
CREATE TABLE Users
(
    username varchar(50) NOT NULL,
    hashed_password CHAR(60) NOT NULL,
    PRIMARY KEY (username)
);

CREATE DATABASE vstrader_portfolios;
USE vstrader_portfolios;
CREATE TABLE Portfolios
(
    owner varchar(50) NOT NULL,
    balance DOUBLE NOT NULL,
    PRIMARY KEY (owner)
);

CREATE TABLE StockPositions
(
    owner varchar(50) NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    count INT NOT NULL,
    average_price DOUBLE NOT NULL,
    PRIMARY KEY (owner, ticker),
    FOREIGN KEY (owner) REFERENCES Portfolios (owner)
);

CREATE USER 'vstrader_users_client'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON vstrader_users.*  TO 'vstrader_users_client'@'localhost';

CREATE USER 'vstrader_portfolios_client'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON vstrader_portfolios.*  TO 'vstrader_portfolios_client'@'localhost';

FLUSH PRIVILEGES;

end;
