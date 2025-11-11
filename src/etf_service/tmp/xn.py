import numpy as np
import matplotlib.pyplot as plt

def draw_shannon_grid(init_price: float,
                      grid_percent: float = 0.05,
                      n_levels_up: int = 10,
                      n_levels_down: int = 10,
                      price_series: list | np.ndarray = None,
                      multiplicative: bool = True,
                      figsize=(8, 10),
                      label_every: int = 1):
    """
    绘制香农半仓网格线（仅画线，不计算持仓）。
    """

    # === 计算网格线价格 ===
    if multiplicative:
        ks = np.arange(-n_levels_down, n_levels_up + 1)
        levels = init_price * (1 + grid_percent) ** ks
    else:
        step = init_price * grid_percent
        ks = np.arange(-n_levels_down, n_levels_up + 1)
        levels = init_price + ks * step

    levels = np.sort(levels)

    # === 创建图 ===
    fig, ax = plt.subplots(figsize=figsize)

    # 如果传入价格序列，则画出价格曲线
    if price_series is not None:
        price_series = np.asarray(price_series)
        ax.plot(price_series, color='tab:orange', label="实盘价格", linewidth=1.5)
        x_min, x_max = 0, len(price_series) - 1
    else:
        x_min, x_max = 0, 1
        ax.set_xticks([])

    # === 绘制网格线 ===
    for i, lvl in enumerate(levels):
        if np.isclose(lvl, init_price, rtol=1e-9):
            ax.hlines(lvl, x_min, x_max, colors='tab:blue', linestyles='-', linewidth=2)
            ax.text(x_max, lvl, f"初始价 {lvl:.2f}", va='center', ha='right', fontsize=9, color='tab:blue')
        else:
            ax.hlines(lvl, x_min, x_max, colors='gray', linestyles='--', linewidth=0.8)
            if i % label_every == 0:
                pct = (lvl / init_price - 1) * 100
                ax.text(x_max, lvl, f"{lvl:.2f} ({pct:+.1f}%)",
                        va='center', ha='right', fontsize=8, color='black', alpha=0.7)

    # === 样式设置 ===
    ax.set_title(f"香农半仓网格图（初始价={init_price:.2f}, 网格={grid_percent*100:.1f}%）", fontsize=12)
    ax.set_ylabel("价格", fontsize=10)
    ax.grid(False)
    if price_series is not None:
        ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

    return levels


# ==== 示例运行 ====
if __name__ == "__main__":
    init_price = 2.2
    grid_percent = 0.05  # 每格 5%
    n_up = 10
    n_down = 10

    # 你可以不传 price_series，这样只画网格
    levels = draw_shannon_grid(init_price=init_price,
                               grid_percent=grid_percent,
                               n_levels_up=n_up,
                               n_levels_down=n_down,
                               price_series=None,  # 示例：不传数据
                               multiplicative=True)
    print("生成的网格价格：", np.round(levels, 4))
