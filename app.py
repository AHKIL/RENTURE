from tkinter.messagebox import NO
from turtle import onclick, width
from numpy import empty
import streamlit as st
import glob
import random
from streamlit_option_menu import option_menu
import os
import json
from PIL import Image 

st.set_page_config(layout="wide",page_title="RENTURE")
hide_st_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)
arr1 = st.columns([1,2,.2,.4,.25,.25])
arr1[0].title('RENTURE')
arr1[1].text_input('',placeholder='Search')
arr1[3].title('')
arr1[3].write('###### hello, Sign in')
arr1[4].title('')
arr1[4].write('###### Return')
arr1[5].title('')
arr1[5].write('###### Cart')

books_arr=glob.glob('books/*')
col=4
size=int(len(books_arr)/col)
fill_star = '<img src="https://img.icons8.com/fluency/344/filled-star.png"  width="20" >'
half_star = '<img src="https://img.icons8.com/fluency/344/star-half.png" width="20">'
empty_star = '<img src="https://img.icons8.com/color/344/star--v1.png" width="20">'

rating_arr =[half_star+empty_star*4,
                fill_star+empty_star*4,
                fill_star+half_star+empty_star*3,
                fill_star*2+empty_star*3,
                fill_star*2+half_star+empty_star*2,
                fill_star*3+empty_star*2,
                fill_star*3+half_star+empty_star,
                fill_star*4+empty_star,
                fill_star*4+half_star,
                fill_star*5]

if 'state' not in st.session_state:
    st.session_state['state'] = 'home'

if 'curr_book' not in st.session_state:
    st.session_state['curr_book'] = ''

def state_change(i,j):
    st.session_state['curr_book'] = books_arr[(i*col+j)]
    st.session_state['state'] = 'rent'

def state_change_back():
    st.session_state['curr_book'] = ''
    st.session_state['state'] = 'home'

def state_change_seller():
    st.session_state['state'] = 'seller'

arr2 = st.columns([8.7,1.1])
if st.session_state['state'] == 'home':
    arr2[1].button('Rent/Sell books', on_click=state_change_seller)

if st.session_state['state'] == 'seller':
    arr2[1].button('Buy/Rent books', on_click=state_change_back)

if st.session_state['state'] == 'home':
    st.header('Best sellers')
    st.subheader('')
    for i in range(size):
        arr=st.columns([1]*col)
        for j in range(col):
            arr[j].image(books_arr[(i*col+j)]+'/0.jpg',width=200)
            with open(books_arr[(i*col+j)]+'/details.json',"r") as f:
                data = json.load(f)
            arr[j].markdown(f'''{data['Book name']}<br>
            {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
            Rent Price:  <span style="color:green">₹{data['Rent price']}</span>''',True)
            arr[j].button('Rent/Buy',key=str(i)+str(j),on_click=state_change,args=(i,j))
        st.title('')
    arr=st.columns([1]*col)
    for i in range(len(books_arr)%col):
            arr[i].image(books_arr[(size*col)+i]+'/0.jpg',width=200)
            with open(books_arr[(size*col)+i]+'/details.json',"r") as f:
                data = json.load(f)
            arr[i].markdown(f'''{data['Book name']}<br>
            {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
            Rent Price:  <span style="color:green">₹{data['Rent price']}</span>''',True)
            arr[i].button('Rent/Buy',key=str(i),on_click=state_change,args=(size,i))

if st.session_state['state'] == 'rent':
    arr=st.columns([1.5,3.7,1.2])
    with open(st.session_state['curr_book']+'/details.json',"r") as f:
        data = json.load(f)
    arr[0].image(st.session_state['curr_book']+'/0.jpg', width=250)
    arr[1].header(data['Book name'])
    arr[1].markdown(f'''by {data['Author name']}<br>
                        {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
                        Rent Price:  <span style="color:green">₹{data['Rent price']}</span>''',True)
    with arr[1].container():
         buy_rent = option_menu(None,['Rent ₹'+data['Rent price'],'Buy ₹'+data['Sell price']], icons=['truck','bag-fill'], menu_icon="check2-circle", orientation="horizontal",
                            styles={"container": {"background-color": "#0d1017",
                             "width":"500px", "margin-left": "0", "padding-left":"0"}})
    
    arr[1].write(data['Description'][:500]+'....')

    with arr[2].form('buy'):
        st.write(buy_rent.split(' ')[0]+' price:',buy_rent.split(' ')[-1])
        st.write('Discount: -₹50')
        st.write('Shipping charges: ₹50')
        st.write('##### Total: '+buy_rent.split(' ')[-1])
        st.write('###### Estimated time: 2hrs')
        st.form_submit_button('Buy Now')
    arr[2].button('Continue Shopping',on_click=state_change_back)

    st.header('')
    st.write('---')

    st.header('Recommended Books')
    st.header('')
    for i in range(min(2,int(len(books_arr)/col)+1)):
        arr=st.columns([1]*col)
        for j in range(min(col,len(books_arr)-col*i)):
            arr[j].image(books_arr[(i*col+j)]+'/0.jpg',width=200)
            with open(books_arr[(i*col+j)]+'/details.json',"r") as f:
                data = json.load(f)
            arr[j].markdown(f'''{data['Book name']}<br>
            {random.choice(rating_arr)} {str(random.randint(500,5000))} <br>
            Rent Price:  <span style="color:green">₹{data['Rent price']}</span>''',True)
            arr[j].button('Rent/Buy',key=str(i)+str(j),on_click=state_change,args=(i,j))
        st.title('')

if st.session_state['state'] == 'seller':
    dic = {}
    with st.form('seller',clear_on_submit=True):
        arr=st.columns(3)
        dic['Book name'] = arr[0].text_input("Book name")
        dic['Author name'] = arr[1].text_input("Author name")
        dic['Rent price'] = arr[0].text_input("Rent price")
        dic['Sell price'] = arr[1].text_input("Sell price")
        dic['Location'] = arr[2].text_input("Genre")
        dic['Description'] = st.text_area("Description",height=200)
        files = arr[2].file_uploader("Add photos",accept_multiple_files=True)
        if st.form_submit_button("Upload"):
            eror=0
            for k in dic.keys():
                if dic[k]=='':
                    st.error('All files are mandatory')
                    eror=1
                    break
            if eror==0:
                os.makedirs(f"Books/{dic['Book name']}", exist_ok=True)
                for no_,imag in enumerate(files):
                    img = Image.open(imag)
                    new_image = img.resize((400, 600)) 
                    new_image.save(f"Books/{dic['Book name']}/{no_}.jpg")
                with open(f"Books/{dic['Book name']}/details.json", "w") as p:
                    json.dump(dic, p)
