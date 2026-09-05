
# Databricks notebook source
"""Create the Gold star schema and export it for Azure SQL loading."""

# COMMAND ----------

from pyspark.sql import functions as F


dbutils.widgets.text("storage_account", "stweatherdevyahia")

storage_account = dbutils.widgets.get("storage_account")
container = "datalake"

gold_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/"
    "gold/daily_city_weather/"
)
serving_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/serving/sql/"
)
gold_model_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/gold/"
)

gold_df = spark.read.format("delta").load(gold_path)

if gold_df.limit(1).count() == 0:
    raise ValueError("No Gold weather data is available for the SQL exports.")

dim_city_df = (
    gold_df
    .select(
        F.col("city_id").alias("city_key"),
        F.col("city").alias("city_name"),
        "country",
        "latitude",
        "longitude",
    )
    .dropDuplicates(["city_key"])
)

dim_date_df = (
    gold_df
    .select(F.col("weather_date").alias("full_date"))
    .distinct()
    .select(
        F.date_format("full_date", "yyyyMMdd").cast("integer").alias("date_key"),
        "full_date",
        F.year("full_date").alias("year"),
        F.month("full_date").alias("month"),
        F.dayofmonth("full_date").alias("day"),
        F.date_format("full_date", "MMMM").alias("month_name"),
    )
)

fact_weather_df = gold_df.select(
    F.col("city_id").alias("city_key"),
    F.date_format("weather_date", "yyyyMMdd").cast("integer").alias("date_key"),
    "average_temperature",
    "minimum_temperature",
    "maximum_temperature",
    "average_humidity",
    "average_wind_speed",
    "observation_count",
)

# COMMAND ----------

tables = {
    "dim_city": dim_city_df,
    "dim_date": dim_date_df,
    "fact_weather": fact_weather_df,
}

spark.sql("CREATE SCHEMA IF NOT EXISTS weather.gold")

for table_name, table_df in tables.items():
    delta_path = f"{gold_model_path}{table_name}/"

    (
        table_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(delta_path)
    )

    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS weather.gold.{table_name}
        USING DELTA
        LOCATION '{delta_path}'
        """
    )

    table_df.write.mode("overwrite").parquet(
        f"{serving_path}{table_name}/"
    )

    print(f"{table_name}: {table_df.count()} rows created and exported.")
