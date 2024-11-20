import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import random

# バージョン確認
st.write(st.__version__)

def create_test_pdf(df, test_config, test_number=None):
    """
    PDF出力用のHTMLを生成する関数
    """
    if test_number is None:
        date_str = datetime.now().strftime('%Y%m%d')
        test_number = f"{date_str}001"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 20px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 30px;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
            }}
            .title-section {{
                flex: 2;
            }}
            .test-title {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .test-info {{
                font-size: 14px;
                color: #666;
            }}
            .test-number {{
                color: #888;
                font-size: 12px;
            }}
            .name-section {{
                flex: 1;
                text-align: right;
            }}
            .name-field {{
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 12px 25px;
                min-width: 250px;
                min-height: 25px;
                position: relative;
                margin-top: 20px;
            }}
            .name-field:before {{
                content: '氏名';
                position: absolute;
                top: -10px;
                left: 10px;
                background: white;
                padding: 0 5px;
                color: #666;
                font-size: 14px;
            }}
            .problems-container {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .problem-row {{
                display: grid;
                grid-template-columns: 40px 0.8fr 1.2fr;
                gap: 20px;
                align-items: center;
            }}
            .number {{
                width: 32px;
                height: 32px;
                background: #f8f9fa;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: #2c3e50;
            }}
            .question {{
                font-size: 14px;
                padding: 8px 15px;
                background: #f8f9fa;
                border-radius: 4px;
                line-height: 1.5;
            }}
            .answer-space {{
                border-bottom: 2px solid #e0e0e0;
                min-height: 35px;
                font-size: 16px;
                padding: 5px 0;
            }}
            @media print {{
                body {{
                    padding: 0;
                }}
                .container {{
                    padding: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="title-section">
                    <div class="test-title">英単語テスト</div>
                    <div class="test-info">出題範囲: {test_config['start_num']}～{test_config['end_num']}</div>
                    <div class="test-number">テスト番号: {test_number}</div>
                </div>
                <div class="name-section">
                    <div class="name-field"></div>
                </div>
            </div>
            <div class="problems-container">
    """
    
    # 問題の生成
    selected_indices = test_config['selected_indices']
    for i, idx in enumerate(selected_indices, 1):
        row = df.loc[idx]
        
        # 問題文と解答欄の生成
        if test_config['direction'] == 'ja_to_en':
            question = row['訳']
            if test_config['test_type'] == 'partial':
                answer_format = row['英作問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
            else:
                answer_format = '___________________________'
        else:
            question = row['フレーズ']
            if test_config['test_type'] == 'partial':
                answer_format = row['和訳問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
            else:
                answer_format = '___________________________'
        
        html_template += f"""
                <div class="problem-row">
                    <div class="number">{i}</div>
                    <div class="question">{question}</div>
                    <div class="answer-space">{answer_format}</div>
                </div>
        """
    
    html_template += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def create_answer_pdf(df, test_config, test_number=None):
    """
    答え付きバージョンのHTMLを生成する関数
    """
    if test_number is None:
        date_str = datetime.now().strftime('%Y%m%d')
        test_number = f"{date_str}001"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 20px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 30px;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
            }}
            .title-section {{
                flex: 2;
            }}
            .test-title {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .test-info {{
                font-size: 14px;
                color: #666;
            }}
            .test-number {{
                color: #888;
                font-size: 12px;
            }}
            .problems-container {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .problem-row {{
                display: grid;
                grid-template-columns: 40px 1fr;
                gap: 20px;
                align-items: center;
            }}
            .number {{
                width: 32px;
                height: 32px;
                background: #f8f9fa;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: #2c3e50;
            }}
            .question {{
                font-size: 14px;
                padding: 8px 15px;
                background: #f8f9fa;
                border-radius: 4px;
                line-height: 1.5;
            }}
            .answer {{
                color: #D63230;
                font-weight: bold;
                margin-top: 5px;
                font-size: 14px;
            }}
            .answer-label {{
                color: #2c3e50;
                font-size: 12px;
                margin-right: 5px;
            }}
            @media print {{
                body {{
                    padding: 0;
                }}
                .container {{
                    padding: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="title-section">
                    <div class="test-title">英単語テスト（解答）</div>
                    <div class="test-info">出題範囲: {test_config['start_num']}～{test_config['end_num']}</div>
                    <div class="test-number">テスト番号: {test_number}</div>
                </div>
            </div>
            <div class="problems-container">
    """
    
    # 問題と答えの生成
    selected_indices = test_config['selected_indices']
    for i, idx in enumerate(selected_indices, 1):
        row = df.loc[idx]
        
        if test_config['direction'] == 'ja_to_en':
            question = row['訳']
            answer = row['フレーズ']
        else:
            question = row['フレーズ']
            answer = row['訳']
        
        html_template += f"""
                <div class="problem-row">
                    <div class="number">{i}</div>
                    <div class="question">
                        {question}
                        <div class="answer">
                            <span class="answer-label">答え:</span>{answer}
                        </div>
                    </div>
                </div>
        """
    
    html_template += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def init_app():
    """アプリケーションの初期化"""
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

            # 答え作成オプション
            create_answer = st.checkbox(
                "答えも合わせて作成する",
                key="create_answer"
            )
        
        # テスト作成ボタン
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("テスト作成", key="create_test_button", use_container_width=True):
                # 選択された範囲から問題のインデックスを取得
                available_indices = list(range(range_values[0], range_values[1] + 1))
                
                if len(available_indices) > num_questions:
                    # ランダムに問題を選択
                    selected_indices = random.sample(available_indices, num_questions)
                else:
                    selected_indices = available_indices

                if random_order:
                    random.shuffle(selected_indices)
                else:
                    selected_indices.sort()
                
                # テスト設定の作成
                test_config = {
                    'start_num': range_values[0],
                    'end_num': range_values[1],
                    'selected_indices': selected_indices,
                    'direction': direction[1],
                    'test_type': test_type[1]
                }
                
                # HTMLの生成
                html_content = create_test_pdf(df, test_config)
                
                # 問題のダウンロードリンク
                b64 = base64.b64encode(html_content.encode()).decode()
                st.markdown(
                    f'<a href="data:text/html;base64,{b64}" download="test.html">テストをダウンロード</a>', 
                    unsafe_allow_html=True
                )
                
                # 答え付きバージョンの生成（チェックボックスがオンの場合）
                if create_answer:
                    answer_html = create_answer_pdf(df, test_config)
                    b64_answer = base64.b64encode(answer_html.encode()).decode()
                    st.markdown(
                        f'<a href="data:text/html;base64,{b64_answer}" download="test_answer.html">解答をダウンロード</a>', 
                        unsafe_allow_html=True
                    )
                
                # プレビューの表示（問題のみ）
                st.markdown("### プレビュー")
                st.components.v1.html(html_content, height=600)
    
    else:
        st.error("システムエラー: 管理者に連絡してください")

if __name__ == "__main__":
    create_test_maker_app()