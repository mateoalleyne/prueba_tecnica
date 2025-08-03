import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR




#-------------------------LECTURA Y LIMPIEZA DE DATOS--------------------------------
data=pd.read_csv('restaurants_dataset.csv',index_col='Registration Number')
print(data.columns)
print(data.head())

#Análisis de la cantidad de registros válidos que tiene cada columna
print(f'Cantidad de datos válidos en cada columna: \n{data.count()}')
#Se evidencia que las columnas 'Comedy Gigs Rating','Value Deals Rating', 'Live Sports Rating' no contienen una cantidad de datos representiva, serán dropeadas
cols_drop=['Comedy Gigs Rating','Value Deals Rating', 'Live Sports Rating']
data.drop(cols_drop,axis=1,inplace=True)
print(f'Datos luego de limpieza de columnas:\n{data.head()}')
print(f'Cantidad de datos válidos en cada columna: \n{data.count()}')

#Eliminar Outliners del set de datos:
numeric_data=data.select_dtypes(include=['number'])
Q1=numeric_data.quantile(0.25)
Q3=numeric_data.quantile(0.75)
IQR=Q3-Q1
print(IQR)

mask=mask = ~((numeric_data < (Q1 - 1.5 * IQR)) | (numeric_data > (Q3 + 1.5 * IQR))).any(axis=1)
data = data[mask]

#Para los valores que son Tiers y Ratings se va a aplicar normalización para encontrar correlaciones entre estas y la facturación anual
cols_norm=['Resturant Tier','Restaurant City Tier','Restaurant Zomato Rating','Order Wait Time','Staff Responsivness',
           'Hygiene Rating', 'Food Rating','Overall Restaurant Rating','Value for Money','Ambience','Lively','Service','Comfortablility','Privacy','Resturant Tier']

for col in cols_norm:
    data[col]=(data[col]-data[col].min())/(data[col].max()-data[col].min())


#Después de eliminar los Outliners y normalizar los datos, se evidencia que se eliminan todos los registros de la columna Resturant Tier
#esto se debe a que todos los valores son 2, normalizamos asignando un valor de 1 a todos sus valores
data['Resturant Tier']=1

#Para la columna City se tienen 118 valores que no contienen información, se eliminan estos valores
data=data[data['City']!='-1']

print(f'Datos luego de limpieza de datos:\n{data.head()}')
print(f'Cantidad de datos válidos en cada columna: \n{data.count()}')

#---------------VISUALIZACIÓN DE LOS DATOS--------------------------
Y=data['Annual Turnover']
X1=data['Facebook Popularity Quotient']
X2=data['Instagram Popularity Quotient']
X3=data['Resturant Tier']
X4=data['Restaurant City Tier']
X5=data['Restaurant Zomato Rating']
X6=data['Comfortablility']
X7=data['Ambience']
X8=data['Lively']
X9=data['Food Rating']
X10=data['Overall Restaurant Rating']
X11=data['Value for Money']
X12=data['Privacy']

figure, axis = plt.subplots(2, 2)

axis[0,0].scatter(X1,Y,c='blue',label='Facebook',s=2)
axis[0,0].scatter(X2,Y,c='red',label='Instagram',s=2)
axis[0,0].set_xlabel('Facebook/Instagram Popularity Quotient')
axis[0,0].set_ylabel('Annual Turnover')
axis[0,0].legend()

axis[0,1].scatter(X3,Y,c='green',label='Restarurant',s=2)
axis[0,1].scatter(X4,Y,c='orange',label='Restarurant City',s=2)
axis[0,1].set_xlabel('Tiers')
axis[0,1].set_ylabel('Annual Turnover')
axis[0,1].legend()

axis[1,0].scatter(X5,Y,c='blue',label='Zomato',s=2)
axis[1,0].scatter(X11,Y,c='orange',label='Value for Money',s=2)
axis[1,0].scatter(X9,Y,c='gray',label='Food',s=2)
axis[1,0].scatter(X10,Y,c='red',label='Overall',s=2)
axis[1,0].set_xlabel('Ratings')
axis[1,0].set_ylabel('Annual Turnover')
axis[1,0].legend()

axis[1,1].scatter(X6,Y,c='black',label='Comfortablility',s=2)
axis[1,1].scatter(X7,Y,c='yellow',label='Ambience',s=2)
axis[1,1].scatter(X8,Y,c='gray',label='Lively',s=2)
axis[1,1].scatter(X12,Y,c='brown',label='Privacy',s=2)
axis[1,1].set_xlabel('Attributes')
axis[1,1].set_ylabel('Annual Turnover')
axis[1,1].legend()
plt.show()

plt.figure(figsize=(10,5))
cols_exclude=['Fire Audit',
    'Liquor License Obtained', 'Situated in a Multi Complex',
    'Dedicated Parking', 'Open Sitting Available', 'Resturant Tier']
