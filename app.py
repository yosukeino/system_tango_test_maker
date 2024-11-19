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
            /* 基本的なスタイルは同じ */
            /* 答えの表示用のスタイルを追加 */
            .answer {{
                color: #D63230;  /* 答えは赤系の色で表示 */
                font-weight: bold;
                margin-top: 5px;
                font-size: 14px;
            }}
            .answer-label {{
                color: #2c3e50;
                font-size: 12px;
                margin-right: 5px;
            }}
            /* 他のスタイルは create_test_pdf と同じ */
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
            answer = row['フレーズ']  # 完全な英文
            if test_config['test_type'] == 'partial':
                answer_format = row['英作問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
            else:
                answer_format = '___________________________'
        else:
            question = row['フレーズ']
            answer = row['訳']  # 日本語訳
            if test_config['test_type'] == 'partial':
                answer_format = row['和訳問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
            else:
                answer_format = '___________________________'
        
        html_template += f"""
                <div class="problem-row">
                    <div class="number">{i}</div>
                    <div class="question">
                        {question}
                        <div class="answer">
                            <span class="answer-label">答え:</span>{answer}
                        </div>
                    </div>
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

# テスト作成ボタンが押されたときの処理を修正
if st.button("テスト作成", type="primary"):
    # ... 既存のコード ...
    
    # 問題用HTMLの生成
    html_content = create_test_pdf(df, test_config)
    
    # 問題のダウンロードリンク
    b64 = base64.b64encode(html_content.encode()).decode()
    st.markdown(f'<a href="data:text/html;base64,{b64}" download="test.html">テストをダウンロード</a>', 
               unsafe_allow_html=True)
    
    # 答え付きバージョンの生成（チェックボックスがオンの場合）
    if create_answer:
        answer_html = create_answer_pdf(df, test_config)
        b64_answer = base64.b64encode(answer_html.encode()).decode()
        st.markdown(f'<a href="data:text/html;base64,{b64_answer}" download="test_answer.html">解答をダウンロード</a>', 
                   unsafe_allow_html=True)
    
    # プレビューの表示（問題のみ）
    st.markdown("### プレビュー")
    st.components.v1.html(html_content, height=600)
