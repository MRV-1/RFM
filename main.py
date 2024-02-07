###############################################################
# Customer Segmentation with RFM
###############################################################

# 1. Business Problem. 
# 2. Data Understanding
# 3. Data Preparation
# 4. Calculating RFM Metrics
# 5.  Calculating RFM Scores
# 6. Creating & Analyzing RFM Segments
# 7. Functionalization of the whole process

###############################################################
# 1. Business Problem
###############################################################

# Dataset  Story
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II dataset of a UK-based online retail store
# It includes sales between 01/12/2009 - 09/12/2011.
# The company sells souvenirs, most of its customers are wholesalers.
# So the company's customers are corporate customers.
# The aim is to segment these corporate customers according to frequency and recency metrics that are important to me and to deal with my customers on these segments.


# Variables

# InvoiceNo: Invoice number. Unique number for each transaction, i.e. invoice. If it starts with C, the canceled transaction.
# StockCode: Product code. Unique number for each product.
# Description: Open name of the product
# Quantity: Product quantity. It expresses how many of the products in the invoices are sold.
# InvoiceDate: Invoice date and time.
# UnitPrice: Product price (in pounds sterling)
# CustomerID Unique customer number
# Country: Country name. The country where the customer lives.


###############################################################
# 2. Data Understanding
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


df_ = pd.read_excel("path/dataset/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.shape
df.isnull().sum()


df["Description"].nunique()   

df["Description"].value_counts().head()  

df.groupby("Description").agg({"Quantity": "sum"}).head() #which product is the most ordered
#incoming quantities have an error because this value cannot be negative

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()

df["Invoice"].nunique()

df["TotalPrice"] = df["Quantity"] * df["Price"]
#total price of product

df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()
#total money spent per invoice

# Multiplexed values in the tables will be deduplicated for segmentation, there are multiple values belonging to the same invoice number
# So we took the sum of total prices according to invoices


###############################################################
# 3. Data Preparation
###############################################################

df.shape
df.isnull().sum()
df.describe().T

df = df[(df['Quantity'] > 0)]
df.dropna(inplace=True)                 #dropna is used to delete missing values
df = df[~df["Invoice"].str.contains("C", na=False)]     
#df = df[~(df["Invoice"]).astype(str).str.contains("C", na=False)]

# the values with C at the beginning of the invoice were representing returns, the result of which was causing some negative values to come up

df["Invoice"].head

# outlier cleaning in rfm is optional

###############################################################
# 4. Calculating RFM Metrics
###############################################################

# Calculating R, F, M values for each customer
# Recency, Frequency, Monetary
# Recency : analysis date - last purchase date

df.head()

# We will take the day of analysis as the last date in the dataset
# Recency : today_date - maximum date for each customer
# After groupBy by customer_id we will access the unique number of invoices for each customer
# After groupbying by customer_id, if we take the sum of totalPrice, we can calculate how much each customer left in total


df["InvoiceDate"].max()

today_date = dt.datetime(2010, 12, 11)
type(today_date)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
rfm.head()

rfm.columns = ['recency', 'frequency', 'monetary']

rfm.describe().T

rfm = rfm[rfm["monetary"] > 0]
rfm.shape

# The stage of creating R, F, M metrics in a data set prepared on  accounting records was completed
# These metrics need to be translated into scores

###############################################################
# 5. Calculating RFM Scores
###############################################################
#Recency was inverted, frequecy and monetary values had the perception of size and smallness in a straight way
#Frequency and Monatery large ones score 5 points, while recency small ones score 5 points


rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# what quantile does is it sorts a variable from smallest to largest and divides it according to certain parts, naming the parts as given by the user


rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

#if any one or more of the intervals being split have the same values, the error edges must be unique will be thrown,
#To solve this problem, rank method is used, method: first is used to assign the first class to the first class and this problem is avoided.

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.describe().T

rfm[rfm["RFM_SCORE"] == "55"]  # who are the champions

rfm[rfm["RFM_SCORE"] == "11"]  # who are low value customers



###############################################################
# 6. Creating & Analysing RFM Segments
###############################################################
# regex
# matrix structure will be created using the classes I mentioned in my medium article

# RFM naming
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
# If you see 1 or 2 in the first element and 1 or 2 in the second element, hibernating works like this


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


# When a department requests information about this class, it is necessary to select these classes and forward the index information to the relevant department

rfm[rfm["segment"] == "cant_loose"].head()
rfm[rfm["segment"] == "cant_loose"].index


#extract ids from the desired segment
new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)


new_df.to_csv("new_customers.csv")
rfm.to_csv("rfm.csv")



###############################################################
# 7. Functionalization of the whole process
###############################################################

def create_rfm(dataframe, csv=False):

    # PREPARING DATASET
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # CALCULATING RFM METRICS
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # CALCULATING RFM SCORES
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])


    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # NAMING SEGMENTS
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df, csv=True)






