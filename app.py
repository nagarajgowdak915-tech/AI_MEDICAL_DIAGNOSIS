import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import shap
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from chatbot import get_chatbot_response
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="AI Medical Dashboard", page_icon="🩺", layout="wide")

st.markdown("""
<style>
/* Main page: force readable dark text on the light background */
.stApp, [data-testid="stAppViewContainer"] {background:#f4f7fb;}
[data-testid="stAppViewContainer"] .main,
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main label,
[data-testid="stAppViewContainer"] .main [data-testid="stMarkdownContainer"],
[data-testid="stAppViewContainer"] .main [data-testid="stHeader"],
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main h4,
[data-testid="stAppViewContainer"] .main .stCaption,
[data-testid="stAppViewContainer"] .main [data-testid="stCaptionContainer"] {
    color:#18365e !important;
}
/* Sidebar keeps its dark-blue theme and white text */
[data-testid="stSidebar"] {background:linear-gradient(180deg,#08264a,#103d70);}
[data-testid="stSidebar"] * {color:#f4f8ff !important;}
/* Light, readable input fields */
[data-testid="stAppViewContainer"] .main input,
[data-testid="stAppViewContainer"] .main textarea {
    background:#ffffff !important;
    color:#18365e !important;
    border-color:#cbd8e8 !important;
}
[data-testid="stAppViewContainer"] .main [data-baseweb="select"] > div {
    background:#ffffff !important;
    color:#18365e !important;
    border-color:#cbd8e8 !important;
}
[data-testid="stAppViewContainer"] .main [data-baseweb="select"] input,
[data-testid="stAppViewContainer"] .main [data-baseweb="select"] span {
    color:#18365e !important;
}
div[data-testid="stMetric"] {
    background:white;border:1px solid #e1eaf5;padding:15px;border-radius:14px;
    box-shadow:0 3px 12px #15385f0d;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color:#18365e !important;
}
.main-title {color:#102f59;font-size:2rem;font-weight:800;}
.subtitle {color:#5e7290;margin-bottom:1.1rem;}
/* Keep button labels readable */
[data-testid="stAppViewContainer"] .main button {color:#ffffff;}
</style>
""", unsafe_allow_html=True)

FEATURES = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]
COLUMNS = FEATURES + ["Outcome"]
DEFAULTS = {"Pregnancies":2,"Glucose":120,"BloodPressure":70,"SkinThickness":20,"Insulin":80,"BMI":28.0,"DiabetesPedigreeFunction":0.5,"Age":30}
LANGUAGES = ["English","Kannada","Hindi","Tamil","Telugu"]
LANGUAGE_CODES = {"English":"en","Kannada":"kn","Hindi":"hi","Tamil":"ta","Telugu":"te"}

@st.cache_data
def load_data():
    df = pd.read_csv("diabetes.csv", header=None)
    if df.shape[1] == 9:
        df.columns = COLUMNS
    else:
        df = pd.read_csv("diabetes.csv")
        df.columns = [str(c).strip() for c in df.columns]
    return df

