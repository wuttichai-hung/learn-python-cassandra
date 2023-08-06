![getting-started-with-apache-cassandra](/images/getting-started-with-apache-cassandra.jpg)

# 1. Understanding Apache Cassandra

Apache Cassandra is a highly scalable and distributed NoSQL database known for its ability to handle massive amounts of data across multiple commodity servers. This blog post provides an introduction to Apache Cassandra and covers the key concepts, features, and steps to get started with this powerful database solution. Whether you're a beginner or experienced in database technologies, this guide will help you understand the basics of Apache Cassandra and kickstart your journey with this robust distributed database system.

# 2. Setting Up Apache Cassandra

To set up Apache Cassandra using Docker Compose, you can follow the steps below:

Step 1: Create a Docker Compose YAML file
Create a file named docker-compose.yaml and add the following contents

```yml:docker-compose.yml
version: '3.9'

networks:
  cassandra-network:
    driver: bridge

services:
  cassandra-seed:
    image: cassandra:4.1.2
    container_name: cassandra1
    ports:
      - 9042:9042
    environment:
      - CASSANDRA_CLUSTER_NAME=datahungry-cluster
      - CASSANDRA_SEEDS=cassandra-seed
    networks:
      - cassandra-network

  cassandra2:
    image: cassandra:4.1.2
    container_name: cassandra2
    ports:
      - 9043:9042
    environment:
      - CASSANDRA_CLUSTER_NAME=datahungry-cluster
      - CASSANDRA_SEEDS=cassandra-seed
    networks:
      - cassandra-network

  cassandra3:
    image: cassandra:4.1.2
    container_name: cassandra3
    ports:
      - 9044:9042
    environment:
      - CASSANDRA_CLUSTER_NAME=datahungry-cluster
      - CASSANDRA_SEEDS=cassandra-seed
    networks:
      - cassandra-network
```

Step 2: Start the Apache Cassandra container
Open a terminal or command prompt, navigate to the directory containing the docker-compose.yaml file, and run the following command:

```bash
docker-compose up -d
```

# 3. Data Modeling with Apache Cassandra

1. Data modeling in Apache Cassandra requires a different approach compared to traditional relational databases. In Cassandra, the data model is designed based on query patterns and specific use cases rather than relying on a predefined schema. Here are some key aspects to consider when performing data modeling with Apache Cassandra:

2. Denormalization: In Cassandra, denormalization is a common practice to optimize read performance. Instead of relying on complex joins, data is duplicated and stored in multiple tables based on the query patterns. This allows for efficient retrieval of data with fewer round trips.

3. Partitioning and Distribution: Data in Cassandra is distributed across multiple nodes based on the partition key. The partition key determines the node responsible for storing and serving the data. It is crucial to choose an appropriate partition key that evenly distributes the data and avoids hotspots.

4. Clustering Columns: Clustering columns define the order of data within a partition. They are used to sort and organize data within each partition. By defining clustering columns, you can control the order of data retrieval in queries.

5. Materialized Views: Cassandra supports materialized views, which provide precomputed, denormalized representations of data stored in base tables. Materialized views allow you to create alternative views of your data, optimized for different query patterns.

6. Time-to-Live (TTL): Cassandra offers the ability to set a Time-to-Live (TTL) on individual rows, allowing automatic deletion of data after a specified time period. This feature is useful for managing data expiration or implementing data retention policies.

7. Secondary Indexes: Cassandra supports secondary indexes to query data based on non-primary key columns. However, it is important to use secondary indexes judiciously as they can impact performance and might not scale well with large datasets.

8. Data Model Testing: Due to the nature of distributed systems, it is crucial to test and validate your data model using representative workloads. This helps ensure that your data model performs well under real-world scenarios and handles scalability and performance requirements.

# 4. Performing CRUD Operations

Performing CRUD operations (Create, Read, Update, Delete) in Apache Cassandra involves using the Cassandra Query Language (CQL) to interact with the database. Here's an overview of how to perform CRUD operations in Apache Cassandra:

1. Create (Insert) Data:

Use the INSERT INTO statement to add data to a table.
Specify the column names and values for the new row.
Example:

```sql:insert_users.sql
INSERT INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com');
```

2. Read (Select) Data:

Use the SELECT statement to retrieve data from a table.
Specify the column names or use \* for all columns.
Add optional clauses like WHERE for filtering and LIMIT for result size.
Example:

```sql:select_users.sql
SELECT name, email FROM users WHERE id = 1;
```

3. Update Data:

Use the UPDATE statement to modify existing data in a table.
Specify the column names and new values to update.
Add optional WHERE clause to specify the row(s) to update.
Example:

```sql:update_users.sql
UPDATE users SET name = 'Jane Doe' WHERE id = 1;
```

4. Delete Data:

