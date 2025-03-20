import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Make the page layout wide so columns can sit side-by-side
st.set_page_config(layout='wide')

def plot_two_stock_efficient_frontier(mu_A, mu_B, sigma_A, sigma_B, corr_AB):
    """
    Plot two-stock frontier, with:
    - Dashed line for the portion below (inefficient).
    - Solid line for the portion above (efficient).
    - A marker for the minimum-variance portfolio (MVP).
    """

    # 1) Compute covariance
    cov_AB = corr_AB * sigma_A * sigma_B

    # 2) Parametric frontier: weight w in [0..1] for Stock A, (1-w) for Stock B
    n_points = 200
    weights = np.linspace(0, 1, n_points)
    port_returns = []
    port_stdevs  = []

    for w in weights:
        p_return = w * mu_A + (1 - w) * mu_B
        p_var    = (w**2)*(sigma_A**2) + ((1-w)**2)*(sigma_B**2) + 2*w*(1-w)*cov_AB
        port_returns.append(p_return)
        port_stdevs.append(np.sqrt(p_var))

    port_returns = np.array(port_returns)
    port_stdevs  = np.array(port_stdevs)

    # 3) Identify minimum-variance portfolio (MVP)
    idx_min = np.argmin(port_stdevs)
    mvp_x = port_stdevs[idx_min]
    mvp_y = port_returns[idx_min]

    # 4) Split frontier into two segments:
    #    "Inefficient" part: from w=0 up to w=idx_min (lower returns)
    #    "Efficient" part: from w=idx_min to w=1 (higher returns)
    x_inef = port_stdevs[:idx_min+1]
    y_inef = port_returns[:idx_min+1]
    x_ef   = port_stdevs[idx_min:]
    y_ef   = port_returns[idx_min:]

    # 5) Generate random portfolios (for illustration)
    n_portfolios = 3000
    rand_w = np.random.rand(n_portfolios)
    rand_returns = []
    rand_stdevs  = []

    for w in rand_w:
        rp_return = w * mu_A + (1 - w) * mu_B
        rp_var    = (w**2)*(sigma_A**2) + ((1-w)**2)*(sigma_B**2) + 2*w*(1-w)*cov_AB
        rand_returns.append(rp_return)
        rand_stdevs.append(np.sqrt(rp_var))

    # 6) Create the plot
    fig, ax = plt.subplots(figsize=(5, 3))

    # Random portfolios as gray scatter
    ax.scatter(rand_stdevs, rand_returns, alpha=0.2, s=10, color='gray', label='Random Portfolios')

    # Plot dashed line for inefficient portion (lower-return side)
    ax.plot(x_inef, y_inef, 'r--', label='Inefficient')

    # Plot solid line for efficient portion (upper side)
    ax.plot(x_ef, y_ef, 'r-', linewidth=2, label='Efficient Frontier')

    # Mark Stock A and Stock B themselves (100% in one stock)
    ax.scatter(sigma_A, mu_A, s=50, marker='o', label='Stock A')
    ax.scatter(sigma_B, mu_B, s=50, marker='o', label='Stock B')

    # Mark the Minimum-Variance Portfolio
    ax.scatter(mvp_x, mvp_y, s=80, marker='*', color='black', label='Minimum-Variance Portfolio')

    # Axis labels, legend, etc.
    ax.set_title('Two-Stock Frontier')
    ax.set_xlabel('Standard Deviation (Risk)')
    ax.set_ylabel('Expected Return')
    ax.legend(loc='best')
    plt.tight_layout()

    st.pyplot(fig)

def main():
    st.title("Two-Stock Frontier: Dashed Inefficient Portion & MVP")

    # Columns: sliders on the left, chart on the right
    col_sliders, col_chart = st.columns([3, 2])

    with col_sliders:
        st.markdown("### Adjust the Parameters")

        # Rename "Asset" → "Stock"
        mu_A = st.slider("Expected Return of Stock A", 0.00, 0.20, 0.10, 0.01)
        mu_B = st.slider("Expected Return of Stock B", 0.00, 0.20, 0.15, 0.01)
        sigma_A = st.slider("Standard Deviation of Stock A", 0.01, 0.40, 0.20, 0.01)
        sigma_B = st.slider("Standard Deviation of Stock B", 0.01, 0.40, 0.30, 0.01)
        corr_AB = st.slider("Correlation Between Stocks A and B", -1.0, 1.0, 0.20, 0.05)

    with col_chart:
        plot_two_stock_efficient_frontier(mu_A, mu_B, sigma_A, sigma_B, corr_AB)

if __name__ == "__main__":
    main()
