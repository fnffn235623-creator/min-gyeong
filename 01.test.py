import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="특수검진 대상자 조회 시스템", layout="centered")

st.title("🔍 특수검진 대상자 조회")
st.info("사원번호를 입력하여 본인의 검진 대상 여부를 확인하세요.")

# --- 관리자 구역 (사이드바) ---
with st.sidebar:
    st.header("⚙️ 관리자 설정")
    admin_password = st.text_input("관리자 비밀번호", type="password")
    
    # 비밀번호 설정 (예: admin1234)
    if admin_password == "admin1234":
        st.success("관리자 인증 성공")
        uploaded_file = st.file_uploader("데이터 엑셀 업로드 (사번, 성명, 부서, 대상여부 포함)", type=["xlsx"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.session_state['data'] = df
            st.write("✅ 데이터 업로드 완료!")
            st.dataframe(df, use_container_width=True) # 관리자용 전체 보기
    elif admin_password:
        st.error("비밀번호가 틀렸습니다.")

# --- 사용자 조회 구역 ---
st.divider()

if 'data' in st.session_state:
    search_id = st.text_input("사원번호를 입력하세요 (예: 2024001)", placeholder="사번 입력")

    if st.button("조회하기"):
        df = st.session_state['data']
        # 사번 열 이름은 '사번' 또는 '사원번호'로 가정 (엑셀 양식에 맞게 수정 가능)
        id_col = '사번' if '사번' in df.columns else '사원번호'
        
        # 데이터 검색 (타입 불일치 방지를 위해 문자열로 변환 후 비교)
        result = df[df[id_col].astype(str) == search_id]

        if not result.empty:
            # 개인 정보 추출
            name = result.iloc[0]['성명']
            dept = result.iloc[0]['부서']
            is_target = result.iloc[0]['대상여부'] # O 또는 X

            # 결과 화면 출력
            col1, col2, col3 = st.columns(3)
            col1.metric("성명", name)
            col2.metric("부서", dept)
            col3.metric("검진 대상 여부", is_target)

            if is_target == "O":
                st.warning(f"📢 {name}님은 올해 특수검진 대상자입니다. 일정을 확인해주세요.")
            else:
                st.success(f"✅ {name}님은 대상자가 아닙니다.")
        else:
            st.error("해당 사번으로 조회된 정보가 없습니다. 관리자에게 문의하세요.")
else:
    st.warning("⚠️ 현재 조회 가능한 데이터가 없습니다. 관리자가 엑셀 파일을 먼저 업로드해야 합니다.")



        