"""Regression model for parking revenue analysis"""
import pandas as pd 
from sklearn.cross_validation import train_test_split 
import statsmodels.formula.api as sm
from statsmodels.regression import linear_model as lm
from sklearn.metrics import mean_squared_error


df = pd.read_csv(r'C:\Utkarsh\GIT\Python\ParkingRevenueAnalysis\Data.csv')#INSERT DATA FILE PATH
y_axis = df['DailyLongTerm']


WeekDayNo_dummies = pd.get_dummies(df['WeekDayNo']).rename(columns=lambda x: 'WeekDayNo_' + str(x))
WeekDayNo_dummies = pd.DataFrame(WeekDayNo_dummies)
df = pd.concat([df, WeekDayNo_dummies], axis=1) 
df = df.drop('WeekDayNo',axis=1)

Event_dummies = pd.get_dummies(df['Event']).rename(columns=lambda x: 'Event_' + str(x))
Event_dummies = pd.DataFrame(Event_dummies)
df = pd.concat([df, Event_dummies], axis=1) 
df = df.drop('Event',axis=1)

df_predictor = df[['Holiday','WeekDayNo_1','WeekDayNo_2','WeekDayNo_3','WeekDayNo_4','WeekDayNo_5','WeekDayNo_6','WeekDayNo_7']]
y_target = df['DailyLongTerm_Vessey']

df_predictor = lm.add_constant(df_predictor)
df_fit, df_eval, y_fit, y_eval= train_test_split( df_predictor, y_target, test_size=.2, random_state=1 )

ols_model = lm.OLS(y_fit,df_fit,).fit()
prediction = ols_model.predict(df_eval)
print(ols_model.summary())

prediction = pd.DataFrame(prediction)
prediction.columns = ['predicted_values']
y_eval = y_eval.reset_index(drop=True)
y_eval.columns = ['DailyLongTerm_Vessey']

RMSE = mean_squared_error(y_eval, prediction)**0.5
result_compare = pd.concat([prediction,y_eval], axis=1)
print(result_compare,RMSE)

result = sm.ols(formula="DailyLongTerm_Vessey ~ Holiday + WeekDayNo_1 + WeekDayNo_2 + WeekDayNo_3 + WeekDayNo_4 + WeekDayNo_5 + WeekDayNo_6 + WeekDayNo_7",data=df).fit() 
print(result.summary())
 



