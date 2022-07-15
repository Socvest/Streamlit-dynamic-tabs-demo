import streamlit as st
from dynamic_tabs import dynamic_tabs
import time
st.set_page_config(layout="wide")

st.subheader("Dynamic Tabs")
st.markdown('<style>' + open('./iFrame.css').read() + '</style>', unsafe_allow_html=True)

styles = {'title-of-tab':{'border': 'solid'}} 

if "tabs" not in st.session_state:
    st.session_state['tabs'] = [{'title':''}]

existing_tabs = [{'title':''}] #[{'title':'Tab 1'}, {'title':'Tab 2'}]

d_tabs = dynamic_tabs(tabTitle=existing_tabs, limitTabs=False, numOfTabs=0, styles=None, key="foo")

if d_tabs == 0:
    time.sleep(1)
    st.info("""Click on a tab to view contents \n - Name tab by clicking in the input area \n - After renaming, click save to save the tab's title \n - To close the tab, hover over the tab click the close button that slides out""")
    st.stop()

elif d_tabs['title'] == "":
    time.sleep(1)
    st.title("New Tab")

else:
    time.sleep(1)
    title_placeholder = st.empty()
    title_placeholder.title(d_tabs['title'])
    if d_tabs['title'] == "":
        title_placeholder.title('New Tab')
        st.info("Create new tabs")
        if d_tabs != "":
            st.write("Inside tab")
