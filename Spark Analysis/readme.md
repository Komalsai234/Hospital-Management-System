
# Spark Analysis on Hospital Data

## Prerequisites
- Apache Spark
- Scala

## How to connect to AWS RDS/Localhost from Spark Shell

**Download the JDBC Connector from the below link and save it in accessible location**

* [JDBC Connector](https://drive.google.com/file/d/1KYVzaDqZOTQrM0Uzj2j5yLMYdEXvoAJB/view?usp=sharing)

- **Start the Spark Shell by giving the path of JDBC Connector as argument**

```
spark-shell --jars path/to/mysql-connector-java-8.0.23.jar
```

- **Establish JDBC Connection** 

```
val jdbcUrl = "jdbc:mysql://[database-endpoint]:[database-port]/[database-name]"

val connectionProperties = new java.util.Properties()

connectionProperties.setProperty("user", "[username]")

connectionProperties.setProperty("password", "[password]")

connectionProperties.setProperty
("Driver", "com.mysql.cj.jdbc.Driver")

```

- **Read the Tables from the database as dataframe and perform required anlaysis**

```
def readTable(tableName: String) = {
 spark.read.jdbc(jdbcUrl, your-table-name, connectionProperties)
}
```
