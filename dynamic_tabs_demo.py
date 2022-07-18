import streamlit as st
from dynamic_tabs import dynamic_tabs
import time
st.set_page_config(layout="wide")

st.subheader("Dynamic Tabs")
st.markdown('<style>' + open('./iFrame.css').read() + '</style>', unsafe_allow_html=True)

sidebar_nav = st.sidebar.radio("Dynamic tabs capabilities", ("General", "Add and delete data functionality"))

if sidebar_nav == 'General':

    styles = {'title-of-tab':{'border': 'solid'}} 

    existing_tabs = [{'title':''}] #[{'title':'Tab 1'}, {'title':'Tab 2'}]

    d_tabs = dynamic_tabs(tabTitle=existing_tabs, limitTabs=False, numOfTabs=0, styles=None, key="foo")

    if d_tabs == 0:
        time.sleep(1)
        st.info("""Click on a tab to view contents \n - Name tab by clicking in the input area \n - After renaming, click save to save the tab's title \n - To close the tab, hover over the tab click the close button that slides out \n - If there is only one tab, it cannot be closed. """)
        st.stop()

    elif d_tabs['currentTab']['title'] == "":
        time.sleep(1)
        st.title("New Tab")

    else:
        time.sleep(1)
        st.title(d_tabs['currentTab']['title'])
        
elif sidebar_nav == 'Add and delete data functionality':
    
    if 'selBox' not in st.session_state:
        st.session_state['selBox'] = 0
    
    if 'mulSelBox' not in st.session_state:
        st.session_state['mulSelBox'] = None
    
    def load_database():
        with open("data.json") as json_file:
            user_data_loaded = json.load(json_file)
            if type(user_data_loaded) != list:
                user_data_loaded = [user_data_loaded]
            else:
                user_data_loaded = user_data_loaded

        user_tabs_list = []
        for tabs in user_data_loaded:

            title_of_tab = dict([list(tabs.items())[0]])
            user_tabs_list.append(title_of_tab) 

        return user_tabs_list, user_data_loaded

    def save_new_tab_title(new_title):

        data = {'title': new_title,
                'data': {'selectBox_widget':0, 'multi_select_widget':None}}
        with open("data.json") as json_file:
            user_data_loaded = json.load(json_file)
            user_data_loaded.append(data)

        with open('data.json', 'w') as f:
            json.dump(user_data_loaded, f) 

    def delete_tab(new_list_to_store):            

        with open('data.json', 'w') as f:
            json.dump(new_list_to_store, f) 

    def save_new_tabs_data(selected_tab_title):

        if not any(d['title'] == selected_tab_title for d in user_tabs): 
            user_data_loaded.append(data)
            with open('data.json', 'w') as f:
                json.dump(user_data_loaded, f) 

    try:
        user_tabs, user_data_loaded = load_database()

    except:
        user_data_loaded = False
        user_tabs = [{'title': ""}]
    
    
    d_tabs = dynamic_tabs(tabTitle=user_tabs, limitTabs=False, numOfTabs=0, styles=None, key="foo")

    if d_tabs == 0:
        time.sleep(1)
        st.info("""Click on a tab to view contents \n - Name tab by clicking in the input area \n - After renaming, click save to save the tab's title \n - To close the tab, hover over the tab click the close button that slides out""")
        st.stop()

    elif d_tabs['currentTab']['title'] == "": 
        time.sleep(1)

        st.title("New Tab")

        options = ['Hi', 'I', 'am', 'just', 'some', 'random', 'data']

        st.selectbox("Choose something", options=options, key="new_tab_sel_box", disabled=True)

        numbers_to_plot = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 9, 8]
        ## or
        plot_options = st.multiselect("choose what to plot", options=numbers_to_plot, key='new_tab_mul_select', disabled=True)
        st.info("Please name tab before continuing")
        st.stop()
        # st.line_chart(plot_options)  


    else:

        st.title(st.session_state['foo']['currentTab']['title'])

        if user_data_loaded != False: # and st.session_state['load_data']: #st.session_state['clicked_on_existing_tab'] == True:

            if any(d['title'] == st.session_state['foo']['currentTab']['title'] for d in user_tabs) == False:

                new_title = st.session_state['foo']['currentTab']['title']

                save_new_tab_title(new_title)

            else:

                load_data = [d for d in user_data_loaded if d['title'] == st.session_state['foo']['currentTab']['title']][0]

                selBox = load_data['data']['selectBox_widget']
                multSelect = load_data['data']['multi_select_widget']

                st.session_state['selBox'] = selBox
                st.session_state['mulSelBox'] = multSelect

        st.write(st.session_state['foo'])


        options = ['Hi', 'I', 'am', 'just', 'some', 'random', 'data']

        st.selectbox("Choose something", options=options,index=st.session_state['selBox'], key="existing_tab_sel_box")

        numbers_to_plot = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 9, 8]
        plot_options = st.multiselect("choose what to plot", options=numbers_to_plot, default=st.session_state['mulSelBox'], key='existing_tab_mult_sel_box')
        st.line_chart(plot_options)  

        if st.session_state['foo']['deletedTab']['title'] != "None":
            new_list_to_store = [x for x in user_data_loaded if not (st.session_state['foo']['deletedTab']['title'] == x.get('title'))]

            delete_tab(new_list_to_store)

        save_data = st.button("Save updates")

        if save_data:
            selected_tab_title = st.session_state['foo']['currentTab']['title']
            select_box_index_to_load = options.index(st.session_state['existing_tab_sel_box'])
            multi_select_box_user_options = st.session_state['existing_tab_mult_sel_box']

            data = {'title':selected_tab_title,
                    'data': {
                        'selectBox_widget': select_box_index_to_load,
                        'multi_select_widget': multi_select_box_user_options
                           }}

            ## First check if the database exists. IF not then save it to it.
            def where_json(file_name):
                return os.path.exists(file_name)

            if not where_json('data.json'):
                with open('data.json', 'w') as f:
                    json.dump([data], f) 

            # if it does exist, we want to update saved values with current values from the current tab
            elif any(d['title'] == selected_tab_title for d in user_tabs):
                data_to_update = [d for d in user_data_loaded if d['title'] == selected_tab_title][0] 
                data_to_update['data']['selectBox_widget'] = select_box_index_to_load
                data_to_update['data']['multi_select_widget'] = multi_select_box_user_options

                with open('data.json', 'w') as f:
                    json.dump(user_data_loaded, f) 

            ## Checking to see if the tab title already exists - if it does then don't append data, we only want to append new data and save it to a database
            else:

                save_new_tabs_data(selected_tab_title)
        
