# RFM

RFM : Recency, Frequency, Monetary consists of the initials Recency, Frequency, Monetary.

 1. Business Problem. 
 2. Data Understanding
 3. Data Preparation
 4. Calculating RFM Metrics
 5.  Calculating RFM Scores
 6. Creating & Analyzing RFM Segments
 7. Functionalization of the whole process

 An e-commerce company segments its customers and then organizes them according to these segments wants to define marketing strategies.

# Data Set Story

** I could not add the file to the project directory because the file size is large. Download it from the link below.
https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

 Online Retail II dataset of a UK-based online retail store
 It includes sales between 01/12/2009 - 09/12/2011.
 The company sells souvenirs, most of its customers are wholesalers.
 So the company's customers are corporate customers.
 The aim is to segment these corporate customers according to frequency and recency metrics that are important to me and to deal with my customers on these segments.

 ** If you cannot access the data, I can provide the data if you contact me.

 # Variables

 InvoiceNo: Invoice number. Unique number for each transaction, i.e. invoice. If it starts with C, the canceled transaction.</br>
 StockCode: Product code. Unique number for each product.<br/>
 Description: Open name of the product <br/>
 Quantity: Product quantity. It expresses how many of the products in the invoices are sold. <br/>
 InvoiceDate: Invoice date and time. <br/>
 UnitPrice: Product price (in pounds sterling) <br/>
 CustomerID Unique customer number <br/>
 Country: Country name. The country where the customer lives. <br/>


NOTE  : Let's say the manager of the sales and marketing team makes a request, we think we need to take care of our customers, we want to focus on the need_attention class. 

So we will need to provide the department with the information of the group that provides these features. This code is designed to do just that.

The sub-features given in chapter 7 can be broken down. The stages PREPARE DATA, CALCULATE RFM METRICS, CALCULATE RFM SCORES, NAME SEGMENTS can be broken down into functions.

# What is fragmentation good for?

1) There may be changes in the data set or there may be a desire to intervene in these segments during the flow, so it is useful to fragment.


2) This analysis may be repetitive from time to time, the customers within the segments change from time to time over time periods, so it is critical to observe these changes. We should be able to run this job every month, we should be able to report the changes in the segments that occur after running it every month, and for example, a report was created in the first month and a list was sent to a department to take action, that department took action, so what will happen after that? 

Even in many companies that can do RFM segmentation, this is a problem, it is tried to be overcome.

After the departments take action, there is a follow-up problem, so after a person enters these CRM jobs, one foot must always stay here because the results of the action recommendations given 1-2 months later must be evaluated by the person who made it. 

For more information about RFM, please see my article below.

https://medium.com/@merveatasoy48/customer-segmentation-with-rfm-8db8171eb6d5

 
