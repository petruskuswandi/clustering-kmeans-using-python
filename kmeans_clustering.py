import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# Upload file data
uploaded_file = st.file_uploader("Unggah File Data", type=["txt", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".txt"):
            data = pd.read_csv(uploaded_file, sep=';')
        elif uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file, sep=";")
        else:
            st.error("Format file tidak didukung. Mohon gunakan file .txt atau .csv.")
    except Exception as e:
        st.error(f"Kesalahan dalam membaca file: {e}")
else:
    st.warning("Mohon unggah file data terlebih dahulu.")

if 'data' in locals():
    # Sidebar
    st.sidebar.title("Filter Data")
    kategori = st.sidebar.multiselect("Pilih Kategori", data['kategori'].unique(), default=data['kategori'].unique())

    # Filter data berdasarkan kategori yang dipilih
    filtered_data = data[data['kategori'].isin(kategori)]

    # Main content
    st.title("Dashboard Produk")

    # Tampilkan jumlah produk per kategori
    st.subheader("Jumlah Produk per Kategori")
    kategori_counts = filtered_data['kategori'].value_counts()
    st.bar_chart(kategori_counts)

    # Tampilkan produk terlaris
    st.subheader("Produk Terlaris")
    top_sellers = filtered_data.nlargest(10, 'terjual')
    st.write(top_sellers[['nama_produk', 'terjual']])

    # Clustering dengan K-Means
    st.subheader("Clustering Produk dengan K-Means")
    num_clusters = st.slider("Pilih Jumlah Cluster", 2, 3, 3, step=1) # Batasi jumlah cluster maksimal 3

    # Lakukan clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(filtered_data[['stok_awal', 'stok_akhir', 'terjual']])
    filtered_data['cluster'] = cluster_labels + 1  # Ubah label cluster menjadi 1, 2, 3, ...

    # # Tampilkan hasil clustering
    # cluster_stats = filtered_data.groupby('cluster')[['stok_awal', 'stok_akhir', 'terjual']].mean()
    # st.write("Rata-rata Fitur per Cluster:")
    # st.write(cluster_stats)

    # # Tampilkan nama produk pada setiap cluster
    # st.write("Nama Produk per Cluster:")
    # for cluster in cluster_stats.index:
    #     st.write(f"Cluster {cluster}:")
    #     cluster_products = filtered_data[filtered_data['cluster'] == cluster]['nama_produk'].tolist()
    #     st.write(", ".join(cluster_products))

    # Tampilkan tabel data dengan hasil clustering
    st.subheader("Tabel Data dengan Hasil Clustering")
    st.write(filtered_data[['data_ke', 'nama_produk', 'kategori', 'stok_awal', 'stok_akhir', 'terjual', 'cluster']])