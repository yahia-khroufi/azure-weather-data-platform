IF OBJECT_ID(N'weather.dim_city', N'U') IS NULL
BEGIN
    CREATE TABLE weather.dim_city (
        city_key BIGINT NOT NULL,
        city_name NVARCHAR(100) NOT NULL,
        country CHAR(2) NULL,
        latitude DECIMAL(9, 6) NULL,
        longitude DECIMAL(9, 6) NULL,
        CONSTRAINT pk_dim_city PRIMARY KEY (city_key)
    );
END;

IF OBJECT_ID(N'weather.dim_date', N'U') IS NULL
BEGIN
    CREATE TABLE weather.dim_date (
        date_key INT NOT NULL,
        full_date DATE NOT NULL,
        [year] SMALLINT NOT NULL,
        [month] TINYINT NOT NULL,
        [day] TINYINT NOT NULL,
        month_name NVARCHAR(20) NOT NULL,
        CONSTRAINT pk_dim_date PRIMARY KEY (date_key),
        CONSTRAINT uq_dim_date_full_date UNIQUE (full_date)
    );
END;
