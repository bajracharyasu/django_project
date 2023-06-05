import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from .models import Patient
# getting the data from the database
conn = psycopg2.connect(
    host="localhost",
    database="DBemotion",
    user="postgres",
    password="Sudeepa0613$"
    )
cur = conn.cursor()
query = 'SELECT patient_id_id, always,none.often,sometimes FROM public."MindsetApp_output" WHERE patient_id_id = %s'
patient_id = Patient.objects.latest('id').id
cur.execute(query,[patient_id])
rows = cur.fetchall()
# for preprocessing the data
X = []
y = []
for row in rows:
    feature1 = row[0]
    feature2 = row[1]

    target = row[2]
    X.append([feature1,feature2])
    y.append(target)
# splitting the data into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# creating the model
model = DecisionTreeClassifier()
model.fit(X_train,y_train)
# predicting the output
accuracy = model.score(X_test,y_test)   