@st.cache_resource
def train_model(data):
    X, y = data[FEATURES].copy(), data["Outcome"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(X_train, y_train)
    scaler = model.named_steps["standardscaler"]
    explainer = shap.LinearExplainer(model.named_steps["logisticregression"], scaler.transform(X_train))
    return model, scaler, explainer, X_test, y_test, model.score(X_test, y_test)

try:
    data = load_data()
    if "Outcome" not in data.columns or not set(FEATURES).issubset(data.columns):
        st.error("Dataset columns do not match the expected diabetes dataset.")
        st.stop()
    model, scaler, explainer, X_test, y_test, accuracy = train_model(data)
except FileNotFoundError:
    st.error("Could not find diabetes.csv. Keep it in the same folder as app.py.")
    st.stop()
except Exception as error:
    st.error(f"Could not load/train model: {error}")
    st.stop()

with st.sidebar:
    st.markdown("# 💙 AI Medical")
    st.caption("Smarter Health, Brighter Future")
    st.markdown("---")
    page = st.radio("NAVIGATION", ["Dashboard","Diabetes Prediction","SHAP Explanation","Dataset Analytics","Model Performance","Chatbot"])
    st.markdown("---")
    st.markdown("🛡️ **Your health data matters**")
    st.caption("Educational prototype only—not a validated diagnostic system.")

head_left, head_right = st.columns([5,1])
with head_left:
    st.markdown('<div class="main-title">Explainable AI for Medical Diagnosis Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-powered insights for better healthcare decisions</div>', unsafe_allow_html=True)
with head_right:
    selected_language = st.selectbox("Language", LANGUAGES, key="global_language")

positive_count = int((data["Outcome"] == 1).sum())
positive_pct = positive_count / max(len(data), 1) * 100

def chart_style(fig, height=320):
    fig.update_layout(height=height, paper_bgcolor="white", plot_bgcolor="white",
        font=dict(color="#18365e", family="Arial"), margin=dict(l=15,r=15,t=55,b=25), legend_title_text="")
    fig.update_xaxes(showgrid=True, gridcolor="#e9eff7", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#e9eff7", zeroline=False)
    return fig

def prediction_form():
    st.markdown("### 🩺 Diabetes Prediction")
    st.caption("Enter sample measurements and run the educational model.")
    with st.form("prediction_form"):
        cols = st.columns(4)
        entered = {}
        for i, feature in enumerate(FEATURES):
            with cols[i % 4]:
                entered[feature] = st.number_input(feature, min_value=0.0, value=float(DEFAULTS[feature]), step=1.0, key=f"pred_{feature}")
        submitted = st.form_submit_button("🔍 Run Prediction", type="primary", use_container_width=True)
    if submitted:
        patient = pd.DataFrame([entered], columns=FEATURES)
        st.session_state["last_patient"] = entered
        st.session_state["last_prediction"] = int(model.predict(patient)[0])
        st.session_state["last_probability"] = float(model.predict_proba(patient)[0][1])
    if "last_prediction" in st.session_state:
        pred, prob = st.session_state["last_prediction"], st.session_state["last_probability"]
        if pred == 1:
            st.warning(f"Model output: Outcome 1 (positive class) · Model probability for Outcome 1: {prob:.1%}")
        else:
            st.success(f"Model output: Outcome 0 (negative class) · Model probability for Outcome 1: {prob:.1%}")
        st.info("This is an educational model output, not a medical diagnosis or validated personal risk estimate. Consult a qualified healthcare professional for testing.")
        if st.button("Show SHAP explanation"):
            patient = pd.DataFrame([st.session_state["last_patient"]], columns=FEATURES)
            scaled = pd.DataFrame(scaler.transform(patient), columns=FEATURES)
            try:
                explanation = explainer(scaled)
                fig, ax = plt.subplots(figsize=(8,4))
                shap.plots.bar(explanation, show=False)
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.warning(f"Could not display explanation: {e}")

if page == "Dashboard":
    a,b,c,d = st.columns(4)
    a.metric("Total Records", f"{len(data):,}", "Dataset samples")
    b.metric("Diabetes-positive", f"{positive_count:,}", f"{positive_pct:.1f}% of records")
    c.metric("Test Accuracy", f"{accuracy:.1%}", "Logistic Regression")
    d.metric("Input Features", len(FEATURES), "Health parameters")
    left, middle, right = st.columns([1.15,1.05,0.95], gap="medium")
    plot_data = data.copy()
    plot_data["Outcome label"] = plot_data["Outcome"].map({0:"Outcome 0",1:"Outcome 1"})
    with left:
        st.markdown("#### Health Metrics Overview")
        x_feature = st.selectbox("X-axis", FEATURES, index=1, key="dash_x")
        y_feature = st.selectbox("Y-axis", FEATURES, index=5, key="dash_y")
        fig = px.scatter(plot_data, x=x_feature, y=y_feature, color="Outcome label",
            color_discrete_map={"Outcome 0":"#1478ed","Outcome 1":"#f34f78"}, opacity=.72,
            title=f"{x_feature} vs {y_feature}", hover_data=FEATURES)
        st.plotly_chart(chart_style(fig,350), use_container_width=True)
    with middle:
        st.markdown("#### Feature Distribution")
        feature = st.selectbox("Select feature", FEATURES, index=1, key="dash_dist")
        fig = px.histogram(plot_data, x=feature, color="Outcome label", barmode="overlay", opacity=.72,
            marginal="box", color_discrete_map={"Outcome 0":"#1478ed","Outcome 1":"#f34f78"}, title=f"{feature} distribution")
        st.plotly_chart(chart_style(fig,350), use_container_width=True)
        fig = px.pie(data, names="Outcome", hole=.62, color="Outcome",
            color_discrete_map={0:"#1478ed",1:"#f34f78"}, title="Outcome class balance")
        st.plotly_chart(chart_style(fig,250), use_container_width=True)
    with right:
        st.markdown("#### Quick Prediction")
        glucose = st.number_input("Glucose", min_value=0.0, value=120.0, key="quick_glucose")
        bmi = st.number_input("BMI", min_value=0.0, value=28.0, key="quick_bmi")
        age = st.number_input("Age", min_value=1.0, value=30.0, key="quick_age")
        if st.button("Estimate with model", type="primary", use_container_width=True):
            sample = pd.DataFrame([[2,glucose,70,20,80,bmi,.5,age]], columns=FEATURES)
            st.session_state["quick_pred"] = int(model.predict(sample)[0])
            st.session_state["quick_prob"] = float(model.predict_proba(sample)[0][1])
        if "quick_pred" in st.session_state:
            st.write("Model output:", "Outcome 1" if st.session_state["quick_pred"] else "Outcome 0")
            st.metric("Model probability for Outcome 1", f'{st.session_state["quick_prob"]:.1%}')
            st.caption("Educational only—not a diagnosis.")
        st.markdown("---")
        st.markdown("#### Health Information")
        st.write("• Discuss screening with a healthcare professional.")
        st.write("• A model output cannot diagnose diabetes.")
        st.write("• Dataset patterns may not generalize to everyone.")

elif page == "Diabetes Prediction":
    prediction_form()

elif page == "SHAP Explanation":
    st.markdown("### 🧠 SHAP Explanation")
    st.write("Feature influence explains the model output, not medical causation.")
    patient_values = st.session_state.get("last_patient", DEFAULTS)
    try:
        patient = pd.DataFrame([patient_values], columns=FEATURES)
        scaled = pd.DataFrame(scaler.transform(patient), columns=FEATURES)
        explanation = explainer(scaled)
        fig, ax = plt.subplots(figsize=(8,4))
        shap.plots.bar(explanation, show=False)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.warning(f"SHAP chart could not be displayed: {e}")

elif page == "Dataset Analytics":
    st.markdown("### 📈 Dataset Analytics")
    left,right = st.columns(2)
    with left:
        feature = st.selectbox("Choose a feature", FEATURES)
        fig = px.histogram(data, x=feature, color="Outcome", marginal="box", barmode="overlay",
            title=f"{feature} distribution by outcome", color_discrete_map={0:"#1478ed",1:"#f34f78"})
        st.plotly_chart(chart_style(fig), use_container_width=True)
    with right:
        corr = data[FEATURES+["Outcome"]].corr(numeric_only=True)
        fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="Blues", title="Feature correlation matrix")
        st.plotly_chart(chart_style(fig,420), use_container_width=True)
    filter_choice = st.selectbox("Filter dataset", ["All records","Outcome 1","Outcome 0"])
    filtered = data if filter_choice == "All records" else data[data["Outcome"] == int(filter_choice[-1])]
    st.dataframe(filtered, use_container_width=True, height=300)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
        file_name="diabetes_dataset_filtered.csv", mime="text/csv")

