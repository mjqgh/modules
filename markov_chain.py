import numpy as np

def overall_conversion_rate(P, start_index=0, conversion_index=-2):
    """
    计算整体转化率（从 Start 出发，最终进入转化吸收态的概率）
    """
    n = P.shape[0]
    t = n - 2  # 暂态数量（假设最后两个是吸收态：转化、Null）
    Q = P[:t, :t]
    R = P[:t, t:]
    N = np.linalg.inv(np.eye(t) - Q)
    B = N @ R
    return B[start_index, 0]  # 转化列是 R 的第一列

def removal_effects(P, channel_indices, start_index=0):
    """
    计算各渠道的移除效应系数和贡献度

    参数：
    P : numpy.ndarray
        转移矩阵
    channel_indices : dict
        渠道名称 -> 索引 的映射（不含 Start/转化/Null）
    start_index : int
        Start 状态索引（默认0）

    返回：
    dict
        {渠道: {"移除后转化率": x, "移除效应系数": y, "贡献度": z}}
    """
    base_rate = overall_conversion_rate(P, start_index=start_index)
    effects = {}

    for ch, idx in channel_indices.items():
        # 构造新的矩阵，移除该渠道
        keep = [i for i in range(P.shape[0]) if i != idx]
        P_new = P[np.ix_(keep, keep)]
        new_rate = overall_conversion_rate(P_new, start_index=0)
        effect = 1 - new_rate / base_rate
        effects[ch] = {"移除后转化率": new_rate, "移除效应系数": effect}

    # 归一化贡献度
    total = sum(v["移除效应系数"] for v in effects.values())
    for ch in effects:
        effects[ch]["贡献度"] = effects[ch]["移除效应系数"] / total

    return base_rate, effects
