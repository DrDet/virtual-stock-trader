begin;

CREATE DATABASE vstrader;
USE vstrader;
CREATE TABLE Portfolios
(
    portfolio_id BIGINT NOT NULL,
    balance DOUBLE NOT NULL,
    PRIMARY KEY (portfolio_id)
);
CREATE TABLE StockPositions
(
    portfolio_id BIGINT NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    count INT NOT NULL,
    average_price DOUBLE NOT NULL,
    PRIMARY KEY (portfolio_id, ticker)
);

CREATE USER 'vstrader_client'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON vstrader.*  TO 'vstrader_client'@'localhost';
FLUSH PRIVILEGES;

end;
