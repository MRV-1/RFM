###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.
# Şirket hediyelik eşya satıyor, müşterilerinin büyük çoğunluğu toptancıdır.
# Dolayısıyla şirketin müşterileri kurumsal müşterilerdir.
# Bu kurumsal müştrileri benim için önemli sayılabilecek, frequency ve recency metriklerine göre segmentlere ayırayım ve
# bu segmentler üzerinde müşterilerimle ilgileneyim amacı yer alır.

# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürünün açık ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
#sayısal değişkenlerin virgülden sonra kaç basamağının gösterileceği bilgisi

df_ = pd.read_excel("C:/Users/MerveATASOY/Desktop/data_scientist-miuul/eğitim_teorik_içerikler/Bölüm_4_CRM_Analitiği/2_RFM_Analizi/projeler/dataset/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.shape
df.isnull().sum()
#Customer id ve description için boş satır geldi, eksik değerleri silmeliyiz çünkü müşterinin id'si belli değilse
#müşteri özelinde segmentasyon çalışmaları yapacak olduğumdan dolayı bu ölçülebilirlik değeri taşımadığından hepsi silinmelidir


# essiz urun sayisi nedir?
df["Description"].nunique()   #eşsiz sınıflarının sayısı

df["Description"].value_counts().head()  #hangi üründen kaçar tane olduğu

df.groupby("Description").agg({"Quantity": "sum"}).head() #en çok sipariş edilen ürün hangisidir
#gelen quantity'lerde hata var çünkü bu değer - olamaz

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()

df["Invoice"].nunique()

df["TotalPrice"] = df["Quantity"] * df["Price"]
#ürünlerin toplam kazancı

df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()
#fatura başına toplam harcanan para

#Segmentasyona gidiş için tablolardaki çoklanan değerler tekilleştirilecek, aynı fatura numarasına ait birden fazla değer var
#bu yüzden invoice'lere göre total price'lerin sum'ı alındı


###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################

df.shape
df.isnull().sum()
df.describe().T
#burada - değerler gelmektedir, bunların yok edilmesi gerekir
df = df[(df['Quantity'] > 0)]
df.dropna(inplace=True)                 #dropna eksik değeleri silmek için kullanılır
df = df[~df["Invoice"].str.contains("C", na=False)]     #burada string hatası veriyor aşağıdaki gibi çalıştırınca kabul etti
#df = df[~(df["Invoice"]).astype(str).str.contains("C", na=False)]

#invoice'de başında C olan değerler iadeleri ifade etmekteydi bunların sonucu bazı - değerlerin gelmesine sebep olmaktaydı

df["Invoice"].head

#rfm'de outlier temizliği yapılmalı mı ?
#isteyen yapabilir
#ama burada zaten outlier'lar 5 skoruna denk geleceğinden dolayı aykırı değer temizlemesini yapmamayı tercih edebilirsiniz



###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

#her bir müşteri özelinde R, F, M değerlerinin hesaplanması
# Recency, Frequency, Monetary
# Recency : analiz tarihi - son satın alma tarihi

df.head()

#analizin yapıldığı günü veri setinin içerisindeki son tarih ne ise o olarak alacağız
# Recency : today_date - her bi müşterinin maximum tarihi
# customer_id'ye göre groupBy'a aldıktan sonra her bir müşterinin eşsiz fatura sayısına erişeceğiz
# customer_id'ye göre groupby yaptıktan sonra totalPrice'ın sum'ı alınırsa her bir müşterinin toplam kaç para bıraktığı hesaplanır


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

# muhasebe kayıtları üzerinde hazırlanan bir veri setinde R, F, M metriklerinin oluşturulması aşaması tamamlandı
# bu metriklerin skorlara çevrilmesi lazım


###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################
#Recency ters, frequecy ve monetary değerleri düz bir şekilde büyüklük küçüklük algısı vardı
#frequency ve monatery'de büyük olanlar 5 puan alırken, recency'de küçük olanlar 5 puan alır


rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
#quantile'ın asıl yaptığı işlem bir değişkeni küçükten büyüğe sıralar ve belirli parçalara göre bunu böler, böldüğü parçalara kullanıcının verdiği isimlendirmeleri yapar

# 0-100, 0-20, 20-40, 40-60, 60-80, 80-100

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
#eğer bölünen aralıklardan herhangibirinde ya da birkaçında aynı değerler yer alıyorsa edges must be unique hatası yer alır,
#bu problemi çözmek için rank methodu kullanılır, method: first diyerek ilk gördüğünü ilk sınıfa ata dendi ve bu problemin önüne geçildi

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.describe().T

rfm[rfm["RFM_SCORE"] == "55"]  #şampiyonlar kimler

rfm[rfm["RFM_SCORE"] == "11"]  #az değerli müşteriler



###############################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
###############################################################
# regex
#slaytta bahsedilen sınıflar kullanılarak matris yapısı oluşturulacak

# RFM isimlendirmesi
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
# 1. elemanında 1 ya da 2, ikinci elemanında 1 ya da 2 görürsen hibernating isimlendimesini yap şeklinde çalışır


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


#şuana kadar yapılan işlemlerde kural tabanlı bir şekilde müşteriler segmentlere ayrıldı

#diyelimki satış pazarlama takımının yöneticisi şöyle bir talepte bulundu, biz senin anlattıklarından ikna olduk, müşterilerimizle ilgilenmemiz gerektiğini düşünüyoruz, need_attention sınıfına özel odaklanmak istiyoruz,

#eğer bu sınıf ilgi görmezse bunun gideceği yer churn'dur yani önce uykuya sonrasında bizi terk etme durumuna geçecektir

# bir departman bu sınıfa ait bilgileri istediğinde; bu sınıfları seçip index bilgilerini ilgili departmana iletmek gerekir



rfm[rfm["segment"] == "cant_loose"].head()
rfm[rfm["segment"] == "cant_loose"].index


#istenilen segmentteki id'leri  dışarı çıkartalım
new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)
#ondalıklardan kurtulmak için astype(int) yapıldı

