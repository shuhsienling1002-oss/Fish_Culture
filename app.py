import streamlit as st
import pandas as pd
import time
import random

# ==========================================
# 1. 系統設定與資料庫 (System Config & Data)
# ==========================================
st.set_page_config(
    page_title="阿美族漁獵文化教學系統",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 模擬資料庫：阿美語詞彙 (已包含 mato'asay)
VOCABULARY = {
    "foting": "魚",
    "'afar": "蝦",
    "kalang": "蟹",
    "riyar": "海洋",
    "'alo": "河流",
    "mifoting": "捕魚",
    "mipaliw": "互助/換工",
    "rakar": "魚筌 (陷阱)",
    "tafokod": "八卦網",
    "paysin": "禁忌/規矩",
    "mato'asay": "長老/領導者"
}

# 模擬資料庫：教案內容 (細節強化版本)
LESSON_PLANS = {
    "低年級教案": [
        {"Title": "L1 大海是個大冰箱", "Obj": "認識環境，能量概念", "Act": "故事時間：講述阿美族孩子在溪邊的故事，學習 riyar（海）和 'alo（河）。討論「吃魚就是得到魚的能量」。"},
        {"Title": "L2 魚兒點點名", "Obj": "認識食物與能量，感官分類", "Act": "感官體驗：摸魚鱗/蟹殼的觸感。學習說出 foting（魚）和 'afar（蝦）並搭配動作。"},
        {"Title": "L3 安靜！魚會聽見", "Obj": "規矩與專注，訊號與噪聲", "Act": "遊戲：「魚在聽」。當老師轉過身時，學生必須保持靜止不動。理解大聲吵鬧會嚇跑魚兒。"},
        {"Title": "L4 小小漁夫動手做", "Obj": "動手嘗試，能量輸出", "Act": "操作體驗：使用網勺撈取水中的玩具魚。練習模仿撒網的動作 （將手部能量釋放出去）。"},
        {"Title": "L5 大家一起吃", "Obj": "分享與愛，正向回饋", "Act": "情境模擬：捕到的「魚」（餅乾或糖果）要先分給長輩和朋友。理解分享會讓友誼的網絡更強。"},
        {"Title": "L6 Mallah 派對", "Obj": "文化連結，建立網絡連結", "Act": "文化體驗：全班圍坐成圓圈，老師解釋 Malaholol（團聚）代表的意義是「我們是一家人」。"}
    ],
    "中年級教案": [
        {"Title": "L1 季節的時鐘", "Obj": "生態時序，資源流動", "Act": "製作「魚的洄游路線圖」。重點標註魚類繁殖期（休漁期），理解不捕撈小魚是為了確保明年的資源流動。"},
        {"Title": "L2 工具大揭密", "Obj": "工具原理，最小阻力路徑", "Act": "原理分析：深入觀察魚筌（Rakar）的構造細節 ，討論竹條如何編織成單向入口，實現「只進不出」的陷阱邏輯。"},
        {"Title": "L3 陷阱工程師(上)", "Obj": "PBL實作，網絡節點", "Act": "設計草圖：繪製模擬河道地形。討論魚會在哪裡休息？哪裡的水流最適合佈置陷阱？這就是尋找「高流量節點」。"},
        {"Title": "L4 陷阱工程師(下)", "Obj": "PBL實作，試錯與優化", "Act": "實作優化：用回收材料製作魚筌模型並測試。小組分享如何修正，使其更符合水流原理，提高捕獲率。"},
        {"Title": "L5 超級團隊 Mipaliw", "Obj": "團隊分工，網絡帶寬", "Act": "遊戲：模擬「趕魚與圍捕」。強調趕魚者的訊號必須清晰，撒網者要快速響應，才能達到最大捕獲效率。"},
        {"Title": "L6 漁獲怎麼分？", "Obj": "分享交換，公平分配", "Act": "討論：如果只分給抓魚的人，生病或受傷的人怎麼辦？理解平均分配是為了部落的持續運作。學習將食物分給 mato'asay 的禮儀。"}
    ],
    "高年級教案": [
        {"Title": "L1 南島的基因", "Core_Idea": "部落互助的力量 (網絡拓撲)", "Obj": "地理與基因，強連結特性", "Act": "地圖分析：分析南島語族擴散的地圖 。討論阿美族社會階層（如 Kapah 青壯年、mato'asay 長老）在漁獵中的網絡分工。"},
        {"Title": "L2 規矩與智慧", "Core_Idea": "祖先的生存智慧 (風險管理)", "Obj": "批判思考，風險極小化策略", "Act": "深究 Paysin（禁忌）與現代安全規範的異同。討論為何傳統規定女性不能靠近漁獵場地。深討出獵前儀式（Milamo）。"},
        {"Title": "L3 物理與力學", "Core_Idea": "大自然永續的規則 (能量轉換)", "Obj": "科學原理，能量轉換效率", "Act": "案例分析：八卦網（Tafokod）的構造細節 。討論網邊的鉛墜如何透過慣性與離心力，讓網面在水中均勻展開。"},
        {"Title": "L4 公地悲劇", "Core_Idea": "大自然永續的規則 (資源保護)", "Obj": "賽局理論，對抗資源耗竭", "Act": "賽局實驗：進行資源有限性模擬遊戲。討論氣候變遷下，現代社會如何從阿美族的「不貪婪」哲學中學習資源分配。"},
        {"Title": "L5 社會安全網", "Core_Idea": "部落互助的力量 (冗餘生存)", "Obj": "社會正義，冗餘生存策略", "Act": "分配與正義：模擬分配魚貨。深入討論 Mipaliw 互助精神如何建立社會資本，確保 mato'asay 和弱勢節點在網絡中不會被孤立。"},
        {"Title": "L6 永續宣言", "Core_Idea": "祖先的生存智慧 (適應與進化)", "Obj": "反思應用，高效率運算", "Act": "PBL 最終產出：讓學生撰寫一份現代生活的「自然公約」，涵蓋資源使用規範與部落互助原則。"}
    ]
}

# ==========================================
# 2. 介面設計 (UI Layout)
# ==========================================

# 側邊欄導航
with st.sidebar:
    st.title("🏹 漁獵文化教學導航")
    mode = st.radio(
        "選擇功能模組：",
        ["🏠 首頁與理念", "🟢 低年級教案", "🟡 中年級教案", "🔴 高年級教案", "🛠️ 數位教具箱", "📚 族語單字卡"]
    )
    st.info("💡 提示：本系統專為教師設計，結合 PBL 與跨領域教學。")

# --- 🏠 首頁 ---
if mode == "🏠 首頁與理念":
    st.title("Mifoting 的智慧：海洋與土地的協定")
    st.subheader("阿美族漁獵文化跨領域教學系統")
    
    st.markdown("""
    ### 核心教學理念 (祖先的生存邏輯)
    本教案不只是介紹「如何捕魚」，而是解構阿美族生存背後的**底層智慧**：
    
    * **🌊 流動 (flow)**：順應季節，永續利用，符合**大自然永續的規則**。
    * **🕸️ 連結 (position)**：透過分享建立社會互助，強化**部落互助的力量**。
    * **🛡️ 規矩 (rule)**：禁忌 (paysin) 是古老的**風險極小化**演算法，體現**祖先的生存智慧**。
    
    ### 使用說明
    1. 選擇左側對應年級。
    2. 依照 6 節課流程進行教學。
    3. 使用「數位教具箱」進行互動演示。
    """)
    st.image("https://images.unsplash.com/photo-1544551763-46a013bb70d5?q=80&w=2070&auto=format&fit=crop", caption="順應自然的智慧 (示意圖)", use_column_width=True)

# --- 🟢🟡🔴 各年級教案展示 ---
elif "教案" in mode:
    grade_level = mode
    st.title(f"{grade_level} - 教學流程表")
    
    # 解決 KeyError 的穩健邏輯
    try:
        # 移除開頭的表情符號和空格，只留下 '低年級教案'
        clean_key = grade_level.split(" ", 1)[-1]
        lessons = LESSON_PLANS[clean_key]
    except KeyError:
        st.error(f"**系統錯誤！** 找不到教案內容。請檢查數據庫 Key: {clean_key}")
        st.stop()
    
    # 建立 Tabs
    tabs = st.tabs([f"第 {i+1} 節" for i in range(6)])
    
    for i, tab in enumerate(tabs):
        with tab:
            lesson = lessons[i]
            st.header(f"第 {i+1} 節：{lesson['Title']}")
            
            # 核心概念顯示
            if 'Core_Idea' in lesson:
                st.info(f"💡 **核心概念**：{lesson['Core_Idea']}")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**🎯 學習目標**\n\n{lesson['Obj']}")
                st.markdown(f"**⏱️ 建議時間**\n\n40 分鐘")
            with col2:
                st.markdown(f"**🎬 主要活動**\n\n{lesson['Act']}")
                
            st.markdown("---")
            st.write("📝 **教師備課筆記區** (可在此輸入重點):")
            st.text_area(f"L{i+1}_notes_{grade_level}", placeholder="例如：記得準備相關的圖文資料以輔助教學...", height=100)

# --- 🛠️ 數位教具箱 (互動功能核心) ---
elif mode == "🛠️ 數位教具箱":
    st.title("🛠️ 教師專用：數位教具箱")
    
    tool_choice = st.selectbox("選擇教具：", ["⚖️ 漁獲分配計算機 (高年級)", "📅 季節規矩轉盤 (中年級)", "🔇 聲量監測器 (低年級)"])
    
    # Tool 1: 分配計算機 (高年級 L5 - 部落互助的力量)
    if "分配計算機" in tool_choice:
        st.subheader("🐟 阿美族社會安全網 - 分配模擬器 (部落互助的力量)")
        st.markdown("此工具模擬傳統分配機制，確保部落整體生存的**冗餘性**。")
        
        total_catch = st.number_input("輸入今日總漁獲量 (公斤):", min_value=0, value=100)
        
        if st.button("開始分配"):
            # 模擬算法 (15% 敬老, 10% 弱勢, 75% 勞動者均分)
            elder_share = total_catch * 0.15
            welfare_share = total_catch * 0.10
            worker_share = total_catch - elder_share - welfare_share
            
            col1, col2, col3 = st.columns(3)
            col1.metric("敬老 (mato'asay)", f"{elder_share:.1f} kg", "優先分配 (智慧傳承)") 
            col2.metric("勞動者 (均分)", f"{worker_share:.1f} kg", "多勞多得 (能量輸出)")
            col3.metric("社會福利 (弱勢)", f"{welfare_share:.1f} kg", "照顧孤寡 (網絡韌性)")
            
            st.success("這就是『共享』的演化策略！犧牲單次最大化，換取群體長久生存。")

    # Tool 2: 季節規矩轉盤 (中年級 L1 - 大自然永續的規則)
    elif "季節規矩" in tool_choice:
        st.subheader("📅 漁獵季節行事曆 (大自然永續的規則)")
        st.markdown("此工具用於展示「不時不食」的 **資源流動管理**，避免資源耗竭。")
        
        season = st.select_slider("現在是幾月？", options=range(1, 13))
        
        if 4 <= season <= 9:
            st.success(f"{season}月：🌊 漁獵旺季！")
            st.write("活動：洄游魚類捕捉、準備豐年祭。")
            st.write("💡 核心：允許資源**高流動**，但需**遵守流量上限**。")
        else:
            st.warning(f"{season}月：⛔ 休養生息期")
            st.write("任務：讓魚類繁殖、修補漁具。")
            st.write("💡 核心：**限制流動**，進行**環境維護**，恢復資源秩序。")

    # Tool 3: 聲量監測 (低年級 L3 - 祖先的生存智慧)
    elif "聲量監測" in tool_choice:
        st.subheader("🔇 模擬聲量監測器 (祖先的生存智慧)")
        st.markdown("此工具訓練學生將吵鬧聲視為影響漁獵的 **噪聲**。")
        
        if st.button("開始監測"):
            with st.empty():
                for i in range(5, 0, -1):
                    st.write(f"倒數 {i} 秒，保持安靜...")
                    time.sleep(1)
                st.balloons()
                st.success("魚兒訊號清晰！大家都很安靜，生存率提高！")

# --- 📚 族語單字卡 ---
elif mode == "📚 族語單字卡":
    st.title("📚 阿美語漁獵單字卡")
    
    # 1. 初始化 session_state
    if "vocab_list" not in st.session_state:
        st.session_state["vocab_list"] = list(VOCABULARY.items())

    # 2. 按鈕邏輯
    if st.button("🔀 重新洗牌"):
        random.shuffle(st.session_state["vocab_list"])

    # 3. 顯示
    current_vocab = st.session_state["vocab_list"]
    
    col1, col2 = st.columns(2)
    half = len(current_vocab) // 2
    
    with col1:
        for word, meaning in current_vocab[:half]:
            with st.expander(f"❓ {word}"):
                st.markdown(f"### 👉 {meaning}")
                
    with col2:
        for word, meaning in current_vocab[half:]:
            with st.expander(f"❓ {word}"):
                st.markdown(f"### 👉 {meaning}")

# Footer
st.markdown("---")
st.caption("Designed with FP-CRF Logic | 阿美族漁獵文化教育專案")

