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

            # 問題順序選択
            random_order = st.checkbox(
                "ランダムに問題を並べ替え",
                key="random_order"
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

            # 答え作成オプション
            create_answer = st.checkbox(
                "答えも合わせて作成する",
                key="create_answer"
            )

        # ボタンにユニークなkeyを追加
        if st.button("テスト作成", key="create_test_button", type="primary"):
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
            
            # 問題用HTMLの生成
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
