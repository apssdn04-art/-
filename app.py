import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="한글 맞춤법·띄어쓰기 도우미 '마띠'",
    page_icon="🤖",
    layout="centered"
)

# 커스텀 CSS 적용 (깔끔한 UI 및 말풍선 디자인)
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #3B82F6;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown('<p class="main-title">🤖 한글 맞춤법·띄어쓰기 도우미 「마띠」</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">교과서 및 한글 맞춤법 규정을 바탕으로 궁금증을 명쾌하게 해결해 드려요!</p>', unsafe_allow_html=True)

# 규정 지식 베이스 사전 (문서 내용 기반)
KNOWLEDGE_BASE = {
    "되/돼": """### 💡 **되 / 돼** 구분법
- **되-**: '되다'의 어간으로, 홀로 쓸 수 없으며 뒤에 어미가 붙습니다. (예: 시간 안 **되**나요?, 시간 **되**지)
- **돼**: '되어'의 준말입니다. 문맥에 **'되어'**를 넣어 어색하지 않으면 '돼'로 쓸 수 있습니다.
  - *예시*: 그 날 시간 **돼**? (시간 되어?) / 오늘이 빨리 집에 가서 숙제를 해야 **돼**. (해야 되어 O)""",
    
    "안/않": """### 💡 **안 / 않** 구분법
- **안**: 부사 '아니'의 준말이며, 뒤에 오는 서술어와 **띄어** 씁니다. ('아니'를 넣어 말이 되면 '안')
  - *예시*: 생각보다 **안** 어렵네 (아니 어렵네 O)
- **않-**: '아니하-'의 준말입니다. ('아니하'를 넣어 말이 되면 '않')
  - *예시*: 생각보다 어렵지 **않**네 (어렵지 아니하네 O)""",
    
    "웬/왠": """### 💡 **웬 / 왠** 구분법
- **웬**: '어찌 된', '어떠한'의 뜻을 지닌 관형사로, 뒤에 오는 체언과 **띄어** 씁니다.
  - *예시*: **웬** 떡이냐, **웬**만하면 공부 좀 하지.
- **왠**: '왜인지'의 준말로, **'왠지'**라는 형태로만 주로 쓰이고 '왠' 단독으로는 쓰이지 않습니다.
  - *예시*: 오늘은 **왠지** 공부가 잘 된다.""",
    
    "데/대": """### 💡 **-데 / -대** 구분법
- **-데**: 과거에 직접 **경험하여 알게 된 사실**을 현재로 옮겨와 말할 때 씁니다.
  - *예시*: 걔가 아주 말 잘하**데**
- **-대**: **'-다고 해'의 준말**로, 다른 사람한테 들은 사실을 전달할 때 씁니다.
  - *예시*: 경수가 그 영화 재밌**대**""",
    
    "며칠/몇일": """### 💡 **며칠** 표기 규정
- **바른 표기**: **며칠** (‘몇 일’은 틀린 표기입니다.)
- **이유**: '몇 일'로 적으면 [며딜]로 소리가 나야 하지만, 실제 발음은 [며칠]입니다. '몇'과 '일(日)'의 결합으로 분석되지 않고 소리 나는 대로 '며칠'로 적습니다.""",
    
    "띄어쓰기(만큼/대로/뿐)": """### 💡 **의존 명사 vs 조사 띄어쓰기**
용언의 관형사형 뒤에는 띄어 쓰고, 체언(명사 등) 뒤에는 붙여 씁니다.
1. **만큼**
   - 조사(붙임): 너**만큼** 공부한 사람 (체언 뒤)
   - 의존 명사(띄어): 노력한 **만큼** 보상을 받으니 (관형사형 뒤)
2. **대로**
   - 조사(붙임): 법**대로**, 약속**대로** (체언 뒤)
   - 의존 명사(띄어): 아는 **대로** 말해 봐 (관형사형 뒤)
3. **뿐**
   - 조사(붙임): 셋**뿐**이다, 남자**뿐**이다 (체언 뒤)
   - 의존 명사(띄어): 웃을 **뿐**이다 (관형사형 뒤)""",

    "총칙": """### 💡 **한글 맞춤법 제1항 (기본 원리)**
- **표준어를 소리대로 적되**: 발음에 따라 적는 원칙입니다. (예: [달리다] -> 달리다)
- **어법에 맞도록 함을 원칙으로 한다**: 뜻을 파악하기 쉽도록 각 형태소의 본모양을 밝혀 적는 원칙입니다. (예: [꼬치], [꼰만]으로 소리 나더라도 형태소를 밝혀 '꽃이', '꽃만'으로 적음)"""
}