elif page == "Model Performance":
    from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score
    st.markdown("### 📊 Model Performance")
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:,1]
    a,b,c = st.columns(3)
    a.metric("Accuracy", f"{accuracy:.1%}")
    b.metric("ROC-AUC", f"{roc_auc_score(y_test,prob):.3f}")
    c.metric("Test records", len(y_test))
    left,right = st.columns(2)
    with left:
        cm = confusion_matrix(y_test,pred)
        fig = px.imshow(cm, text_auto=True, x=["Predicted 0","Predicted 1"], y=["Actual 0","Actual 1"],
            color_continuous_scale="Blues", title="Confusion Matrix")
        st.plotly_chart(chart_style(fig,360), use_container_width=True)
    with right:
        fpr,tpr,_ = roc_curve(y_test,prob)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr,y=tpr,mode="lines",name="Logistic Regression"))
        fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",name="Baseline",line=dict(dash="dash")))
        fig.update_layout(title="ROC Curve",xaxis_title="False Positive Rate",yaxis_title="True Positive Rate")
        st.plotly_chart(chart_style(fig,360), use_container_width=True)
    st.dataframe(pd.DataFrame(classification_report(y_test,pred,output_dict=True,zero_division=0)).transpose().round(3), use_container_width=True)

elif page == "Chatbot":
    st.markdown("### 💬 Multilingual Healthcare Chatbot")
    st.caption("General health information in English, Kannada, Hindi, Tamil, or Telugu.")
    language = st.selectbox("Choose response language", LANGUAGES, index=LANGUAGES.index(selected_language), key="chat_language")
    question = st.text_input("Ask a health question", key="chat_question")
    spoken = speech_to_text(language="en", start_prompt="🎤 Start speaking", stop_prompt="⏹️ Stop recording", key="health_voice_input")
    if spoken:
        st.session_state["chat_question"] = spoken
        st.success(f"You said: {spoken}")
    if st.button("Send to Chatbot", type="primary"):
        question = st.session_state.get("chat_question","").strip()
        if question:
            answer = get_chatbot_response(question, language)
            st.markdown("**Chatbot response**")
            st.write(answer)
            try:
                from gtts import gTTS
                buffer = BytesIO()
                gTTS(text=answer, lang=LANGUAGE_CODES.get(language,"en")).write_to_fp(buffer)
                st.audio(buffer.getvalue(), format="audio/mp3")
            except Exception as e:
                st.warning(f"Could not generate speech; check internet connection. Details: {e}")
        else:
            st.warning("Please enter a question or use the microphone.")

st.markdown("---")
st.caption("Educational prototype only • Not a clinically validated diagnostic system • Seek qualified medical advice for diagnosis or treatment.")
