# streamlit 라이브러리 호출
import streamlit as st

# --- 페이지 설정 ---
# st.set_page_config는 반드시 스크립트의 첫 Streamlit 명령어로 실행되어야 합니다.
st.set_page_config(
    page_title="🎨 MBTI 학습 유형 진단",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- 상태 초기화 함수 ---
# '다시하기' 버튼을 누르거나 페이지가 처음 로드될 때 호출됩니다.
def initialize_state():
    st.session_state.clear() # 모든 세션 상태를 초기화
    st.session_state.current_page = 'home'
    st.session_state.mbti_result = None
    st.session_state.user_answers = {}

# --- 데이터 정의 ---
# MBTI 문항 데이터 (이전과 동일)
questions = [
    {"question": "1. 다른 사람들과 함께 어울리는 것이 즐겁다.","options": ["그렇다", "아니다"],"dimension": ("E", "I")},
    {"question": "2. 새로운 아이디어나 이론에 대해 깊이 생각하는 것을 좋아한다.","options": ["그렇다", "아니다"],"dimension": ("N", "S")},
    {"question": "3. 결정을 내릴 때 논리적이고 객관적인 사실을 중요하게 생각한다.","options": ["그렇다", "아니다"],"dimension": ("T", "F")},
    {"question": "4. 계획을 세우고 체계적으로 일을 진행하는 것을 선호한다.","options": ["그렇다", "아니다"],"dimension": ("J", "P")},
    {"question": "5. 처음 만나는 사람에게 먼저 다가가 대화하는 것이 편하다.","options": ["그렇다", "아니다"],"dimension": ("E", "I")},
    {"question": "6. 경험을 통해 배우는 것보다 개념과 원리를 이해하는 것이 더 중요하다.","options": ["그렇다", "아니다"],"dimension": ("N", "S")},
    {"question": "7. 다른 사람의 감정에 공감하고, 그들의 입장에서 생각하려 노력한다.","options": ["아니다", "그렇다"],"dimension": ("T", "F")},
    {"question": "8. 즉흥적으로 상황에 맞춰 행동하는 것을 즐긴다.","options": ["아니다", "그렇다"],"dimension": ("J", "P")}
]
# MBTI 유형별 학습 스타일 설명 (이전과 동일)
learning_styles = {
    "ISTJ": "**소금형 🧂:** 사실에 근거하여 체계적으로 학습하며, 꾸준하고 신중한 노력을 통해 지식을 쌓아갑니다. 명확한 목표와 계획을 선호합니다.",
    "ISFJ": "**권력형 💪:** 다른 사람들을 돕고 지원하면서 학습할 때 가장 효과적입니다. 실용적이고 구체적인 정보를 바탕으로 차근차근 학습하는 것을 좋아합니다.",
    "INFJ": "**예언자형 🔮:** 깊은 통찰력과 직관을 통해 복잡한 개념을 이해합니다. 자신만의 비전과 가치를 학습에 연결시키려는 경향이 있습니다.",
    "INTJ": "**과학자형 🔬:** 논리적이고 분석적인 사고를 바탕으로 시스템 전체를 이해하려 합니다. 독립적으로 학습하며, 효율성과 독창성을 중시합니다.",
    "ISTP": "**백과사전형 📖:** 직접 경험하고 문제를 해결하며 배우는 것을 선호합니다. 실용적인 기술과 원리에 관심이 많으며, 유연한 사고를 가집니다.",
    "ISFP": "**성인군자형 😇:** 조화로운 환경에서 자신의 가치와 일치하는 내용을 학습할 때 동기부여를 받습니다. 관찰과 실습을 통해 부드럽게 지식을 습득합니다.",
    "INFP": "**잔다르크형 👩‍🌾:** 자신의 이상과 가치를 실현할 수 있는 학습에 몰두합니다. 창의적이고 상상력이 풍부하며, 개별화된 학습 환경을 선호합니다.",
    "INTP": "**아이디어형💡:** 지적 호기심이 강하며, 논리적 분석과 추상적인 개념 탐구를 즐깁니다. 복잡한 이론을 이해하고 새로운 아이디어를 만들어내는 데 능숙합니다.",
    "ESTP": "**활동가형 🏃:** 직접 부딪히고 경험하며 배우는 실천가입니다. 역동적이고 재미있는 학습 환경에서 가장 높은 효율을 보이며, 문제 해결에 강합니다.",
    "ESFP": "**사교형 🤝:** 사람들과 교류하고 협력하며 배우는 것을 즐깁니다. 긍정적이고 활기찬 분위기에서 실용적인 지식을 습득하는 것을 선호합니다.",
    "ENFP": "**스파크형 ✨:** 열정적으로 새로운 가능성을 탐색하며 배웁니다. 창의적인 아이디어를 자유롭게 탐구하고, 다른 사람들과 영감을 주고받는 것을 좋아합니다.",
    "ENTP": "**발명가형 👨‍🔬:** 지적인 도전을 즐기며, 논쟁과 토론을 통해 아이디어를 발전시킵니다. 기존의 방식에 의문을 제기하고 새로운 해결책을 찾는 데 뛰어납니다.",
    "ESTJ": "**사업가형 🏢:** 명확한 목표와 구조화된 계획에 따라 학습합니다. 실용적이고 효율적인 방법을 선호하며, 학습한 내용을 현실에 적용하는 능력이 뛰어납니다.",
    "ESFJ": "**친선도모형 🤗:** 다른 사람들과의 관계 속에서 협력하며 배우는 것을 중요하게 생각합니다. 조화로운 분위기에서 실질적인 도움을 주고받으며 성장합니다.",
    "ENFJ": "**언변능숙형 🎤:** 다른 사람들을 이끌고 영감을 주며 함께 성장하는 학습을 선호합니다. 사람들의 잠재력을 이끌어내는 데 열정적이며, 교육적인 역할을 즐깁니다.",
    "ENTJ": "**지도자형 👑:** 장기적인 비전을 세우고, 목표 달성을 위해 전략적으로 학습합니다. 도전적인 과제를 해결하며 리더십을 발휘할 때 가장 크게 성장합니다."
}

# --- 앱 UI 및 로직 ---

# 페이지가 처음 로드되었는지 확인
if 'current_page' not in st.session_state:
    initialize_state()

# --- 제목 및 설명 ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://em-content.zobj.net/source/samsung/380/brain_1f9e0.png", width=100)
with col2:
    st.title("MBTI 학습 유형 진단")
    st.caption("나에게 꼭 맞는 학습 스타일을 찾아보세요!")

st.divider()

# --- 결과 표시 ---
# 진단 결과가 세션 상태에 저장되어 있는 경우
if st.session_state.mbti_result:
    result_mbti = st.session_state.mbti_result

    # 결과를 강조하는 컨테이너
    with st.container(border=True):
        st.subheader(f"🎉 당신의 유형은 **'{result_mbti}'** 입니다!", anchor=False)
        st.write(learning_styles.get(result_mbti, "결과를 분석 중입니다..."))

    # 다시하기 버튼
    if st.button("🔄️ 다시하기", use_container_width=True):
        initialize_state()
        st.rerun() # 페이지를 새로고침하여 초기 상태로 돌아감

# --- 설문 시작 ---
# 아직 진단을 시작하지 않은 경우
else:
    # 설문지를 감싸는 컨테이너
    with st.container(border=True):
        st.info("💡 각 문항에 대해 솔직하게 답변해주세요.")
        
        # 폼(Form) 생성
        with st.form("mbti_form"):
            # 각 문항에 대해 라디오 버튼 생성
            for i, item in enumerate(questions):
                st.radio(
                    label=f'**{item["question"]}**',
                    options=item["options"],
                    key=f"q_{i}",
                    horizontal=True,
                )
            
            # 제출 버튼
            submitted = st.form_submit_button("✔️ 결과 보기", use_container_width=True, type="primary")

    # 제출 버튼을 눌렀을 때 실행될 로직
    if submitted:
        # MBTI 점수 계산
        scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
        for i, item in enumerate(questions):
            # st.session_state에서 직접 답변을 가져옴
            user_answer = st.session_state[f"q_{i}"]
            option_index = item["options"].index(user_answer)
            dimension = item["dimension"][option_index]
            scores[dimension] += 1

        # 최종 MBTI 유형 결정
        mbti = ""
        mbti += "E" if scores["E"] >= scores["I"] else "I"
        mbti += "N" if scores["N"] >= scores["S"] else "S"
        mbti += "T" if scores["T"] >= scores["F"] else "F"
        mbti += "J" if scores["J"] >= scores["P"] else "P"
        
        # 결과를 세션 상태에 저장
        st.session_state.mbti_result = mbti
        
        # 결과 제출 시 축하 효과
        st.balloons()
        
        # 페이지를 새로고침하여 결과 화면을 표시
        st.rerun()