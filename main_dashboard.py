import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#import main dataframe
full_join_df = pd.read_csv('main_data.csv')
datetime_columns = ["order_date", "delivery_date"]
full_join_df.sort_values(by="order_date", inplace=True)
full_join_df.reset_index(inplace=True)
 
for column in datetime_columns:
    full_join_df[column] = pd.to_datetime(full_join_df[column])

# Banyaknya pelanggan berdasarkan customer_state
customer_by_state = full_join_df.groupby(by="customer_state").customer_unique_id.nunique().sort_values(ascending=False).reset_index()
# Banyaknya pelanggan berdasarkan customer_city
customer_by_city = full_join_df.groupby(by="customer_city").customer_unique_id.nunique().sort_values(ascending=False).reset_index()
# Banyaknya orderan yang dilakukan oleh customer
count_order = full_join_df.groupby(by="customer_unique_id").agg(count_order= ("order_id", "nunique"), sum_order = ("total_order_value", "sum")).reset_index()
count_order_sort = count_order.sort_values(by=['count_order','sum_order'], ascending=False).head(10)
# Banyaknya penjual berdasarkan seller_state
seller_by_state = full_join_df.groupby(by="seller_state").seller_id.nunique().sort_values(ascending=False).reset_index()
# Banyaknya penjual berdasarkan seller_city
seller_by_city = full_join_df.groupby(by="seller_city").seller_id.nunique().sort_values(ascending=False).reset_index()
# Banyaknya produk yang terjual
seller_count_order = full_join_df.groupby(by="seller_id").agg(seller_count_order= ("order_id", "nunique"), seller_sum_order = ("total_order_value", "sum")).reset_index()
seller_count_order = seller_count_order.sort_values(by=['seller_count_order','seller_sum_order'], ascending=False).head(10)
# Kategori produk dengan total order terendah
order_by_product_category = full_join_df.groupby(by="product_category").agg(num_of_order = ('order_id','count'), sum_order_value = ('total_order_value', 'sum')).reset_index()
# Kategori produk dengan total order tertinggi
order_by_product_category.sort_values(by=['num_of_order','sum_order_value'], ascending=False).head(10)
# Pesanan berdasarkan hari
day_count = full_join_df.groupby("day_order").order_id.nunique().reset_index().sort_values(
    by='order_id', ascending=False)
# Pesanan berdasarkan keadaan daytime
daytime_count = full_join_df.groupby("daytime_order").order_id.nunique().sort_values(ascending=False).reset_index()
# Pesanan berdasarkan keadaan waktu
hour_count = full_join_df.groupby("hour_order").order_id.nunique().sort_values(ascending=False).reset_index()
# Menggunakan groupby untuk mengelompokkan berdasarkan tahun
yearly_orders = full_join_df.groupby(full_join_df['order_date'].dt.year).agg(
    count_order=('order_id', 'nunique'),
    sum_order_value=('total_order_value', 'sum')
).reset_index()
# Mengubah nama kolom
yearly_orders = yearly_orders.rename(columns={'order_date': 'year'})
yearly_orders_sorted = yearly_orders.sort_values(by='count_order', ascending=False)
# Menggunakan groupby untuk mengelompokkan berdasarkan bulan
monthly_orders = full_join_df.groupby(full_join_df['order_date'].dt.to_period("M")).agg(
    count_order=('order_id', 'nunique'),
    sum_order_value=('total_order_value', 'sum')
).reset_index()
# Mengubah nama kolom dan format tanggal
monthly_orders = monthly_orders.rename(columns={'order_date': 'month_order'})
monthly_orders['month_order'] = monthly_orders['month_order'].dt.to_timestamp().dt.strftime('%Y-%m')
monthly_orders_sorted = monthly_orders.sort_values(by='count_order', ascending=False)
# Menghitung RFM
recent_order_date = full_join_df['order_date'].max().date()
rfm_df = full_join_df.groupby('customer_unique_id').agg(
    recency=('order_date', lambda x: (recent_order_date - x.max().date()).days),
    frequency=('order_id', 'nunique'),
    monetary=('total_order_value', 'sum')
).reset_index()
    