Use the DELETE statement to remove data from a table.
Specify the row(s) to delete using the WHERE clause.
Example:

```sql:delete_users.sql
DELETE FROM users WHERE id = 1;
```

Remember, in Apache Cassandra, data is typically denormalized, so you might need to consider the relationships and queries specific to your data model when performing CRUD operations. It is essential to design your tables based on your application's access patterns and query requirements.

Additionally, Apache Cassandra provides additional features like batch operations, lightweight transactions (IF conditions), and collections (lists, sets, maps) to handle more complex data scenarios.

By leveraging the power of CQL and understanding the principles of data modeling in Apache Cassandra, you can effectively perform CRUD operations to store, retrieve, update, and delete data in your Cassandra database.

# 5. Cassandra with Python

These code blocks demonstrate various operations when working with Cassandra using the DataStax Python driver. They cover connecting to the cluster, creating a keyspace, creating a table, inserting data from a DataFrame, and querying data into a DataFrame. These examples provide a foundation for interacting with Cassandra using Python and can be customized for specific use cases and requirements.

install cassandra-driver

```bash
pip install cassandra-driver pandas tqdm
```

```python:connect_cluster.py
import pandas as pd
from tqdm.notebook import tqdm
from cassandra.cluster import Cluster

cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()

# show keyspaces
r = session.execute('select * from system_schema.keyspaces')
df = pd.DataFrame(r)
df
```

`connect_cluster.py` This block of code establishes a connection to the Cassandra cluster by creating a Cluster object and connecting to it using the provided host and port. The session object is obtained from the cluster connection. It then executes a CQL query to retrieve all keyspaces in the system schema. The result is fetched and stored in a pandas DataFrame for further analysis.

```python:create_keyspace.py
# create keyspace
session.execute("""
CREATE KEYSPACE IF NOT EXISTS datahungry
  WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 3
  };
""").one()

# set keyspace
session.set_keyspace('datahungry')
```

`create_keyspace.py` This code block creates a new keyspace named "datahungry" if it doesn't already exist. It uses the CREATE KEYSPACE statement with the desired replication strategy and replication factor. The execute method is called on the session object to execute the query. The one() method is used to wait for the completion of the query execution.

```python:create_table.py
# create table
session.execute("""
CREATE TABLE user_profile(
    ssn text,
    username text,
    name text,
    sex text,
    mail text,
    birthdate date,
    address text,
    residence text,
    blood_group text,
    job text,
    company text,
    PRIMARY KEY (ssn)
   );
""").one()
```

`create_table.py` This section creates a table named "user_profile" within the "datahungry" keyspace. The table definition includes various columns like "ssn", "username", "name", "sex", and others. The PRIMARY KEY constraint is set on the "ssn" column. The execute method is used to execute the CREATE TABLE query, and the one() method ensures the completion of the query.

```python:insert_from_dataframe.py
# insert from dataframe
df = pd.read_csv("./data/profile.csv", sep="|")
df = df[['ssn', 'username', 'name', 'sex', 'mail', 'birthdate', 'address', 'residence', 'blood_group', 'job', 'company']]

query = "INSERT INTO user_profile(ssn, username, name, sex, mail, birthdate, address, residence, blood_group, job, company) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
prepared = session.prepare(query)

for v in df.values:
    session.execute(prepared, v)
```

you can use `session.execute_async(prepared, v)` for async

`insert_from_dataframe.py` This code block demonstrates how to insert data into the "user_profile" table from a pandas DataFrame. It reads the data from a CSV file into a DataFrame, selects the required columns, and prepares an INSERT query with placeholders. The for loop iterates over the rows of the DataFrame, executing the prepared query with the values of each row using the session.execute method.

```python:query_data_to_dataframe.py
# select data to dataframe
r = session.execute("SELECT * FROM user_profile")
df = pd.DataFrame(r)
df
```

`query_data_to_dataframe.py` This section fetches data from the "user_profile" table and stores it in a pandas DataFrame. It executes the SELECT query using the session.execute method, and the result is converted to a DataFrame using the pandas library. The DataFrame contains the retrieved data from the Cassandra table.

# 6. Conclusion

With this comprehensive guide, you now have the knowledge and practical examples to start your journey with Apache Cassandra. You understand the fundamental concepts, have successfully set up a Cassandra cluster, and can perform essential CRUD operations using CQL. As you continue your exploration, remember to dive deeper into advanced topics and best practices to leverage the full potential of Apache Cassandra in your projects.

By harnessing the power of Apache Cassandra's scalability, fault tolerance, and performance, you can build robust and highly available data-driven applications. Embrace the flexibility of the Cassandra data model and the simplicity of CQL, and you'll be well on your way to creating scalable and reliable solutions that meet your organization's data storage and processing needs.
