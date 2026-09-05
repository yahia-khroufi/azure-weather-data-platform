# Databricks notebook source
"""Clean and flatten the Bronze weather data into a Silver Delta table."""

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

dbutils.widgets.text("storage_account", "stweatherdevyahia")

storage_account = dbutils.widgets.get("storage_account")
container = "datalake"

bronze_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/bronze/weather/"
)
silver_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/silver/weather/"
)

spark.conf.set("spark.sql.session.timeZone", "UTC")

# COMMAND ----------

bronze_df = spark.read.format("delta").load(bronze_path)

silver_df = (
    bronze_df
    .select(
        F.col("id").cast("long").alias("city_id"),
        F.col("name").alias("city"),
        F.col("sys.country").alias("country"),
        F.col("coord.lat").cast("double").alias("latitude"),
        F.col("coord.lon").cast("double").alias("longitude"),
        F.col("main.temp").cast("double").alias("temperature"),
        F.col("main.feels_like").cast("double").alias("feels_like"),
        F.col("main.temp_min").cast("double").alias("temperature_min"),
        F.col("main.temp_max").cast("double").alias("temperature_max"),
        F.col("main.humidity").cast("integer").alias("humidity"),
        F.col("main.pressure").cast("integer").alias("pressure"),
        F.col("wind.speed").cast("double").alias("wind_speed"),
        F.col("wind.deg").cast("integer").alias("wind_direction"),
        F.col("clouds.all").cast("integer").alias("cloudiness"),
        F.col("visibility").cast("integer").alias("visibility"),
        F.col("weather").getItem(0).getField("main").alias("weather_main"),
        F.col("weather").getItem(0).getField("description").alias(
            "weather_description"
        ),
        F.to_timestamp(F.from_unixtime(F.col("dt"))).alias("observed_at"),
        F.col("ingested_at"),
        F.col("source_file"),
    )
    .filter(F.col("city_id").isNotNull())
    .filter(F.col("city").isNotNull())
    .filter(F.col("temperature").isNotNull())
    .filter(F.col("humidity").between(0, 100))
    .dropDuplicates(["city_id", "observed_at"])
)

if silver_df.limit(1).count() == 0:
    raise ValueError("No valid weather data remains after cleaning.")

# COMMAND ----------

(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(silver_path)
)

spark.sql("CREATE SCHEMA IF NOT EXISTS weather.silver")
spark.sql(
    f"""
    CREATE TABLE IF NOT EXISTS weather.silver.weather
    USING DELTA
    LOCATION '{silver_path}'
    """
)

print(f"Silver table created with {silver_df.count()} rows.")