#JUDUL
st.header('E-Commerce Data Collection Dashboard :fire:')

st.subheader('Customer Analysis')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

# Plot berdasarkan Kota
ax[0].barh(customer_by_city.head(10)["customer_city"], customer_by_city.head(10)["customer_unique_id"], color=colors)
ax[0].set_xlabel(None)
ax[0].set_title("Berdasarkan Kota", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)
ax[0].tick_params(axis='y', labelrotation=0, labelsize=15)

# Plot berdasarkan Negara Bagian
ax[1].barh(customer_by_state.head(10)["customer_state"], customer_by_state.head(10)["customer_unique_id"], color=colors)
ax[1].set_xlabel(None)
ax[1].set_title("Berdasarkan Negara Bagian", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
ax[1].tick_params(axis='y', labelrotation=0, labelsize=15)

plt.suptitle("Persebaran Jumlah Pelanggan Berdasarkan Kota dan Negara Bagian", fontsize=20)
plt.tight_layout()
st.pyplot(fig)

# Bar Plot Frekuensi Order
fig, ax = plt.subplots(figsize=(10, 8))

colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

sns.barplot(x="count_order", y="customer_unique_id", data= count_order_sort, palette=colors)
ax.set_ylabel('Customer Unique ID', fontsize=12)
ax.set_xlabel('Jumlah Order', fontsize=12)
ax.set_title("Frekuensi Pelanggan yang Suka Memesan", loc="center", fontsize=15)
ax.bar_label(ax.containers[0], label_type='center')
ax.tick_params(axis ='y', labelsize=10)
st.pyplot(fig)

# SELLER
st.subheader('Seller Analysis')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

# Plot berdasarkan Kota
ax[0].barh(seller_by_city.head(10)["seller_city"], seller_by_city.head(10)["seller_id"], color=colors)
ax[0].set_xlabel(None)
ax[0].set_title("Berdasarkan Kota", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)
ax[0].tick_params(axis='y', labelrotation=0, labelsize=15)

# Plot berdasarkan Negara Bagian
ax[1].barh(seller_by_state.head(10)["seller_state"], seller_by_state.head(10)["seller_id"], color=colors)
ax[1].set_xlabel(None)
ax[1].set_title("Berdasarkan Negara Bagian", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
ax[1].tick_params(axis='y', labelrotation=0, labelsize=15)
plt.suptitle("Persebaran Jumlah Pelanggan Berdasarkan Kota dan Negara Bagian", fontsize=20)
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 8))

colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

sns.barplot(x="seller_count_order", y="seller_id", data= seller_count_order, palette=colors)
ax.set_ylabel('Seller ID', fontsize=12)
ax.set_xlabel('Jumlah Order', fontsize=12)
ax.set_title("Frekuensi Produk Seller yang Terjual", loc="center", fontsize=15)
ax.bar_label(ax.containers[0], label_type='center')
ax.tick_params(axis ='y', labelsize=10)
st.pyplot(fig)


st.subheader('Product Analysis')

# Your color palette
colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

# Create a bar plot and set the figure size
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="num_of_order", y="product_category", data=order_by_product_category.sort_values(by=['num_of_order','sum_order_value'], ascending=False).head(10), palette=colors, ax=ax)

# Set labels and title
plt.xlabel('Jumlah Pesanan')
plt.ylabel('Kategori Produk')
plt.title('Jumlah Pesanan Terbanyak untuk Kategori Produk', fontsize=15)

# Display the figure
st.pyplot(fig)