new_df.to_csv("new_customers.csv")
rfm.to_csv("rfm.csv")



###############################################################
# 7. Tüm Sürecin Fonksiyonlaştırılması
###############################################################

def create_rfm(dataframe, csv=False):

    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklendi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
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


#alt özellikler parçalanabilir --> VERIYI HAZIRLAMA, RFM METRIKLERININ HESAPLANMASI, RFM SKORLARININ HESAPLANMASI, SEGMENTLERIN ISIMLENDIRILMESI aşamaları fonksiyonlara ayrılabilir

#Parçalamak ne işe yarar?
#veri setinde değişiklik meydana gelebilir ya da akış esnasında bu parçalara müdahele edilmek isteniyor olabilir, dolayısıyla parçalamakta fayda vardır


#bu analiz dönem dönem tekrar ediyor olabilir, segmentlerin içerisindeki müşteriler zaman periyotları içerisinde dönem dönem değişir,  dolaıysıyla bu değişimleri gözlemlemek oldukça kritik, oldukça değerlidir, bu işi her ay çalıştırabiliyor olmamız gerekir, her ay çalıştırdıktan sonra oluşan segmentlerdeki değişimleri raporlayabilmeli ve örneğin ilk ay bir rapor oluşturuldu ve bir departmana aksiyon alması için bir liste gönderildi, o departman aksiyon aldı, peki bunun sonrasında ne olacak ? RFM segmentasyonunu yapabilen birçok şirkette dahi bu bir problemdir, aşılmaya çalışılır
# departmanlar aksiyon aldıktan sonra bir takip etme problemi vardır, dolayısıyla bir kişi bu CRM işlerine girdikten sonra bir ayağı hep burada kalmak zorundadır çünkü 1-2 ay sonra verilen aksiyon tavsiyelerinin sonuçları bunu yapan kişi tarafından değerlendirilmelidir





