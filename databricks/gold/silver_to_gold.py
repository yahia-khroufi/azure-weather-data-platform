# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

dbutils.widgets.text("storage_account", "stweatherdevyahia")

storage_account = dbutils.widgets.get("storage_account")
container = "datalake"

silver_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/silver/weather/"
)
gold_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/"
    "gold/daily_city_weather/"
)


silver_df = spark.read.format("delta").load(silver_path)

gold_df = (
    silver_df
    .withColumn("weather_date", F.to_date("observed_at"))
    .groupBy("city", "country", "weather_date")
    .agg(
        F.round(F.avg("temperature"), 2).alias("average_temperature"),
        F.min("temperature").alias("minimum_temperature"),
        F.max("temperature").alias("maximum_temperature"),
        F.round(F.avg("humidity"), 2).alias("average_humidity"),
        F.round(F.avg("wind_speed"), 2).alias("average_wind_speed"),
        F.count("*").alias("observation_count"),
    )
)

if gold_df.limit(1).count() == 0:
    raise ValueError("No Silver weather data is available for aggregation.")

# COMMAND ----------

(
    gold_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(gold_path)
)

spark.sql("CREATE SCHEMA IF NOT EXISTS weather.gold")
spark.sql(
    f"""
    CREATE TABLE IF NOT EXISTS weather.gold.daily_city_weather
    USING DELTA
    LOCATION '{gold_path}'
    """
)

print(f"Gold table created with {gold_df.count()} rows.")