fig, axs = plt.subplots(nrows=3, figsize=(24, 18))
st.subheader('Time and Condition Analysis')
# Bar Plot Berdasarkan Jam Pemesanan
sns.barplot(
    y="hour_order",
    x="order_id",
    data=hour_count.sort_values(by='hour_order', ascending=True),
    ax=axs[0]
)
axs[0].set_xlabel('Jumlah Pesanan', fontsize=15)
axs[0].set_ylabel('Jam Pemesanan', fontsize=15)
axs[0].set_title("Berdasarkan Jam Pemesanan", loc="center", fontsize=18)
axs[0].tick_params(axis='x', labelsize=15)

# Bar Plot Berdasarkan Saat Pemesanan
sns.barplot(
    y="daytime_order",
    x="order_id",
    data=full_join_df.groupby('daytime_order').order_id.nunique().reset_index(),
    ax=axs[1]
)
axs[1].set_xlabel('Jumlah Pesanan', fontsize=15)
axs[1].set_ylabel('Saat Pemesanan', fontsize=15)
axs[1].set_title("Berdasarkan Saat Pemesanan", loc="center", fontsize=18)
axs[1].tick_params(axis='x', labelsize=15)

# Bar Plot Berdasarkan Hari Pemesanan
sns.barplot(
    y="day_order",
    x="order_id",
    data=full_join_df.groupby('day_order').order_id.nunique().reset_index().sort_values(by='order_id', ascending=False),
    ax=axs[2]
)
axs[2].set_xlabel('Jumlah Pesanan', fontsize=15)
axs[2].set_ylabel('Hari Pemesanan', fontsize=15)
axs[2].set_title("Berdasarkan Hari Pemesanan", loc="center", fontsize=18)
axs[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Jumlah Pesanan Pelanggan Berdasarkan Waktu Pemesanan", fontsize=20)
plt.tight_layout()
st.pyplot(fig)

plt.figure(figsize=(10, 5))
plt.plot(
    yearly_orders.year,
    yearly_orders.count_order,
    marker= 'o',
    linewidth= 3,
    color= "#3187d4"
    )
plt.title("Perkembangan Jumlah Order per Tahun" , loc="center", fontsize=18, pad=10)
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)

st.pyplot(fig)

st.subheader('RFM Analysis')
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

sns.histplot(rfm_df['recency'], bins=20, kde=True, color='skyblue', ax=axs[0])
axs[0].set_title('Recency Distribution')
axs[0].set_xlabel('Recency (days)')

sns.histplot(rfm_df['frequency'], bins=20, kde=True, color='salmon', ax=axs[1])
axs[1].set_title('Frequency Distribution')
axs[1].set_xlabel('Frequency')

sns.histplot(rfm_df['monetary'], bins=20, kde=True, color='green', ax=axs[2])
axs[2].set_title('Monetary Distribution')
axs[2].set_xlabel('Monetary Value')

plt.suptitle('RFM Analysis - Customer Segmentation')
plt.tight_layout()
st.pyplot(fig)


fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(28, 8))
colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]

# Fungsi untuk membuat bar plot
def create_bar_plot(x, y, data, ax, ylabel, title):
    sns.barplot(x=x, y=y, data=data, palette=colors, ax=ax)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xlabel(None)
    ax.set_title(title, loc="center", fontsize=16)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=14)

# Bar plot Recency
create_bar_plot("customer_unique_id", "recency", rfm_df.sort_values(by='recency', ascending=True).head(10), axs[0], 'Hari', 'Berdasarkan Recency')

# Bar plot Frequency
create_bar_plot("customer_unique_id", "frequency", rfm_df.sort_values(by='frequency', ascending=False).head(10), axs[1], None, 'Berdasarkan Frequency')

# Bar plot Monetary
create_bar_plot("customer_unique_id", "monetary", rfm_df.sort_values(by='monetary', ascending=False).head(10), axs[2], 'R$', 'Berdasarkan Monetary')

plt.suptitle("Pelanggan Terbaik Berdasarkan Parameter RFM", fontsize=20)
st.pyplot(fig)
