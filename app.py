import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="سری فوریه گسسته", layout="wide")

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg,#ff4b6e,#7b2ff7,#00c9a7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 25px;
        font-size: 1rem;
    }
    .section-box {
        background: #f8f9fc;
        border-radius: 14px;
        padding: 18px 22px;
        border: 1px solid #e6e8ef;
        margin-bottom: 18px;
    }
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #2b2d42;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📈 محاسبه و رسم سری فوریه گسسته</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">زوج‌های مرتب و مقدار N را وارد کنید</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box"><div class="section-title">📝 ۱) ورود زوج‌های مرتب (x, y)</div>', unsafe_allow_html=True)
default_points = """0, 1
1, 2
2, 0
3, -1
4, 1
5, 3
6, 2
7, 0"""
text = st.text_area("هر خط یک نقطه: x, y", value=default_points, height=200, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box"><div class="section-title">🔢 ۲) ورود مقدار N</div>', unsafe_allow_html=True)
N = st.slider("N", min_value=0, max_value=50, value=5, step=1, label_visibility="collapsed")
st.markdown(f"<div style='text-align:center;font-size:1.3rem;font-weight:700;color:#7b2ff7;'>N = {N}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

def parse_points(text):
    xs, ys = [], []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.replace("(", "").replace(")", "").split(",")
        if len(parts) != 2:
            raise ValueError(f"خط نامعتبر: {line}")
        xs.append(float(parts[0]))
        ys.append(float(parts[1]))
    return np.array(xs), np.array(ys)

try:
    x, y = parse_points(text)
except Exception as e:
    st.error(f"❌ خطا: {e}")
    st.stop()

M = len(y)
if M < 2:
    st.error("حداقل دو نقطه لازم است.")
    st.stop()

n_idx = np.arange(M)
a = np.zeros(N + 1)
b = np.zeros(N + 1)
a[0] = np.sum(y) / M

for k in range(1, N + 1):
    a[k] = (2 / M) * np.sum(y * np.cos(2 * np.pi * k * n_idx / M))
    b[k] = (2 / M) * np.sum(y * np.sin(2 * np.pi * k * n_idx / M))

def fourier_series(t, a, b, M):
    result = np.full_like(t, a[0], dtype=float)
    for k in range(1, len(a)):
        result += a[k] * np.cos(2 * np.pi * k * t / M) + b[k] * np.sin(2 * np.pi * k * t / M)
    return result

st.markdown('<div class="section-box"><div class="section-title">📊 ۳) ضرایب فوریه</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("a₀ (DC)", f"{a[0]:.4f}")
with col2:
    st.markdown("**aₖ**")
    st.dataframe({"k": list(range(1, N + 1)), "aₖ": np.round(a[1:], 6)}, use_container_width=True, height=250)
with col3:
    st.markdown("**bₖ**")
    st.dataframe({"k": list(range(1, N + 1)), "bₖ": np.round(b[1:], 6)}, use_container_width=True, height=250)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box"><div class="section-title">📉 ۴) نمودار</div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor("#f8f9fc")
ax.plot(x, y, "o--", color="#2b2d42", label="سیگنال اصلی", linewidth=1.5, markersize=8)
t_dense = np.linspace(x.min(), x.max(), 1000)
ax.plot(t_dense, fourier_series(t_dense, a, b, M), "-", color="#ff4b6e", linewidth=2.2, label=f"سری فوریه (N={N})")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend()
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box"><div class="section-title">🧮 ۵) معادله</div>', unsafe_allow_html=True)
terms = [f"{a[0]:.4f}"]
for k in range(1, N + 1):
    terms.append(f"{a[k]:+.4f}·cos(2π·{k}·n/{M})")
    terms.append(f"{b[k]:+.4f}·sin(2π·{k}·n/{M})")
st.code("y(n) ≈ " + " ".join(terms), language="text")
st.markdown('</div>', unsafe_allow_html=True)