c= data.select_dtypes(include=['number']).drop(columns=cols_exclude).corr()
sns.heatmap(c,cmap="BrBG",annot=True)
plt.title('Mapa de Calor (Correlación)')
plt.show()

data.groupby('City')['Annual Turnover'].mean().nlargest(20).plot(kind='bar')
plt.title('Avg. Annual Turnover ($) in top 20 cities by avg. annual turnover')
plt.show()


#-----------------------ENTRENAMIENTO DE MODELOS DE ML-------------------------------------------
#Para la validación del performance del modelo voy a utilizar el Error Medio Absoluto (MAE)
def get_mae(modelo,X_train,X_valid,y_train,y_valid):
    modelo.fit(X_train,y_train)
    val_prediccion=modelo.predict(X_valid)
    return(mean_absolute_error(y_valid,val_prediccion))


#Para la preparación de los datos, primero me ocuparé de los valores numéricos. Voy a llenar los valores nulos con el promedio de la columna (Método Inputer)
num_cols=data.select_dtypes(include=np.number).columns
data[num_cols] = data[num_cols].fillna(data[num_cols].mean())

parameters=data.drop(['Annual Turnover'],axis=1)
y=data['Annual Turnover']
X=data.drop(['Annual Turnover'],axis=1)

#Ahora me ocupo de los valores categóricos, utilizaré un Original Encode para asignar un valor a cada valor que pueda tomar
X_obj=parameters.select_dtypes(include='object')
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,random_state=10)

#Identificar todas las columnas categóricas en el set de datos
object_cols= [col for col in X_train.columns if X_train[col].dtype == 'object']

#Columnas que tienen los mismo valores únicos en el set de entrenamiento y en el de validación
ok_label_cols = [col for col in object_cols if set(X_valid[col]).issubset(set(X_train[col]))]

#Columnas que no cumplen condición anterior
not_ok_label_cols = list(set(object_cols)-set(ok_label_cols))

print(f'Columnas categóricas que están bien para hacer ordinal encode: {ok_label_cols}\nVan a ser eliminadas: {not_ok_label_cols}')

#Separar datos de validación con los de entrenamiento
X_train,X_valid,y_train,y_valid=train_test_split(X,y,train_size=0.8,test_size=0.2,random_state=0)
print(X_train.head())

label_X_train = X_train.drop(not_ok_label_cols, axis=1)
label_X_valid = X_valid.drop(not_ok_label_cols, axis=1)

#Ordinal encode
ordinal_encoder=OrdinalEncoder()
label_X_train[ok_label_cols] = ordinal_encoder.fit_transform(X_train[ok_label_cols])
label_X_valid[ok_label_cols] = ordinal_encoder.transform(X_valid[ok_label_cols])

#Definición de Modelos:
modelo_1=DecisionTreeRegressor(max_leaf_nodes=50,random_state=0)
modelo_2=RandomForestRegressor(n_estimators=100,random_state=0,criterion='absolute_error')
modelo_3=LinearRegression()
modelo_4= MLPRegressor(
    hidden_layer_sizes=(100, 50),  # Dos capas ocultas con 100 y 50 neuronas
    activation='relu',             # Función de activación: 'identity', 'logistic', 'tanh', 'relu'
    solver='adam',                 # Optimizador: 'lbfgs', 'sgd', 'adam'
    max_iter=1000,
    random_state=42
)

print(f'MAE para primer Modelo (Tree Regressor): {get_mae(modelo_1,label_X_train, label_X_valid, y_train, y_valid)}')
print(f'MAE para segundo Modelo (Forest Regressor): {get_mae(modelo_2,label_X_train, label_X_valid, y_train, y_valid)}')
print(f'MAE para tercer Modelo (Linear Regressor): {get_mae(modelo_3,label_X_train, label_X_valid, y_train, y_valid)}')
print(f'MAE para cuarto Modelo (Red Neuronal): {get_mae(modelo_4,label_X_train, label_X_valid, y_train, y_valid)}')


#El modelo con el mejor perfomance es el de Regresión Lineal, vamos a aplicar HyperParameter Tuning al modelo Random Forest Regressor para refinarlo un poco más.
print('Haciendo hyperparameter tuning al modelo con el mejor score...')
param_grid = {
    'n_estimators': [50, 100, 150, 200, 250],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
}
grid_search = GridSearchCV(estimator=modelo_2, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
grid_search.fit(label_X_train, y_train)
print(grid_search.best_params_)
print(grid_search.best_score_)

#Los parámetros que obtuvieron el mejor score fueron {'max_depth': 10, 'min_samples_split': 5, 'n_estimators': 300}
print('--------PREDICIENDO ANNUAL TURNOVER PARA LOS SIGUIENTES 5 ESTABLECIMIENTOS CON MEJOR MODELO----------------')
print(X_valid.head())
print("--------------------LAS PREDICCIONES SON-----------------------")
print(grid_search.best_estimator_.predict(label_X_valid.head()))

