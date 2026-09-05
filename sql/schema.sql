IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = N'weather'
)
BEGIN
    EXEC(N'CREATE SCHEMA weather AUTHORIZATION dbo');
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = N'adf-weather-dev-yahia'
)
BEGIN
    EXEC(N'CREATE USER [adf-weather-dev-yahia] FROM EXTERNAL PROVIDER');
END;

ALTER ROLE db_datareader ADD MEMBER [adf-weather-dev-yahia];
ALTER ROLE db_datawriter ADD MEMBER [adf-weather-dev-yahia];
