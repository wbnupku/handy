import numpy as np
import pandas as pd
import lightgbm as lgb

# 准备数据
train_fea_pdf = pd.read_pickle('./train.pkl')
val_fea_pdf = pd.read_pickle('./val.pkl')

X_train = train_fea_pdf.iloc[:, 1:-1].to_numpy()
y_train = train_fea_pdf.iloc[:, -1].to_numpy()
X_val = val_fea_pdf.iloc[:, 1:-1].to_numpy()
y_val = val_fea_pdf.iloc[:, -1].to_numpy()
train_data = lgb.Dataset(X_train, label=y_train)

train_data = lgb.Dataset(X_train, label=y_train, feature_name=['title_score', 'title_rating', 'cover_quality_score', 'cover_qoe_score', 'cover_quality_tag', 'video_quality_score', 'vertical_style',  'base_rating', 'cj_rating'], categorical_feature=['title_rating', 'cover_quality_tag', 'vertical_style', 'base_rating'])
val_data = lgb.Dataset(X_train, label=y_train, feature_name=['title_score', 'title_rating', 'cover_quality_score', 'cover_qoe_score', 'cover_quality_tag', 'video_quality_score', 'vertical_style',  'base_rating', 'cj_rating'], categorical_feature=['title_rating', 'cover_quality_tag', 'vertical_style', 'base_rating'])

# 训练
param = {'num_leaves': 31, 'objective': 'binary'}
param['metric'] = ['auc', 'binary_logloss']

num_round = 2000
bst = lgb.train(param, train_data, num_round, valid_sets=[val_data], early_stopping_rounds=5)
# bst = lgb.cv(param, train_data, num_round, nfold=5)
bst.save_model('model.txt', num_iteration=bst.best_iteration)

# cross validation
# bst = lgb.cv(param, train_data, num_round, nfold=5)
# bst.save_model('carrier_detect_model.txt', num_iteration=bst.best_iteration)


# 输出指标和画图
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve

y_pred = bst.predict(X_test)

# pr曲线
prec, recall, threshs = precision_recall_curve(y_test, y_pred)
plt.plot(recall, prec)

# roc曲线
from sklearn import metrics
fpr, tpr, thresholds =  metrics.roc_curve(y_test, y_pred)
print('auc:', metrics.auc(fpr, tpr))
plt.plot(fpr, tpr)
