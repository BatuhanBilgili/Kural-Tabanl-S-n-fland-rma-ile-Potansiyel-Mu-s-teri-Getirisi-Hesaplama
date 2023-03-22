##########################
# Görev 1:
##########################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.,
import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv("persona.csv")
df.head()
df.shape
df.info()

#  Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()
# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df.groupby("COUNTRY")["PRICE"].count()

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE":"sum"})

# Soru 7: SOURCE türlerine göre satış sayıları nedir?
df.groupby("SOURCE")["PRICE"].count()
df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE":"mean"})


#  Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE":"mean"})

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE":"mean"})

##########################
# Görev 2:COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
##########################
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE":"mean"}).head()


##########################
# Görev 3: Çıktıyı PRICE’a göre sıralayınız.
##########################
# • Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
# • Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE":"mean"}).sort_values("PRICE", ascending=False)
agg_df.head()

##########################
# Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz.
##########################
# • Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.
agg_df = agg_df.reset_index()
agg_df.head()

##########################
# Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
##########################
# • Age sayısal değişkenini kategorik değişkene çeviriniz.
# • Aralıkları ikna edici şekilde oluşturunuz.
# • Örneğin: ‘0_18', ‘19_23', '24_30', '31_40', '41_70'

agg_df["AGE"].describe()


# AGE değişkeninin nerelerden bölüneceğini belirleyelim:
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim:
labels = ["0_18", "19_23", "24_30", "31_40", "41_" + str(agg_df["AGE"].max())]

# age'i bölme:
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=labels)
agg_df.head()

##########################
# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
##########################
# CUStomers_ leve l_based adinda bir deg1şken tanim Lay1n1z ve veri setine bu degişkeni ekleyln1z.
# Dikkat!
# list comp ile customers_level_based değerleri olusturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# v Orneğin birden fazla şu ifadeden olabilir : USA_ANDROID_MALE_0_18
# Bunlari groupby 'a allp price ontalamalarını almak gerekmektedir.

# değişken isimleri:
agg_df.columns

# gözlem değerlerine erişmek için:
for row in agg_df.values:
    print(row)


# COUNTRY, SOURCE, SEX ve age_cat değişkenlerinin DEGERLERINI yan yana koymak ve alt tireyle birleştirmek istiyoruz.
#Bunu List comprehension ile yapabiliriz.
#Yukaridaki döngüdeki gözlem değerlerinin bize lazim olanlarini seçecek şekilde işlemi gerçekletirelim :
[row[0].upper ()+ "" + row[1] .upper ()+ "_" + row[2] . upper () + "_" + row [5] . upper () for row in agg_df. values]

# Veri setine ekleyelim:
agg_df["customers_level_based"] = [row[0].upper()+ "-" + row[1].upper() + "-" + row[2].upper() + "-" + row[5].upper() for row in agg_df.values]
agg_df.head()

# Gereksiz değişkenleri çikaralim:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))

# Amacim1za bir adim daha yaklaştik.
#Burada ufak bir problem var. Birçok ayni segment olacak.
# örneğin USA_ANDROID_MALE_0_18 segmentinden birkok say1da olabilir.
# kontrol edelim:
agg_df["customers_level_based"].value_counts()

#Bu sebeple segmentlere göre groupby yaptiktan sonra price ortalamalarini almali ve segmentleri tekilleştirmeliyiz.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

# customers_level_based index'te yer almaktadır. Bunu değişkene çevirelim:
agg_df = agg_df.reset_index()
agg_df.head()

# Kontrol edelim. Her bir persona'nın 1 tane olmasını bekleriz:
agg_df["customers_level_based"].value_counts()
agg_df.head()


##########################
# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
##########################
# • Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# • Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# • Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["SEGMENT"] = pd.cut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE":"mean"})

##########################
# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
##########################
# • 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# • 35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]