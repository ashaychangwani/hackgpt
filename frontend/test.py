import streamlit as st

if 'options' not in st.session_state:
    st.session_state['options'] = ""

def sidebar_callback():
    st.session_state['options'] = st.session_state['sidebar']
def button1_callback():
    st.session_state['options'] = "foo"
def button2_callback():
    st.session_state['options'] = "bar"

placeholder = st.empty()

st.sidebar.selectbox(
     "Examples:",
     ("tirsdag var travel for ukrainas president volodymyr zelenskyj på morgenen tok han imot polens statsminister mateusz morawiecki","tirsdagvartravelforukrainaspresidentvolodymyrzelenskyjpåkveldentokhanimotpolensstatsministermateuszmorawiecki","deterikkelettåholderedepåstoreogsmåbokstavermanmåforeksempelhuskestorforbokstavnårmanskriveromkrimhalvøyamenkunbrukelitenforbokstavnårmanhenvisertilenkrimroman","detteerenlitendemosomerlagetavperegilkummervoldhanerenforskersomtidligerejobbetvednasjonalbiblioteketimoirana", "sentpå60talletvardetfaktisknoensomkalteungensinperegilkummervoldidagerdetikkelengersåvanligåbrukedobbeltnavninorgehvasynesduomdet"),
     key = 'sidebar', on_change = sidebar_callback)

st.button('Run DeUnCaser', on_click = button1_callback)
st.button('Run DeUnCaser but not like before', on_click = button2_callback)

with placeholder:
    text = st.text_area(f"",max_chars=1000, key = 'options')