import streamlit as st
import pandas as pd
from datetime import datetime
import base64

def init_app():
    """アプリケーションの初期化"""
    # CSVファイルの読み込み（サーバー上の固定ファイル）
    try:
        df = pd.read_csv('list.csv', encoding='shift-jis')
        return df
    except Exception as e:
        st.error(f"データファイルの読み込みに失敗しました: {e}")
        return None

def create_test_maker_app():
    st.title("英単語テストメーカー")
    
    # データの読み込み
    df = init_app()
    
    if df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            # 問題範囲選択
            max_range = len(df)
            range_values = st.slider(
                "出題範囲を選択",
                1, max_range, (1, 20),
                key="range_slider"
            )
            
            # 出題数選択
            num_questions = st.number_input(
                "出題数",
                min_value=1,
                max_value=50,
                value=20,
                key="num_questions"
            )
        
        with col2:
            # 問題形式選択
            direction = st.radio(
                "問題形式",
                options=[
                    ('日本語→英語', 'ja_to_en'),
                    ('英語→日本語', 'en_to_ja')
                ],
                format_func=lambda x: x[0],
                key="direction"
            )
            
            # テストタイプ選択
            test_type = st.radio(
                "解答形式",
                options=[
                    ('一部空欄', 'partial'),
                    ('全文記入', 'full')
                ],
                format_func=lambda x: x[0],
                key="test_type"
            )
            
            # 問題順序選択
            random_order = st.checkbox(
                "ランダムに問題を並べ替え",
                key="random_order"
            )
        
        if st.button("テスト作成", type="primary"):
            # テスト設定の作成
            test_config = {
                'start_num': range_values[0],
                'end_num': range_values[1],
                'selected_indices': range(range_values[0], range_values[1] + 1),
                'direction': direction[1],
                'test_type': test_type[1]
            }
            
            # HTMLの生成（既存の create_test_pdf 関数を使用）
            html_content = create_test_pdf(df, test_config)
            
            # HTMLをダウンロード可能な形式に変換
            b64 = base64.b64encode(html_content.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="test.html">テストをダウンロード</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # プレビューの表示
            st.markdown("### プレビュー")
            st.components.v1.html(html_content, height=600)
    
    else:
        st.error("システムエラー: 管理者に連絡してください")

if __name__ == "__main__":
    create_test_maker_app()
