# Twitter hashtags monitoring

## 1. Créez votre fichier d'environnement et insérez vos tokens and consumer key twitter
`mv .env.sample .env`

## 2. Initialisez le docker-compose 
`docker-compose up --build`

## 3. Récupérer l'url dans les logs du pyspark notebook pour accéder au notebook (pour le token)
`docker-compose logs pyspark-notebook`

|               | Port  | Description           | 
|---------------|-------|-----------------------|
| Mongo-Express | 8081  | Interface Web MongoDB |
| MongoDB       | 27017 |                       |  
| Hadoop-WebUI  | 9870  |                       |  
| Hadoop-HDFS   | 9000  |                       |  
| Streamlit     | 8501  | Data Monitoring | 
| Jupyter Notebook     | 8888  | Live Coding | 

## 4. Lancez dans l'ordre les notebook 
+ kafka-producer_step_1
+ kafka-consumer_step_2
+ spark_batch_step_3

## Credits & Licence
25/06/2021 - GPL3 Licence (Open Source)

**Noé ABDEL KALEK**  - *Developer*

**Zayd SELMANI**  - *Developer*

**Jeremie VANG FOUA**  - *Developer*    
