# Loan Help
## How to Issue Smarter Loans
![Dollar Bill](https://cdn-images-1.medium.com/max/800/0*C1vM24QHhRynMy9U)

The objective of this repository is to present a way to issue loan using techniques from data science and machine learning.
This project is hosted on Heroku.com under a free tier. Feel free to play with it and see what you get!

[Try the App on Heroku](https://loan-help.herokuapp.com/ "Loan Help App")


## Repository Organization

```bash
  .
  ├─ model
  ├─ notebooks
  │  ├─ plots
  │  ├─ 00_Train_Test_split.ipynb
  │  ├─ 01_Clean_Wrangle.ipynb
  │  ├─ 02_plots.ipynb
  │  ├─ 03_Model_Selection.ipynb
  │  ├─ 04_FeatureImportance.ipynb
  │  ├─ 05_CompactModel.ipynb
  │  ├─ 06_Model_Tuning.ipynb
  │  ├─ 07_Conf_Interval.ipynb
  │  ├─ LCDataDictionary.xlsx
  │  └─ utils.py
  ├─ templates
  │  └─ main.html
  ├─ Procfile
  ├─ app.py
  ├─ requirements.txt
  └─ runtime.txt
```

## Data Acquisition
The data is based on Lending Club (LC) observations can be accessed for free on Kaggle:
https://www.kaggle.com/wendykan/lending-club-loan-data

## Analytics Overview 

The majority of LC users have average to good credit rating, denoted by"sub_grade". A1 is the best grade possible and G5 is the woest possible. 

![sub_grade distribution](https://github.com/NadimKawwa/loan-help/blob/master/notebooks/plots/sub_grade_count.png)

We also note that the existing debt to income ratio (DTI) prior to issuing the loan is normally distributed along debtors who pay in full and those who default.<br>

![DTI Plot](https://github.com/NadimKawwa/loan-help/blob/master/notebooks/plots/hist_dti.png)

## Using the App

Using the app is rather easy. Simply input the required information, press submit, and get your results:
![app input](https://cdn-images-1.medium.com/max/800/1*1NzIFLjy0GaBv1hM3zxwhw.png)

![app_result](https://cdn-images-1.medium.com/max/800/1*b34KeqVu9oXDuvGiIDOsSQ.png)
