import pandas as pd
import numpy as np
from myTools.pdTools.auto_ml_tool.amt_2_3 import Amtl

data_path = 'train.csv'
train_data = pd.read_csv(data_path)
list_org = ['PassengerId', 'Survived', 'Pclass', "Sex", "Age", "SibSp", "Fare", "Cabin", "Embarked"]
#list_org = ['PassengerId', 'Survived', 'Pclass',  "Age", "SibSp", "Fare", "Cabin"]
one_hot_list = ["Sex"]
gender_map_a = {np.NaN: 1}
train_data["Cabin"] = train_data["Cabin"].map(gender_map_a)

gender_map_b = {np.NaN: 0, 1: 1}
train_data["Cabin"] = train_data["Cabin"].map(gender_map_b)

train_data.loc[train_data['Age'] < 15, 'Age'] = 1
train_data.loc[(train_data['Age'] >= 15) & (train_data['Age'] <= 50), 'Age'] = 2
train_data.loc[train_data['Age'] > 50, 'Age'] = 3
train_data.replace(np.nan, 2, inplace=True)

#n_estimators默认100，max_depth默认3，min_child_weight默认1,gamma默认0，learning_rate默认0.1
cv_param = {
            'n_estimators': np.arange(20, 80, 5),
            'max_depth': np.arange(2, 5, 1),
            'min_child_weight': np.arange(1, 2, 1),
            'gamma': np.arange(0.1, 0.2, 0.05),
            'learning_rate': np.arange(0.1, 0.2, 0.05)
            }

psl = Amtl(train_data, 'PassengerId', 'Survived', model='C', fearture_list=list_org,
            cv_dic=cv_param, pca_param_s=None, pca_param_d=None, one_hot_list=one_hot_list)
psl.fit()
print(psl.rf.score(psl.X_train, psl.Y_train))

'''
使用手册
所提供的功能有：
1.数据分离（随机1000个值，其中不是纯数字的为文本型特征，不包括空值）
2.数据转换，文本型先转化为0，1，2...（按文本频率从高到低）
3.数据补齐，对于文本型中位数补齐，对于数值型平均数补齐
4.数据标准化，测试集使用训练集的标准化标准
5.one_hot 编码（可选）
6.PCA降维 int型为固定维度，float为按比例保留维度
7.xgb主要参数的网格搜索（支持插入自建模型）目标函数：回归MAE，分类acc
8.配合预测类一起使用，同样的处理方式，其中模型可单独提出 self.rf

原始参数一共有
train_pandas, Id, target, model='R', pca_param_s=None, pca_param_d=None,
                 fearture_list=None, one_hot_list=None, cv_dic=None
1.train_pandas是处理后的pandas格式数据，训练和测试做特征工作应以训练集为标准
2.Id 为定位key特征字段,不能重复
3.target为目标变量字段
4.model R为回归，C为分类
5.pca_param_s 为文本型降维保留分数，int型为固定维度，float为按比例保留维度
6.pca_param_d 为数值型降维保留分数，int型为固定维度，float为按比例保留维度
7.fearture_list 为指定特征字段list，必须包含Id, target字段，并按pandas导入的字段顺序排列,None为所有字段一起处理
8.one_hot_list 为指定的one_hot编码字段，要求必须要文本特征中，None是对所有文本型进行处理，‘off’是对所有都不处理
9.cv_dic 为主要参数的search，字典类型关闭为默认或者自建参数格式如下：
cv_param = {
            'n_estimators': np.arange(20, 80, 5),
            'max_depth': np.arange(2, 5, 1),
            'min_child_weight': np.arange(1, 2, 1),
            'gamma': np.arange(0.1, 0.2, 0.05),
            'learning_rate': np.arange(0.1, 0.2, 0.05)
            }
example
train
psl = Amtl(train_data, 'PassengerId', 'Survived', model='C', fearture_list=list_org,
            cv_dic=cv_param, pca_param_s=None, pca_param_d=None, one_hot_list=one_hot_list)
#psl.rf = model()
psl.fit()
需要使用自建模型在psl.fit()前写入 

predict
pslp =Amtl_predict(train_data, model_path, Show_title=True, math_format=0)
result = pslp.rf_predict() 预测结果
#pslp.print_csv()   打印为csv文件
'''

