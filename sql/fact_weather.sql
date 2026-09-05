IF OBJECT_ID(N'weather.fact_weather', N'U') IS NULL
BEGIN
    CREATE TABLE weather.fact_weather (
        city_key BIGINT NOT NULL,
        date_key INT NOT NULL,
        average_temperature DECIMAL(6, 2) NULL,
        minimum_temperature DECIMAL(6, 2) NULL,
        maximum_temperature DECIMAL(6, 2) NULL,
        average_humidity DECIMAL(5, 2) NULL,
        average_wind_speed DECIMAL(6, 2) NULL,
        observation_count INT NOT NULL,
        CONSTRAINT pk_fact_weather PRIMARY KEY (city_key, date_key),
        CONSTRAINT fk_fact_weather_city
            FOREIGN KEY (city_key) REFERENCES weather.dim_city(city_key),
        CONSTRAINT fk_fact_weather_date
            FOREIGN KEY (date_key) REFERENCES weather.dim_date(date_key)
    );
END;