# 세션 스테이트를 이용한 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 저는 맞춤법과 띄어쓰기 도우미 **'마띠'**입니다. 평소 헷갈렸던 표현이나 규정이 있다면 무엇이든 물어보세요! 😊"}
    ]

# 예시 질문 버튼 영역 (사이드바 또는 상단)
st.markdown("#### 📌 자주 묻는 질문 바로가기")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("되 vs 돼"):
        st.session_state.messages.append({"role": "user", "content": "'되'와 '돼'는 어떻게 구분하나요?"})
        st.session_state.messages.append({"role": "assistant", "content": KNOWLEDGE_BASE["되/돼"]})
        st.rerun()
with col2:
    if st.button("안 vs 않"):
        st.session_state.messages.append({"role": "user", "content": "'안'과 '않'의 차이를 알려주세요."})
        st.session_state.messages.append({"role": "assistant", "content": KNOWLEDGE_BASE["안/않"]})
        st.rerun()
with col3:
    if st.button("웬 vs 왠"):
        st.session_state.messages.append({"role": "user", "content": "'웬'과 '왠'은 언제 쓰나요?"})
        st.session_state.messages.append({"role": "assistant", "content": KNOWLEDGE_BASE["웬/왠"]})
        st.rerun()
with col4:
    if st.button("며칠 vs 몇일"):
        st.session_state.messages.append({"role": "user", "content": "'며칠'이 맞아요, '몇일'이 맞아요?"})
        st.session_state.messages.append({"role": "assistant", "content": KNOWLEDGE_BASE["며칠/몇일"]})
        st.rerun()

st.markdown("---")

# 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
user_query = st.chat_input("질문이나 헷갈리는 문장을 입력해 주세요 (예: '금방'과 '방금 차이', '만큼 띄어쓰기')")

if user_query:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 답변 생성 로직 (키워드 매칭 및 안내)
    query_lower = user_query.lower()
    
    if "되" in query_lower and "돼" in query_lower:
        answer = KNOWLEDGE_BASE["되/돼"]
    elif "안" in query_lower and "않" in query_lower:
        answer = KNOWLEDGE_BASE["안/않"]
    elif "웬" in query_lower or "왠" in query_lower:
        answer = KNOWLEDGE_BASE["웬/왠"]
    elif "데" in query_lower and "대" in query_lower:
        answer = KNOWLEDGE_BASE["데/대"]
    elif "며칠" in query_lower or "몇일" in query_lower:
        answer = KNOWLEDGE_BASE["며칠/몇일"]
    elif "띄어쓰기" in query_lower or "만큼" in query_lower or "대로" in query_lower or "뿐" in query_lower:
        answer = KNOWLEDGE_BASE["띄어쓰기(만큼/대로/뿐)"]
    elif "제1항" in query_lower or "총칙" in query_lower or "원리" in query_lower:
        answer = KNOWLEDGE_BASE["총칙"]
    else:
        answer = f"""### 📝 마띠의 답변입니다
입력하신 **"{user_query}"**에 대한 답변입니다.

첨부된 한글 맞춤법 및 띄어쓰기 교과서 규정에 따르면, 표준어는 **소리대로 적는 것**과 **어법에 맞도록 형태소의 본모양을 밝혀 적는 것**을 원칙으로 합니다. 

질문하신 내용이 특정 단어나 띄어쓰기 규정(예: *되/돼, 안/않, 웬/왠, 며칠, 만큼, 대로*)과 관련 있다면 해당 키워드를 포함해서 다시 질문해 주시면 규정에 근거해 더 정확하게 설명해 드릴게요! ✨"""

    # 어시스턴트 메시지 추가
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)