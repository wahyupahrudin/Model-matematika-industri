import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Model Matematika Industri", layout="wide")

# Sidebar instruksi
with st.sidebar:
    st.title("Instruksi Penggunaan")
    st.write("Aplikasi ini berisi 4 model matematika industri:")
    st.markdown("1. Optimasi Produksi\n2. Model EOQ\n3. Model Antrian M/M/1\n4. Break-even Analysis")

# Tabs utama
tab1, tab2, tab3, tab4 = st.tabs([
    "Optimasi Produksi", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Model Matematika Lain"
])

# 1. Optimasi Produksi
with tab1:
    st.header("Optimasi Produksi (Linear Programming)")
    st.markdown("Contoh Kasus: Sebuah pabrik memproduksi dua jenis produk, A dan B. Waktu mesin dan keuntungan berbeda.")

    st.subheader("Input Data")
    profit_A = st.number_input("Keuntungan per unit Produk A", value=40.0)
    profit_B = st.number_input("Keuntungan per unit Produk B", value=30.0)
    waktu_mesin1 = st.number_input("Batas waktu mesin 1", value=40.0)
    waktu_mesin2 = st.number_input("Batas waktu mesin 2", value=60.0)

    if waktu_mesin1 > 0 and waktu_mesin2 > 0 and profit_A >= 0 and profit_B >= 0:
        c = [-profit_A, -profit_B]
        A = [[1, 1], [2, 1]]
        b = [waktu_mesin1, waktu_mesin2]

        res = linprog(c, A_ub=A, b_ub=b, method='highs')

        if res.success:
            st.success(f"Produksi Optimal:\n- Produk A = {res.x[0]:.2f}\n- Produk B = {res.x[1]:.2f}\n- Total Profit = {-res.fun:.2f}")
            fig, ax = plt.subplots()
            ax.bar(['Produk A', 'Produk B'], res.x, color=['skyblue', 'salmon'])
            ax.set_ylim(bottom=0)
            ax.set_title("Jumlah Produksi Optimal")
            st.pyplot(fig)
        else:
            st.error("Gagal menyelesaikan optimisasi. Periksa input Anda.")
    else:
        st.warning("Input harus bernilai positif.")

# 2. Model EOQ
with tab2:
    st.header("Model Persediaan EOQ")
    st.markdown("Contoh Kasus: Toko ingin menentukan jumlah pemesanan optimal untuk meminimalkan total biaya persediaan.")

    D = st.number_input("Permintaan Tahunan (D)", value=1000.0)
    S = st.number_input("Biaya Pemesanan (S)", value=50.0)
    H = st.number_input("Biaya Penyimpanan per unit per tahun (H)", value=2.0)

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit")

        q = np.linspace(max(1, EOQ * 0.5), EOQ * 2, 100)
        TC = (D / q) * S + (q / 2) * H
        fig, ax = plt.subplots()
        ax.plot(q, TC, label="Total Cost")
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_title("Total Cost vs EOQ")
        ax.set_xlabel("Order Quantity")
        ax.set_ylabel("Total Cost")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Semua input harus lebih besar dari 0.")

# 3. Model Antrian M/M/1
with tab3:
    st.header("Model Antrian (M/M/1)")
    st.markdown("Contoh Kasus: Sebuah loket layanan menerima pelanggan dengan rata-rata kedatangan dan waktu layanan tertentu.")

    λ = st.number_input("Rata-rata kedatangan per jam (λ)", value=2.0)
    μ = st.number_input("Rata-rata pelayanan per jam (μ)", value=4.0)

    if λ > 0 and μ > 0:
        if λ < μ:
            ρ = λ / μ
            L = ρ / (1 - ρ)
            W = 1 / (μ - λ)
            st.success(f"ρ = {ρ:.2f}, L = {L:.2f}, W = {W:.2f} jam")
            fig, ax = plt.subplots()
            ax.bar(['ρ', 'L', 'W'], [ρ, L, W], color=['lightgreen', 'orange', 'purple'])
            ax.set_ylim(bottom=0)
            ax.set_title("Karakteristik Sistem Antrian")
            st.pyplot(fig)
        else:
            st.error("λ harus lebih kecil dari μ")
    else:
        st.warning("Input harus bernilai positif.")

# 4. Model Tambahan - Break-even
with tab4:
    st.header("Break-even Analysis")
    st.markdown("Contoh Kasus: Sebuah usaha ingin mengetahui titik impas penjualannya.")

    FC = st.number_input("Biaya Tetap (FC)", value=10000.0)
    VC = st.number_input("Biaya Variabel/unit (VC)", value=20.0)
    P = st.number_input("Harga Jual/unit (P)", value=50.0)

    if FC >= 0 and VC >= 0 and P > VC:
        BEQ = FC / (P - VC)
        st.success(f"Break-even Quantity: {BEQ:.2f} unit")

        q = np.linspace(0, max(1, 2 * BEQ), 100)
        total_cost = FC + VC * q
        revenue = P * q

        fig, ax = plt.subplots()
        ax.plot(q, total_cost, label='Total Cost')
        ax.plot(q, revenue, label='Revenue')
        ax.axvline(BEQ, color='gray', linestyle='--', label='Break-even Point')
        ax.set_title("Analisis Titik Impas")
        ax.set_xlabel("Kuantitas")
        ax.set_ylabel("Rupiah")
        ax.legend()
        st.pyplot(fig)
    elif P <= VC:
        st.error("Harga jual harus lebih besar dari biaya variabel.")
    else:
        st.warning("Input harus valid dan bernilai positif.")
